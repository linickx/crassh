#!/usr/bin/env python
from distutils.core import setup

setup(name='CraSSH',
      version='2.02',
      description='Cisco Remote Automation via SSH (or C.R.A.SSH for short) is a python script for automating commands on Cisco devices.',
      author='Nick Bettison',
      url='https://github.com/linickx/crassh/',
      download_url='https://github.com/linickx/crassh/tarball/pip-install',
      keywords = ['Cisco', 'SSH', 'Automation', 'IOS', 'Router', 'Switch', 'Firewall', 'ASA', 'Catalyst'],
      py_modules=['crassh'],
      install_requires=['paramiko >= 1.10'],
      scripts=['bin/crassh'],
     )