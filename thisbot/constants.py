from dataclasses import dataclass

APP_NAME = "Oogway-Mixin-Bot"


@dataclass(frozen=True)
class _UserTypes:
    MIXIN_GROUP: str = "MIXIN_GROUP"
    MIXIN_USER: str = "MIXIN_USER"
    MIXIN_APP: str = "MIXIN_APP"


USER_TYPES = _UserTypes()
