import subprocess
import os
import time
#import signal


print "\nPython simulation\n"

blond_dir = '/afs/cern.ch/work/k/kiliakis/BLonD'
os.environ['PYTHONPATH'] = blond_dir
# os.environ['GOMP_CPU_AFFINITY'] = '0-13 28-41 14-27 42-55'

exe_dir = blond_dir + '/__TEST_CASES/main_files/'

exe_list = ['TC8_Phase_Loop']
#datafiles = '/afs/cern.ch/work/k/kiliakis/workspace/BLonD-minimal-cpp/Release/'
outfiles = '/afs/cern.ch/work/k/kiliakis/results/raw/python/PSB/v1/'

n_particles_list = ['1000000']
#['100000', '500000', '1000000']
n_turns_list = ['1000']
#['10000', '20000', '50000', '100000']
n_slices_list = ['100', '500', '1000', '10000', '20000']
#['100', '200', '500', '1000']
n_threads_list = ['56']
# ['1', '4', '8', '14', '20', '28', '40', '48', '56']


repeats = 4
total_sims = len(n_particles_list) * len(n_turns_list) * \
    len(n_slices_list) * len(n_threads_list) * repeats


os.chdir(exe_dir)

current_sim = 0
for n_particles in n_particles_list:
    os.environ['N_PARTICLES'] = n_particles
    for n_turns in n_turns_list:
        os.environ['N_TURNS'] = n_turns
        for n_slices in n_slices_list:
            os.environ['N_SLICES'] = n_slices
            for n_threads in n_threads_list:
                os.environ['N_THREADS'] = n_threads
                for exe in exe_list:
                    name = exe+'n_p' + n_particles + 'n_t' + n_turns + 'n_s' + \
                        n_slices + 'n_thr' + n_threads
                    if not os.path.exists(outfiles):
                        os.makedirs(outfiles)
                    #res = open(outfiles + name+'.res', 'w')
                    stdout = open(outfiles + name+'.stdout', 'w')
                    for i in range(0, repeats):
                        exe_args = ['python',
                                    exe + '.py'
                                    ]
                        print n_particles, n_turns, n_slices, n_threads, i
                        #start = time.time()
                        subprocess.call(exe_args,
                                        stdout=stdout,
                                        stderr=stdout,
                                        env=os.environ.copy()
                                        )
                        #end = time.time()
                        current_sim += 1
                        #res.write(str(end-start)+'\n')
                        print "%lf %% is completed" % (100.0 * current_sim / total_sims)
