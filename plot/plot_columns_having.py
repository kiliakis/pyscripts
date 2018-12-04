#!/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
import sys

project_dir = './'
res_dir = project_dir
images_dir = project_dir + 'results/haswell/plots/'

# reference_files = [res_dir + 'python/PSB/v1/result-s'+a+'.csv'] * 4
csv_files = [res_dir +
             'results/haswell/csv/dummy2-swap-1/dummy2cpu-mem.csv',
             res_dir +
             'results/haswell/csv/dummy2-swap-1/dummy2cpu-mem.csv',
             res_dir +
             'results/haswell/csv/dummy2-swap-1/dummy2cpu-mem.csv',
             res_dir +
             '../phoenix-new/results/haswell/csv/dummy2-swap-1/dummy2cpu-mem.csv']

num_files = len(csv_files)

having = [['ratio'], ['ratio'], ['ratio'],
          []]
x_names = ['bval'] * num_files
y_names = ['realtime'] * num_files
y_err_names = ['realtime_std'] * num_files

line_names = ['ratio-1', 'ratio-2', 'ratio-3', 'original']
image_names = [images_dir+'dummy2cpu-mem-v1.png',
               images_dir + 'dummy2cpu-mem-v1.pdf']

x_label = 'Combine Workload Heaviness'
y_label = 'Run Time (sec)'
title = 'Effect of Workload on Optimal Map/ Combine Ratio'
annotate_min_flag = [True]
annotate_max_flag = [True]
annotate_points = [True, False, False, False]
x_lims = [0, 2000]
y_lims = [2, 10]


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

markers=['o', 's', 'D', '^']
def plot(x, y, label='', yerr=None):

    plt.grid(True, which='major', alpha=1)
    # plt.grid(True, which='minor', alpha=0.8)
    # plt.minorticks_on()
    plt.errorbar(x, y, yerr=yerr, marker=markers.pop(), 
        markersize=8, linewidth='1.5', label=label)


def group_by(input_dict, col, name):
    res_dict = {}
    for k, values in input_dict.items():
        for v in values:
            key = k+name+' '+v[col]+'-'
            if(key not in res_dict):
                res_dict[key] = []
            res_dict[key].append(v)
    return res_dict

if __name__ == '__main__':

    plt.figure(figsize=(8, 5))
    # plt.figure()
    # plt.tick_params(labelright=True)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    if(x_lims):
        plt.xlim(x_lims)
    if(y_lims):
        plt.ylim(y_lims)

    i = 0
    while i < len(csv_files):
        file = csv_files[i]
        # ref_file = reference_files[i]

        # x_name, y_name = x_names[i], y_names[i]
        # yerr_name = y_err_names[i]
        # line_name = line_names[i]

        # ref = import_results(ref_file)
        values = import_results(file)

        header = values[0]
        print header
        # header_ref = ref[0]
        values = values[1:]

        # TODO group_by

        # group_by = having[i]

        sub_values = {'': values}
        for string in having[i]:
            col = header.index(string)
            sub_values = group_by(sub_values, col, string)

        # print sub_values
        for key in sorted(sub_values):
            values = sub_values[key]
            array = np.array(values)
            # array_ref = np.array(ref[1:])
            c = header.index(x_names[i])
            x = array[:, c].astype(int)
            c = header.index(y_names[i])
            y = array[:, c].astype(float)
            c = header.index(y_err_names[i])
            yerr = array[:, c].astype(float)
            if(not key):
                key = 'Phoenix++'
            else:
                key = 'De-MapR, map/combine '+key[:-1]
            plot(x, y, key, yerr)
            # if(annotate_points[i]):
            #     annotate(plt.gca(), x, y_ref / y)
            i += 1
            # print x
            # print y
            # print yerr
        # c = header_ref.index(x_name)
        # x_ref = array_ref[:, c].astype(int)
        # c = header_ref.index(y_name)
        # y_ref = array_ref[:, c].astype(float)

        # if not np.array_equal(x_ref, x):
        #     print 'x_ref', x_ref
        #     print 'x', x
        #     sys.exit(
        #         'Error: x refernce values and x values should be the same')
        '''
        if(annotate_min_flag[i]):
            annotate_min(x, y)
        if(annotate_max_flag[i]):
            annotate_max(x, y)
        '''

    plt.legend(loc='best', fancybox=True, fontsize='11')
    plt.axvline(700.0, color='k', linestyle='--', linewidth=1.5)
    plt.axvline(1350.0, color='k', linestyle='--', linewidth=1.5)
    plt.annotate('Light\nCombine\nWorkload', xy=(200, 6.3), textcoords='data', size='16')
    plt.annotate('Moderate\nCombine\nWorkload', xy=(800, 6.3), textcoords='data', size='16')
    plt.annotate('Heavy\nCombine\nWorkload', xy=(1400, 8.2), textcoords='data', size='16')

    for image_name in image_names:
        plt.savefig(image_name, bbox_inches='tight')
    plt.tight_layout()
    plt.show()
    plt.close()
