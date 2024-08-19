"""TAP Factory module. used to generate TAP related objects."""

import pyvo
import requests

from ..services.tap import TAPOperationsService

__all__ = ["TAPFactory"]


class TAPFactory:
    """TAP client factory class."""

    def __init__(self) -> None:
        pass

    @staticmethod
    def make_client(auth_token: str, app: str) -> pyvo.dal.TAPService:
        """Create a TAP client with an authenticated session.

        Parameters
        ----------
        auth_token
            The authentication token.
        app
            The application name.

        Returns
        -------
        pyvo.dal.TAPService: The TAP client object.
        """
        tap_url = TAPOperationsService.get_api_endpoint("tap", app)
        s = requests.Session()
        s.headers["Authorization"] = "Bearer " + auth_token
        auth = pyvo.auth.AuthSession()
        auth.credentials.set("lsst-token", s)
        auth.add_security_method_for_url(tap_url, "lsst-token")
        auth.add_security_method_for_url(tap_url + "/sync", "lsst-token")
        auth.add_security_method_for_url(tap_url + "/async", "lsst-token")
        auth.add_security_method_for_url(tap_url + "/tables", "lsst-token")
        return pyvo.dal.TAPService(tap_url, auth)
