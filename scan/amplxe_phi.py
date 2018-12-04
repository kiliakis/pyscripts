import subprocess
import os

datafiles = '/home/iliakis/testcases/'
outfiles = '/home/iliakis/custom-phoenix/results/raw/amplxe-all-v2/'
exe_dir = '/home/iliakis/custom-phoenix/'

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
    'dummy2cpu-cpu': {'FILL': '1'},
    'dummy2cpu-mem': {'FILL': '1'},
    'dummy2mem-cpu': {'FILL': '1'},
    'dummy2mem-mem': {'FILL': '1'}

}

testcases = {
    'word_count': [datafiles + 'word_count_datafiles/word_600MB.txt'],
    # 'mr_matrix_multiply': ['-s1000'],
    'histogram': [datafiles + 'histogram_datafiles/big.bmp'],
    'linear_regression': [datafiles + 'histogram_datafiles/big.bmp'],
    'kmeans': ['-d4', '-c100', '-p100000'],
    'pca': ['-r3000', '-c5000']
    #'dummy2cpu-cpu': ['-m0', '-r0', '-b50', '-t1', '-d3', '-c160', '-p500000'],
    #'dummy2cpu-mem': ['-m0', '-r1', '-b4000', '-t1', '-d3', '-c40', '-p500000'],
    #'dummy2mem-mem': ['-m1', '-r1', '-b100', '-t1', '-d4', '-c400', '-p500000'],
    #'dummy2mem-cpu': ['-m1', '-r0', '-b150', '-t1', '-d3', '-c8000', '-p500000']
}

# buf_sizes = {
#     'word_count': range(1000, 2001, 1000),
#     'mr_matrix_multiply': range(9000, 11000, 500),
#     'histogram': range(1000, 2001, 1000),
#     'linear_regression': range(4000, 5001, 1000),
#     'kmeans': range(4000, 5001, 1000),
#     'pca': range(1000, 2001, 1000),
#     'dummy2cpu-cpu': range(1000, 2001, 1000),
#     'dummy2cpu-mem': range(1000, 2001, 1000),
#     'dummy2mem-cpu': range(1000, 2001, 1000),
#     'dummy2mem-mem': range(1000, 2001, 1000)
# }

buf_sizes = {
    'word_count': [10000],
    'mr_matrix_multiply': [10000],
    'histogram': [10000],
    'linear_regression': [10000],
    'kmeans': [10000],
    'pca': [2000],
    'dummy2cpu-cpu': [10000],
    'dummy2cpu-mem': [10000],
    'dummy2mem-cpu': [10000],
    'dummy2mem-mem': [10000]
}

ratios = {
    'word_count': ['5', '7'],
    'mr_matrix_multiply': ['3'],
    'histogram': ['5'],
    'linear_regression': ['3'],
    # 'kmeans': ['15'],
    'kmeans': ['11', '13'],
    'pca': ['2'],
    'dummy2cpu-cpu': ['3'],
    'dummy2cpu-mem': ['3'],
    'dummy2mem-cpu': ['3'],
    'dummy2mem-mem': ['3']
}

batch_sizes = {
    # 'word_count': ['1', '5', '10'],
    'word_count': ['5', '10'],
    'mr_matrix_multiply': ['15', '20', '25'],
    # 'histogram': [5', '10'],
    'histogram': ['50', '100'],
    # 'linear_regression': ['5', '10'],
    'linear_regression': ['50', '100'],
    'kmeans': ['100', '200'],
    # 'pca': ['50', '100', '200'],
    'pca': ['10', '150'],
    'dummy2cpu-cpu': ['100', '200'],
    'dummy2cpu-mem': ['10', '50'],
    'dummy2mem-cpu': ['100', '200'],
    'dummy2mem-mem': ['100', '200']

}


events_per_run = 4
event_list = [
    ('DATA_READ', 'A'),
    ('DATA_WRITE', 'B'),
    ('DATA_READ_MISS', 'C'),
    ('DATA_WRITE_MISS', 'D'),
    ('INSTRUCTIONS_EXECUTED', 'E'),
    ('CPU_CLK_UNHALTED', 'F'),
    ('BRANCHES', 'G'),
    ('BRANCHES_MISPREDICTED', 'H'),
    ('L2_DATA_READ_MISS_CACHE_FILL', 'I'),
    ('L2_DATA_WRITE_MISS_CACHE_FILL', 'J'),
    ('L2_DATA_READ_MISS_MEM_FILL', 'K'),
    ('L2_DATA_WRITE_MISS_MEM_FILL', 'L')
]

amplxe_args = ['amplxe-cl', '-collect-with', 'runsa', '-no-summary',
               '-target-system=mic-native:mic0', '-knob', '']

repeats = 3

total_sims = 0
for app in testcases.keys():
    total_sims += len(buf_sizes[app]) * len(ratios[app]) * \
        len(policies[app]) * len(batch_sizes[app]) * \
        ((len(event_list) + events_per_run - 1) / events_per_run)
total_sims *= repeats

print('Total runs: ', total_sims)
current_sim = 0


for app, size in testcases.items():
    for buf in buf_sizes[app]:
        buf = str(buf)
        for batch in batch_sizes[app]:
            for policy_name, policy in policies[app].items():
                for r in ratios[app]:
                    outdir = outfiles + app + '/' + policy_name + '/'
                    if not os.path.exists(outdir):
                        os.makedirs(outdir)
                    for e in range(0, len(event_list), events_per_run):
                        events, letters = map(
                            list, zip(
                                *event_list[e:min(
                                    e+events_per_run, len(event_list))]))
                        amplxe_args[-1] = 'event-config=' + ','.join(events)
                        letters = ''.join(letters)
                        for i in range(0, repeats):
                            file_name = outdir + 'buf' + buf + 'batch' + \
                                batch + 'ratio' + r + 'e' + \
                                letters + 'run' + str(i)
                            stdout = open(file_name + '.stdout', 'w')
                            print(app, policy_name, r, buf, batch, i)
                            exe = app
                            environ = ['MR_BUF_SIZE='+buf,
                                       'MR_BATCH_SIZE=' +
                                       str(int(buf) / int(batch)),
                                       'MR_THR_TO_CPU_POLICY='+policy,
                                       'MR_MAP_COMBINE_RATIO='+r]
                            if 'dummy2' in app:
                                exe = 'dummy2'
                            elif 'pca' in app:
                                environ += ['MR_CHUNKSIZE=-4']
                            exe_list = amplxe_args + ['-result-dir', file_name] +\
                                ['--', '/home/iliakis/export-and-exec.sh'] +\
                                environ +\
                                ['cmd', exe_dir + exe] + size
                            subprocess.call(exe_list,
                                            stdout=stdout,
                                            stderr=stdout,
                                            env=os.environ.copy())
                            current_sim += 1
                            print('%lf %% is completed' % (100.0 * current_sim /
                                                           total_sims))
