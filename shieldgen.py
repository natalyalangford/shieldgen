#!/usr/bin/python3
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


def main() -> None:
    """
    Main flow for shieldgen .
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--about', help='README',
                        type=str, default='')
    parser.add_argument('--source', help='Source of log file',
                        type=str, default='', required=True)
    parser.add_argument('--project', help='Name of debian project',
                        type=str, default='', required=True)
    parser.add_argument('--output', help='Shield json file',
                        type=str, default='')
    parser.add_argument('--debug', help='Activates logger',
                        type=str, default = '')
    args = parser.parse_args()

    shield_dict = {
        "schemaVersion": 1,
        "label": "rickslab.com downloads",
        "message": "",
        "color": "orange"
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

    if args.source:
        if not os.path.isfile(args.source):
            print('Incorrect log file')
            sys.exit(-1)

    outpath = pathlib.Path(__file__).parent.absolute()
    if not os.path.isdir(outpath):
        print('Path to output does not exist')
        sys.exit(-1)

    searchpattern = re.compile(r'{}.*pool.*all.deb.*200'.format(args.project), re.IGNORECASE)
    counter = 0
    logfiles = glob.glob('{}*'.format(args.source))
    for file in logfiles:
        with open(file) as fp:
            for line in fp:
                if re.search(searchpattern, line):
                    counter += 1
    shield_dict['message'] = str(counter)
    try:
        with open(args.output, 'w') as fp:
            json.dump(shield_dict, fp)
    except OSError as err:
        print(err)

 #   if args.debug:


if __name__ == '__main__':
    main()
