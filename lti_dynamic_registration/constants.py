from enum import Enum


class CanvasVisibility(str, Enum):
    PUBLIC = "public"
    ADMINS = "admins"
    MEMBERS = "members"

    def __str__(self) -> str:
        return self.value


class CanvasPrivacyLevel(str, Enum):
    ANONYMOUS = "anonymous"
    NAME_ONLY = "name_only"
    EMAIL_ONLY = "email_only"
    PUBLIC = "public"

    def __str__(self) -> str:
        return self.value
