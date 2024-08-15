"""Readers for reading data from files to be used by tests."""
import json
from pathlib import Path
from typing import Any

from ..config import urls

__all__ = ["ConfigReaderService"]


class ConfigReaderService:
    """Service class for reading data from configuration files."""

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_queries(data_dir: str, app: str) -> list[dict[str, Any]]:
        """
        Fixture to get queries from a JSON file given the data directory and app
        name.

        Parameters
        ----------
        data_dir
            The data directory path.
        app
            The application name.

        Returns
        -------
        list[dict[str, Any]]
            A list of queries with expected durations and row counts.
        """
        queries_file_path = Path(data_dir) / app / "queries.json"
        path = Path(str(queries_file_path))
        with path.open() as file:
            data = json.load(file)
        return data.get("queries", [])

    @staticmethod
    def get_url(app: str) -> str:
        """Get the URL for the given application from the mapped URLS in the
        config.

        Parameters
        ----------
        app
            The application name.

        Returns
        -------
        str
            The URL for the application.
        """
        app_name = app.lower()
        if app_name not in urls:
            raise ValueError(f"Invalid app name: {app_name}")
        return urls[app_name]
