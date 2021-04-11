#!/usr/bin/python3
""" shieldgen - generate json badge content for rickslab.

    Copyright (C) 2021  Natalya

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
__author__ = 'Natalya Langford'
__copyright__ = 'Copyright (C) 2021 Natalya Langford'
__credits__ = ['Rick Langford - Testing, Debug, Verification, and Documentation']
__license__ = 'GNU General Public License'
__program_name__ = 'shieldgen'
__maintainer__ = 'Natalya'
__version__ = '0.0.2'
__status__ = 'Development Status :: 3 - Alpha'
__docformat__ = 'reStructuredText'
# pylint: disable=multiple-statements
# pylint: disable=line-too-long
# pylint: disable=bad-continuation

import os
import pathlib
import re
import argparse
import sys
import glob
import json


def deb_cnt_src(source: str, shield_dict: dict) -> bool:
    """

    :param source:
    :param shield_dict:
    :return:
    """
    searchpattern = re.compile(r'{}.*pool.*all.deb.*200'.format(shield_dict["project"]), re.IGNORECASE)
    counter = 0
    logfiles = glob.glob('{}*'.format(source))
    for file in logfiles:
        with open(file) as fp:
            for line in fp:
                if re.search(searchpattern, line):
                    counter += 1
    shield_dict['message'] = str(counter)
    return True


def main():
    """
    Main flow for shieldgen .
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--about', help='README',
                        type=str, default='')
    parser.add_argument('--deb_cnt_src', help='Source of log file',
                        type=str, default='', required=True)
    parser.add_argument('--project', help='Name of debian project',
                        type=str, default='', required=True)
    parser.add_argument('--output', help='Shield json file',
                        type=str, default='')
    parser.add_argument('--debug', help='Activates logger',
                        type=bool, default=False)
    args = parser.parse_args()

    shield_dict = {
        "schemaVersion": 1,
        "label": "rickslab.com downloads",
        "message": "",
        "color": "orange",
        "project": args.project
    }

    # About me
    if args.about:
        print(__doc__)
        print('Author: ', __author__)
        print('Copyright: ', __copyright__)
        print('Credits: ', *['\n      {}'.format(item) for item in __credits__])
        print('License: ', __license__)
        print('Version: ', __version__)
        print('Maintainer: ', __maintainer__)
        print('Status: ', __status__)
        sys.exit(0)

    if args.deb_cnt_src:
        if not os.path.isfile(args.deb_cnt_src):
            print('Incorrect log file')
            sys.exit(-1)
        deb_cnt_src(args.deb_cnt_src, shield_dict)

    if not args.output:
        print(shield_dict)
    else:
        outpath = pathlib.Path(__file__).parent.absolute()
        if not os.path.isdir(outpath):
            print('Path to output does not exist')
            sys.exit(-1)
        try:
            with open(args.output, 'w') as fp:
                json_dict = [{k: v} for k, v in shield_dict.items() for k in ["shemaVersion", "label", "message", "color"]]
                json.dump(json_dict, fp)
        except OSError as err:
            print(err)


if __name__ == '__main__':
    main()
