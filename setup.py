#!/usr/bin/python3

import glob, os
from distutils.core import setup

share_path = '/usr/share'
inst_path = share_path+'/com.github.mirkobrombin.football/football'
icons_path = share_path+'/icons/hicolor/scalable/apps'

install_data = [(share_path+'/metainfo', ['data/com.github.mirkobrombin.football.appdata.xml']),
                (share_path+'/applications', ['data/com.github.mirkobrombin.football.desktop']),
                (icons_path,['data/com.github.mirkobrombin.football.svg']),
                (inst_path,['football/wine.py']),
                (inst_path,['football/__init__.py'])]

setup(  name='Football',
        version='1.2.1',
        python_requires='>3.5.2',
        author='Mirko Brombin',
        description='Track Football scores',
        url='https://git.mirko.pm/brombinmirko/football',
        license='GNU GPL3',
        scripts=['com.github.mirkobrombin.football'],
        packages=['football'],
        data_files=install_data)
