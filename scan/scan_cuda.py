import subprocess
import os
import time
#import signal


print '\nCuda simulation\n'

#os.environ['GOMP_CPU_AFFINITY'] = '0 28 1 29 2 30 3 31 4 32 5 33 6 34 7 35 8 36 9 37 10 ' + \
#    '38 11 39 12 40 13 41 14 42 15 43 16 44 17 45 18 46 19 47 20 48 21 49 22 50 23 51 24 52 25 53 26 54 27 55'

blond_dir = '/afs/cern.ch/work/k/kiliakis/git/cuda-benchmark/BLonD++/'
exe_dir = blond_dir + 'build/'
exe = './TC5_Wake_impedance_frequency'
#datafiles = '/afs/cern.ch/work/k/kiliakis/workspace/BLonD-minimal-cpp/Release/'
outfiles = '/afs/cern.ch/work/k/kiliakis/results/raw/cuda/TC5_freq/thread-scalability/v1/'

n_particles_list = ['1000']#, '1000000']
#['100000', '500000', '1000000']
n_turns_list = ['10000']
#['10000', '20000', '50000', '100000']
n_slices_list = ['256']
#['100', '200', '500', '1000']
n_threads_list = ['1']#, '2', '4', '8', '10', '14', '18', '22', '28', '32', '56']
repeats = 5

total_sims = len(n_particles_list) * len(n_turns_list) * \
    len(n_slices_list) * len(n_threads_list) * repeats

os.chdir(exe_dir)

current_sim = 0
for n_particles in n_particles_list:
    for n_turns in n_turns_list:
        for n_slices in n_slices_list:
            for n_threads in n_threads_list:
                name = 'n_p' + n_particles + 'n_t' + n_turns + 'n_s' + \
                    n_slices + 'n_thr' + n_threads
                if not os.path.exists(outfiles):
                    os.makedirs(outfiles)
                #res = open(outfiles + name+'.res', 'w')
                stdout = open(outfiles + name+'.stdout', 'w')
                for i in range(0, repeats):
                    exe_list = [exe,
                                '-p' + n_particles,
                                '-t' + n_turns,
                                '-s' + n_slices,
                                '-m' + n_threads
                                ]
                    print n_particles, n_turns, n_slices, n_threads, i
                    #start = time.time()
                    subprocess.call(exe_list,
                                    stdout=stdout,
                                    stderr=stdout
                                    )
                    #end = time.time()
                    current_sim += 1
                    #res.write(str(end-start)+'\n')
                    print "%lf %% is completed" % (100.0 * current_sim / total_sims)
