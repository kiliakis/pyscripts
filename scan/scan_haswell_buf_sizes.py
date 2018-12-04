import subprocess
import os
import numpy as np
import csv


def get_time(phase, string):
    time = 0.0
    for line in string.split('\n'):
        if phase in line:
            time += float(line.split(phase)[1])
    return time


datafiles = '/afs/cern.ch/work/k/kiliakis/git/thesis/testcases/'
outfiles = '/afs/cern.ch/work/k/kiliakis/git/thesis/custom-phoenix/results/raw/buf-sizes2/'
exe_dirs = ['/afs/cern.ch/work/k/kiliakis/git/thesis/custom-phoenix/build_gcc_dynamic/custom-phoenix/']
# exe_dir_static =
# exe_dir_dynamic =
# 0: DEDICATED
# 1: FILL
# 2: PUSH
policies = {
    'word_count': {'FILL': '1'},
    'mr_matrix_multiply': {'FILL': '1'},
    'histogram': {'FILL': '1'},
    'linear_regression': {'FILL': '1'},
    'kmeans': {'FILL': '1'},
    'pca': {'FILL': '1'},
    'dummy2cpu-cpu': {'FILL': '1'},
    'dummy2cpu-mem': {'FILL': '1'},
    'dummy2mem-cpu': {'FILL': '1'},
    'dummy2mem-mem': {'FILL': '1'}

}

testcases = {
    # 'word_count': [datafiles + 'word_count_datafiles/word_1GB.txt'],
    # 'mr_matrix_multiply': ['-s1000'],
    # 'histogram': [datafiles + 'histogram_datafiles/huge.bmp'],
    # 'linear_regression': [datafiles + 'histogram_datafiles/huge.bmp'],
    'kmeans': ['-d4', '-c100', '-p500000']
    # 'pca': ['-r3000', '-c5000']
    # 'dummy2cpu-cpu': ['-m0', '-r0', '-t1', '-b400', '-d32', '-c1000', '-p100000'],
    # 'dummy2cpu-mem': ['-m0', '-r1', '-t1', '-b5000', '-d32', '-c1000', '-p50000'],
    # 'dummy2mem-mem': ['-m1', '-r1', '-t1', '-b1000', '-d32', '-c4000', '-p50000'],
    # 'dummy2mem-cpu': ['-m1', '-r0', '-t1', '-b100', '-d32', '-c7000', '-p100000']
}


buf_sizes = {
    'word_count': range(1000, 10001, 1000),
    'mr_matrix_multiply': range(1000, 10001, 1000),
    'histogram': range(1000, 10001, 1000),
    'linear_regression': range(1000, 10001, 1000),
    # 'kmeans': range(1000, 10001, 1000),
    'kmeans': [1000, 2000, 3000, 4000, 5000, 6000, 10000],
    'pca': range(1000, 10001, 1000),
    'dummy2cpu-cpu': [10000],
    'dummy2cpu-mem': [10000],
    'dummy2mem-cpu': [10000],
    'dummy2mem-mem': [10000]
}


ratios = {
    'word_count': ['1'],
    'mr_matrix_multiply': ['3'],
    'histogram': ['1'],
    'linear_regression': ['1'],
    'kmeans': ['13'],
    'pca': ['1'],
    'dummy2cpu-cpu': ['1'],
    'dummy2cpu-mem': ['1'],
    'dummy2mem-cpu': ['1'],
    'dummy2mem-mem': ['1']
}

batch_sizes = {
    'word_count': ['10'],
    'mr_matrix_multiply': ['10'],
    'histogram': ['10'],
    'linear_regression': ['10'],
    'kmeans': ['10'],
    'pca': ['10'],
    'dummy2cpu-cpu': ['10', '20', '50', '100'],
    'dummy2cpu-mem': ['10', '20', '50', '100'],
    'dummy2mem-cpu': ['10', '20', '50', '100'],
    'dummy2mem-mem': ['10', '20', '50', '100']
}
repeats = 20

total_sims = 0
for app in testcases.keys():
    total_sims += len(buf_sizes[app]) * len(ratios[app]) * \
        len(policies[app]) * len(batch_sizes[app])
total_sims *= repeats * len(exe_dirs)

print "Total runs: ", total_sims
current_sim = 0

# os.chdir(exe_dir)
header = ['app', 'policy', 'buf_size', 'batch_size', 'ratio',
          'realtime', 'realtime_std', 'cputime', 'cputime_std',
          'utilization', 'utilization_std']

for app, size in testcases.items():
    outdir = outfiles
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    name = outdir + app + '_timings.csv'
    out = open(name, 'w')
    writer = csv.writer(out, delimiter=' ')
    writer.writerow(header)
    rows = []
    for exe_dir in exe_dirs:
        for policy_name, policy in policies[app].items():
            os.environ['MR_THR_TO_CPU_POLICY'] = policy
            for buf in buf_sizes[app]:
                buf = str(buf)
                os.environ['MR_BUF_SIZE'] = buf
                for batch in batch_sizes[app]:
                    os.environ['MR_BATCH_SIZE'] = str(int(buf)/int(batch))
                    for r in ratios[app]:
                        os.environ['MR_MAP_COMBINE_RATIO'] = r
                        stdout = open(outfiles + 'stdout', 'w')
                        times = []
                        for i in range(0, repeats):
                            exe = app
                            if 'dummy2' in app:
                                exe = 'dummy2'
                            elif 'pca' in app:
                                os.environ['MR_CHUNKSIZE'] = '-8'
                            elif 'linear_regression' in app:
                                os.environ['MR_CHUNKSIZE'] = '-32'
                            elif 'word_count' in app:
                                os.environ['MR_CHUNKSIZE'] = '-8'
                            print app, policy_name, r, buf, batch, i
                            # start = time.time()
                            output = subprocess.check_output(
                                [exe_dir + exe] + size,
                                # stderr=subprocess.STDOUT,
                                env=os.environ.copy())
                            # end = time.time()
                            stdout.write(output)
                            time = get_time(
                                'map-combine phase real time:', output)
                            cputime = get_time(
                                'map-combine phase cpu time:', output)
                            utilization = 100.0 * (cputime) / (time)
                            times.append((time, cputime, utilization))
                            current_sim += 1
                            print("%lf %% is completed" %
                                  (100.0 * current_sim / total_sims))
                        times = sorted(times)[:10]
                        means = np.mean(times, axis=0)
                        stds = np.std(times, axis=0)
                        rows.append([app, policy_name, buf, batch, r,
                                     means[0], stds[0], means[1], stds[1],
                                     means[2], stds[2]])
    rows.sort(
        key=lambda a: (a[1], a[2], int(a[3]), int(a[4]), int(a[5])))
    writer.writerows(rows)
