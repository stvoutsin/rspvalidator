"Exceptions for rspvalidator suite."

__all__ = ["FileSizeError"]


class FileSizeError(Exception):
    """Raised when the file size does not meet the expected size."""

    error = "File size error"
