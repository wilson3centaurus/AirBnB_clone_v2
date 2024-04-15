#!/usr/bin/python3
"""Full deployment of a web_static folder."""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

env.hosts = ['142.44.167.228', '144.217.246.195']


def do_pack():
    """Generate .tgz archive."""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            local("mkdir -p versions")
        archive_path = f"versions/web_static_{date}.tgz"
        local(f"tar -cvzf {archive_path} web_static")
        return archive_path
    except Exception as e:
        print(f"Pack failed: {e}")
        return False


def do_deploy(archive_path):
    """Distribute archive to servers."""
    if not exists(archive_path):
        return False
    try:
        file_name = archive_path.split('/')[-1]
        base_name = file_name.split('.')[0]
        release_path = f"/data/web_static/releases/{base_name}"
        put(archive_path, '/tmp/')
        run(f"mkdir -p {release_path}/")
        run(f"tar -xzf /tmp/{file_name} -C {release_path}/")
        run(f"rm /tmp/{file_name}")
        run(f"mv {release_path}/web_static/* {release_path}/")
        run(f"rm -rf {release_path}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {release_path}/ /data/web_static/current")
        return True
    except Exception as e:
        print(f"Deploy failed: {e}")
        return False


def deploy():
    """Create and distribute archive."""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
