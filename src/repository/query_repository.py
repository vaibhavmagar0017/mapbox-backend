import importlib
from logging import getLogger
from typing import Optional, Any

from sqlalchemy.sql import text

import sqlalchemy.exc
from sqlalchemy.sql import bindparam
from sqlalchemy.ext.asyncio import AsyncSession
from src.base.error import ApplicationError
from src.base.unit_of_work import logger

logger = getLogger(__name__)


class QueryRepository:
    session: AsyncSession


    def __init__(self, session: AsyncSession):
        self.session = session

    async def _exec_query(self, query: str, params: Optional[dict[str, Any]], extend_option: bool = True):
        params = params or {}
        new_params = params.copy()
        if extend_option:
            for key, val in params.items():
                if isinstance(val, list):
                    query = query.bindparams(bindparam(key, expanding=True))
                    new_params[f"is_{key}_empty"] = not bool (val)
                    if new_params[f"is_{key}_empty"]:
                        new_params[key] = ['']

        result = await self.session.execute(query, params=new_params)
        return result

    def get_query(self, query_name: str) -> str:
        try:
            logger.debug(f"Finding {query_name} in src.repository.queries.*")
            query_file = importlib.import_module(f"src.repository.queries.{query_name}", query_name)
            sql_query = getattr(query_file, query_name)

            # Wrap the query string in the text() function
            sql_query = text(sql_query)  # Ensure this line is added

            logger.info(f"Found {query_name} in src.repository.queries.*")
            return sql_query
        except ImportError as ie:
            logger.error(
                f"Unable to load module src.repository.queries.{query_name}: {ie}", exc_info=True,
            )
            raise ApplicationError(
                response_code=500, message="Unable to load sql query"
            )
        except AttributeError as ae:
            logger.error(
                f"Not found {query_name} in src.repository.queries.{query_name}: {ae}"
            )
            raise ApplicationError(
                response_code=500, message="Unable to find sql query"
            )

    async def execute_query(self, query_name, params: Optional[dict[str, Any]] = None, extend_option: bool = True):
        query = self.get_query(query_name)
        logger.info(f"Executing query: {query_name}")
        logger.debug(f"sql query: {query}")
        logger.debug(f"SQl Parameters: {params}")
        try:
            result = await self._exec_query(query, params=params, extend_option=extend_option)
            return result
        except OSError as de:
            logger.error(f"Error while connecting database: {de}", exc_info=True)
            raise ApplicationError(
                response_code=500, message="Error In Connecting database."
            )
        except sqlalchemy.exc.DatabaseError as de:
            logger.error(f"Error while connecting sql: {de}", exc_info=True)
            raise ApplicationError(
                response_code=500, message="Error in executing SQL."
            )