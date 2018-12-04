import subprocess
import os
import time
#import signal

print "\nPython simulation\n"

blond_dir = '/afs/cern.ch/work/k/kiliakis/BLonD-original'
exe_dir = blond_dir + '/__TEST_CASES/main_files/'
# exe_dir = '/afs/cern.ch/work/k/kiliakis/testcases/htimko/LHC/re_3b_extremes_batch/'
# exe = '_LHC_acc.py'
# exe_list = ['TC1_Acceleration.py', 'TC5_Wake_impedance.py']
exe_list = ['TC5_Wake_impedance.py']
#datafiles = '/afs/cern.ch/work/k/kiliakis/workspace/BLonD-minimal-python/__TEST_CASES/main_files/'
# outfiles = '/afs/cern.ch/work/k/kiliakis/results/raw/python/_LHC_acc/for-slides/'
outfiles = '/afs/cern.ch/work/k/kiliakis/results/raw/python/for-slides/'

#os.chdir(blond_dir)
#subprocess.call(['python', 'setup_cpp.py'])


n_particles_list = ['500000']
n_turns_list = ['20000']
#['10000', '20000', '50000', '100000']
n_slices_list = ['256']
#['100', '200', '500', '1000']
n_threads_list = ['1', '4', '8', '14', '20', '28', '42', '56']
# n_threads_list = ['14', '20', '28', '42', '56']
repeats = 1
os.chdir(exe_dir)

total_sims = len(n_particles_list) * len(n_turns_list) * \
    len(n_slices_list) * len(n_threads_list) * len(exe_list) * repeats

current_sim = 0
os.environ['PYTHONPATH'] = blond_dir
for exe in exe_list:
    for n_particles in n_particles_list:
        os.environ['N_PARTICLES'] = n_particles
        for n_turns in n_turns_list:
            os.environ['N_TURNS'] = n_turns
            for n_slices in n_slices_list:
                os.environ['N_SLICES'] = n_slices
                for n_threads in n_threads_list:
                    os.environ['N_THREADS'] = n_threads
                    os.environ['OMP_NUM_THREADS'] = n_threads
                    name = 'n_p' + n_particles + 'n_t' + n_turns + 'n_s' + \
                        n_slices + 'n_thr' + n_threads
                    if not os.path.exists(outfiles + exe + '/'):
                        os.makedirs(outfiles + exe + '/')
                    #res = open(outfiles + name+'.res', 'w')
                    stdout = open(outfiles + exe + '/' + name+'.stdout', 'w')
                    for i in range(0, repeats):
                        print n_particles, n_turns, n_slices, n_threads, i
                        #start = time.time()
                        subprocess.call(['python', exe],
                                        stdout=stdout,
                                        stderr=stdout,
                                        env=os.environ.copy()
                                        )
                        #end = time.time()
                        current_sim += 1
                        #res.write(str(end-start)+'\n')
                        print "%lf %% is completed" % (100.0 * current_sim / total_sims)

