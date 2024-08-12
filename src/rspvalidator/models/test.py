"""Module to define the Test related models."""
from dataclasses import dataclass, field

from .tap import QueryMode, TAPApplication

__all__ = ["TestScenario"]


@dataclass
class TestScenario:
    """
    Dataclass to store test configuration data.

    Attributes
    ----------
    app: TAPApplication
        The TAP application.
    mode: QueryMode
        The query mode (sync or async
    users: int
        The number of concurrent users
    """

    app: TAPApplication
    mode: QueryMode
    users: int
    description: str = field(init=False)

    def __post_init__(self) -> None:
        self.description = (
            f"{self.app.value.upper()} {self.mode.value} query [{self.users} "
            f"user{'s' if self.users > 1 else ''}]"
        )
