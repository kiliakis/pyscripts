#!/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.ticker import *

import os

thesis_dir = './'
res_dir = thesis_dir + 'results/raw/buf-sizes/'
# res_dir2 = thesis_dir + 'results/raw/phi/buf-sizes/'

images_dir = thesis_dir + 'results/haswell/plots/buf-sizes/'
image_names = ['buf-sizes-haswell.pdf']
# input_folder = res_dir

y_label = 'Real Time (sec)'
x_label = 'Buffer Size (x1000)'
# title = 'Buffer Size Effect'
y_name = 'realtime'
x_name = 'buf_size'
yerr_name = 'realtime_std'
names = {
    'word_count': 'WC',
    'linear_regression': 'LR',
    'mr_matrix_multiply': 'MM',
    'pca': 'PCA',
    'histogram': 'Hist',
    'kmeans': 'KMeans'
}

y_lims = {
    # 'WC': [2.0, 5.0],
    'WC': [],
    # 'Hist': [0.4, 0.6],
    # 'Hist': [1, 2],
    'Hist': [],
    # 'LR': [1.0, 2.0],
    # 'LR': [2.6, 3.5],
    'LR': [],
    'PCA': [],
    'KMeans': [],
    'MM': []
}

x_lims = {
    'WC': [],
    'Hist': [],
    'LR': [],
    'PCA': [],
    'KMeans': [],
    'MM': []
}

show = 'show'


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000
    # add more suffixes if you need them
    return '%d%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


def annotate(ax, A, B):
    for x, y in zip(A, B):
        ax.annotate('%.2f' % y, xy=(x, 1.05*y), textcoords='data', size='12')


def annotate_min(A, B):
    y = min(B)
    i = B.index(y)
    # i = B[y]
    plt.subplot().annotate('%.2e' % float(y), xy=(A[i], y), size='large')


def annotate_max(A, B):
    y = max(B)
    i = B.index(y)
    # i = B[y]
    plt.subplot().annotate('%.2e' % float(y), xy=(A[i], y), size='large')


def import_results(file):
    d = np.loadtxt(file, dtype='str')
    return d.tolist()


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.02*height,
                '%.2lf' % float(height),
                ha='left', va='bottom')

hatces=['/', '\\', 'x']

def plot(x, y, label='', yerr=None):
    plt.figure(figsize=(3, 2.5))
    # plt.xlabel(x_label)
    # plt.ylabel(y_label)
    # if (label == 'Hist') or (label == 'MM'):
    #     plt.ylabel(y_label)
    # plt.title(label)
    # plt.yscale("linear", nonposy='clip')
    # if(x_lims):
    #     plt.xlim(x_lims)

    # plt.grid(True, which='major', alpha=1)
    # plt.grid(True, which='minor', alpha=0.8)
    # plt.minorticks_on()
    x = np.array(x) / 1000
    plt.errorbar(x, y, yerr=yerr, marker='o', linewidth='1.5', label=label,
                 elinewidth='1')
    if(y_lims[label]):
        plt.ylim(y_lims[label])
        # if max(y) > max(y_lims[label]):
        #     plt.gca().text(x[y.argmax()], 0.99 * max(y_lims[label]),
        #                    '%.1lf' % float(max(y)),
        #                    ha='left', va='top', style='oblique')
    # plt.xscale("log", nonposx='mask')
    # plt.yscale("log", nonposy='mask')

    # xticks = []
    # for i in x:
    #     xticks.append(human_format(i))
    # plt.xticks(x, xticks)
    # plt.legend(loc='best', fancybox=True, framealpha=0.5, fontsize='9')
    ax = plt.gca()
    ax.yaxis.set_major_locator(MaxNLocator(3))
    plt.tight_layout()

    # plt.show()
    if show == 'show':
        plt.show()
    else:
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        for image_name in image_names:
            plt.savefig(images_dir + label + '-' + image_name, bbox_inches='tight')
    plt.close()


def group_by(input_dict, col, name):
    res_dict = {}
    for k, values in input_dict.items():
        for v in values:
            key = k+name+v[col]+'-'
            if(key not in res_dict):
                res_dict[key] = []
            res_dict[key].append(v)
    return res_dict


if __name__ == '__main__':

    for dirpath, dirnames, filenames in os.walk(input_folder):
        for file in filenames:
            if('timings.csv' not in file):
                continue
            values = import_results(dirpath + file)
            header = values[0]
            values = np.array(values[1:])

            c = header.index(x_name)
            x = values[:, c].astype(int)
            arg = x.argsort()
            x = x[arg]
            c = header.index(y_name)
            y = values[:, c].astype(float)
            y = y[arg]
            c = header.index(yerr_name)
            yerr = values[:, c].astype(float)
            yerr = yerr[arg]
            name = names[file.split('_timings.csv')[0]]
            plot(x, y, yerr=yerr, label=name)
