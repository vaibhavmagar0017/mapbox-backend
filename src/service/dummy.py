from src.service.base import BaseService

from typing import Any, Dict


class DummyService(BaseService):

    async def get_user_list(self) -> Dict[str, Any]:
        async with self.uow:
            # Assuming you are fetching one row from the "employees" table
            result = await self.uow.queries.execute_query("dummy")

            for record in result:
                first_name = record[0]
                last_name = record[1]
                email = record[2]
                hire_date = record[3]
                salary = record[4]
                employee_id = record[5]

            # Ensure that the result is in the format expected by AccountStatementBaseSchema
            result_res = {
                "employee_id": employee_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "hire_date": hire_date,
                "salary": salary,
            }

            return result_res  # This now matches the expected schema
