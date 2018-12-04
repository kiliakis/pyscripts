#!/usr/bin/python
import os
import csv
import sys
import numpy as np
import operator


def string_between(string, before, after):
    temp = string.split(before)[1]
    temp = temp.split(after)[0]
    return temp


def import_results(output_file):
    d = np.loadtxt(output_file, dtype='str')
    return d.tolist()

names = {
    'word_count': 'WC',
    'linear_regression': 'LR',
    'mr_matrix_multiply': 'MM',
    'pca': 'PCA',
    'histogram': 'Hist',
    'kmeans': 'KMeans'
}

input_size = {
    'WC': 1e9,
    'Hist': 1.6e9,
    'LR': 1.6e9,
    'PCA': 2*64e6,
    'KMeans': 2e9,
    'MM': 4e6
}

metrics = {
    'GCycles_total': ['CPU_CLK_UNHALTED.THREAD_map_worker',
                      'CPU_CLK_UNHALTED.THREAD_combine_worker', '+',
                      1e9, '/'
                      ],
    'ipb_total': ['INST_RETIRED.ANY_map_worker', 'INST_RETIRED.ANY_combine_worker',
                  '+', 'input_size', '/'],
    # 'spb_total': ['RESOURCE_STALLS.ANY_map_worker', 'RESOURCE_STALLS.ANY_combine_worker', '+',
    #               'input_size', '/'],
    # 'spi_map_worker': ['RESOURCE_STALLS.ANY_map_worker',
    #                    'INST_RETIRED.ANY_map_worker', '/'],
    # 'spi_combine_worker': ['RESOURCE_STALLS.ANY_combine_worker',
    #                        'INST_RETIRED.ANY_combine_worker', '/'],
    'rspi_total': ['RESOURCE_STALLS.ANY_map_worker', 'RESOURCE_STALLS.ANY_combine_worker', '+',
                  'INST_RETIRED.ANY_map_worker', 'INST_RETIRED.ANY_combine_worker', '+', '/'],
    'mspi_total': ['CYCLE_ACTIVITY.STALLS_LDM_PENDING_map_worker', 'CYCLE_ACTIVITY.STALLS_LDM_PENDING_combine_worker', '+',
                  'INST_RETIRED.ANY_map_worker', 'INST_RETIRED.ANY_combine_worker', '+', '/'],

    'spb_total': ['RESOURCE_STALLS.ANY_map_worker', 'RESOURCE_STALLS.ANY_combine_worker', '+',
                  'CYCLE_ACTIVITY.STALLS_LDM_PENDING_map_worker', 'CYCLE_ACTIVITY.STALLS_LDM_PENDING_combine_worker', '+', '+',
                  'input_size', '/'],
    # 'cpi_total': ['CPU_CLK_UNHALTED.THREAD_map_worker',
    #               'INST_RETIRED.ANY_map_worker', '/']
    # 'GCycles_map_worker': ['CPU_CLK_UNHALTED.THREAD_map_worker', 1e9, '/'],
    # 'GResStalls_map_worker': ['RESOURCE_STALLS.ANY_map_worker', 1e9, '/'],
    # 'ipb_map_worker': ['INST_RETIRED.ANY_map_worker', 'input_size', '/'],
    # 'stallspinstr_map_worker': ['RESOURCE_STALLS.ANY_map_worker',
    #                             'INST_RETIRED.ANY_map_worker', '/'],
    # 'cpi_map_worker': ['CPU_CLK_UNHALTED.THREAD_map_worker', 'INST_RETIRED.ANY_map_worker', '/'],

    # # 'GIdleCycles_map_worker': ['CYCLE_ACTIVITY.CYCLES_NO_EXECUTE_map_worker', 1e9, '/'],
    # 'GInst_map_worker': ['INST_RETIRED.ANY_map_worker', 1e9, '/'],
    # 'mpki_map_worker': [1e3, 'LONGEST_LAT_CACHE.REFERENCE_map_worker', '*',
    #                     'INST_RETIRED.ANY_map_worker', '/'],
    # 'cpa_map_worker': ['CPU_CLK_UNHALTED.THREAD_map_worker',
    #                    'MEM_UOPS_RETIRED.ALL_LOADS_map_worker', 'MEM_UOPS_RETIRED.ALL_STORES_map_worker', '+',
    #                    '/'],
    # 'GCycles_combine_worker': ['CPU_CLK_UNHALTED.THREAD_combine_worker', 1e9, '/'],
    # 'GResStalls_combine_worker': ['RESOURCE_STALLS.ANY_combine_worker', 1e9, '/'],
    # 'GIdleCycles_combine_worker': ['CYCLE_ACTIVITY.CYCLES_NO_EXECUTE_combine_worker', 1e9, '/'],
    # 'GInst_combine_worker': ['INST_RETIRED.ANY_combine_worker', 1e9, '/'],
    # 'mpki_combine_worker': [1e3, 'LONGEST_LAT_CACHE.REFERENCE_combine_worker', '*',
    #                         'INST_RETIRED.ANY_combine_worker', '/']
    # 'stallspinstr_combine_worker': ['RESOURCE_STALLS.ANY_combine_worker',
    #                             'INST_RETIRED.ANY_combine_worker', '/'],
    # 'ipb_combine_worker': ['INST_RETIRED.ANY_combine_worker' ,'input_size', '/'],
    # 'cpi_combine_worker': ['CPU_CLK_UNHALTED.THREAD_combine_worker', 'INST_RETIRED.ANY_combine_worker', '/']
    # 'cpa_combine_worker': ['CPU_CLK_UNHALTED.THREAD_combine_worker',
    #                        'MEM_UOPS_RETIRED.ALL_LOADS_combine_worker', 'MEM_UOPS_RETIRED.ALL_STORES_combine_worker', '+',
    #                        '/']
    '': []
}

ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.div
}

y_name = 'event_count'


def calculate_metrics(input, output):
    for dirs, subdirs, files in os.walk(input):
        if subdirs:
            continue
        # print dirs
        app = dirs.split('/')[-1]
        print '\n', app
        header = []
        data = []
        for metric_name in sorted(metrics):
            equation = metrics[metric_name]
            stack = []
            if not metric_name:
                continue
            for symbol in equation:
                if isinstance(symbol, float):
                    # print "I found an int %d" % symbol
                    stack.append(float(symbol))
                elif (symbol in ops):
                    # print "I found an operator %s" % symbol
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                    stack.append(ops[symbol](operand1, operand2))
                elif (symbol == 'input_size'):
                    stack.append(input_size[names[app]])
                elif (isinstance(symbol, (str))):
                    # print "I found a string %s" % symbol
                    file_name = dirs + '/' + symbol + '.csv'
                    values = import_results(file_name)
                    header = values[0]
                    values = values[1:]
                    values = np.array(values)
                    data = values
                    c = header.index(y_name)
                    operand = values[:, c].astype(float)
                    stack.append(operand)
            print "%s :" % (metric_name), stack[0][0]
            c = header.index(y_name)
            data[:, c] = stack.pop()
            data = data[:, :-1]
            header[c] = 'metric'
            header = header[:-1]
            out = open(
                dirs + '/' + metric_name + '.csv', 'w')
            writer = csv.writer(out, delimiter=' ')
            writer.writerow(header)
            writer.writerows(data)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "You should specify input and output directory"
        exit(-1)
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    calculate_metrics(input_dir, output_dir)
