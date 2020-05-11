import graphene
from graphene import relay
from graphql_jwt.exceptions import PermissionDenied

from ...core.permissions import AccountPermissions
from ...csv import models
from ..account.types import User
from ..core.connection import CountableDjangoObjectType
from ..core.types.common import Job
from ..utils import get_user_or_app_from_context
from .enums import ExportEventEnum


class ExportEvent(CountableDjangoObjectType):
    date = graphene.types.datetime.DateTime(
        description="Date when event happened at in ISO 8601 format.", required=True,
    )
    type = ExportEventEnum(description="Export event type.", required=True)
    user = graphene.Field(
        User, description="User who performed the action.", required=True
    )
    message = graphene.String(description="Content of the event.", required=True,)

    class Meta:
        description = "History log of export file."
        model = models.ExportEvent
        interfaces = [relay.Node]
        only_fields = ["id"]

    @staticmethod
    def resolve_user(root: models.ExportEvent, info):
        requestor = get_user_or_app_from_context(info.context)
        if (
            requestor == root.user
            or requestor.has_perm(AccountPermissions.MANAGE_USERS)
            or requestor.has_perm(AccountPermissions.MANAGE_STAFF)
        ):
            return root.user
        raise PermissionDenied()

    @staticmethod
    def resolve_message(root: models.ExportEvent, _info):
        return root.parameters.get("message", None)


class ExportFile(CountableDjangoObjectType):
    url = graphene.String(description="The URL of field to download.")
    events = graphene.List(
        graphene.NonNull(ExportEvent),
        description="List of events associated with the order.",
    )

    class Meta:
        description = "Represents a job data of exported file."
        interfaces = [relay.Node, Job]
        model = models.ExportFile
        only_fields = ["id", "created_by", "url"]

    @staticmethod
    def resolve_url(root: models.ExportFile, info):
        content_file = root.content_file
        if not content_file:
            return None
        return info.context.build_absolute_uri(content_file.url)

    @staticmethod
    def resolve_created_by(root: models.ExportFile, info):
        requestor = get_user_or_app_from_context(info.context)
        if requestor == root.created_by or requestor.has_perm(
            AccountPermissions.MANAGE_USERS
        ):
            return root.created_by
        raise PermissionDenied()

    @staticmethod
    def resolve_events(root: models.ExportFile, _info):
        return root.events.all().order_by("pk")
