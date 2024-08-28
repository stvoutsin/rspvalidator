"""Validators used to assert the expected behavior of the Rubin Science Platform."""

import time
from abc import ABC, abstractmethod
from pathlib import Path

import pyvo
from jinja2 import Environment, FileSystemLoader
from lxml import etree
from playwright.sync_api import Page, expect

from ..config import BASE_URL, logger, taplint_maximums
from ..constants import TAP_SCHEMA_QUERY
from .configreader import ConfigReaderService
from .taplint import TaplintParserService

__all__ = [
    "TAPValidationService",
    "SquareOneValidationService",
    "TaplintValidationService",
    "BaseValidationService",
]


class BaseValidationService(ABC):
    """Abstract base class for validation services."""

    @abstractmethod
    def validate(self) -> None:
        """Abstract method for validation."""
        ...


class TAPValidationService:
    """
    Validators used to assert the expected behavior of the
    Rubin Science Platform's TAP service.
    """

    def __init__(self, tap_client: pyvo.dal.TAPService, app: str) -> None:
        self.tap_client = tap_client
        self.app = app

    def validate(self) -> None:
        """Validate the TAP service."""
        self.validate_tables()
        self.validate_uws_endpoint()

    def validate_uws_endpoint(self) -> None:
        """Validate the UWS endpoint."""
        query = TAP_SCHEMA_QUERY
        job = self.tap_client.submit_job(query)
        job.run()
        start_time = time.time()
        timedout = False

        while job.phase in ("EXECUTING", "PENDING", "QUEUED"):
            if time.time() - start_time > 30:
                timedout = True
                break
            time.sleep(1)

        assert not timedout
        assert job.phase == "COMPLETED"
        assert job.destruction is not None
        assert job.owner is not None
        assert job.quote is not None
        assert job.execution_duration is not None
        assert job.job_id is not None
        assert job.query == TAP_SCHEMA_QUERY
        assert job.result.href.startswith(f"{BASE_URL}/api/{self.app}/results")
        job.delete()

    @staticmethod
    def validate_capabilities(
        app: str,
        *,
        include_datamodel: bool = False,
        include_geometry: bool = False,
        include_upload: bool = False,
        actual_capabilities: bytes,
    ) -> None:
        """
        Validate the /capabilities endpoint.

        Parameters
        ----------
        app
            The application name.
        include_datamodel
            Whether to include the Obscore datamodel in the capabilities.
        include_geometry
            Whether to include the additional ADQL geometry in the capabilities.
        include_upload
            Whether to include TAP_UPLOAD in the capabilities.
        actual_capabilities
            The actual capabilities XML.
        """
        # Go up one directory level and then into the 'templates' directory
        templates_dir = Path(__file__).parent.parent / "templates"
        env = Environment(  # noqa: S701
            loader=FileSystemLoader(templates_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        template = env.get_template("capabilities.xml")

        # Render the template
        expected_capabilities = template.render(
            BASE_URL=BASE_URL,
            app=app,
            include_datamodel=include_datamodel,
            include_geometry=include_geometry,
            include_upload=include_upload,
        )
        expected_root = etree.fromstring(  # noqa: S320
            expected_capabilities.encode()
        )
        actual_root = etree.fromstring(actual_capabilities)  # noqa: S320

        actual_xml_str = etree.tostring(
            actual_root, pretty_print=True, encoding="unicode"
        )
        expected_xml_str = etree.tostring(
            expected_root, pretty_print=True, encoding="unicode"
        )

        assert (
            actual_xml_str == expected_xml_str
        ), "The actual XML does not match the expected XML"

    def validate_tables(self) -> None:
        """Validate that the TAP client has tables."""
        tables = self.tap_client.tables
        assert tables is not None
        assert len(tables) > 0


class SquareOneValidationService:
    """Validators used to assert the expected behavior of the
    Rubin Science Platform's squareone app.
    """

    def __init__(self, page: Page) -> None:
        self.page = page

    def validate(self) -> None:
        """Validate the Rubin Science Platform's squareone app."""
        self.validate_squareone_homepage()

    def validate_squareone_homepage(self) -> None:
        """Validate the RSP (squareone) homepage."""
        self.page.goto(ConfigReaderService.get_url("squareone"))
        self.page.goto(BASE_URL)
        expect(self.page.locator("h1")).to_contain_text("Rubin Science Platform")
        expect(self.page.locator("section")).to_contain_text("Portal")
        expect(self.page.locator("section")).to_contain_text("Notebooks")
        expect(self.page.locator("section")).to_contain_text("APIs")


class TaplintValidationService:
    """Validators used to assert the expected behavior of the
    Rubin Science Platform's tap & ssotap apps using taplint.
    """

    def __init__(self, app: str, output: str) -> None:
        self._max_errors = taplint_maximums[app]["errors"]
        self._max_warnings = taplint_maximums[app]["warnings"]
        self.output = output

    def validate(self) -> None:
        """Validate the Rubin Science Platform's squareone app."""
        self.validate_summary()

    def validate_summary(self) -> None:
        """Validate an RSP Taplint run."""
        error_count, warning_count = TaplintParserService.parse_summary(self.output)

        assert error_count is not None, "Failed to parse TAPLINT summary"

        assert error_count <= self._max_errors, (
            f"TAPLINT reported {error_count} errors, which exceeds the limit "
            f"of {self._max_errors}"
        )

        assert warning_count <= self._max_warnings, (
            f"TAPLINT reported {warning_count} warnings, which exceeds the "
            f"limit of {self._max_warnings}"
        )

        logger.info("Full output:")
        logger.info(self.output)
