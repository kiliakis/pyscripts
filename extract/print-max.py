#!/usr/bin/python
import os
#import csv
#import statistics as s
import sys
import numpy as np
import argparse

#from prettytable import PrettyTable
parser = argparse.ArgumentParser(description='Raw results parser and printer')
parser.add_argument('-t', '--top', type=int, default=1,
                    help='Number of top results to print. 0 for all, default 1')
parser.add_argument('-r', '--reference', type=str, default='',
                    help='Reference file for a relative output(speedup/speedown)')
parser.add_argument('input', type=str, default='',
                    help='Input directory. Required argument.')


def string_between(string, before, after):
    temp = string.split(before)[1]
    temp = temp.split(after)[0]
    return temp


def extract_reference(in_file):
    refs = import_results(in_file)
    d = {}
    for r in refs:
        d[r[0]] = r[1]
    return d


def print_top(input, top=1, refs=None):
    header = []
    results = []
    if top == 0:
        top = -1
    for dirs, subdirs, files in os.walk(input):
        if subdirs:
            continue
        for file in files:
            if(('realtime.csv' not in file) or ('top' in file)):
                continue
            app = file.split('.csv')[0]
            a = import_results(dirs + file)
            header = a[0]
            if('realtime' in header):
                index = header.index('realtime')
            elif('time' in header):
                index = header.index('time')
            a = a[1:]
            a.sort(key=lambda x: float(x[index]))
            # print l[0]
            if refs:
                header[-2] = 'SpeedUp'
                for i in range(len(a[:top])):
                    a[i][index] = str(float(refs[app]) / float(a[i][index]))
            results.append(a[:top])
    print ' '.join(header)
    for app in results:
        for res in app:
            print ' '.join(res)
        print


def import_results(output_file):
    d = np.loadtxt(output_file, dtype='str')
    return d.tolist()

if __name__ == '__main__':
    args = parser.parse_args()
    input_dir = args.input
    print input_dir
    reference = args.reference
    top = args.top
    d = {}
    if reference:
        d = extract_reference(reference)
    print_top(input_dir, top, d)
