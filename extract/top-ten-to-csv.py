#!/usr/bin/python
import os
import csv
import sys
import numpy as np



def string_between(string, before, after):
    temp = string.split(before)[1]
    temp = temp.split(after)[0]
    return temp


def extract_top_ten(input_dir, output_file):
    out = open(output_file, 'w')
    writer = csv.writer(out, delimiter=' ')
    first = True
    for dirs, subdirs, files in os.walk(input_dir):
        if subdirs:
            continue
        for file in files:
            if('.csv' not in file):
                continue
            app = file.split('.csv')[0]
            l = import_results(dirs+file)
            if first:
                writer.writerow(l[0])
                first = False
            l = l[1:]
            l.sort(key=lambda a: float(a[-2]))
            writer.writerows(l[:10])
            writer.writerow([])

def import_results(output_file):
    d = np.loadtxt(output_file, dtype='str')
    return d.tolist()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "You should specify an input directory and an output file"
        exit(-1)
    input_dir = sys.argv[1]
    output_file = sys.argv[2]
    extract_top_ten(input_dir, output_file)
