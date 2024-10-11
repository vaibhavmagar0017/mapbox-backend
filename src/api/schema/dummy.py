import datetime

from pydantic import BaseModel
from pydantic import Field


class DummyBaseSchema(BaseModel):
    employee_id: int | None = Field(default=None)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    email: str | None = Field(default=None)
    hire_date: datetime.date | None = Field(default=None)
    salary: float | None = Field(default=0.0, title="Salary")
