#!/usr/bin/python
import os
import csv
import sys
import numpy as np
import subprocess

delimiter = ';'


def string_between(string, before, after):
    temp = string.split(before)[1]
    temp = temp.split(after)[0]
    return temp

app = ''
policy = ''
buf_size = ''
batch = ''
ratio = ''
event_list = []


def process_line(line, events):
    global event_list
    if('Function' in line) and ('Event Count' in line):
        event_line = line.split(delimiter)[1:]
        event_list = []
        for e in event_line:
            event_list.append(e.split('Event Count:')[1].strip())
            if(e.split('Event Count:')[1].strip() not in events):
                events[e.split('Event Count:')[1].strip()] = {}
    elif('MapReduce' in line) and ('map_worker' in line):
        counters = line.split(delimiter)[1:]
        for i in range(len(counters)):
            event = event_list[i]
            if('map_worker' not in events[event]):
                events[event]['map_worker'] = []
            events[event]['map_worker'].append(int(counters[i]))
    elif('MapReduce' in line) and ('combine_worker' in line):
        counters = line.split(delimiter)[1:]
        for i in range(len(counters)):
            event = event_list[i]
            if('combine_worker' not in events[event]):
                events[event]['combine_worker'] = []
            events[event]['combine_worker'].append(int(counters[i]))
    return

# First we have to create a dictionary
# one key per application
# one key per event
# one key for map/ combine
# a list for every run to extract mean/ std


def extract_results(input, outdir):
    outdir = os.path.abspath(outdir)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    os.chdir(input)
    header = ['app', 'policy', 'buf_size',
              'batch', 'ratio', 'event_count', 'std']
    app_dict = {}
    for dirs, subdirs, files in os.walk('./'):
        for file in files:
            if('.report' not in file):
                continue
            # print dirs, subdirs, files
            events = {}
            print dirs + '/' + file
            app = dirs.split('/')[1]
            policy = dirs.split('/')[2]
            buf_size = string_between(file, 'buf', 'batch')
            batch = string_between(file, 'batch', 'ratio')
            ratio = string_between(file, 'ratio', 'e')
            if(app not in app_dict):
                app_dict[app] = {}
            for line in open(os.path.join(dirs, file), 'r'):
                process_line(line, events)
            for event, workers in events.items():
                if(event not in app_dict[app]):
                    app_dict[app][event] = {}
                for worker, counters in workers.items():
                    if(worker not in app_dict[app][event]):
                        app_dict[app][event][worker] = []
                    print len(counters)
                    app_dict[app][event][worker].append([app, policy, buf_size,
                                                         batch, ratio,
                                                         np.mean(counters),
                                                         np.std(counters)])
            # print app_dict[app]
    for app, events in app_dict.items():
        for event, workers in events.items():
            for worker, combos in workers.items():
                if not os.path.exists(outdir + '/' + app + '/'):
                    os.makedirs(outdir + '/' + app + '/')
                out = open(outdir + '/' + app + '/' + event + '_' + worker + '.csv', 'w')
                writer = csv.writer(out, delimiter=' ')
                writer.writerow(header)
                combos.sort(
                    key=lambda a: (a[1], int(a[2]), int(a[3]), int(a[4]), int(a[5])))
                writer.writerows(combos)


def import_results(output_file):
    d = np.loadtxt(output_file, dtype='str')
    return d.tolist()


def extract_reports(input_dir):
    for dirs, subdirs, files in os.walk(input_dir):
        if('batch' in dirs):
            continue
        for res_dir in subdirs:
            print dirs + '/' + res_dir
            try:
                app = dirs.split('/')[1]
                policy = dirs.split('/')[2]
                buf_size = string_between(res_dir, 'buf', 'batch')
                batch = string_between(res_dir, 'batch', 'ratio')
                ratio = string_between(res_dir, 'ratio', 'e')
            except IndexError as e:
                continue
            exe_list = ['amplxe-cl', '-report', 'hw-events',
                        '-limit=10', '-csv-delimiter=semicolon',
                        '-column=Hardware',
                        '-result-dir=' + dirs + '/' + res_dir]
            null = open('/dev/null', 'w')
            report_name = dirs + '/' + res_dir.replace('run', '')[:-1]
            output = subprocess.check_output(exe_list)
            out_file = open(report_name + '.report', 'a')
            out_file.write(output)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "You should specify input and output directory"
        exit(-1)
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    if (len(sys.argv) == 4) and (sys.argv[3] == 'report'):
        extract_reports(input_dir)
    extract_results(input_dir, output_dir)
