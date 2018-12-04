#!/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
import sys

res_dir = '/afs/cern.ch/work/k/kiliakis/results/csv/'
images_dir = '/afs/cern.ch/work/k/kiliakis/results/images/'


csv_files = [res_dir + 'cpp/TC1/for-slides.csv',
             res_dir + 'cpp/TC5_time_time/for-slides.csv',
             res_dir + 'cpp/TC5_time_freq/for-slides.csv',
             res_dir + 'cpp/LHC-acc/for-slides.csv']

num_lines = len(csv_files)

reference_files = [res_dir + 'python/TC1/for-slides.csv',
                   res_dir + 'python/TC5_time_time/for-slides.csv',
                   res_dir + 'python/TC5_time_freq/for-slides.csv',
                   res_dir + 'python/LHC-acc/for-slides.csv']


x_names = ['n_threads'] * num_lines
y_names = ['turn_time'] * num_lines

line_names = ['TC1_Acceleration',
              'TC5_Wake_impedance_conv',
              'TC5_Wake_impedance_fft',
              'LHC_acc_re_3b']

image_name = images_dir + 'BLonDpp-speedup.png'
x_label = 'Threads'
y_label = 'Speedup'
title = 'BLonD/BLonD++ Mean Turn Time'
annotate_min_flag = [False]
annotate_max_flag = [False]
annotate_points = [False] * num_lines
x_lims = []
y_lims = []


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
    d = np.loadtxt(file, dtype='str', delimiter=',')
    return d.tolist()


def plot(x, y, label):

    plt.grid(True, which='major', alpha=1)
    plt.grid(True, which='minor', alpha=0.8)
    plt.minorticks_on()
    plt.plot(x, y, marker='o', linewidth='2', label=label)


if __name__ == '__main__':

    # plt.figure(figsize=(12, 7))
    plt.figure()
    plt.tick_params(labelright=True)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    if(x_lims):
        plt.xlim(x_lims)
    if(y_lims):
        plt.ylim(y_lims)

    for i in range(len(csv_files)):
        file = csv_files[i]
        ref_file = reference_files[i]

        x_name, y_name = x_names[i], y_names[i]
        line_name = line_names[i]
        print line_name

        ref = import_results(ref_file)
        l = import_results(file)

        header = l[0]
        print header
        header_ref = ref[0]

        array_ref = np.array(ref[1:])
        array = np.array(l[1:])
        print array
        c = header.index(x_name)
        x = array[:, c].astype(int)
        c = header.index(y_name)
        y = array[:, c].astype(float)

        c = header_ref.index(x_name)
        x_ref = array_ref[:, c].astype(int)
        c = header_ref.index(y_name)
        y_ref = array_ref[:, c].astype(float)

        if not np.array_equal(x_ref, x):
            print 'x_ref', x_ref
            print 'x', x
            sys.exit(
                'Error: x refernce values and x values should be the same')

        plot(x, y_ref / y, line_name)

        if(annotate_points[i]):
            annotate(plt.gca(), x, y_ref / y)

        '''
        if(annotate_min_flag[i]):
            annotate_min(x, y)
        if(annotate_max_flag[i]):
            annotate_max(x, y)
        '''
    plt.legend(loc='best', fancybox=True, framealpha=0.5)
    plt.savefig(image_name, bbox_inches='tight')
    plt.tight_layout()
    plt.close()
