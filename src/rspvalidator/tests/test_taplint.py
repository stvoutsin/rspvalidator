from pathlib import Path

from ..config import TOKEN
from ..services.configreader import ConfigReaderService
from ..services.taplint import TaplintService
from ..services.validation import TaplintValidationService


def test_stilts_taplint_sso(stilts_jar: Path) -> None:
    """
    Test the SSO TAP service with STILTS taplint.

    Parameters
    ----------
    stilts_jar
        The Path to the stilts jar
    """
    tap_url = ConfigReaderService.get_url("ssotap")
    username = "x-oauth-token"
    password = TOKEN

    stdout, exit_status = TaplintService.run(
        stilts_jar, tap_url, username, password
    )

    assert (
        exit_status == 0
    ), f"STILTS TAPLINT failed with exit status {exit_status}"

    TaplintValidationService("ssotap").validate_summary(stdout)


def test_stilts_taplint_tap(stilts_jar: Path) -> None:
    """
    Test the TAP service with STILTS taplint.

    Parameters
    ----------
    stilts_jar
        The Path to the stilts jar
    """
    tap_url = ConfigReaderService.get_url("tap")
    username = "x-oauth-token"
    password = TOKEN

    stdout, exit_status = TaplintService.run(
        stilts_jar, tap_url, username, password
    )

    assert (
        exit_status == 0
    ), f"STILTS TAPLINT failed with exit status {exit_status}"

    TaplintValidationService("tap").validate_summary(stdout)
