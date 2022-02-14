import logging
from typing import List, Optional, Tuple

from ....order.models import Fulfillment
from ...interface import PaymentData, RefundData
from ...models import Payment
from .api_helpers import (
    cancel,
    format_price,
    get_goods_with_discount,
    get_refunded_goods,
    handle_unrecoverable_state,
    np_request,
    register,
    report,
)
from .api_types import (
    ApiConfig,
    PaymentResult,
    PaymentStatus,
    error_payment_result,
    errors_payment_result,
)
from .const import PRE_FULFILLMENT_ERROR_CODE
from .errors import (
    FULFILLMENT_REPORT,
    NO_PSP_REFERENCE,
    TRANSACTION_CANCELLATION,
    TRANSACTION_CHANGE,
    TRANSACTION_REGISTRATION,
    add_action_to_code,
    get_error_messages_from_codes,
)
from .utils import get_shipping_company_code

logger = logging.getLogger(__name__)


def register_transaction(
    config: ApiConfig, payment_information: "PaymentData"
) -> PaymentResult:
    """Create a new transaction in NP Atobarai.

    On pending status from NP the transaction is cancelled and
    reason for pending is returned as error message.
    """
    action = TRANSACTION_REGISTRATION
    result, error_codes = register(config, payment_information)

    if error_codes:
        error_messages = get_error_messages_from_codes(action, error_codes=error_codes)
        return errors_payment_result(error_messages)

    status = result["authori_result"]
    transaction_id = result["np_transaction_id"]
    error_messages = []

    if status == PaymentStatus.PENDING:
        if cancel_error_codes := cancel(config, transaction_id).error_codes:
            handle_unrecoverable_state(
                None, "cancel", transaction_id, cancel_error_codes
            )
        error_messages = get_error_messages_from_codes(
            action, error_codes=result["authori_hold"]
        )

    return PaymentResult(
        status=status,
        psp_reference=transaction_id,
        errors=error_messages,
    )


def cancel_transaction(
    config: ApiConfig, payment_information: PaymentData
) -> PaymentResult:
    action = TRANSACTION_CANCELLATION
    psp_reference = payment_information.psp_reference

    if not psp_reference:
        return error_payment_result(
            add_action_to_code(action, error_code=NO_PSP_REFERENCE)
        )

    result, error_codes = cancel(config, psp_reference)

    if error_codes:
        error_messages = get_error_messages_from_codes(action, error_codes=error_codes)
        return errors_payment_result(error_messages)

    return PaymentResult(status=PaymentStatus.SUCCESS)


def change_transaction(
    config: ApiConfig,
    payment: Payment,
    payment_information: PaymentData,
    refund_data: Optional[RefundData],
) -> PaymentResult:
    """Change transaction.

    If the fulfillment was reported prior to changing given transaction,
    then no change is applied and payment status is set to FOR_REREGISTRATION.
    """
    if refund_data:
        goods = get_refunded_goods(config, refund_data, payment_information)
    else:
        goods = get_goods_with_discount(config, payment_information)

    data = {
        "transactions": [
            {
                "np_transaction_id": payment.psp_reference,
                "billed_amount": format_price(
                    payment.captured_amount - payment_information.amount,
                    payment_information.currency,
                ),
                "goods": goods,
            }
        ]
    }

    result, error_codes = np_request(config, "patch", "/transactions/update", json=data)

    if not error_codes:
        status = result["authori_result"]
        transaction_id = result["np_transaction_id"]

        if status == PaymentStatus.PENDING:
            if cancel_error_codes := cancel(config, transaction_id).error_codes:
                handle_unrecoverable_state(
                    payment.order, "cancel", transaction_id, cancel_error_codes
                )
            error_messages = result["authori_hold"]
            return errors_payment_result(error_messages)

        return PaymentResult(
            status=PaymentStatus.SUCCESS,
        )

    if PRE_FULFILLMENT_ERROR_CODE in error_codes:
        logger.info(
            "Fulfillment for payment with id %s was reported",
            payment_information.graphql_payment_id,
        )
        return PaymentResult(status=PaymentStatus.FOR_REREGISTRATION)

    error_messages = get_error_messages_from_codes(
        action=TRANSACTION_CHANGE, error_codes=error_codes
    )
    return errors_payment_result(error_messages)


def reregister_transaction_for_partial_return(
    config: ApiConfig,
    payment: Payment,
    payment_information: PaymentData,
    shipping_company_code: Optional[str],
    tracking_number: Optional[str],
    refund_data: Optional[RefundData],
) -> PaymentResult:
    """Change transaction.

    Use it after capturing the payment, otherwise `change_transaction`
    is the preferred function.
    """
    psp_reference = payment.psp_reference
    action = TRANSACTION_REGISTRATION

    if not psp_reference:
        return error_payment_result(
            add_action_to_code(
                action,
                error_code=NO_PSP_REFERENCE,
            )
        )

    if cancel_error_codes := cancel(config, psp_reference).error_codes:
        error_messages = get_error_messages_from_codes(
            action=TRANSACTION_CANCELLATION, error_codes=cancel_error_codes
        )
        return errors_payment_result(error_messages)

    if refund_data:
        goods = get_refunded_goods(config, refund_data, payment_information)
    else:
        goods = get_goods_with_discount(config, payment_information)

    billed_amount = format_price(
        payment.captured_amount - payment_information.amount,
        payment_information.currency,
    )

    result, error_codes = register(
        config,
        payment_information,
        billed_amount,
        goods,
    )

    if not error_codes:
        new_psp_reference = result["np_transaction_id"]

        result, error_codes = report(
            config, shipping_company_code, new_psp_reference, tracking_number
        )

        if error_codes:
            error_messages = get_error_messages_from_codes(
                FULFILLMENT_REPORT, error_codes=error_codes
            )
            return errors_payment_result(error_messages)

        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            psp_reference=new_psp_reference,
        )

    error_messages = get_error_messages_from_codes(action, error_codes=error_codes)

    return errors_payment_result(error_messages)


def report_fulfillment(
    config: ApiConfig, payment: Payment, fulfillment: Fulfillment
) -> Tuple[List[str], bool]:
    """Report fulfillment.

    After this action, given payment is captured in NP Atobarai.
    """
    shipping_company_code = get_shipping_company_code(config, fulfillment)

    result, error_codes = report(
        config,
        shipping_company_code,
        payment.psp_reference,
        fulfillment.tracking_number,
    )

    errors = get_error_messages_from_codes(
        action=FULFILLMENT_REPORT, error_codes=error_codes
    )
    already_reported = PRE_FULFILLMENT_ERROR_CODE in error_codes

    return errors, already_reported
