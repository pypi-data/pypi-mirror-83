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
Prompt String-like Print
'''


import os
from pathlib import Path
from configparser import ConfigParser
from .classes import InfoPrint


DEFAULT_PRINT = InfoPrint()


def _set_opts(rcfile) -> None:
    '''
    infile: rc file to read
    '''
    conf = ConfigParser(allow_no_value=True)
    conf.read(rcfile)
    for mark in conf:
        if mark == "DEFAULT":
            DEFAULT_PRINT.short =\
                conf[mark].getboolean("short", fallback=False)
            DEFAULT_PRINT.pad =\
                conf[mark].getboolean("pad", fallback=False)
            DEFAULT_PRINT.print_kwargs['sep'] =\
                conf[mark].get("sep", fallback="\t") or "\t"
            DEFAULT_PRINT.print_kwargs['end'] =\
                conf[mark].get("end", fallback="\n") or "\n"
            DEFAULT_PRINT.print_kwargs['flush'] =\
                conf[mark].getboolean("flush", fallback=False)
            fname = conf[mark].get("file", fallback=None)  # I discourage this
            if fname is not None:
                DEFAULT_PRINT.print_kwargs['file'] = open(fname, "a")
        else:
            kwargs = {
                'pref_long_str': None,
                'pref_short_str': None,
                'index_str': mark
            }
            for key, val in conf[mark].items():
                if key in ("index", "pref_color", "pref_gloss",
                           "text_color", "text_gloss"):
                    val = int(val)
                kwargs[key] = val
            try:
                DEFAULT_PRINT.edit_style(**kwargs)
            except ValueError as err:
                print()
                print(f"'{mark}' from {rcfile}")
                print("couldn't be parsed due to following error:")
                print(f"'{err}'")
                print()


RC_LOCATIONS = {
    'root': Path("/etc/psprint/style.conf"),
    'user': Path(os.environ["HOME"]).joinpath("." + "psprintrc"),
    'config': Path(os.environ["HOME"]).joinpath(
        ".config", "psprint", "style.conf"
    ),
    'xdg_config': Path().joinpath("psprintrc"),  # juvenile user|fails
    'local': Path(os.getcwd()).joinpath("." + "psprintrc"),
}

try:
    RC_LOCATIONS['xdg_config'] = Path(
        os.environ["XDG_CONFOG_HOME"]
    ).joinpath("psprint", "style.conf")
except KeyError:
    pass


for loc in 'root', 'user', 'config', 'xdg_config', 'local':
    if RC_LOCATIONS[loc].exists():
        _set_opts(RC_LOCATIONS[loc])


PRINT = DEFAULT_PRINT.psprint
__all__ = [
    'InfoPrint',
    'DEFAULT_PRINT',
    'PRINT'
]
