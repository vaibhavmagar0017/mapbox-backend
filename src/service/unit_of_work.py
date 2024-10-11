from src.base.unit_of_work import SqlAlchemyUnitOfWork
from src.repository.query_repository import QueryRepository


class UnitOfWork(SqlAlchemyUnitOfWork):
    """ """
    queries: QueryRepository = None

    async def __aenter__(self):
        await super(UnitOfWork, self).__aenter__()
        self.queries = QueryRepository(session=self.session)
