#!/usr/bin/python3
""" Fabfile that create a .tgz archive from
the contents of web_static folder"""

# if __name__ == '__main__':
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """ this function will pack the contents of the web static folder and
    compress it into an archive named by the date and time of its creation.
    """
    try:
        # Create the archive name
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = f"web_static_{date}.tgz"

        # Start the packing
        directory_name = "versions"
        print(f"Packing web_static to {directory_name}/{archive_name}")

        # Create the destination folder if it doesn't exist
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        # Create the archive of the web_static folder
        local(f"tar -czvf {directory_name}/{archive_name} web_static")

        # Display the size of the archive
        archive_size = os.path.getsize(f"{directory_name}/{archive_name}")
        print("web_static packed: {}/{} -> {}".format(directory_name,
                                                      archive_name,
                                                      archive_size))

        # Retrun the archive path
        archive_path = f"{directory_name}/{archive_name}"
        return archive_path

    except Exception:
        return None
