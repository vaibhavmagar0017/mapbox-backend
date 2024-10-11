import typing
from enum import Enum

import inject
from pydantic import UUID4, BaseModel, Field
from datetime import date

from src.base.settings import CoreSettings
from src.base.enums import OrderEnum


class ResponseType(str, Enum):
    success: str = "SUCCESS"
    error: str = "ERROR"
    warning: str = "WARNING"
    info: str = "INFO"


class ApiInfoSchema(BaseModel):
    name: str = Field(..., title="Name", description="Name of the app")
    version: str = Field(..., title="Version", description="Version of the app")
    api_version: str = Field(..., title="API Version", description="Version of the API")
    message: str = Field(..., title="Message", description="Welcome message")


class ResponseSchema(BaseModel):
    response_code: int = Field(..., title="Response Code", description="Unique response " "code specific to error")
    response_type: ResponseType = Field(None, title="Response Type", description="Response type")
    message: str = Field(..., title="Message", description="Message may be useful for user")
    description: typing.Optional[str] = Field(
        default=None, title="Description", description="Debug " "information for developer"
    )


    def __init__(self, **kwargs):
        super(ResponseSchema, self).__init__(**kwargs)
        settings = inject.instance(CoreSettings)
        if settings.current_env == "PROD":
            self.description = None


class BaseRequestSchema(BaseModel):
    pass


class PaginationResponseSchema(BaseModel):
    data: typing.List[dict] = Field(default_factory=list, title="List of records")
    total_count: int = Field(default=0, title="Total record count")
    page_size: int = Field(default=10, title="Records per page")
    page: int = Field(default=1, title="Current Page Number")
    total_pages: int = Field(default=1, title="Total number of pages")
    has_next_page: bool = Field(default=False, title="Has next page")
    has_prev_page: bool = Field(default=False, title="Has previous page")


class SearchPaginatedRequestSchema(BaseModel):
    search: str | None = Field(default=None, title="Filter records")
    page: int = Field(default=1, title="Requested page number", gt=0)
    page_size: int = Field(default=10, title="Number of records per page", gt=0)
    order_by: str = Field(default="created_at", title="Sort records by")
    order: OrderEnum = Field(default=OrderEnum.desc, title="Sort order")
