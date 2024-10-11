import enum


class ResponseTypeEnum(str, enum.Enum):
    success: str = "SUCCESS"
    error: str = "ERROR"
    warning: str = "WARNING"
    info: str = "INFO"


class OrderEnum(str, enum.Enum):
    desc: str = "DESC"
    asc: str = "ASC"
