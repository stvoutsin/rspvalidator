"""Provide utility methods for configuration files."""
from pathlib import Path

import requests

from ..exceptions import FileSizeError

__all__ = ["FileManagerService"]


class FileManagerService:
    """A class that provides utility methods for reading onfiguration
    files.
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def check_auth_file() -> None:
        """
        Check if the auth.json file exists in the user's home directory.

        Raises
        ------
        FileNotFoundError
            If the auth.json file is not found in the user's home directory.
        """
        home_dir = Path.home()
        auth_file_path = home_dir / "auth.json"

        if not auth_file_path.exists():
            raise FileNotFoundError(
                f"Error: The file 'auth.json' was not found "
                f"in the home directory: {home_dir}"
            )

    @staticmethod
    def file_exists_and_valid(
        file_path: Path, min_size_bytes: int = 15_000_000
    ) -> bool:
        """
        Check if a file exists and meets the minimum size requirement.

        Args:
            file_path (Path): The path to the file.
            min_size_bytes (int): The minimum file size in bytes (default:
            15MB).

        Returns
        -------
            bool: True if the file exists and is valid, False otherwise.
        """
        if file_path.exists() and file_path.is_file():
            if file_path.stat().st_size >= min_size_bytes:
                return True
            else:
                raise FileSizeError(
                    f"File {file_path} is smaller than expected."
                )
        return False

    @staticmethod
    def download_file(url: str, file_path: Path) -> None:
        """
        Download a file from a given URL.

        Parameters
        ----------
        url
            The URL to download the file from.
        file_path
            The path to save the file to.

        """
        if FileManagerService.file_exists_and_valid(file_path):
            return

        response = requests.get(url, timeout=120)
        response.raise_for_status()
        with file_path.open("wb") as file:
            file.write(response.content)
