#!/usr/bin/python3
"""Fabric script to generate tgz archive."""

from datetime import datetime
from fabric.api import local
from os.path import isdir


def do_pack():
    """Generate tgz archive."""
    date_str = datetime.now().strftime("%Y%m%d%H%M%S")
    if not isdir("versions"):
        local("mkdir -p versions")
    archive_path = f"versions/web_static_{date_str}.tgz"
    try:
        local(f"tar -cvzf {archive_path} web_static")
        return archive_path
    except Exception as e:
        print(f"Archive creation failed: {e}")
        return None
