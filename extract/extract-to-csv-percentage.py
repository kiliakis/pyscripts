#!/usr/bin/python
import matplotlib.pyplot as plt
import os
# import numpy as np
import statistics as stat
import csv
from __builtin__ import file
import sys

if len(sys.argv) < 3:
    print "You should specify input directory and output file"
    exit(-1)

input_dir = sys.argv[1]
output_file = sys.argv[2]


def string_between(string, before, after):
    temp = string.split(before)[1]
    temp = temp.split(after)[0]
    return temp


def dump_results(input, out):
    header = ['n_threads', 'n_macroparticles', 'n_turns',
              'n_slices', 'tracking', 'slicing']
    records = []
    for dirs, subdirs, files in os.walk(input):
        for file in files:
            if ('.stdout' not in file):
                continue
            t = []
            s = []
            threads = string_between(file, 'n_thr', '.stdout')
            turns = string_between(file, 'n_t', 'n_s')
            slices = string_between(file, 'n_s', 'n_thr')
            n_p = string_between(file, 'n_p', 'n_t')
            #implementation = dirs.split('/')[-2]
            print file
            for line in open(os.path.join(dirs, file), 'r'):
                if 'Track ' in line:
                    temp = string_between(line, '(', '% )')
                    t.append(float(temp.strip()))
                elif 'Slice ' in line:
                    temp = string_between(line, '(', '% )')
                    s.append(float(temp.strip()))
            if t and s:
                records.append([threads, n_p, turns, slices,
                                stat.mean(t), stat.mean(s)])
                #percent = 100.0 * stat.stdev(l) / stat.mean(l)
                #if percent > 10:
                    #print "The previous file has %.2f %% error" % percent
            else:
                print "I found an empty file called %s" % file
    records.sort(key=lambda a: (int(a[0]), int(a[1]), int(a[2]), int(a[3])))
    writer = csv.writer(open(out, 'w'), lineterminator='\n', delimiter='\t')
    writer.writerow(header)
    writer.writerows(records)


if __name__ == '__main__':
    dump_results(input_dir, output_file)
