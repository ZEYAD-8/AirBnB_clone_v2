#!/usr/bin/python3

from fabric.api import local, lcd
from datetime import datetime
import os

def do_pack():
    """ this function will pack the contents of the web static folder and
    compress it into an archive named by the date and time of its creation.
    """
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = f"web_static_{date}.tgz"
        directory_name = "versions"
        print(f"Packing web_static to {directory_name}/{archive_name}")

        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        with lcd(directory_name):
            local(f"tar -zcvf {archive_name} ../web_static/")
            archive_size = os.path.getsize(f"{archive_name}")

        print("web_static packed: {}/{} -> {}".format(directory_name, 
                                                      archive_name, 
                                                      archive_size))

        return f"{directory_name}/{archive_name}"

    except Exception:
        return None
