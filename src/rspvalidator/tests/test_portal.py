"""Test the portal page."""

import re
import time
from collections.abc import Callable

from playwright.sync_api import Page, expect

from ..services.configreader import ConfigReaderService


def test_query_dp02(page: Page) -> None:
    """Test the portal with a dp02 query."""
    # Go to Portal page
    portal_url = ConfigReaderService.get_url("portal")
    page.goto(portal_url)

    # Open DP03 Tab and execute ADQL query
    page.get_by_role("tab", name="Search DP0.2 catalogs").click()
    page.locator("div").filter(
        has_text=re.compile(r"^View: UI assistedEdit ADQL$")
    ).first.click()
    page.get_by_role("button", name="Edit ADQL", exact=True).click()
    page.locator("#adqlEditor").fill(
        """
        SELECT *
        FROM dp02_dc2_catalogs.Object
        WHERE CONTAINS(POINT('ICRS', coord_ra, coord_dec),
        CIRCLE('ICRS', 62, -37, 0.05)) = 1
        ORDER BY coord_ra desc
        """
    )

    # Run query
    page.get_by_role("button", name="Search").click()

    # Validate results
    expect(page.get_by_role("grid")).to_contain_text("62.0620699")

    # Check UWS job info
    page.get_by_role("button", name="Show additional table info").click()
    expect(page.locator("#dialogRootDiv")).to_contain_text("COMPLETED")


def test_query_dp03(page: Page) -> None:
    """Test the portal with a DP03 query."""
    # Go to Portal page
    page.goto(ConfigReaderService.get_url("portal"))

    # Open DP03 Tab and execute ADQL query
    page.get_by_role("tab", name="Search DP0.3 catalogs").click()
    page.locator("div").filter(
        has_text=re.compile(r"^View: UI assistedEdit ADQL$")
    ).first.click()
    page.get_by_role("button", name="Edit ADQL", exact=True).click()
    page.locator("#adqlEditor").fill(
        "SELECT TOP 1000 * FROM dp03_catalogs_10yr.SSObject ORDER BY ssObjectId"
    )

    # Run query
    page.get_by_role("button", name="Search").click()

    # Check first row value
    expect(page.get_by_role("grid")).to_contain_text("112.6117")
    expect(page.get_by_role("grid")).to_contain_text("60513")

    # Check UWS job info
    page.get_by_role("button", name="Show additional table info").click()
    expect(page.locator("#dialogRootDiv")).to_contain_text("COMPLETED")


def test_query_dp02_obscore(page: Page, assert_snapshot: Callable) -> None:
    """Test the portal with a dp02 obscore query."""
    # Go to Portal page
    page.goto(ConfigReaderService.get_url("portal"))

    # Open DP03 Tab and execute ADQL query
    page.get_by_role("tab", name="Search DP0.2 catalogs").click()
    page.locator("div").filter(
        has_text=re.compile(r"^View: UI assistedEdit ADQL$")
    ).first.click()
    page.get_by_role("button", name="Edit ADQL", exact=True).click()
    page.locator("#adqlEditor").fill(
        "SELECT TOP 5 * FROM ivoa.ObsCore ORDER BY obs_id ASC"
    )

    # Run query
    page.get_by_role("button", name="Search").click()

    # Check Datalink exists
    expect(page.get_by_role("grid")).to_contain_text(
        f"{ConfigReaderService.get_url('datalink')}/links?ID=butler"
    )

    time.sleep(20)
    # Take a screenshot and assert it is as expected
    assert_snapshot(page.screenshot())

    # Check UWS job info
    page.get_by_role("button", name="Show additional table info").click()
    expect(page.locator("#dialogRootDiv")).to_contain_text("COMPLETED")
