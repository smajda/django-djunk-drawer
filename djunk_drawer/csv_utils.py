import csv
import re

from collections import namedtuple, OrderedDict


def generate_rows(f):
    """
    Generator that builds Row namedtuple from first row, then
    yields Row's from subsequent rows
    """
    spaces = re.compile(r'\s')
    headers = tuple(re.sub(spaces, '', i) for i in next(f, tuple()))
    Row = namedtuple('Row', headers)
    for line in f:
        yield Row(**OrderedDict(zip(headers, map(str.strip, line))))


def generate_csv_rows(csv_path):
    """
    Wraps generate_rows with csv open, reader machinery. i.e.:

        for line in generate_csv_rows('data.csv'):
            print line

    """
    with open(csv_path, 'rU') as f:
        reader = csv.reader(f)
        for line in generate_rows(reader):
            yield line
