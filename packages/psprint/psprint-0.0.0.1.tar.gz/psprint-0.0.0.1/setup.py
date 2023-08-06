#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
#
# Copyright 2020 Pradyumna Paranjape
# This file is part of psprint.
#
# psprint is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# psprint is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with psprint.  If not, see <https://www.gnu.org/licenses/>.
#
'''
Initialized banner for psprint
'''

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


class PostDevelop(develop):
    '''Extension for cupy installation'''
    def run(self) -> None:
        pass


class PostInstall(install):
    '''Extension for cupy installation'''
    def run(self) -> None:
        pass


setup(
    name="psprint",
    version="0.0.0.1",
    description="""
    psprint - Prompt String Print
    """,
    license="LGPLv3",
    author="Pradyumna Paranjape",
    author_email="pradyparanjpe@rediffmail.com",
    url="https://github.com/pradyparanjpe/",
    packages=['psprint'],
    install_requires=["colorama"],
    scripts=[],
)
