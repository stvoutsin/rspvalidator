"""Config file."""
import os
import sys

import pyvo
import structlog

from .models.tap import QueryMode, TAPApplication
from .models.test import TestScenario
from .services.filemanager import FileManagerService

logger = structlog.get_logger()

# Load environment variables
HOSTNAME = os.getenv("HOSTNAME", "data-dev.lsst.cloud")
BASE_URL = f"https://{HOSTNAME}"
HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"
TOKEN = os.getenv("TOKEN", "")
SKIP_TESTS = True

try:
    FileManagerService.check_auth_file()
except FileNotFoundError as e:
    logger.exception("Auth file not found", exc_info=e)
    sys.exit(1)

if not HOSTNAME:
    logger.error("HOSTNAME environment variable is not set.")
    raise ValueError("HOSTNAME environment variable is not set.")

if not TOKEN:
    logger.error("TOKEN environment variable is not set.")
    raise ValueError("TOKEN environment variable is not set.")

capability_includes = {
    "tap": {
        "include_upload": os.getenv("TAP_INCLUDE_UPLOAD", "False").lower()
        == "true",
        "include_datamodel": os.getenv("TAP_INCLUDE_DATAMODEL", "True").lower()
        == "true",
        "include_geometry": os.getenv("TAP_INCLUDE_GEOMETRY", "False").lower()
        == "true",
    },
    "ssotap": {
        "include_upload": os.getenv("SSOTAP_INCLUDE_UPLOAD", "True").lower()
        == "true",
        "include_datamodel": os.getenv(
            "SSOTAP_INCLUDE_DATAMODEL", "False"
        ).lower()
        == "true",
        "include_geometry": os.getenv("SSOTAP_INCLUDE_GEOMETRY", "True").lower()
        == "true",
    },
}

# Mapping of app name to RSP endpoint
urls = {
    "portal": f"{BASE_URL}/portal/app",
    "nublado": f"{BASE_URL}/nb",
    "api": f"{BASE_URL}/api/tap",
    "squareone": f"{BASE_URL}/",
    "tap": f"{BASE_URL}/api/tap",
    "ssotap": f"{BASE_URL}/api/ssotap",
    "datalink": f"{BASE_URL}/api/datalink",
}

query_methods = {
    QueryMode.SYNC: pyvo.dal.TAPService.run_sync,
    QueryMode.ASYNC: pyvo.dal.TAPService.run_async,
}

SCENARIOS = [
    TestScenario(TAPApplication.SSOTAP, QueryMode.SYNC, 5),
    TestScenario(TAPApplication.SSOTAP, QueryMode.SYNC, 10),
    TestScenario(TAPApplication.SSOTAP, QueryMode.ASYNC, 1),
    TestScenario(TAPApplication.SSOTAP, QueryMode.ASYNC, 10),
    TestScenario(TAPApplication.TAP, QueryMode.SYNC, 1),
    TestScenario(TAPApplication.TAP, QueryMode.SYNC, 10),
    TestScenario(TAPApplication.TAP, QueryMode.ASYNC, 1),
    TestScenario(TAPApplication.TAP, QueryMode.ASYNC, 10),
]

taplint_maximums = {
    "tap": {"errors": 92, "warnings": 2},
    "ssotap": {"errors": 47, "warnings": 1},
}
