#!/usr/bin/python3
""" Creates and distributes an archive to web servers,
using created function deploy and pack"""
from fabric.api import *
import os

do_pack = __import__('1-pack_web_static').do_pack
do_deploy = __import__('2-do_deploy_web_static').do_deploy
env.hosts = ['34.207.156.226', '54.90.63.216']


def deploy():
    """ Pack and deploy all of web static """

    archive_path = do_pack()
    if not archive_path:
        print("Archive was not succesfully created")
        return False

    return_value = do_deploy(archive_path)
    return return_value
