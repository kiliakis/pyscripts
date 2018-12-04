import matplotlib.pyplot as plt
import numpy as np

res_dir = '/afs/cern.ch/work/k/kiliakis/git/cpp-benchmark/histogram/results/csv/run6/'
images_dir = '/afs/cern.ch/work/k/kiliakis/git/cpp-benchmark/histogram/results/'

csv_files = [res_dir + 'histogram2-m100000-s100.csv',
             res_dir + 'histogram2-m100000-s1000.csv',
             res_dir + 'histogram2-m500000-s500.csv',
             res_dir + 'histogram2-m500000-s5000.csv',
             res_dir + 'histogram2-m1000000-s1000.csv',
             res_dir + 'histogram2-m1000000-s10000.csv']

num_lines = len(csv_files)

x_names = ['n_threads'] * num_lines
xerr_names = None
y_names = ['Throughput'] * num_lines
yerr_names = ['Stdev'] * num_lines

line_names = ['100k Particles - 100 Slices',
              '100k Particles - 1k Slices',
              '500k Particles - 500 Slices',
              '500k Particles - 5k Slices',
              '1M Particles - 1k Slices',
              '1M Particles - 10k Slices']

image_name = images_dir+'histogram-new.png'
x_label = 'Threads'
y_label = 'Throughput (Mp/s)'
title = 'new histogram throughput'
annotate_min_flag = [False] * num_lines
annotate_max_flag = [False] * num_lines
annotate_points = [False] * num_lines


def annotate(ax, A, B):
    for x, y in zip(A, B):
        ax.annotate('%.1e' % y, xy=(x, y), textcoords='data', size='12')


def annotate_min(A, B):
    y = min(B)
    i = B.index(y)
    #i = B[y]
    plt.subplot().annotate('%.2e' % float(y), xy=(A[i], y), size='large')


def annotate_max(A, B):
    y = max(B)
    i = B.index(y)

    #i = B[y]
    plt.subplot().annotate('%.2e' % float(y), xy=(A[i], y), size='large')


def import_results(file):
    d = np.loadtxt(file, dtype='str')
    return d.tolist()


def plot(x, y, label, xerr=None, yerr=None):

    plt.grid(True, which='major', alpha=1)
    plt.grid(True, which='minor', alpha=1)
    plt.minorticks_on()
    plt.errorbar(
        x, y, xerr=xerr, yerr=yerr, marker='o', linewidth='2', label=label)


if __name__ == '__main__':

    plt.figure(figsize=(12, 7))
    plt.tick_params(labelright=True)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    for i in range(len(csv_files)):
        file = csv_files[i]
        x_name, y_name = x_names[i], y_names[i]
        if xerr_names:
            xerr_name = xerr_names[i]
        else:
            xerr_name = None

        if yerr_names:
            yerr_name = yerr_names[i]
        else:
            yerr_name = None

        line_name = line_names[i]
        l = import_results(file)
        header = l[0]
        array = np.array(l[1:])
        c = header.index(x_name)
        x = array[:, c].astype(float).tolist()
        c = header.index(y_name)
        y = array[:, c].astype(float).tolist()
        if xerr_name:
            c = header.index(xerr_name)
            xerr = array[:, c].astype(float).tolist()
        else:
            xerr = None
        if yerr_name:
            c = header.index(yerr_name)
            yerr = array[:, c].astype(float).tolist()
        else:
            yerr = None

        plot(x, y, line_name, xerr, yerr)

        if(annotate_points[i]):
            annotate(plt.gca(), x, y)
        if(annotate_min_flag[i]):
            annotate_min(x, y)
        if(annotate_max_flag[i]):
            annotate_max(x, y)

    plt.legend(loc='best', fancybox=True, framealpha=0.5)
    plt.savefig(image_name, bbox_inches='tight')
    plt.tight_layout()
    plt.close()
