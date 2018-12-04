#!/usr/bin/python
import os
import csv
import statistics as stat
import sys
import numpy as np

from prettytable import PrettyTable


def string_between(string, before, after):
    temp = string.split(before)[1]
    temp = temp.split(after)[0]
    return temp


def process_line(line, t, imp, track, slice, phaseloop):
    if 'Average' not in line:
        return

    if 'Average Turn Time' in line:
        temp = line.split(':')[1]
        t.append(float(temp.strip()))
    elif 'Average Induced Voltage' in line:
        temp = line.split(':')[1]
        imp.append(float(temp.strip()))
    elif 'Average Tracker Track Time' in line:
        temp = line.split(':')[1]
        track.append(float(temp.strip()))
    elif 'Average Slice Track Time' in line:
        temp = line.split(':')[1]
        slice.append(float(temp.strip()))
    elif 'Average PhaseLoop Time' in line:
        temp = line.split(':')[1]
        phaseloop.append(float(temp.strip()))
    else:
        print line

def extract_results(input, out):
    header = ['thr', 'parts', 'turns',
              'slices', 'turn_m', 'turn_err',
              'imp_m', 'imp_err',
              'tracker_m', 'tracker_err',
              'slice_m', 'slice_err',
              'pl_m', 'pl_err']
    records = []
    for dirs, subdirs, files in os.walk(input):
        for file in files:
            if ('.stdout' not in file):
                continue
            t = []
            imp = [0,0]
            phaseloop = []
            track = []
            slice = []
            threads = string_between(file, 'n_thr', '.')
            turns = string_between(file, 'n_t', 'n_s')
            slices = string_between(file, 'n_s', 'n_thr')
            n_p = string_between(file, 'n_p', 'n_t')
            #implementation = dirs.split('/')[-2]
            for line in open(os.path.join(dirs, file), 'r'):
                #print line
                process_line(line, t, imp, track, slice, phaseloop)
            if not (t and imp and track and slice):
                print 'File : ', file, ' corrupted!'
                continue
            
            records.append([threads, n_p, turns, slices,
                            stat.mean(t), stat.stdev(t),
                            stat.mean(imp), stat.stdev(imp),
                            stat.mean(track), stat.stdev(track),
                            stat.mean(slice), stat.stdev(slice),
                            stat.mean(phaseloop), stat.stdev(phaseloop)
                            ])
    records.sort(key=lambda a: (int(a[0]), int(a[1]), int(a[2])))
    for r in records:
        for i in range(len(r)):
            if(isinstance(r[i], float)):
                r[i] = '%.3e' % r[i]
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
    # if os.path.exists(output_file):
    #     os.mkdirs(output_file)
    extract_results(input_dir, output_file)
