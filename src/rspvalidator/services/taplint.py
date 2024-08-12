import re
from pathlib import Path

import pexpect

from ..config import logger

__all__ = ["TaplintService", "TaplintParserService"]


class TaplintService:
    """Handles the execution of STILTS TAPLINT."""

    @staticmethod
    def run(
        jar_path: Path, tap_url: str, username: str, password: str
    ) -> tuple[str, int]:
        """
        Run STILTS TAPLINT on a given TAP URL.

        Parameters
        ----------
        jar_path
            Path to the STILTS JAR file.
        tap_url
            The TAP URL to test.
        username
            The username for authentication.
        password
            The password for authentication.

        Returns
        -------
            Tuple[str, int]: A tuple containing the output string and exit status.
        """
        child = None
        command = f"java -jar {jar_path} taplint tapurl={tap_url}"
        timeout = 150000
        try:
            child = pexpect.spawn(command, timeout=timeout)

            child.expect("Username:", timeout=timeout)
            child.sendline(username)

            child.expect("Password:", timeout=timeout)
            child.sendline(password)

            output = child.read().decode(errors="replace")
            child.close()

            return output, child.exitstatus  # noqa: TRY300
        except pexpect.TIMEOUT:
            logger.exception(
                f"Timeout occurred. Last output: {child.before.decode(errors='replace')}"
            )
            return f"Timeout occurred after {timeout} seconds", -1
        except pexpect.EOF:
            logger.exception(
                f"EOF encountered. Last output: {child.before.decode(errors='replace')}"
            )
            return "Process ended unexpectedly", child.exitstatus
        except Exception as e:
            logger.exception(f"An error occurred: {e!s}")
            return f"Error: {e!s}", -1


class TaplintParserService:
    """Parses TAPLINT output."""

    @staticmethod
    def parse_summary(output: str) -> tuple[int, int]:
        """
        Parse the summary of TAPLINT output to extract error and warning counts.

        Parameters
        ----------
        output
            The TAPLINT output string.

        Returns
        -------
        tuple[int, int]
            A tuple containing the number of errors and warnings.
        """
        errors, warnings = 0, 0
        lines = output.split("\n")
        for line in reversed(lines):
            if line.startswith("Totals:"):
                error_match = re.search(r"Errors:\s+(\d+)", line)
                if error_match:
                    errors = int(error_match.group(1))
                warning_match = re.search(r"Warnings:\s+(\d+)", line)
                if warning_match:
                    warnings = int(warning_match.group(1))
                break
        return errors, warnings
