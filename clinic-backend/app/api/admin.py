"""
Deprecated: admin API has moved to app.admin.api.

This module remains only as a thin wrapper to avoid breaking imports
that still reference app.api.admin.admin_bp.
"""

from app.admin.api import admin_bp  # noqa: F401
