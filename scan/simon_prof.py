import subprocess
import os
import time
#import signal

print "\nProfiling Simon's simulations\n"

blond_dir = '/afs/cern.ch/work/k/kiliakis/testcases/LEIRTestCase/BLonD/'
#exe = 'TC1_Acceleration.py'
datafiles = '/afs/cern.ch/work/k/kiliakis/testcases/LEIRTestCase/'
outfiles = '/afs/cern.ch/work/k/kiliakis/results/profiling/'

os.chdir(blond_dir)
subprocess.call(['python', 'setup_cpp.py'])
#path=os.getenv('PYTHONPATH')
os.environ['PYTHONPATH'] =  blond_dir


os.chdir(datafiles)

#python -m cProfile -o myscript.cprof myscript.py
stdout = open('PSB.stdout', 'w')

subprocess.call(['python', '-mcProfile', '-oLEIR.cprof','PSBMain.py'],
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

