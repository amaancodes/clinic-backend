"""
Deprecated: auth API has moved to app.auth.api.

This module remains only as a thin wrapper to avoid breaking imports
that still reference app.api.auth.auth_bp.
"""

from app.auth.api import auth_bp  # noqa: F401
