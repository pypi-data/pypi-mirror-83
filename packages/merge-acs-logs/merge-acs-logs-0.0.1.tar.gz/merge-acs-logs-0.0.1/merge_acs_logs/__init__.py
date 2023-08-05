#!/usr/bin/env python3
"""Merge ACS logs by time

If a file contains lines, that do not start with an ISO 8601 string
those lines are considered a part of a multiline log output and stay
together with latest line above them, which still contained a date string.

Implementation is not very memory friendly .. we read all files into mem,
parse them, sort them, and write them again. Can be improved if needed.

Example:

  merge_logs $ACSDATA/logs/*/*

Usage:
  merge_logs [-q] [-o NAME] [INPUT ...]

Options:
  -h --help         Show this screen.
  -o --output NAME  outfile name, default is "merged_<current_date>.log"
  -q                quiet, no progress bar
"""
from docopt import docopt
import iso8601
from datetime import datetime
from tqdm import tqdm

def parse_file_into_chunks(path):
    with open(path) as file:
        reversed_lines = file.readlines()[::-1]

    chunks = []
    current_chunk = None

    for line in reversed_lines:
        if current_chunk is None:
            current_chunk = []
        current_chunk.append(line)
        try:
            date_str = line.split(sep=None, maxsplit=1)[0]
            date = iso8601.parse_date(date_str)
            chunks.append((date, current_chunk[::-1]))
            current_chunk = None
        except (iso8601.ParseError, IndexError):
            continue
    return chunks


def main():
    arguments = docopt(__doc__)
    print(arguments)

    paths = arguments["INPUT"]

    if arguments["-q"]:
        paths_iter = paths
    else:
        paths_iter = tqdm(paths)

    if arguments["--output"] is None:
        out_path = "merged_{0:%Y_%m_%dT%H_%M_%S}.log".format(datetime.utcnow())
    else:
        out_path = arguments["--output"]

    complete = []
    for path in paths_iter:
        chunks = parse_file_into_chunks(path)
        complete += chunks


    with open(out_path, "w") as file:
        for date, ch in sorted(complete):
            for line in ch:
                file.write(line)


if __name__ == '__main__':
    main()
