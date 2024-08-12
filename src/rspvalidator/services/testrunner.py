"""Runner service module, used for running tests concurrently."""
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, List

from ..models.tap import QueryResult

__all__ = ["Runner"]


class Runner:
    """Runner service class, used for running tests concurrently."""

    def __init__(self) -> None:
        pass

    @staticmethod
    def run_concurrent_test(
        test_function: Callable,
        test_data: list[dict[str, Any]],
        user_count: int,
        **kwargs: Any,
    ) -> list[list[QueryResult]]:
        """
        Run a test function concurrently with a specified number of users.

        Parameters
        ----------
        test_function
            The function to be executed concurrently.
        test_data
            The data to be passed to each test function call.
        user_count
            The number of concurrent users (threads) to simulate.
        **kwargs
            Additional keyword arguments to pass to the test function.

        Returns
        -------
        List[Dict[str, Any]]
            A list of results from the test function calls
        """
        client = kwargs.pop("client", None)
        mode = kwargs.pop("mode", None)

        def _run_user_tests() -> list[QueryResult]:
            """
            Run the user tests concurrently.

            Returns
            -------
            List[QueryResult]
                A list of results from the test function calls

            """
            return [
                test_function(client, data, mode, **kwargs)
                for data in test_data
            ]

        with ThreadPoolExecutor(max_workers=user_count) as executor:
            futures = [
                executor.submit(_run_user_tests) for _ in range(user_count)
            ]
            return [future.result() for future in as_completed(futures)]
