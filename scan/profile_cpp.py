import subprocess
import os
import time
#import signal


print '\nCpp simulation\n'

# os.environ['GOMP_CPU_AFFINITY'] = '0 28 1 29 2 30 3 31 4 32 5 33 6 34 7 35 8 36 9 37 10 ' + \
#    '38 11 39 12 40 13 41 14 42 15 43 16 44 17 45 18 46 19 47 20 48 21 49 22 50 23 51 24 52 25 53 26 54 27 55'
# os.environ['GOMP_CPU_AFFINITY'] = '0-13 28-41 14-27 42-55'
os.environ['GOMP_CPU_AFFINITY'] = '0-55'

blond_dir = '/afs/cern.ch/work/k/kiliakis/git/BLonD-minimal-cpp/'
exe_dir = blond_dir + 'build/'
exe_list = ['TC8_Phase_Loop']
#datafiles = '/afs/cern.ch/work/k/kiliakis/workspace/BLonD-minimal-cpp/Release/'
outfiles = '/afs/cern.ch/work/k/kiliakis/results/raw/cpp/PSB/v3/'

n_particles_list = ['1000000']
#['100000', '500000', '1000000']
n_turns_list = ['1000']
#['10000', '20000', '50000', '100000']
n_slices_list = ['100', '1000', '10000']
#['100', '200', '500', '1000']
n_threads_list = ['1', '4', '8', '14', '20', '28', '40', '48', '56']


repeats = 4
total_sims = len(n_particles_list) * len(n_turns_list) * \
    len(n_slices_list) * len(n_threads_list) * len(exe_list) * repeats


os.chdir(exe_dir)

current_sim = 0
for n_particles in n_particles_list:
    #os.environ['N_PARTICLES'] = n_particles
    for n_turns in n_turns_list:
        #os.environ['N_TURNS'] = n_turns
        for n_slices in n_slices_list:
            #os.environ['N_SLICES'] = n_slices
            for n_threads in n_threads_list:
                for exe in exe_list:
                    #os.environ['N_THREADS'] = n_threads
                    name = exe+'n_p' + n_particles + 'n_t' + n_turns + \
                        'n_s' + n_slices + 'n_thr' + n_threads
                    if not os.path.exists(outfiles):
                        os.makedirs(outfiles)
                    #res = open(outfiles + name+'.res', 'w')
                    stdout = open(outfiles + name+'.stdout', 'w')
                    for i in range(0, repeats):
                        exe_args = [
                            # 'valgrind',
                            # '--tool=callgrind',
                            # '--dump-instr=yes',
                            # '--trace-jump=yes',
                            # '--cache-sim=yes',
                            # '--callgrind-out-file=' +
                            # outfiles+name+'.prof',
                            './'+exe,
                            '-p' + n_particles,
                            '-t' + n_turns,
                            '-s' + n_slices,
                            '-m' + n_threads
                        ]
                        print exe, n_particles, n_turns, n_slices, n_threads, i
                        #start = time.time()
                        subprocess.call(exe_args,
                                        stdout=stdout,
                                        stderr=stdout
                                        )
                        #end = time.time()
                        current_sim += 1
                        # res.write(str(end-start)+'\n')
                        print "%lf %% completed" % (100.0 * current_sim / total_sims)
