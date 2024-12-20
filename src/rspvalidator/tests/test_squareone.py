"""Test the Squareone homepage."""

from collections.abc import Callable

from playwright.sync_api import Page, expect

from ..config import logger
from ..services.validation import SquareOneValidationService


def test_squareone_homepage_anonymous(
    assert_snapshot: Callable, page_anonymous: Page
) -> None:
    """Test accessing the (Squareone) homepage."""
    validator = SquareOneValidationService(page=page_anonymous)
    validator.validate_squareone_homepage()
    # Ensure that the "Log in" button is present
    expect(page_anonymous.get_by_role("banner")).to_contain_text("Log in")
    assert_snapshot(page_anonymous.screenshot())
    logger.info("Squareone homepage (anonymous) validated.")


def test_squareone_homepage(page: Page) -> None:
    """Test accessing the (Squareone) homepage."""
    validator = SquareOneValidationService(page=page)
    validator.validate_squareone_homepage()
    # Ensure that the "Log in" button is present
    expect(page.get_by_role("banner")).not_to_contain_text("Log in")
    logger.info("Squareone homepage (anonymous) validated.")
