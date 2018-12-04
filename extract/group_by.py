import numpy as np
import csv
from prettytable import PrettyTable

input_file = '/afs/cern.ch/work/k/kiliakis/results/csv/cpp/LHC-acc/for-slides.csv'

output_file_prefix = ''
# column_names = ['n_macroparticles', 'n_slices']
column_names = ['n_threads']
# prefixes = ['-m', '-s']
prefixes = ['-thr']



def group_by(list, key_names, prefixes):
    h = list[0]
    d = {}
    for r in list[1:]:
        key = []
        for k in key_names:
            key += [prefixes[key_names.index(k)]+r[h.index(k)]]
        key = ''.join(key)
        if key not in d:
            d[key] = []
        d[key] += [r]

    return (d, h)


def dump_to_files(header, prefix, records):
    file = output_file_prefix + prefix + '.csv'
    writer = csv.writer(open(file, 'w'), lineterminator='\n', delimiter=',')
    writer.writerow(header)
    writer.writerows(records)
    # t = PrettyTable(header)
    # t.align = 'l'
    # t.border = False
    # for r in records:
    #     t.add_row(r)
    # with open(output_file_prefix+prefix+'.csv', 'w') as f:
    #     f.writelines(str(t) + '\n')


def import_results(file):
    d = np.loadtxt(file, dtype='str', delimiter=',')
    return d.tolist()


if __name__ == '__main__':
    if not output_file_prefix:
        output_file_prefix = input_file.split('.csv')[0]
    list = import_results(input_file)
    print list
    grouped_dict, header = group_by(list, column_names, prefixes)
    for k, v in grouped_dict.iteritems():
        dump_to_files(header, k, v)
