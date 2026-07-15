"""Filesystem metadata extraction."""

from __future__ import annotations

import getpass
import os
from datetime import datetime
from pathlib import Path

from file_system_analysis.domain.models import FileRecord


def read_file_metadata(path: Path) -> FileRecord:
    """Read basic metadata for a local file."""
    stat = path.stat()
    return FileRecord(
        path=path,
        file_name=path.name,
        extension=path.suffix.lower(),
        size_bytes=stat.st_size,
        created_at=datetime.fromtimestamp(stat.st_ctime),
        modified_at=datetime.fromtimestamp(stat.st_mtime),
        owner=_read_owner(path),
        status="scanned",
    )


def _read_owner(path: Path) -> str | None:
    """Read the file owner where supported, falling back to the current user."""
    if os.name == "nt":  # pragma: no cover - requires Windows
        try:
            import win32security

            security = win32security.GetFileSecurity(str(path), win32security.OWNER_SECURITY_INFORMATION)
            owner_sid = security.GetSecurityDescriptorOwner()
            owner, domain, _account_type = win32security.LookupAccountSid(None, owner_sid)
            return f"{domain}\\{owner}" if domain else owner
        except Exception:
            return getpass.getuser()
    return getpass.getuser()
