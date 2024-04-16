#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric import task
from os.path import exists

@task
def do_deploy(c, archive_path, hosts=None):
    """distributes an archive to the web servers"""
    if hosts is None:
        hosts = ['142.44.167.228', '144.217.246.195']

    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        c.put(archive_path, '/tmp/', hosts=hosts)
        c.run('mkdir -p {}{}/'.format(path, no_ext), hosts=hosts)
        c.run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext), hosts=hosts)
        c.run('rm /tmp/{}'.format(file_n), hosts=hosts)
        c.run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext), hosts=hosts)
        c.run('rm -rf {}{}/web_static'.format(path, no_ext), hosts=hosts)
        c.run('rm -rf /data/web_static/current', hosts=hosts)
        c.run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext), hosts=hosts)
        return True
    except:
        return False
