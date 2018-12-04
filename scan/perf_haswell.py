import subprocess
import os
import time
import numpy as np

datafiles = '/afs/cern.ch/work/k/kiliakis/git/thesis/testcases/'
outfiles = '/afs/cern.ch/work/k/kiliakis/git/thesis/custom-phoenix/results/perf/v2/'
exe_dir = '/afs/cern.ch/work/k/kiliakis/git/thesis/custom-phoenix/build_gcc/custom-phoenix/'

# 0: DEDICATED
# 1: FILL
# 2: PUSH
policies = {
    'word_count': {"FILL": '1'},
    'mr_matrix_multiply': {'FILL': '1'},
    'histogram': {'FILL': '1'},
    'linear_regression': {'FILL': '1'},
    'kmeans': {"FILL": '1'},
    'pca': {'FILL': '1'},
    'dummy2cpu-cpu': {'PUSH': '2'},
    'dummy2cpu-mem': {'FILL': '1'}
}

testcases = {
    'word_count': [datafiles + 'word_count_datafiles/word_200MB.txt'],
    'mr_matrix_multiply': ['-s1000'],
    'histogram': [datafiles + 'histogram_datafiles/med.bmp'],
    'linear_regression': [datafiles + 'linear_regression_datafiles/key_file_200MB.txt'],
    'kmeans': ['-d3', '-c100', '-p1000000'],
    'pca': ['-r3000', '-c5000'],
    'dummy2cpu-cpu': ['-m0', '-r0', '-d16', '-c500', '-p1000000'],
    'dummy2cpu-mem': ['-m0', '-r1', '-d16', '-c500', '-p1000000']
}

buf_sizes = {
    'word_count': range(14000, 16000, 500),
    'mr_matrix_multiply': range(9000, 11000, 500),
    'histogram': range(7000, 9000, 500),
    'linear_regression': range(7000, 9000, 500),
    'kmeans': range(3000, 5000, 500),
    'pca': range(9000, 11000, 500),
    'dummy2cpu-cpu': range(7000, 9000, 500),
    'dummy2cpu-mem': range(1000, 3000, 500)
}

ratios = {
    'word_count': ['2', '3'],
    'mr_matrix_multiply': ['4', '5'],
    'histogram': ['1', '2'],
    'linear_regression': ['1', '2'],
    'kmeans': ['10', '11'],
    'pca': ['1', '2'],
    'dummy2cpu-cpu': ['10', '11'],
    'dummy2cpu-mem': ['5', '6']
}

batch_sizes = {
    'word_count': ['10', '15', '20'],
    'mr_matrix_multiply': ['15', '20', '25'],
    'histogram': ['10', '15', '20'],
    'linear_regression': ['10', '15', '20'],
    'kmeans': ['75', '100', '125'],
    'pca': ['75', '100', '125'],
    'dummy2cpu-cpu': ['15', '20', '25'],
    'dummy2cpu-mem': ['40', '50', '60']
}

# event_list = ['task-clock']
event_list = ['L1-dcache-load-misses', 'L1-dcache-loads',
              'LLC-loads', 'LLC-load-misses',
              'mem-loads', 'mem-stores']


perf_args = ['amplxe-perf', 'record', '-e'] + [','.join(event_list)]

repeats = 4

total_sims = 0
for app in testcases.keys():
    total_sims += len(buf_sizes[app]) * len(ratios[app]) * \
        len(policies[app]) * len(batch_sizes[app])
total_sims *= repeats

print "Total runs: ", total_sims
current_sim = 0

os.chdir(exe_dir)

for app, size in testcases.items():
    for buf in buf_sizes[app]:
        buf = str(buf)
        os.environ['MR_BUF_SIZE'] = buf
        for batch in batch_sizes[app]:
            os.environ['MR_BATCH_SIZE'] = str(int(buf) / int(batch))
            for policy_name, policy in policies[app].items():
                os.environ['MR_THR_TO_CPU_POLICY'] = policy
                for r in ratios[app]:
                    os.environ['MR_MAP_COMBINE_RATIO'] = r
                    outdir = outfiles + app + '/' + policy_name + '/'
                    if not os.path.exists(outdir):
                        os.makedirs(outdir)
                    stderr = open(outdir + 'stderr', 'w')
                    for i in range(0, repeats):
                        stdout = open(outdir + 'buf' + buf + 'batch' +
                              batch + 'ratio' + r + 'run' + str(i) + '.stdout', 'w')
                        perf_data = outdir + 'buf' + buf + 'batch' + \
                            batch + 'ratio' + r + 'run' + str(i) + '.perf'
                        print app, policy_name, r, buf, batch, i
                        exe = app
                        if 'dummy2' in app:
                            exe = 'dummy2'
                        exe_list = perf_args + \
                            ['-o', perf_data] + ['--'] + ['./' + exe] + size
                        subprocess.call(exe_list,
                                        stdout=stdout,
                                        stderr=stderr,
                                        env=os.environ.copy())
                        current_sim += 1
                        print "%lf %% is completed" % (100.0 * current_sim /
                                                       total_sims)
