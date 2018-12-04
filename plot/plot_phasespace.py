import matplotlib.pyplot as plt
import numpy as np
import sys

x_label = 'Dt'
y_label = 'DE'
title = 'Phase Space'


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

  
    if len(sys.argv) < 3:
        print "You must specify the input data file and image name"
        exit(-1)
    input_file = sys.argv[1]
    image_name = sys.argv[2]

    dt, de = np.loadtxt(input_file, unpack=True)

    plt.figure()
    plt.tick_params(labelright=True)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    plt.plot(dt[::100], de[::100], marker='o', linewidth='2')
        
    # plt.legend(loc='best', fancybox=True, framealpha=0.5)
    # plt.savefig(image_name, bbox_inches='tight')
    plt.tight_layout()
    plt.show()
    # plt.close()

