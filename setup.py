#!/usr/bin/env python

import glob, os 
from distutils.core import setup

install_data = [('share/applications', ['data/com.github.mirkobrombin.football.desktop']),
                ('share/metainfo', ['data/com.github.mirkobrombin.football.appdata.xml']),
                ('share/icons/hicolor/128x128/apps',['data/com.github.mirkobrombin.football.svg'])]

setup(  name='Football',
        version='0.1',
        author='Mirko Brombin',
        description='Track Football scores',
        url='https://github.com/mirkobrombin/football',
        license='GNU GPL3',
        scripts=['com.github.mirkobrombin.football'],
        packages=['football'],
        data_files=install_data)
