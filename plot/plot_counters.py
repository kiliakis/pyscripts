#!/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
import os

thesis_dir = '../phoenix-new/'
# thesis_dir = './'
# res_dir = thesis_dir + 'results/haswell/csv/metrics/'
# images_dir = thesis_dir + 'results/haswell/plots/'
images_dir = thesis_dir + 'results/haswell/plots/'
image_names = [images_dir + 'ipb_spi_normal_haswell.pdf']

# input_folder = thesis_dir + 'results/haswell/csv/metrics/v1/'
input_folder = thesis_dir + 'results/haswell/csv/metrics/v-hash/'
# , thesis_dir + '../phoenix-new/results/haswell/csv/metrics/v1/']

y_labels = ['Instructions / Byte', 'Stalls / Instruction']
x_label = ''
title = ''
y_name = 'metric'

names = {
    'word_count': 'WC',
    'linear_regression': 'LR',
    'mr_matrix_multiply': 'MM',
    'pca': 'PCA',
    'histogram': 'Hist',
    'kmeans': 'KMeans'
}

metrics = ['ipb_total', 'spi_total']
hatces=['x', '\\', '/']
colors=['.25', '.5', '.75']
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


def autolabel(ax, rects, integer=True):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        if (height > 1.) and integer:
            val = '%d' % round(height)
        else:
            val = '%.1lf' % float(height)
        ax.text(rect.get_x(), 1.0*height,
                val,
                ha='left', va='bottom')


def plot(x, y, label='', yerr=None):

    plt.grid(True, which='major', alpha=1)
    # plt.grid(True, which='minor', alpha=0.8)
    # plt.minorticks_on()
    plt.errorbar(x, y, yerr=yerr, marker='o', linewidth='1', label=label)


def group_by(input_dict, col, name):
    res_dict = {}
    for k, values in input_dict.items():
        for v in values:
            key = k+name+v[col]+'-'
            if(key not in res_dict):
                res_dict[key] = []
            res_dict[key].append(v)
    return res_dict


color_stack = ['y', 'b', 'r']
center = 0


def plot(ax, xticks, bar, label='', ylabel='', integer=True):
    global center, color_stack
    width = 0.5
    N = len(xticks)
    ind = np.linspace(0, 4*N/3.0, N)
    opacity = 0.9
    color = colors.pop()
    hatch = hatces.pop()
    ax.set_ylabel(ylabel, color=color)
    ax.tick_params('y', colors=color)
    plot = ax.bar(ind+center, bar, width, label=label,
                  color=color,hatch=hatch, alpha=opacity)
    center += 5.0*width/4.0
    autolabel(ax, plot, integer)
    ax.set_xticks(ind+width)
    ax.set_xticklabels(xticks)
    return plot

if __name__ == '__main__':

    fig, ax1 = plt.subplots()
    handles = []
    metric = metrics[0]
    metrics = metrics[1:]
    bar = []
    xticks = []
    for dirpath, dirnames, filenames in os.walk(input_folder):
        for file in filenames:
            if metric not in file:
                continue
            filename = dirpath + '/' + file
            print filename
            app = dirpath.split('/')[-1]
            values = import_results(filename)
            header = values[0]
            values = np.array(values[1:])
            c = header.index(y_name)
            bar.append(values[0, c].astype(float))
            xticks.append(names[app])
    xticks = np.array(xticks)
    bar = np.array(bar)
    args = xticks.argsort()
    xticks = xticks[args]
    bar = bar[args]
    ax1.set_yscale('log')
    handles.append(plot(ax1, xticks, bar, label=metric, ylabel=y_labels[0]))
    y_labels = y_labels[1:]
    ax1.set_ylim(10, 12000)

    ax2 = ax1.twinx()
    metric = metrics[0]
    metrics = metrics[1:]
    bar = []
    xticks = []
    for dirpath, dirnames, filenames in os.walk(input_folder):
        for file in filenames:
            if metric not in file:
                continue
            filename = dirpath + '/' + file
            print filename
            app = dirpath.split('/')[-1]
            values = import_results(filename)
            header = values[0]
            values = np.array(values[1:])
            c = header.index(y_name)
            bar.append(values[0, c].astype(float))
            xticks.append(names[app])
    xticks = np.array(xticks)
    bar = np.array(bar)
    args = xticks.argsort()
    xticks = xticks[args]
    bar = bar[args]
    handles.append(plot(ax2, xticks, bar, label=metric, ylabel=y_labels[0],
                        integer=False))
    y_labels = y_labels[1:]

    ax2.legend(loc='best', fancybox=True, framealpha=0.5, fontsize='10.5',
               handles=handles)
    ax2.set_xlim(-0.1)

    fig.tight_layout()
    if show == 'show':
        plt.show()
    else:
        fig.tight_layout()
        for image_name in image_names:
            fig.savefig(image_name, bbox_inches='tight')
    plt.close()
    exit(0)
