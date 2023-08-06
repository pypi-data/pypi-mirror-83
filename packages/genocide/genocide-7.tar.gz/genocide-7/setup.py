#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from setuptools import setup

def mods():
    return ["mods/%s" % x for x in os.listdir("mods") if x.endswith(".py")]

def read():
    return open("README", "r").read()

setup(
    name='genocide',
    version='7',
    url='https://github.com/bthate/genocide',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="The king of the netherlands commits genocide - OTP-CR-117/19/001 - otp.informationdesk@icc-cpi.int - https://genocide.rtfd.io",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license='Public Domain',
    zip_safe=True,
    scripts=["bin/genocide", "bin/genocided", "bin/genocide-install"],
    packages=["ol"],
    data_files=[("modules", mods())],
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
