import subprocess
import os


def get_time(phase, string):
    time = 0.0
    for line in string.split('\n'):
        if phase in line:
            time += float(line.split(phase)[1])
    return time

datafiles = '/afs/cern.ch/work/k/kiliakis/git/thesis/testcases/'
outfiles = '/afs/cern.ch/work/k/kiliakis/git/thesis/custom-phoenix/results/raw/metrics/v-hash/'
exe_dir = '/afs/cern.ch/work/k/kiliakis/git/thesis/custom-phoenix/build_gcc/custom-phoenix-hash/'

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
    # 'word_count': [datafiles + 'word_count_datafiles/word_1GB.txt'],
    # 'mr_matrix_multiply': ['-s800']
    # 'histogram': [datafiles + 'histogram_datafiles/huge.bmp'],
    # 'linear_regression': [datafiles + 'histogram_datafiles/big.bmp']
    # 'kmeans': ['-d4', '-c100', '-p500000'],
    'pca': ['-r4000', '-c4000']
    # 'dummy2cpu-cpu': ['-m0', '-r0', '-t1', '-b400', '-d32', '-c1000', '-p100000'],
    # 'dummy2cpu-mem': ['-m0', '-r1', '-t1', '-b5000', '-d32', '-c1000', '-p50000'],
    # 'dummy2mem-mem': ['-m1', '-r1', '-t1', '-b1000', '-d32', '-c4000', '-p50000'],
    # 'dummy2mem-cpu': ['-m1', '-r0', '-t1', '-b100', '-d32', '-c7000', '-p100000']
}

# buf_sizes = {
#     'word_count': range(2000, 3001, 1000),
#     'mr_matrix_multiply': range(9000, 11001, 1000),
#     'histogram': range(5000, 6001, 1000),
#     'linear_regression': range(1000, 2001, 1000),
#     'kmeans': range(3000, 5001, 1000),
#     'pca': range(2000, 3001, 1000),
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
    'word_count': ['1'],
    'mr_matrix_multiply': ['3'],
    'histogram': ['1'],
    'linear_regression': ['1'],
    'kmeans': ['13'],
    'pca': ['1'],
    # 'pca': ['13'],
    'dummy2cpu-cpu': ['1'],
    'dummy2cpu-mem': ['1'],
    'dummy2mem-cpu': ['1'],
    'dummy2mem-mem': ['1']
}

batch_sizes = {
    'word_count': ['20'],
    'mr_matrix_multiply': ['100'],
    'histogram': ['1000'],
    'linear_regression': ['500'],
    'kmeans': ['200'],
    'pca': ['100'],
    'dummy2cpu-cpu': ['10', '20', '50', '100'],
    'dummy2cpu-mem': ['10', '20', '50', '100'],
    'dummy2mem-cpu': ['10', '20', '50', '100'],
    'dummy2mem-mem': ['10', '20', '50', '100']
}

events_per_run = 4
event_list = [
    ('INST_RETIRED.ANY', 'A'),
    ('CPU_CLK_UNHALTED.THREAD', 'B'),
    ('RESOURCE_STALLS.ANY', 'C'),
    # ('CYCLE_ACTIVITY.CYCLES_NO_EXECUTE', 'D')
    # ('CYCLE_ACTIVITY.CYCLES_L2_PENDING', 'E'),
    # ('CYCLE_ACTIVITY.CYCLES_L1D_PENDING', 'F'),
    # ('CYCLE_ACTIVITY.CYCLES_LDM_PENDING', 'G'),
    # ('CYCLE_ACTIVITY.STALLS_L2_PENDING', 'H'),
    ('CYCLE_ACTIVITY.STALLS_LDM_PENDING', 'I')
    # ('CYCLE_ACTIVITY.STALLS_L1_PENDING', 'J'),
    # ('MEM_UOPS_RETIRED.ALL_LOADS', 'K'),
    # ('MEM_UOPS_RETIRED.ALL_STORES', 'L'),
    # ('MEM_LOAD_UOPS_RETIRED.L1_HIT', 'M'),
    # ('MEM_LOAD_UOPS_RETIRED.L2_HIT', 'N'),
    # ('MEM_LOAD_UOPS_RETIRED.L1_MISS', 'O'),
    # ('MEM_LOAD_UOPS_RETIRED.L2_MISS', 'P'),
    # ('LONGEST_LAT_CACHE.REFERENCE', 'Q'),
    # ('LONGEST_LAT_CACHE.MISS', 'R'),
    # ('L2_RQSTS.RFO_HIT', 'S'),
    # ('L2_RQSTS.RFO_MISS', 'T'),
    # ('L2_RQSTS.ALL_RFO', 'U'),
    # ('L2_STORE_LOCK_RQSTS.MISS', 'V'),
    # ('L2_STORE_LOCK_RQSTS.HIT_M', 'W'),
    # ('L2_STORE_LOCK_RQSTS.ALL', 'X'),
    # ('BR_INST_EXEC.ALL_BRANCHES', 'Y'),
    # ('BR_MISP_EXEC.ALL_BRANCHES', 'Z')
    # ('UOPS_EXECUTED.CORE_CYCLES_GE_1', 'A_A'),
    # ('UOPS_EXECUTED.CORE_CYCLES_GE_2', 'A_B'),
    # ('UOPS_EXECUTED.CORE_CYCLES_GE_3', 'A_C'),
    # ('UOPS_EXECUTED.CORE_CYCLES_GE_4', 'A_D'),
    # ('UOPS_ISSUED.ANY', 'A_E'),
    # ('UOPS_ISSUED.STALL_CYCLES', 'A_F'),
    # ('RESOURCE_STALLS.RS', 'A_G')
]

amplxe_args = ['amplxe-cl', '-collect-with',
               'runsa', '-no-summary', '-knob', '']

repeats = 10

total_sims = 0
for app in testcases.keys():
    total_sims += len(buf_sizes[app]) * len(ratios[app]) * \
        len(policies[app]) * len(batch_sizes[app]) * \
        ((len(event_list) + events_per_run - 1) / events_per_run)
total_sims *= repeats

print('Total runs: ', total_sims)
current_sim = 0

os.chdir(exe_dir)
for app, size in testcases.items():
    for buf in buf_sizes[app]:
        buf = str(buf)
        os.environ['MR_BUF_SIZE'] = buf
        for batch in batch_sizes[app]:
            os.environ['MR_BATCH_SIZE'] = batch
            for policy_name, policy in policies[app].items():
                os.environ['MR_THR_TO_CPU_POLICY'] = policy
                for r in ratios[app]:
                    os.environ['MR_MAP_COMBINE_RATIO'] = r
                    outdir = outfiles + app + '/' + policy_name + '/'
                    if not os.path.exists(outdir):
                        os.makedirs(outdir)
                    for e in range(0, len(event_list), events_per_run):
                        events, letters = map(
                            list, zip(
                                *event_list[e:min(
                                    e + events_per_run, len(event_list))]))
                        amplxe_args[-1] = 'event-config=' + ','.join(events)
                        letters = ''.join(letters)
                        for i in range(0, repeats):
                            file_name = outdir + 'buf' + buf + 'batch' + \
                                batch + 'ratio' + r + 'e' + \
                                letters + 'run' + str(i)
                            stdout = open(file_name + '.stdout', 'w')
                            print(app, policy_name, r, buf, batch, i)
                            exe = app
                            if 'dummy2' in app:
                                exe = 'dummy2'
                            elif 'pca' in app:
                                os.environ['MR_CHUNKSIZE'] = '-8'
                            # elif 'linear_regression' in app:
                            #     os.environ['MR_CHUNKSIZE'] = '-32'
                            # elif 'word_count' in app:
                            #     os.environ['MR_CHUNKSIZE'] = '-8'

                            exe_list = amplxe_args + ['-result-dir', file_name] +\
                                ['--', exe_dir + exe] + size
                            # print(exe_list)
                            subprocess.call(exe_list,
                                            stdout=stdout,
                                            stderr=stdout,
                                            env=os.environ.copy())
                            current_sim += 1
                            print('%lf %% is completed' % (100.0 * current_sim /
                                                           total_sims))
