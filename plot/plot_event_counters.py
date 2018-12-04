import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import os
import argparse

#from prettytable import PrettyTable
parser = argparse.ArgumentParser(description='Event counter plotter')
parser.add_argument('-i', '--input', required=True, type=str,
                    help='Input directory. Required argument.')
parser.add_argument('-o', '--output', type=str, default='./',
                    help='Output directory.')
parser.add_argument('-r', '--reference', type=str, default=None,
                    help='Directory of reference files.')
parser.add_argument('-e', '--events', required=True, type=str,
                    help='List of events to plot, comma separated list.')
parser.add_argument('-n', '--name', type=str, default='',
                    help='Prefix for the image files.')

event_position = []


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000
    # add more suffixes if you need them
    return '%d%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


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


def plot(app, files, events_list, image, ref_dir=None):
    fig, axis = plt.subplots(2, 3, sharex=True, figsize=(16, 12))
    # fig.suptitle(app)
    plots = {}
    references = []
    for file in files:
        csv_file = file.split('/')[-1].replace('.csv', '')
        worker = csv_file.split('_')[-2]
        event = csv_file.split('_' + worker)[0]
        worker = worker.split('_worker')[0]
        if(event not in events_list):
            continue
        position = event_position[events_list.index(event)]
        ax = axis[position % 2][(position / 2) % 3]
        plt.sca(ax)
        plt.title(event, size=10)
        plt.grid(True, which='major', alpha=0.7)
        plt.xlabel('buf_size, batch_size, ratio')
        if(event == 'time'):
            plt.ylabel('Time (sec)')
        else:
            plt.ylabel('Event count')
        x = []
        y = []
        err = []
        open_file = open(file, 'r')
        next(open_file)
        for line in open_file:
            line = line.split(' ')
            x.append(
                human_format(int(line[2])) + ',' + line[3] + ',' + line[4])
            y.append(float(line[-2]))
            err.append(float(line[-1]))
        plt.errorbar(range(len(x)), y, yerr=err, marker='o',
                     linewidth='2', label=event + '-' + worker)
        if event not in plots:
            plots[event] = y
        else:
            print x
            print y
            print plots[event]
            try:
                plt.errorbar(range(len(x)), [a+b for a, b in zip(y, plots[event])],
                             marker='o', linewidth='2', label=event + '-total')
            except ValueError as e:
                print "Problem with event ", event
        plt.xticks(range(len(x)), x, rotation='vertical')
        # if (ref_dir) and ('map' in worker):
        if (ref_dir and event not in references):
            references.append(event)
            ref_file = "%s/%s/%s_map_worker.csv" % (ref_dir, app, event)
            if(not os.path.isfile(ref_file)):
                continue
            lines = open(ref_file, 'r').readlines()
            data = lines[1].split(' ')
            ymin = max(float(data[-2]) - float(data[-1]), 0)
            ymax = float(data[-2]) + float(data[-1])
            plt.axhspan(
                ymin, ymax, label=event + '-ref', color='0.1', alpha=0.8,
                linestyle='solid', linewidth='2', hatch='/', fill=False)

        plt.legend(loc='best', fancybox=True, framealpha=0.1, fontsize=9)
    plt.tight_layout()
    plt.savefig(image, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    args = parser.parse_args()
    input_dir = args.input
    output_dir = args.output
    ref_dir = args.reference
    name_prefix = args.name
    output_dir += name_prefix
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    events_list = args.events.split(',')
    # event_position = []
    for i in range(len(events_list)):
        if(':' in events_list[i]):
            event_position.append(int(events_list[i].split(':')[1]))
            events_list[i] = events_list[i].split(':')[0]
        else:
            event_position.append(i)
    for dirs, subdirs, files in os.walk(input_dir):
        # print dirs, subdirs, files
        if subdirs:
            continue
        app = dirs.split('/')[-1]
        output_image = output_dir + '/' + name_prefix + '-' + app + '.png'
        files = [dirs + '/' + s for s in files]
        plot(app, files, events_list, output_image, ref_dir)
