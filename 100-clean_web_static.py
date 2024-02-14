#!/usr/bin/python3
"""Clean all archives based on the number of
arguements passed"""
from fabric.api import *
import os
from operator import length_hint

env.hosts = ['34.207.156.226', '54.90.63.216']


def do_clean(number=0):
    """Cleans all .tgz files"""
    """if os.path.exists('versions'):
        # with cd('versions'):
        # local('find ')
        path = 'versions'
        files = [file for file in os.listdir(
            path) if 'web' in file and '.tgz' in file]

        print(files)

        length = len(files)
        if int(number) > length:
            exit
        if int(number) == 0 or int(number) == 1:
            last = 1
        else:
            last = int(number)

        if files:
            for index in range(length - last):
              local('rm versions/{}'.format(files[index]))"""

    number = int(number)
    if number == 0:
        number = 2
    else:
        number += 1

    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(path, number))
