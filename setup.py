#!/usr/bin/python3

import glob, os 
from distutils.core import setup

install_data = [('share/applications', ['data/com.github.mirkobrombin.football.desktop']),
                ('share/metainfo', ['data/com.github.mirkobrombin.football.appdata.xml']),
                ('share/icons/hicolor/128x128/apps',['data/com.github.mirkobrombin.football.svg']),
                ('bin/football',['football/main.py']),
                ('bin/football',['football/__init__.py'])]

setup(  name='Football',
        version='1.1.6',
        python_requires='>3.5.2',
        author='Mirko Brombin',
        description='Track Football scores',
        url='https://github.com/brombinmirko/football',
        license='GNU GPL3',
        scripts=['com.github.mirkobrombin.football'],
        packages=['football'],
        data_files=install_data)
