"""Tests for the TAP API."""

from typing import Any

import pytest
import pyvo
from playwright.sync_api import Page

from ..config import SCENARIOS, capability_includes, logger
from ..models.test import Scenario
from ..services.configreader import ConfigReaderService
from ..services.tap import TAPOperationsService, TAPQueryRunnerService
from ..services.testrunner import Runner
from ..services.validation import TAPValidationService


def test_tap_capabilities_ssotap(
    tap_client_ssotap: pyvo.dal.TAPService,
    tap_validation_service_ssotap: TAPValidationService,
    data_dir: str,
    page: Page,
) -> None:
    """Test SSO TAP capabilities endpoint.

    Check that the content of the capabilities XML returned by the SSOTAP
    service matches what is in the data directory.

    Parameters
    ----------
    tap_client_ssotap
        The TAP client object for the SSO TAP service.
    tap_validation_service_ssotap
        The TAP validation service for the SSO TAP service.
    data_dir
        The data directory path.
    page
        The Playwright page object.
    """
    # I used playwright instead of just HTTP access here because I was
    # experimenting with it. I'll probably switch this to use pyvo instead

    app = "ssotap"
    response = page.request.get(
        TAPOperationsService.get_api_endpoint("capabilities", app)
    )
    assert response.status == 200
    tap_validation_service_ssotap.validate_capabilities(
        app=app,
        include_datamodel=capability_includes[app]["include_datamodel"],
        include_geometry=capability_includes[app]["include_geometry"],
        include_upload=capability_includes[app]["include_upload"],
        actual_capabilities=response.body(),
    )


def test_tap_capabilities_tap(
    tap_client_tap: pyvo.dal.TAPService,
    tap_validation_service_tap: TAPValidationService,
    data_dir: str,
    page: Page,
) -> None:
    """Test TAP capabilities endpoint.

    Check that the content of the capabilities XML returned by the TAP service
    matches what is in the data directory.

    Parameters
    ----------
    tap_client_tap
        The TAP client object for the SSO TAP service.
    tap_validation_service_tap
        The TAP validation service for the SSO TAP service.
    data_dir
        The data directory path.
    page
        The Playwright page object.
    """
    app = "tap"
    response = page.request.get(
        TAPOperationsService.get_api_endpoint("capabilities", app)
    )
    assert response.status == 200
    tap_validation_service_tap.validate_capabilities(
        app=app,
        include_datamodel=capability_includes[app]["include_datamodel"],
        include_geometry=capability_includes[app]["include_geometry"],
        include_upload=capability_includes[app]["include_upload"],
        actual_capabilities=response.body(),
    )


@pytest.mark.parametrize("scenario", SCENARIOS, ids=lambda s: s.description)
def test_tap_queries(
    request: Any,
    scenario: Scenario,
    data_dir: str,
) -> None:
    """
    Test synchronous TAP queries for execution time and row count with
    concurrent users.

    This test fetches SQL queries from a JSON file, executes each query
    using a TAP sync query concurrently with a specified number of
    users, and checks if the execution time < 2 * expected duration and if
    the row count matches the expected row count.
    """
    app = scenario.app.value.lower()
    client = request.getfixturevalue("tap_client_" + app)
    results_all_users = Runner.run_concurrent_test(
        test_function=TAPQueryRunnerService.run_query_test,
        test_data=ConfigReaderService().get_queries(data_dir=data_dir, app=app),
        user_count=scenario.users,
        client=client,
        mode=scenario.mode,
    )
    for user_result in results_all_users:
        for result in user_result:
            assert result.status == "OK", "Response status is not OK"
            assert result.execution_duration <= 2 * result.expected_duration, (
                f"Query execution time ({result.execution_duration:.2f}s) is more "
                f"than twice the expected duration ("
                f"{result.expected_duration:.2f}s)"
            )
            assert result.row_count == result.expected_row_count, (
                f"Row count ({result.row_count}) does not match the expected row count "
                f"({result.expected_row_count})"
            )

            logger.info(
                f"{scenario.app.value.upper()} {scenario.mode.value} query "
                f"[{result.query}] test "
                f"completed successfully with {scenario.users}"
                f" users after {result.execution_duration:.2f} seconds."
            )


def test_tap_get_tables_ssotap(
    tap_client_ssotap: pyvo.dal.TAPService,
    tap_validation_service_ssotap: TAPValidationService,
) -> None:
    """Test the SSO TAP tables endpoint."""
    tap_validation_service = TAPValidationService(
        tap_client=tap_client_ssotap, app="ssotap"
    )
    tap_validation_service.validate_tables()


def test_tap_get_tables_tap(
    tap_client_tap: pyvo.dal.TAPService,
    tap_validation_service_tap: TAPValidationService,
) -> None:
    """Test the TAP tables endpoint."""
    tap_validation_service = TAPValidationService(tap_client=tap_client_tap, app="tap")
    tap_validation_service.validate_tables()


def test_tap_uws_endpoint_ssotap(
    tap_client_ssotap: pyvo.dal.TAPService,
    tap_validation_service_ssotap: TAPValidationService,
) -> None:
    """Test the SSO TAP UWS endpoint."""
    tap_validation_service = TAPValidationService(
        tap_client=tap_client_ssotap, app="ssotap"
    )
    tap_validation_service.validate_uws_endpoint()


def test_tap_uws_endpoint_tap(
    tap_client_tap: pyvo.dal.TAPService,
    tap_validation_service_tap: TAPValidationService,
) -> None:
    """Test the TAP UWS endpoint."""
    tap_validation_service = TAPValidationService(tap_client=tap_client_tap, app="tap")
    tap_validation_service.validate_uws_endpoint()


if __name__ == "__main__":
    pytest.main()
