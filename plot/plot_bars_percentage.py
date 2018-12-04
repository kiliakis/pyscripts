#!/usr/bin/python
import matplotlib.pyplot as plt
import os
import numpy as np
import statistics as stat
import csv
from __builtin__ import file
import sys
from operator import truediv
from matplotlib import colors

#results_dir = '/afs/cern.ch/work/k/kiliakis/results/csv/'
#images_dir = '/afs/cern.ch/work/k/kiliakis/results/images/'

d = {}
code = ''

colorList = ['b', 'g', 'r', 'y', 'm']


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
        #print r
        key = human_format(int(r[1])) + ' - ' + human_format(int(r[3]))
        value = float(r[4])
        #slices = float(r[3])
        #err = float(r[5])
        #err = value * np.sqrt(reference_err[key] + err1)
        if r[0] in d:
            d[r[0]].append((key, value))
        else:
            d[r[0]] = [(key, value)]


def plot(file):

    plt.figure()
    #plt.figure(figsize=(14, 8))
    plt.grid(True, which='major')
    plt.grid(True, which='minor',alpha=0.4)
    plt.minorticks_on()
    #legend = []
    keys = sorted(d.iterkeys())
    plt.xlabel('Particles - Slices')
    plt.ylabel('Percentage of Tracking Time')
    plt.title(code+' Tracking vs Slicing')
    plt.ylim(ymax=100)
    #plt.xlim(xmin=0)
    #print ref
    w = 0.8 / len(keys)
    offset = -0.4
    i = 0
    for k in keys:
        print k
        v = d[k]
        #v.sort(key=lambda a:a[0])
        l = map(list, zip(*v))
        name = l[0]
        y = l[1]
        #y = map(truediv, ref, l[1])
        #err = l[2]
        #legend.append(k + ' thread(s)')
        #x = np.arange(1, len(l[0])+1, 1.)
        x = np.linspace(2, 10, num=len(l[0]))
        plt.bar(x+offset, y, w, align='center', label=k+' thr', color=colorList[i])
        i += 1
        offset += w
        plt.xticks(x, name, rotation='30')
        #mean = stat.mean(y)
        #plt.plot(x,[mean]*len(x), linestyle='--', linewidth='2', color='black', label = 'mean value')
    #legend.append('mean value')

    #plt.grid(b=True, which='both')
    plt.legend(loc=[1.01, 0.5], fancybox=True, framealpha=0.5)
    plt.savefig(file, bbox_inches='tight')
    plt.autoscale()
    #plt.subplots_adjust(hspace = 0.02)
    plt.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "You must specify the csv file and image name"
        exit(-1)
    csv_file = sys.argv[1]
    image_name = sys.argv[2]

    read_csv(csv_file)
    plot(image_name)
