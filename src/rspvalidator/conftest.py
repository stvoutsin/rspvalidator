"""Conftest module for the tests."""

import datetime
from pathlib import Path
from typing import Any, Generator  # noqa: UP035

import pytest
import pyvo
from playwright.sync_api import expect, sync_playwright

from .config import HEADLESS, SELECTOR_TIMEOUT, TOKEN, TRACING
from .constants import AUTH_FILE, STILTS_FILENAME, STILTS_URL
from .factories.tap_factory import TAPFactory
from .services.configreader import ConfigReaderService
from .services.filemanager import FileManagerService
from .services.validation import TAPValidationService

# Set default timeout for playwright
expect.set_options(timeout=SELECTOR_TIMEOUT)


@pytest.fixture(scope="session")
def playwright() -> Generator:
    """Fixture to create a playwright instance.

    Returns
    -------
    playwright
        The playwright instance.
    """
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright: Any) -> Generator:
    """
    Fixture to create a playwright browser object.

    Parameters
    ----------
    playwright
        The playwright instance.

    Returns
    -------
    playwright.browser
        The playwright browser object.
    """
    browser = playwright.chromium.launch(
        headless=HEADLESS,
    )
    yield browser
    browser.close()


@pytest.fixture(scope="session")
def auth_token() -> str:
    """Fixture to fetch an authentication token from the environment variables.

    This fixture will be available for all tests in the session. It raises an
    exception if the environment variable for the token is not found.

    Returns
    -------
        str: The authentication token.

    Raises
    ------
        RuntimeError: If the environment variable for the token is not set.
    """
    if not TOKEN:
        raise RuntimeError("Authentication token not found in environment variables.")
    return TOKEN


@pytest.fixture(scope="session")
def tap_client_ssotap(auth_token: str) -> pyvo.dal.TAPService:
    """Fixture to create and provide a TAP client with authenticated session.

    Parameters
    ----------
    auth_token
        The authentication token.

    Returns
    -------
    pyvo.dal.TAPService
        The TAP client object.
    """
    return TAPFactory.make_client(auth_token=auth_token, app="ssotap")


@pytest.fixture(scope="session")
def tap_client_tap(auth_token: str) -> pyvo.dal.TAPService:
    """Fixture to create and provide a TAP client with authenticated session.

    Parameters
    ----------
    auth_token
        The authentication token.

    Returns
    -------
    pyvo.dal.TAPService
        The TAP client object.
    """
    return TAPFactory.make_client(auth_token=auth_token, app="tap")


@pytest.fixture(scope="session")
def page(browser: Any) -> Generator:
    """
    Fixture to create a playwright page object.

    Parameters
    ----------
    browser
        The Playwright browser object

    Returns
    -------
    playwright.page
        The Playwright page object.
    """
    home_auth_path = Path(AUTH_FILE).expanduser()
    context = browser.new_context(storage_state=home_auth_path)
    context.set_default_timeout(SELECTOR_TIMEOUT)

    if TRACING:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    # To add a bearer token: context.set_extra_http_headers({"Authorization":
    # f"Bearer {TOKEN}"}) (This doesn't seem to work atm)
    page = context.new_page()
    yield page

    if TRACING:
        timestamp = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d_%H%M%S")
        context.tracing.stop(path=f"{timestamp}-trace.zip")

    page.close()
    context.close()


@pytest.fixture(scope="session")
def page_anonymous(browser: Any) -> Generator:
    """
    Fixture to create a playwright page object.

    Parameters
    ----------
    browser
        The Playwright browser object

    Returns
    -------
    playwright.page
        The Playwright page object.
    """
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture
def data_dir() -> Path:
    """
    Fixture to return the data directory path.

    Returns
    -------
        str: The data directory path.

    """
    return Path(__file__).parent / "data"


@pytest.fixture
def queries(data_dir: str, app: str) -> list[dict[str, Any]]:
    """
    Fixture to load queries from a JSON file.

    Parameters
    ----------
    data_dir
        The data directory
    app
        The application name.

    Returns
    -------
        list[dict[str, Any]]: A list of queries with expected durations and
        row counts.
    """
    return ConfigReaderService.get_queries(data_dir=data_dir, app=app)


@pytest.fixture
def tap_validation_service_ssotap(
    tap_client_ssotap: pyvo.dal.TAPService,
) -> TAPValidationService:
    """Fixture to provide a TAPValidationService instance for the ssotap app.

    Parameters
    ----------
    tap_client_ssotap
        The TAP client object for the SSO TAP service.

    Returns
    -------
    TAPValidationService
        The TAPValidationService instance.

    """
    return TAPValidationService(tap_client=tap_client_ssotap, app="ssotap")


@pytest.fixture
def tap_validation_service_tap(
    tap_client_tap: pyvo.dal.TAPService,
) -> TAPValidationService:
    """Fixture to provide a TAPValidationService instance for the tap app.

    Parameters
    ----------
    tap_client_tap
        The TAP client object for the TAP service.

    Returns
    -------
    TAPValidationService
        The TAPValidationService instance.

    """
    return TAPValidationService(tap_client=tap_client_tap, app="tap")


@pytest.fixture(scope="module")
def stilts_jar() -> Path:
    """
    Fixture to download the STILTS JAR file.

    Returns
    -------
    Path
        The path to the STILS JAR file.
    """
    url = STILTS_URL
    file_path = Path(STILTS_FILENAME)
    FileManagerService.download_file(url, file_path)
    return file_path
