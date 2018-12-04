#!/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
import os

hatces=['x', '\\', '/']
colors=['.25', '.5', '.75']

thesis_dir = './'
res_dir = thesis_dir + 'results/raw/phi/consume-one-batch/'
images_dir = thesis_dir + 'results/phi/plots/'
image_names = [images_dir + 'consume-one-batch-phi.pdf']
# reference_files = [res_dir + 'python/PSB/v1/result-s'+a+'.csv'] * 4
input_folder = res_dir + 'batch/'

reference_folder = res_dir + 'one/'
y_label = 'Consume Batch Speedup'
x_label = 'Applications'
title = 'Consume One/ Consume Batch comparison'
y_name = 'realtime'
names = {
    'word_count': 'WC',
    'linear_regression': 'LR',
    'mr_matrix_multiply': 'MM',
    'pca': 'PCA',
    'histogram': 'Hist',
    'kmeans': 'KMeans'
}

show = 'plot'

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
        # if (height > 1.) and integer:
        #     val = '%d' % round(height)
        # else:
        val = '%.2lf' % float(height)
        ax.text(rect.get_x(), 1.0*height,
                val,
                ha='left', va='bottom', fontsize='9')


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


if __name__ == '__main__':

    fig, ax = plt.subplots(figsize=(7, 3.))
    # plt.xlabel(x_label)
    ax.set_ylabel(y_label)
    # ax.set_title(title)
    # ax.grid(True, which='major', alpha=1)
    # if(x_lims):
    #     plt.xlim(x_lims)
    # if(y_lims):
    #     plt.ylim(y_lims)
    ax.set_ylim(0, 13)
    xticks = []
    normalized = []
    for dirpath, dirnames, filenames in os.walk(input_folder):
        for file in filenames:
            if('timings.csv' not in file):
                continue
            # print file
            # print reference_folder + file
            values = import_results(dirpath + file)
            header = values[0]
            values = np.array(values[1:])
            c = header.index(y_name)
            real = values[0, c].astype(float)
            # c = header.index(yerr_name)
            # real_err = values[0, c].astype(float)

            values = import_results(reference_folder + file)
            header = values[0]
            values = np.array(values[1:])
            c = header.index(y_name)
            reference = values[0, c].astype(float)
            # c = header.index(yerr_name)
            # reference_err = values[0, c].astype(float)
            xticks.append(names[file.split('_timings')[0]])
            normalized.append(reference/real)
    xticks = np.array(xticks)
    normalized = np.array(normalized)
    # print xticks
    # print normalized
    # for x in xticks:
    #     if(x in names):
    #         xticks[xticks.index(x)] = names[x]
    args = xticks.argsort()
    xticks = xticks[args]
    normalized = normalized[args]
    N = len(xticks)
    width = 0.4
    ind = np.linspace(0.15, 1.3 * N, N)
    opacity = 0.9
    # ind = np.arange(N)
    simple = ax.bar(ind, normalized, width, label='consume-single', color=colors.pop(),
                    alpha=opacity, hatch=hatces.pop())
    batched = ax.bar(ind + width, [1.0] * N,
                     width, label='consume-batch', color=colors.pop(), alpha=opacity, hatch=hatces.pop())

    ax.set_xticks(ind + width)
    ax.set_xticklabels(xticks)
    ax.legend(loc='best', fancybox=True, framealpha=0.5, fontsize='11')

    autolabel(simple)
    # autolabel(batched)

    if show == 'show':
        plt.show()
    else:
        fig.tight_layout()
        for image_name in image_names:
            fig.savefig(image_name, bbox_inches='tight')
    plt.close()
