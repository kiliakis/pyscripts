# import os
# import csv
# import sys
# import numpy as np


def string_between(string, before, after):
    temp = string.split(before)[1]
    temp = temp.split(after)[0]
    return temp


def get_line_matching(string, string_lst):
    for s in string_lst:
        if s in string:
            return string
    return None


def to_human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000
    # add more suffixes if you need them
    return '%d%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


def from_human_format_to_num(num):
    magnitude = {'K': '000', 'M': '000000', 'G': '000000000',
                 'T': '000000000000', 'P': '000000000000000'}
    for k, v in magnitude.items():
        if k in num.upper():
            return int(num.upper().replace(k, v))
