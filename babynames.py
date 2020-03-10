#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BabyNames python coding exercise.

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import argparse

"""
Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 - Extract the year and print it
 - Extract the names and rank numbers and just print them
 - Get the names data into a dict and print it
 - Build the [year, 'name rank', ... ] list and print it
 - Fix main() to use the extract_names list
"""
__author__ = 'Jordan'


def extract_names(filename):
    years = re.compile('in [0-9]+')
    name = re.compile(r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>')
    names = []
    all_names = {}
    with open(filename) as f:
        contents = f.readlines()
        for line in contents:
            if 'Popularity in' in line:
                year = years.search(line)
            else:
                current = name.findall(line)
                if current:
                    for num, boy, girl in current:
                        if boy not in all_names:
                            all_names[boy] = num
                        else:
                            all_names[boy] = str(min(int(num), int(all_names[boy])))
                        if girl not in all_names:
                            all_names[girl] = num
                        else:
                            all_names[girl] = str(min(int(num), int(all_names[girl])))
    names.append(year.group().strip('in '))
    sortedNames = []
    for name in all_names:
        sortedNames.append(name + ' ' + all_names[name])
    sortedNames = sorted(sortedNames)
    names += sortedNames
    print(names)
    return names

def create_summary_file(filename):
    with open(filename + '.summary', 'w') as f:
        text = '\n'.join(extract_names(filename)) + '\n'
        f.write(text)
    


def create_parser():
    """Create a cmd line parser object with 2 argument definitions"""
    parser = argparse.ArgumentParser(description="Extracts and alphabetizes baby names from html.")
    parser.add_argument(
        '--summaryfile', help='creates a summary file', action='store_true')
    # The nargs option instructs the parser to expect 1 or more filenames.
    # It will also expand wildcards just like the shell, e.g. 'baby*.html' will work.
    parser.add_argument('files', help='filename(s) to parse', nargs='+')
    return parser


def main(args):
    # Create a command-line parser object with parsing rules
    parser = create_parser()
    # Run the parser to collect command-line arguments into a NAMESPACE called 'ns'
    ns = parser.parse_args(args)
    file_list = ns.files
    create_summary = ns.summaryfile
    if not ns:
        parser.print_usage()
        sys.exit(1)
    if create_summary:
        for _ in file_list:
            create_summary_file(_)
    for _ in file_list:
        extract_names(_)

if __name__ == '__main__':
    main(sys.argv[1:])
