#!/usr/bin/python
import os
import csv
import statistics as s
import sys
import numpy as np

from prettytable import PrettyTable


def string_between(string, before, after):
    temp = string.split(before)[1]
    temp = temp.split(after)[0]
    return temp


def process_line(line):
    if ('Mean' not in line) or ('track time' not in line):
        return ('', 0.0)

    key = string_between(line, 'Mean', 'track').strip()
    val = float(line.split(' ')[-1])
    return (key, val)


def extract_results(input, out):
    records = []
    for dirs, subdirs, files in os.walk(input):
        for file in files:
            header = ['n_threads', 'n_macroparticles', 'n_turns', 'n_slices']
            d = {}
            count = 0
            if ('.stdout' not in file):
                continue
            l = []
            threads = string_between(file, 'n_thr', '.')
            turns = string_between(file, 'n_t', 'n_s')
            slices = string_between(file, 'n_s', 'n_thr')
            n_p = string_between(file, 'n_p', 'n_t')
            for line in open(os.path.join(dirs, file), 'r'):
                (key, val) = process_line(line)
                if key:
                    d[key] = val
                    # if key not in d:
                    #     d[key] = 0
                    # d[key] += val
                    # count += 1
            count /= len(d.keys())
            r = [threads, n_p, turns, slices]
            for k, v in d.items():
                header.append(k)
                # r.append(v/count)
                r.append(v)
            records.append(r)
    records.sort(key=lambda a: (int(a[0]), int(a[1]), int(a[2]), int(a[3])))
    t = PrettyTable(header)
    t.align = 'l'
    t.border = False
    for r in records:
        t.add_row(r)
    with open(out, 'w') as f:
        f.writelines(str(t) + '\n')


def import_results(output_file):
    d = np.loadtxt(output_file, dtype='str')
    return d.tolist()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "You should specify input directory and output file"
        exit(-1)
    input_dir = sys.argv[1]
    output_file = sys.argv[2]
    extract_results(input_dir, output_file)
