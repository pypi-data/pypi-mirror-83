'''
File: setup.py
Created Date: Sunday, July 0th 2020, 12:03:56 am
Author: Zentetsu

----

Last Modified: Sun Oct 25 2020
Modified By: Zentetsu

----

Project: CorState
Copyright (c) 2020 Zentetsu

----

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

----

HISTORY:
'''


from setuptools import setup, find_packages

setup(
    name='CorState',
    version='0.1.3-dev0',
    author='Zentetsu',
    packages=find_packages(exclude=['tests*']),
    license='GPLv3',
    description='Lightweight and versatile State Machine library',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[],
    url='https://github.com/Zentetsu/CorState',
    python_requires='>=3.5',
)