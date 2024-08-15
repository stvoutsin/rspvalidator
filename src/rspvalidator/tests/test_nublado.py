"""Test Nublado tutorial notebooks."""

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
    page.get_by_text("Kernel", exact=True).click(timeout=100000)
    page.locator("#jp-mainmenu-kernel").get_by_text("Shut Down All Kernels…").click()
    page.get_by_role("button", name="Shut Down All").click()


@pytest.mark.skipif(SKIP_TESTS, reason="Skipping test as per config flag")
def test_nublado_dp02_02b_catalog_access(page: Page) -> None:
    """Test the Nublado tutorial dp02 catalog access notebook."""
    # Go to Nublado homepage
    page.goto(ConfigReaderService.get_url("nublado"), timeout=90000)

    # Go to main directory
    locator = page.locator("[title^='/home/']").first
    locator.locator("path").dblclick(timeout=60000)
    page.get_by_text("File", exact=True).click()
    page.locator("#jp-mainmenu-file").get_by_text("Open from Path…").click()
    page.get_by_placeholder("/path/relative/to/jlab/root").fill(
        "/notebooks/tutorial-notebooks/DP02_02b_Catalog_Queries_with_TAP.ipynb"
    )
    page.get_by_placeholder("/path/relative/to/jlab/root").press("Enter")

    # Wait for tab to load
    # Add check here

    # Run notebook
    page.get_by_text("Run", exact=True).click()
    page.locator("#jp-mainmenu-run").get_by_text("Run All Cells", exact=True).click()

    # Validate some of the expected output
    expect(
        page.get_by_label("DP02_02b_Catalog_Queries_with_TAP.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).to_contain_text("383 unique objects returned", timeout=1000000)
    expect(
        page.get_by_label("DP02_02b_Catalog_Queries_with_TAP.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).to_contain_text("1343", timeout=1000000)

    # Check that there are no errors
    expect(
        page.get_by_label("DP02_02b_Catalog_Queries_with_TAP.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).not_to_contain_text("Traceback", timeout=1000000)
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
    home_dir.locator("path").dblclick(timeout=60000)
    page.get_by_text("File", exact=True).click()
    page.locator("#jp-mainmenu-file").get_by_text("Open from Path…").click()
    page.get_by_placeholder("/path/relative/to/jlab/root").fill(
        "/notebooks/tutorial-notebooks/DP02_06b_Interactive_Catalog_Visualization.ipynb"
    )
    page.get_by_placeholder("/path/relative/to/jlab/root").press("Enter")

    # Ensures that tab is loaded before running
    expect(page.get_by_text("Description: Interactive")).to_be_visible()

    # Run notebook
    page.get_by_text("Run", exact=True).click()
    page.locator("#jp-mainmenu-run").get_by_text("Run All Cells", exact=True).click()

    # Validate some of the expected output
    expect(
        page.get_by_label(
            "DP02_06b_Interactive_Catalog_Visualization.ipynb"
        ).get_by_label("Cells", exact=True)
    ).to_contain_text("BokehJS 3.4.1 successfully loaded.", timeout=1000000)

    expect(
        page.get_by_label(
            "DP02_06b_Interactive_Catalog_Visualization.ipynb"
        ).get_by_label("Cells", exact=True)
    ).to_contain_text("26914", timeout=1000000)

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
    home_dir.locator("path").dblclick(timeout=60000)
    page.get_by_text("File", exact=True).click()
    page.locator("#jp-mainmenu-file").get_by_text("Open from Path…").click()
    page.get_by_placeholder("/path/relative/to/jlab/root").fill(
        "/notebooks/tutorial-notebooks/DP03_06_User_Uploaded_Tables.ipynb"
    )
    page.get_by_placeholder("/path/relative/to/jlab/root").press("Enter")

    # Ensures that tab is loaded before running
    page.get_by_text("Description: Use the TAP").click()

    # Run notebook
    page.get_by_text("Run", exact=True).click()
    page.locator("#jp-mainmenu-run").get_by_text("Run All Cells", exact=True).click()

    # Validate some of the expected output
    expect(
        page.get_by_label("DP03_06_User_Uploaded_Tables.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).to_contain_text("Table length=15", timeout=1000000)
    expect(
        page.get_by_label("DP03_06_User_Uploaded_Tables.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).to_contain_text("Job phase is COMPLETED", timeout=1000000)
    expect(
        page.get_by_label("DP03_06_User_Uploaded_Tables.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).to_contain_text("Table length=672", timeout=1000000)
    expect(
        page.get_by_label("DP03_06_User_Uploaded_Tables.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).to_contain_text("4350915375550808373", timeout=1000000)

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
    home_dir.locator("path").dblclick(timeout=60000)
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

    page.get_by_text("Run", exact=True).click()
    page.locator("#jp-mainmenu-run").get_by_text("Run All Cells", exact=True).click()

    # Validate some of the expected output
    expect(
        page.get_by_label("DP02_13a_Image_Cutout_SciDemo.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).to_contain_text(f"{BASE_URL}/api/datalink/links?", timeout=1000000)
    expect(
        page.get_by_label("DP02_13a_Image_Cutout_SciDemo.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).to_contain_text("Table length=162452", timeout=1000000)
    expect(
        page.get_by_label("DP02_13a_Image_Cutout_SciDemo.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).to_contain_text("Table length=1", timeout=1000000)

    # Check that there are no errors
    expect(
        page.get_by_label("DP02_13a_Image_Cutout_SciDemo.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).not_to_contain_text("Traceback", timeout=1000000)
    expect(
        page.get_by_label("DP02_13a_Image_Cutout_SciDemo.ipynb").get_by_label(
            "Cells", exact=True
        )
    ).not_to_contain_text("Error", timeout=1000000)
