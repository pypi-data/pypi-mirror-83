# This file is part of the SecureFlag Platform.
# Copyright (c) 2020 SecureFlag Limited.

# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.

# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import textwrap
import logging
import prettytable

class clrs:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[33m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

verbose = False
quiet = False

class FatalMsg(Exception):
    pass

def set_verbose():
    global verbose

    verbose = True

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.WARNING) # Disable urllib3 debug

def set_quiet():
    global quiet

    quiet = True

# Warning
def warn(msg):
    if not quiet: print(f'[{clrs.WARNING}!{clrs.ENDC}] {msg}')

# Success
def success(msg):
    if not quiet: print(f'[{clrs.OKGREEN}+{clrs.ENDC}] {msg}')

# Info
def info(msg):
    if not quiet: print(f'[{clrs.OKGREEN}*{clrs.ENDC}] {msg}')

# Multiline prints
def block(msg, end = '', prefix = ''):
   if not quiet: print(textwrap.indent(textwrap.dedent(msg), prefix = prefix), end = end)

def debug(msg):
    if not quiet and verbose: logging.debug(msg)

def tablify(data, header = []):

    if quiet:
        return

    table = prettytable.PrettyTable()

    for row in data:
        table.add_row(row)

    table.align = 'l'
    table.vrules = prettytable.NONE
    table.hrules = prettytable.HEADER
    table.left_padding_width = 1

    if header:
        table.field_names = header
    else:
        table.header = False

    print('\n' + str(table))

