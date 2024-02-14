#!/usr/bin/python3
""""Fabric script that distributes an archive to web servers"""
from fabric.api import *
from datetime import datetime
import os


# Set of servers
env.hosts = ['34.207.156.226', '54.90.63.216']


def do_deploy(archive_path):
    """ deploys the new version to the servers listed
    """

    # Check if the archive exists
    if not os.path.exists(archive_path):
        return False

    try:
        # Transfer the archive
        put(archive_path, "/tmp/")

        # Extract the filename (without the extension)
        # file_name = archive_path.split("/")[-1].split(".")[0]
        file_name = os.path.basename(archive_path).split(".")[0]

        # Create the directory on the server if it doesn't exist
        run(f"mkdir -p /data/web_static/releases/{file_name}")

        # Decompress the archive
        run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
            .format(file_name, file_name))

        # Adjust the content location
        up_to_releases = "/data/web_static/releases"
        run("mv {}/{}/web_static/* {}/{}/".format(up_to_releases,
                                                  file_name,
                                                  up_to_releases,
                                                  file_name))

        run(f"rm -rf /data/web_static/releases/{file_name}/web_static")

        # Remove the archive
        run(f"rm /tmp/{file_name}.tgz")

        # Recreate the symbolic link to the new release
        run(f"rm /data/web_static/current")
        run(f"ln -sf {up_to_releases}/{file_name} /data/web_static/current")

        # Restart nginx service to apply the changes
        run('sudo service nginx restart')

        # Print and return
        print("New version deployed!")
        return True

    except Exception:
        return False
