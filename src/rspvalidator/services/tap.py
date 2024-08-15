"""TAP service module."""
from typing import Any

import pyvo

from ..config import BASE_URL, logger
from ..models.tap import QueryMode, QueryResult
from ..utils.timer import timer

__all__ = ["TAPQueryRunnerService", "TAPOperationsService"]


class TAPQueryRunnerService:
    """TAP query runner class."""

    def __init__(self) -> None:
        pass

    @staticmethod
    def run_query_test(
        client: pyvo.dal.TAPService,
        query: dict[str, Any],
        mode: QueryMode,
    ) -> QueryResult:
        """Run a query test and return the results.

        Parameters
        ----------
        client
            The TAP client object.
        query
            The query to run.
        mode
            The query mode.

        Returns
        -------
            QueryResult: The query test result metadata.
        """
        if mode not in (QueryMode.SYNC, QueryMode.ASYNC):
            raise ValueError("Invalid query mode")

        sql_query: str = query["query"]
        expected_duration: float = query["expected_duration"]
        expected_row_count: int = query["expected_row_count"]
        result, execution_duration = (
            timer(client.run_sync, sql_query)
            if mode == QueryMode.SYNC
            else timer(client.run_async, sql_query)
        )
        row_count: int = len(result.table)

        return QueryResult(
            status=result.status[0],
            row_count=row_count,
            execution_duration=execution_duration,
            expected_duration=expected_duration,
            expected_row_count=expected_row_count,
            query=sql_query,
        )


class TAPOperationsService:
    """TAP operations class."""

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_api_endpoint(endpoint: str, app: str) -> str:
        """
        Get the API endpoint for the given application and endpoint.

        Parameters
        ----------
        endpoint
            The endpoint.
        app
            The application name.

        Returns
        -------
        str
            The API endpoint.

        Raises
        ------
        ValueError
            If the endpoint is not valid.
        """
        api_endpoints: dict[str, str] = {
            "capabilities": f"{BASE_URL}/api/{app}/capabilities",
            "availability": f"{BASE_URL}/api/{app}/availability",
            "logcontrol": f"{BASE_URL}/api/{app}/logging/control",
            "tables": f"{BASE_URL}/api/{app}/tables",
            "tap": f"{BASE_URL}/api/{app}",
        }

        if endpoint not in api_endpoints:
            logger.error(f"Invalid endpoint: {endpoint}")
            raise ValueError(f"Invalid endpoint: {endpoint}")

        return api_endpoints[endpoint]
