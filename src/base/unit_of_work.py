import abc
import logging

import inject
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.asyncio import AsyncSession


logger = logging.getLogger(__name__)


def default_session_factory() -> AsyncSession:
    """
    Default DB Session Factory
    :return:
    """
    return inject.instance(AsyncSession)


class AbstractUnitOfWork(abc.ABC):
    # Database session
    session: Session = None

    def __init__(self):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, ec_type, exc_val, exc_tb):
        pass

    @abc.abstractmethod
    async def commit(self):
        # pass
        raise NotImplementedError



class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    """
    SQLAlchemy Unit of Work
    """

    session: AsyncSession = None
    session_factory = None

    def __init__(self, session: AsyncSession = None, session_factory=default_session_factory):
        """
        Either the session object or session_factory need to be provided
        If session object is passed it will be passed down to the repository
        If Session object is not provided then it will try to create with the session factory
        And then passed it down to the repository
        :param session: sqlalchemy.orm.Session:
        :param session_factory: Callable: which returns the session object
        """
        self.session = session
        self.session_factory = session_factory
        self.close_on_exit = False

    async def __aenter__(self):
        """
        Starts the context manager for the
        :return:
        """
        await super().__aenter__()
        if not self.session:
            # Session is not initialized so creating new session
            self.session = self.session_factory()
            self.close_on_exit = True

        return self

    async def __aexit__(self, ec_type, exc_val, exc_tb):
        await self.rollback()
        if self.close_on_exit:
            # Close the session only if it is started in the context manager
            await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
