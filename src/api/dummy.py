from fastapi import Depends

from fastapi.responses import StreamingResponse
from src.base.router import APIRouter
# from src.service.dummy import DummyServiceService
from src.service.dummy import DummyService
from src.api.schema.dummy import DummyBaseSchema
# from src.api.schema.dummy import AccountStatementSearchPaginatedRequestSchema
#

router = APIRouter(prefix="/dummy", tags=["Dummy"])


@router.get("/user", response_model=DummyBaseSchema)
async def get_user():
    service = DummyService()
    result = await service.get_user_list()  # Await the async function
    return result  # Ensure result matches the response_model
