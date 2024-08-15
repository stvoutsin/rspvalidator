"""Module with TAP related models."""

from dataclasses import dataclass
from enum import Enum

__all__ = ["TAPApplication", "QueryMode", "QueryResult"]


class TAPApplication(Enum):
    """Enumeration of TAP applications.

    Attributes
    ----------
    TAP: str
        The (Qserv)TAP application.
    SSOTAP: str
        The SSO TAP application.
    """

    TAP = "tap"
    SSOTAP = "ssotap"


class QueryMode(Enum):
    """Enumeration of query modes.

    Attributes
    ----------
    SYNC : str
        TAP Synchronous query mode.
    ASYNC : str
        TAPAsynchronous query mode.
    """

    SYNC = "sync"
    ASYNC = "async"


@dataclass
class QueryResult:
    """Dataclass to store query result metadata.

    Attributes
    ----------
    status : str
        The query status.
    row_count : int
        The number of rows returned by the query.
    execution_duration : float
        The actual query execution duration.
    expected_duration : float
        The expected query duration.
    expected_row_count : int
        The expected number of rows.
    query : str
        The query string.
    """

    status: str
    row_count: int
    execution_duration: float
    expected_duration: float
    expected_row_count: int
    query: str
