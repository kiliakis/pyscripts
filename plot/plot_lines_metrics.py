#!/usr/bin/python
import matplotlib.pyplot as plt
import os
import numpy as np
import sys
import csv
from matplotlib import colors

# metrics = ['cache_miss_rate', 'IPC']
metrics = ['cache_miss_rate']
# subplots_format = 111
nrows = 1
ncols = 1


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


def plot_lines(data, image_folder):
    fig, axes = plt.subplots(nrows, ncols, sharex=True)
    if len(metrics) == 1:
        axes = [axes]
    # axes = np.array(axes)
    # plt.grid(True, which='major', alpha=0.5)
    # plt.yticks(range(0, 101, 10))
    # plt.xlabel('Threads')
    # plt.ylabel('Metric')
    # plt.title('Scalability')
    # plt.grid(True, which='minor', alpha=0.4)
    # plt.minorticks_on()
    header = data[0].tolist()
    data = np.array(data[1:], dtype=float)
    ind = np.unique(data[:, 0])
    for i in range(len(metrics)):
        axes[i].set_xlabel('Threads')
        axes[i].grid(True, which='major', alpha=0.5)
        # fig.add_subplot(len(metrics), 1, i+1)
        axes[i].set_ylabel(metrics[i])
        d = {}
        for r in data:
            c = header.index('n_particles')
            if r[c] not in d:
                d[r[c]] = []
            d[r[c]].append(r[header.index(metrics[i])])
        for k, v in d.items():
            print(k, v)
            axes[i].plot(ind, v, linestyle='-', marker='.',
                         label=human_format(float(k))+' Particles')

    axes[-1].legend(loc='best', fancybox=True, framealpha=0.5)
    plt.tight_layout()
    plt.savefig(image_folder, bbox_inches='tight')
    plt.show()
    plt.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("You must specify the input file and image name")
        exit(-1)
    input_file = sys.argv[1]
    image_folder = sys.argv[2]
    data = np.genfromtxt(input_file, dtype=str, delimiter='\t')
    # print(np.array(data[1:], dtype=float))
    plot_lines(data, image_folder)
    # plot_bars(data, image_folder)
