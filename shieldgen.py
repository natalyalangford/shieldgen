#!/usr/bin/python3
__author__ = 'Natalya Langford'
__copyright__ = 'Copyright (C) 2021 Natalya Langford'
__credits__ = ['Rick Langford - Testing, Debug, Verification, and Documentation']
__license__ = 'GNU General Public License'
__program_name__ = 'gpu-ls'
__maintainer__ = 'Natalya'
__version__ = '0.0.1'
__status__ = 'Development'
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
    Main flow for gpu-ls.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--about', help='README',
                        action='store_true', default=False)
    parser.add_argument('--source', help='Source of log file',
                        action='store_true',default=False)
    parser.add_argument('--project', help='Name of debian project',
                        action='store_true',default=False)
    parser.add_argument('--output', help='Shield json file',
                        action='store_true',default=False)
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

    counter = 0
    logfiles = glob.glob('{}*'.format(args.source))
    print(logfiles)
    for file in logfiles:
        with open(file) as fp:
            for line in fp.readline():
                if re.search(r'gpu-utils.*pool.*all.deb.*200'.format(args.project), line):
                    counter += 1
    shield_dict['message'] = str(counter)
    try:
        with open(args.output, 'w') as fp:
            print(args.output)
            json.dump(shield_dict, fp)
    except OSError as err:
        print(err)


if __name__ == '__main__':
    main()
