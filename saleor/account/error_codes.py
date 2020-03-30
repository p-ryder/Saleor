from enum import Enum


class AccountErrorCode(Enum):
    ACTIVATE_OWN_ACCOUNT = "activate_own_account"
    ACTIVATE_SUPERUSER_ACCOUNT = "activate_superuser_account"
    DEACTIVATE_OWN_ACCOUNT = "deactivate_own_account"
    DEACTIVATE_SUPERUSER_ACCOUNT = "deactivate_superuser_account"
    DELETE_NON_STAFF_USER = "delete_non_staff_user"
    DELETE_OWN_ACCOUNT = "delete_own_account"
    DELETE_STAFF_ACCOUNT = "delete_staff_account"
    DELETE_SUPERUSER_ACCOUNT = "delete_superuser_account"
    GRAPHQL_ERROR = "graphql_error"
    INVALID = "invalid"
    INVALID_PASSWORD = "invalid_password"
    NOT_FOUND = "not_found"
    PASSWORD_ENTIRELY_NUMERIC = "password_entirely_numeric"
    PASSWORD_TOO_COMMON = "password_too_common"
    PASSWORD_TOO_SHORT = "password_too_short"
    PASSWORD_TOO_SIMILAR = "password_too_similar"
    REQUIRED = "required"
    UNIQUE = "unique"


class PermissionGroupErrorCode(Enum):
    ASSIGN_NON_STAFF_MEMBER = "assign_non_staff_member"
    CANNOT_ADD_AND_REMOVE = "cannot_add_and_remove"
    OUT_OF_SCOPE_PERMISSION = "out_of_scope_permission"
    OUT_OF_SCOPE_USER = "out_of_scope_user"
    CANNOT_REMOVE_FROM_LAST_GROUP = "cannot_remove_from_last_group"
    REQUIRED = "required"
    UNIQUE = "unique"
