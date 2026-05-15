"""Navigation helpers for page redirects."""

from fastapi.responses import RedirectResponse
from src.ui.constants import ROOT_ROUTE, MENU_ROUTE

def redirect_to_root() -> RedirectResponse:
    """Redirect to the root player selector page."""
    return RedirectResponse(url=ROOT_ROUTE, status_code=307)

def redirect_to_menu() -> RedirectResponse:
    """Redirect to the main menu page."""
    return RedirectResponse(url=MENU_ROUTE, status_code=307)
