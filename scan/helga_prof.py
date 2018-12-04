import subprocess
import os
import time
#import signal

print "\nProfiling Helga's simulations\n"

blond_dir = '/afs/cern.ch/work/k/kiliakis/BLonD'
#exe = 'TC1_Acceleration.py'
datafiles = '/afs/cern.ch/work/k/kiliakis/testcases/synchroLoop/'
outfiles = '/afs/cern.ch/work/k/kiliakis/results/LHC_restart'

#os.chdir(blond_dir)
#subprocess.call(['python', 'setup_cpp.py'])
#path=os.getenv('PYTHONPATH')
os.environ['PYTHONPATH'] =  blond_dir


os.chdir(datafiles)

#python -m cProfile -o myscript.cprof myscript.py
stdout = open('LHC_restart.stdout', 'w')

'''subprocess.call(['python', '-mcProfile', '-oLHC_acc.cprof','_LHC_acc.py'],
                                 stdout=stdout,
                                 stderr=stdout,
                                 env=os.environ.copy()
                                 )
'''

subprocess.call(['python','_LHC_acc_restart.py'],
                                 stdout=stdout,
                                 stderr=stdout,
                                 env=os.environ.copy()
                                 )


'''
os.chdir(datafiles+'PS-SPS')

stdout = open('PS-SPS.stdout', 'w')

subprocess.call(['python', '-mcProfile', '-oPS-SPS.cprof','_PS-SPS_transfer.py'],
                                 stdout=stdout,
                                 stderr=stdout,
                                 env=os.environ.copy()
                                 )


'''

