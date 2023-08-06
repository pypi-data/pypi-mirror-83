#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import atexit, os

from setuptools import setup
from setuptools.command.install import install

class Install(install):
    def __init__(self, *args, **kwargs):
        super(Install, self).__init__(*args, **kwargs)
        atexit.register(postinstall)

def nopen(txt):
    txt += " 2>&1"
    try:
        for line in os.popen(txt).readlines():
            pass
    except:
        pass

def bopen(txt):
    try:
        for line in os.popen(txt).readlines():
            print(line.rstrip())
    except:
        pass

def postinstall():
    nopen("groupadd genocide")
    nopen("useradd genocide -g genocide -d /var/lib/genocide/")
    nopen("mkdir /var/lib/genocide")
    nopen("mkdir /var/lib/genocide/mods/")
    nopen("mkdir /var/lib/genocide/store/")
    nopen("cp mods/*.py /var/lib/genocide/mods")
    nopen("chown -R genocide:genocide /var/lib/genocide/")
    nopen("chmod -R 700 /var/lib/genocide/")
    nopen("chmod -R 400 /var/lib/genocide/mods/*.py")
    #nopen("systemctl daemon-reload")

def mods():
    if not os.path.exists("mods"):
        return []
    return ["mods/%s" % x for x in os.listdir("mods") if x.endswith(".py")]

def read():
    return open("README.rst", "r").read()

setup(
    name='genocide',
    version='8',
    url='https://github.com/bthate/genocide',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="The king of the netherlands commits genocide - OTP-CR-117/19/001 - otp.informationdesk@icc-cpi.int - https://genocide.rtfd.io",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license='Public Domain',
    zip_safe=True,
    install_requires=["botlib"],
    scripts=["bin/genocide", "bin/genocided"],
    packages=["genocide"],
    cmdclass={'install': Install},
    #data_files=[("mods", mods())],
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
