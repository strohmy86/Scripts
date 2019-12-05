#!/usr/bin/env python3

# MIT License

# Copyright (c) 2019 Luke Strohm

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import sys
import argparse
import glob
import csv


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
    print('\n' + Color.DARKCYAN)
    print("*********************************")
    print("* Python 3 Script for Detecting *")
    print("*        Text in Images         *")
    print("*                               *")
    print("*   Written and maintained by   *")
    print("*          Luke Strohm          *")
    print("*     strohm.luke@gmail.com     *")
    print("*  https://github.com/strohmy86 *")
    print("*                               *")
    print("*********************************")
    print(Color.END + '\n')


def main():
    parser = argparse.ArgumentParser(description='Detect text in images.')
    parser.add_argument('-f', '--file', metavar='file', default=False,
                        type=str, help='File to be parsed')
    parser.add_argument('-b', '--batch', metavar='directory', type=str,
                        help='Base directory to be parsed', default=False)
    args = parser.parse_args()

    if args.file == False and args.batch == False:
        parser.print_help()
        parser.exit(2)
    elif args.batch == False and args.file != False:
        text = pytesseract.image_to_string(Image.open(args.file), lang='eng')
        print(Color.BOLD + 'The text detected in ' + Color.END + Color.YELLOW + args.file
             + Color.END + Color.BOLD + ' is:\n')
        print(Color.CYAN + text + Color.END)
    elif args.batch != False and args.file ==False:
        print('Searching ' + args.batch + ' for picture files...')
        with open(args.batch+'OCR-Text.csv', mode='w', newline='') as fa:
            writer = csv.writer(fa)
            headers = ['File Name', 'Detected Text']
            writer.writerow(headers)
            for pic in glob.iglob(args.batch + '**/*.jpg', recursive=True):
                txt = pytesseract.image_to_string(Image.open(pic), lang='eng')
                data = [pic, txt]
                writer.writerow(data)
            for pic in glob.iglob(args.batch + '**/*.jpeg', recursive=True):
                txt = pytesseract.image_to_string(Image.open(pic), lang='eng')
                data = [pic, txt]
                writer.writerow(data)
            for pic in glob.iglob(args.batch + '**/*.png', recursive=True):
                txt = pytesseract.image_to_string(Image.open(pic), lang='eng')
                data = [pic, txt]
                writer.writerow(data)
            for pic in glob.iglob(args.batch + '**/*.gif', recursive=True):
                txt = pytesseract.image_to_string(Image.open(pic), lang='eng')
                data = [pic, txt]
                writer.writerow(data)
        fa.close()
        print(Color.GREEN + '\nResults saved to ' + args.batch+'OCR-Text.csv' + Color.END)

        





if __name__ == "__main__":
   cred()
   main()
