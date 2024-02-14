#!/usr/bin/python3
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
        put(archive_path, "/tmp/", use_sudo=False, mirror_local_mode=False, mode=None)

        # Extract the filename (without the extension)
        # file_name = archive_path.split("/")[-1].split(".")[0]
        file_name = os.path.basename(archive_path).split(".")[0]

        # Create the directory on the server if it doesn't exist
        run(f"mkdir -p /data/web_static/releases/{file_name}")

        # Decompress the archive
        run(f"tar -xzf /tmp/{file_name}.tgz -C /data/web_static/releases/{file_name}/")

        # Adjust the content location
        run(f"mv /data/web_static/releases/{file_name}/web_static/* /data/web_static/releases/{file_name}/")
        run(f"rm -rf /data/web_static/releases/{file_name}/web_static")
        
        # Remove the archive
        run(f"rm /tmp/{file_name}.tgz")

        # Recreate the symbolic link to the new release
        run(f"rm /data/web_static/current")
        run(f"ln -sf /data/web_static/releases/{file_name} /data/web_static/current")

        # Restart nginx service to apply the changes
        run('sudo service nginx restart')


    except Exception:
        return False
    
    # Print and return
    print("New version deployed!")
    return True
    