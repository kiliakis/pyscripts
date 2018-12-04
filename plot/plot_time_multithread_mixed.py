#!/usr/bin/python
import matplotlib.pyplot as plt
import os
import numpy as np
import statistics as stat
import csv
from __builtin__ import file
import sys
from operator import truediv


results_dir = '/afs/cern.ch/work/k/kiliakis/results/csv/'
images_dir = '/afs/cern.ch/work/k/kiliakis/results/images/'

reference = {}
reference_err = {}
d = {}
code = ''

#fig, (ax1, ax2) = plt.subplots(2,sharex=True, sharey=True, figsize=(10,10))
fig = plt.figure(figsize=(14, 9))


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000
    # add more suffixes if you need them
    return '%d%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


def string_between(string, before, after):
    temp = string.split(before)[1]
    temp = temp.split(after)[0]
    return temp


def read_csv(file):
    if 'python' in file:
        code = 'Python'
    elif 'cpp' in file:
        code = 'C++'
    else:
        code = ''

    with open(file, 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        l = list(reader)
    l = l[1:]
    for r in l:
        key = human_format(int(r[1])) + ', ' + human_format(int(r[2])) + ', ' \
            + human_format(int(r[3]))

        value = float(r[4])

        err = float(r[5])
        #err = value * np.sqrt(reference_err[key] + err1)
        if r[0] in d:
            d[r[0]].append((key, value, err))
        else:
            d[r[0]] = [(key, value, err)]


def plot(ax):
    plt.grid(True, which='major', linestyle='-')
    plt.grid(True, which='minor',alpha=0.5)
    plt.minorticks_on()
    keys = sorted(d.iterkeys())
    plt.ylabel('Real Time (sec)')
    for k in keys:
        if int(k) < 14:
            continue
        v = d[k]
        #v.sort(key=lambda a:a[0])
        l = map(list, zip(*v))
        name = l[0]
        y = l[1]
        #y = map(truediv, ref, l[1])
        err = l[2]
        #legend.append(k + ' thread(s)')
        x = range(len(l[0]))
        plt.errorbar(x, y,yerr=err, marker='o', linewidth='2', label= k + ' threads')
        plt.xticks(x, name, rotation='45')
    plt.legend(loc='best', fancybox=True, framealpha=0.5)
   

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "You must specify the cpp csv file, python csv file and image name"
        exit(-1)
    cpp_csv_file = sys.argv[1]
    python_csv_file = sys.argv[2]
    image_name = sys.argv[3]

    ax1 = plt.subplot(211)
    plt.title('C++')
    read_csv(cpp_csv_file)
    plot(ax1)

    d= {}

    ax2 = plt.subplot(212, sharex=ax1, sharey=ax1)
    plt.title('Python')
    read_csv(python_csv_file)
    plot(ax2)
    plt.xlabel('Particles - Turns - Slices')

    plt.subplots_adjust(hspace = 0.45)
    plt.savefig(image_name , bbox_inches='tight')
    plt.tight_layout()
    plt.close()


