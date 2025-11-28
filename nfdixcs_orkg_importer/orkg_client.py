# python
"""
Wrapper for creating an authenticated ORKG client.
"""

from typing import Tuple
from orkg import ORKG

from .config import ORKG_HOST, ORKG_USER, ORKG_PASSWORD, require_credentials


def get_orkg_client(
    host: str | None = None,
    creds: Tuple[str, str] | None = None,
) -> ORKG:
    """
    Return an authenticated ORKG client.

    Priority:
    1) Explicit host / creds arguments
    2) Values from config.py / environment variables
    """
    if host is None:
        host = ORKG_HOST

    if creds is None:
        require_credentials()
        assert ORKG_USER is not None
        assert ORKG_PASSWORD is not None
        creds = (ORKG_USER, ORKG_PASSWORD)

    return ORKG(host=host, creds=creds)
