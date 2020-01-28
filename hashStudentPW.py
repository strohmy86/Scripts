#!/usr/bin/env python3

# MIT License

# Copyright (c) 2020 Luke Strohm

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import pandas as pd
import hashlib
import argparse


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def cred():
    print(Color.DARKCYAN + '\n' +
          '*********************************\n' +
          '*    Password Hash Utility      *\n' +
          '*                               *\n' +
          '*  Written and maintained by:   *\n' +
          '*        Luke Strohm            *\n' +
          '*    strohm.luke@gmail.com      *\n' +
          '*  https://github.com/strohmy86 *\n' +
          '*                               *\n' +
          '*********************************\n' +
          '\n' + Color.END)


def main(csv_file):
    df = pd.read_csv(csv_file)
    df['userPassword'] = df['userPassword'].apply(lambda x:
                                                  hashlib.sha1(str(x).encode(
                                                    'utf-8')).hexdigest())
    df.to_csv(csv_file[:-4]+'_Hashed.csv', index=False)


parser = argparse.ArgumentParser(description='Script to parse a CSV file \
                                 and hash the plaintext passwords')
parser.add_argument('csvfile', metavar='CSV file', default='',
                    type=str, help='Filename with path')
args = parser.parse_args()
csv_file = args.csvfile


cred()
main(csv_file)
