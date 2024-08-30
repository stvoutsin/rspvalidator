"""Test Nublado tutorial notebooks."""

import time

import pytest
from playwright.sync_api import Page, expect

from ..config import BASE_URL, SKIP_TESTS
from ..services.configreader import ConfigReaderService

# Note: The content of these tests is probably too lengthy, maybe break out
# into helper methods or read validation content from a config


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test as per config flag")
def test_restart_kernels(page: Page) -> None:
    """Restart all kernels."""
    # TODO(stvoutsin): Add a check here,
    #  if we get the image selection choose default
    # Go to Nublado homepage
    page.goto(ConfigReaderService.get_url("nublado"))
    page.get_by_text("Kernel", exact=True).click()
    page.locator("#jp-mainmenu-kernel").get_by_text("Shut Down All Kernels…").click()
    page.get_by_role("button", name="Shut Down All").click()


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test as per config flag")
def test_nublado_dp02_02b_catalog_access(page: Page) -> None:
    """Test the Nublado tutorial dp02 catalog access notebook."""
    # Go to Nublado homepage
    page.goto(ConfigReaderService.get_url("nublado"))

    # Go to main directory
    locator = page.locator("[title^='/home/']").first
    locator.locator("path").dblclick()
    page.get_by_text("File", exact=True).click()
    page.locator("#jp-mainmenu-file").get_by_text("Open from Path…").click()
    page.get_by_placeholder("/path/relative/to/jlab/root").fill(
        "/notebooks/tutorial-notebooks/DP02_02b_Catalog_Queries_with_TAP.ipynb"
    )
    page.get_by_placeholder("/path/relative/to/jlab/root").press("Enter")

    # Wait for tab to load
    expect(
        page.get_by_text(
            "Description: Execute complex ADQL queries with the TAP service."
        )
    ).to_be_visible()

    # This is a hack, need to figure out why run is started before things
    # are loaded
    time.sleep(5)

    # Run notebook
    page.get_by_text("Run", exact=True).click()
    page.locator("#jp-mainmenu-run").get_by_text("Run All Cells", exact=True).click()

    # Validate some of the expected output
    expect(
        page.get_by_label("DP02_02b_Catalog_Queries_with_TAP.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).to_contain_text("173 rows")

    expect(
        page.get_by_label("DP02_02b_Catalog_Queries_with_TAP.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).to_contain_text("1651589610221899038")

    # Check that there are no errors
    expect(
        page.get_by_label("DP02_02b_Catalog_Queries_with_TAP.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).not_to_contain_text("Traceback")
    expect(
        page.get_by_label("DP02_02b_Catalog_Queries_with_TAP.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).not_to_contain_text("Error")


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test as per config flag")
def test_nublado_dp02_06b_interactive_visualization(page: Page) -> None:
    """Test the Nublado tutorial dp02 interactive visualization notebook."""
    # Go to Nublado homepage
    page.goto(ConfigReaderService.get_url("nublado"))

    # Open Notebook
    home_dir = page.locator("[title^='/home/']").first
    home_dir.locator("path").dblclick()
    page.get_by_text("File", exact=True).click()
    page.locator("#jp-mainmenu-file").get_by_text("Open from Path…").click()
    page.get_by_placeholder("/path/relative/to/jlab/root").fill(
        "/notebooks/tutorial-notebooks/"
        "DP02_06b_Interactive_Catalog_Visualization.ipynb"
    )
    page.get_by_placeholder("/path/relative/to/jlab/root").press("Enter")

    # Ensures that tab is loaded before running
    expect(page.get_by_text("Description: Interactive")).to_be_visible()

    # This is a hack, need to figure out why run is started before things
    # are loaded
    time.sleep(5)

    # Run notebook
    page.get_by_text("Run", exact=True).click()
    page.locator("#jp-mainmenu-run").get_by_text("Run All Cells", exact=True).click()

    # Validate some of the expected output
    expect(
        page.get_by_label(
            "DP02_06b_Interactive_Catalog_Visualization.ipynb"
        ).get_by_label("Cells", exact=True)
    ).to_contain_text("BokehJS 3.4.2 successfully loaded.")

    expect(
        page.get_by_label(
            "DP02_06b_Interactive_Catalog_Visualization.ipynb"
        ).get_by_label("Cells", exact=True)
    ).to_contain_text("26914")

    # Check that there are no errors
    expect(
        page.get_by_label(
            "DP02_06b_Interactive_Catalog_Visualization.ipynb"
        ).get_by_label("Cells", exact=True)
    ).not_to_contain_text("Traceback")

    expect(
        page.get_by_label(
            "DP02_06b_Interactive_Catalog_Visualization.ipynb"
        ).get_by_label("Cells", exact=True)
    ).not_to_contain_text("Error")


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test as per config flag")
def test_nublado_dp03_06_upload_tables(page: Page) -> None:
    """Test the Nublado tutorial dp03 table upload notebook."""
    page.goto(ConfigReaderService.get_url("nublado"))

    # Open Notebook
    home_dir = page.locator("[title^='/home/']").first
    home_dir.locator("path").dblclick()
    page.get_by_text("File", exact=True).click()
    page.locator("#jp-mainmenu-file").get_by_text("Open from Path…").click()
    page.get_by_placeholder("/path/relative/to/jlab/root").fill(
        "/notebooks/tutorial-notebooks/DP03_06_User_Uploaded_Tables.ipynb"
    )
    page.get_by_placeholder("/path/relative/to/jlab/root").press("Enter")

    # Ensures that tab is loaded before running
    page.get_by_text("Description: Use the TAP").click()

    # This is a hack, need to figure out why run is started before things
    # are loaded
    time.sleep(5)

    # Run notebook
    page.get_by_text("Run", exact=True).click()
    page.locator("#jp-mainmenu-run").get_by_text("Run All Cells", exact=True).click()

    # Validate some of the expected output
    expect(
        page.get_by_label("DP03_06_User_Uploaded_Tables.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).to_contain_text("Table length=15")
    expect(
        page.get_by_label("DP03_06_User_Uploaded_Tables.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).to_contain_text("Job phase is COMPLETED")
    expect(
        page.get_by_label("DP03_06_User_Uploaded_Tables.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).to_contain_text("Table length=672")
    expect(
        page.get_by_label("DP03_06_User_Uploaded_Tables.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).to_contain_text("4350915375550808373")

    # Check that there are no errors
    expect(
        page.get_by_label("DP03_06_User_Uploaded_Tables.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).not_to_contain_text("Traceback")
    expect(
        page.get_by_label("DP03_06_User_Uploaded_Tables.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).not_to_contain_text("Error")


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test as per config flag")
def test_nublado_dp02_13a_image_cutout(page: Page) -> None:
    """Test the Nublado tutorial dp02 Image Cutout demo notebook."""
    # Go to Nublado page
    page.goto(ConfigReaderService.get_url("nublado"))

    # Open Notebook
    home_dir = page.locator("[title^='/home/']").first
    home_dir.locator("path").dblclick()
    page.get_by_text("File", exact=True).click()
    page.locator("#jp-mainmenu-file").get_by_text("Open from Path…").click()
    page.get_by_placeholder("/path/relative/to/jlab/root").fill(
        "/notebooks/tutorial-notebooks/DP02_13a_Image_Cutout_SciDemo.ipynb"
    )
    page.get_by_placeholder("/path/relative/to/jlab/root").press("Enter")

    # Ensures that tab is loaded before running
    page.get_by_label("DP02_13a_Image_Cutout_SciDemo.ipynb").get_by_role(
        "heading", name="Using the image cutout tool"
    ).click()

    # This is a hack, need to figure out why run is started before things
    # are loaded
    time.sleep(5)

    page.get_by_text("Run", exact=True).click()
    page.locator("#jp-mainmenu-run").get_by_text("Run All Cells", exact=True).click()

    # Validate some of the expected output
    expect(
        page.get_by_label("DP02_13a_Image_Cutout_SciDemo.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).to_contain_text(f"{BASE_URL}/api/datalink/links?")
    expect(
        page.get_by_label("DP02_13a_Image_Cutout_SciDemo.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).to_contain_text("Table length=162452")
    expect(
        page.get_by_label("DP02_13a_Image_Cutout_SciDemo.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).to_contain_text("Table length=1")

    # Check that there are no errors
    expect(
        page.get_by_label("DP02_13a_Image_Cutout_SciDemo.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).not_to_contain_text("Traceback")
    expect(
        page.get_by_label("DP02_13a_Image_Cutout_SciDemo.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).not_to_contain_text("Error")
