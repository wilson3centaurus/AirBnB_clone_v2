#!/usr/bin/python3
"""Distribute archives to web servers."""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['142.44.167.228', '144.217.246.195']


def do_deploy(archive_path):
    """Deploy archive to servers."""
    if not exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        base_dir = file_name.split(".")[0]
        release_path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run(f'mkdir -p {release_path}{base_dir}/')
        run(f'tar -xzf /tmp/{file_name} -C {release_path}{base_dir}/')
        run(f'rm /tmp/{file_name}')
        run(f'mv {release_path}{
            base_dir}/web_static/* {release_path}{base_dir}/')
        run(f'rm -rf {release_path}{base_dir}/web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s {release_path}{base_dir}/ /data/web_static/current')
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False
