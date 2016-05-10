#!/usr/bin/env python
from distutils.core import setup

README = open('README.rst').read()

setup(name='CraSSH',
      version='2.5',
      description='Cisco Remote Automation via SSH (or C.R.A.SSH for short) is a python script for automating commands on Cisco devices.',
       long_description=README,
      author='Nick Bettison',
      author_email='linickx gmail com',
      url='https://github.com/linickx/crassh/',
      download_url='https://github.com/linickx/crassh/tarball/master',
      keywords = ['Cisco', 'SSH', 'Automation', 'IOS', 'Router', 'Switch', 'Firewall', 'ASA', 'Catalyst'],
      py_modules=['crassh'],
      install_requires=['paramiko >= 1.10'],
      scripts=['bin/crassh'],
      license = "GPLv2",
     )