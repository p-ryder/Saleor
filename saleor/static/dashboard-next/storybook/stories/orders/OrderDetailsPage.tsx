import { storiesOf } from "@storybook/react";
import * as React from "react";

import * as placeholderImage from "../../../../images/placeholder60x60.png";
import OrderDetailsPage, {
  OrderDetailsPageProps
} from "../../../orders/components/OrderDetailsPage";
import { countries, order as orderFixture } from "../../../orders/fixtures";
import { OrderStatus, PaymentStatusEnum } from "../../../types/globalTypes";
import Decorator from "../../Decorator";

const order = orderFixture(placeholderImage);

const props: OrderDetailsPageProps = {
  countries,
  errors: [],
  onBack: () => undefined,
  onBillingAddressEdit: undefined,
  onFulfillmentCancel: () => undefined,
  onFulfillmentTrackingNumberUpdate: () => undefined,
  onNoteAdd: undefined,
  onOrderCancel: undefined,
  onOrderFulfill: undefined,
  onPaymentCapture: undefined,
  onPaymentPaid: undefined,
  onPaymentRefund: undefined,
  onPaymentRelease: undefined,
  onProductClick: undefined,
  onShippingAddressEdit: undefined,
  order
};

storiesOf("Views / Orders / Order details", module)
  .addDecorator(Decorator)
  .add("default", () => <OrderDetailsPage {...props} />)
  .add("loading", () => <OrderDetailsPage {...props} order={undefined} />)
  .add("pending payment", () => (
    <OrderDetailsPage
      {...props}
      order={{
        ...props.order,
        paymentStatus: PaymentStatusEnum.PREAUTH
      }}
    />
  ))
  .add("payment error", () => (
    <OrderDetailsPage
      {...props}
      order={{
        ...props.order,
        paymentStatus: PaymentStatusEnum.ERROR
      }}
    />
  ))
  .add("payment confirmed", () => (
    <OrderDetailsPage
      {...props}
      order={{
        ...props.order,
        paymentStatus: PaymentStatusEnum.CONFIRMED
      }}
    />
  ))
  .add("no payment", () => (
    <OrderDetailsPage
      {...props}
      order={{
        ...props.order,
        paymentStatus: null
      }}
    />
  ))
  .add("refunded payment", () => (
    <OrderDetailsPage
      {...props}
      order={{
        ...props.order,
        paymentStatus: PaymentStatusEnum.REFUNDED
      }}
    />
  ))
  .add("rejected payment", () => (
    <OrderDetailsPage
      {...props}
      order={{
        ...props.order,
        paymentStatus: PaymentStatusEnum.REJECTED
      }}
    />
  ))
  .add("cancelled", () => (
    <OrderDetailsPage
      {...props}
      order={{
        ...props.order,
        status: OrderStatus.CANCELED
      }}
    />
  ))
  .add("fulfilled", () => (
    <OrderDetailsPage
      {...props}
      order={{
        ...props.order,
        status: OrderStatus.FULFILLED
      }}
    />
  ))
  .add("partially fulfilled", () => (
    <OrderDetailsPage
      {...props}
      order={{
        ...props.order,
        status: OrderStatus.PARTIALLY_FULFILLED
      }}
    />
  ))
  .add("unfulfilled", () => (
    <OrderDetailsPage
      {...props}
      order={{
        ...props.order,
        status: OrderStatus.UNFULFILLED
      }}
    />
  ));
