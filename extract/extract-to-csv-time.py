#!/usr/bin/python
import os
import csv
import sys
import numpy as np

# from prettytable import PrettyTable


def string_between(string, before, after):
    temp = string.split(before)[1]
    temp = temp.split(after)[0]
    return temp


def extract_results(input, out):
    header = ['n_threads', 'n_macroparticles', 'n_turns',
              'n_slices', 'turn_time', 'stdev']
    records = []
    for dirs, subdirs, files in os.walk(input):
        for file in files:
            if ('.stdout' not in file):
                continue
            l = []
            threads = string_between(file, 'n_thr', '.')
            turns = string_between(file, 'n_t', 'n_s')
            slices = string_between(file, 'n_s', 'n_thr')
            n_p = string_between(file, 'n_p', 'n_t')
            # implementation = dirs.split('/')[-2]
            for line in open(os.path.join(dirs, file), 'r'):
                if 'Mean turn time:' in line:
                    l.append(float(string_between(line, ':', 's')))
            if l:
                records.append([threads, n_p, turns, slices,
                                np.mean(l), np.std(l)])
                print file
                percent = 100.0 * np.std(l) / np.mean(l)
                if percent > 10:
                    print "The previous file has %.2f %% error" % percent
            else:
                print "I found an empty file called %s" % file
    records.sort(key=lambda a: (int(a[0]), int(a[1]), int(a[2])))
    # t = PrettyTable(header)
    # t.align = 'l'
    # t.border = False
    # for r in records:
    #     t.add_row(r)
    # with open(out, 'w') as f:
    #     f.writelines(str(t) + '\n')
    # if not os.path.exists(out):
    #     os.makedirs(out)
    writer = csv.writer(open(out, 'w'), lineterminator='\n', delimiter=',')
    writer.writerow(header)
    writer.writerows(records)


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
