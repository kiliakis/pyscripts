import subprocess
import os

apps = ['kmeans',
        'histogram',
        'pca',
        'linear_regression',
        'word_count']

datafiles = '/afs/cern.ch/work/k/kiliakis/git/custom-phoenix/testcases/'

testcases = {
    'word_count': [datafiles + 'word_count_datafiles/word_100MB.txt'],
    #'mr_matrix_multiply' : ['1000', '1'],
    #'string_match' : [datafiles + 'string_match_datafiles/key_file_1000MB.txt'],
    'histogram': [datafiles + 'histogram_datafiles/small.bmp'],
    'linear_regression': [datafiles + 'linear_regression_datafiles/key_file_100MB.txt'],
    'kmeans': ['-d3', '-c100', '-p10000'],
    'pca': ['-r1000', '-c1000']
}

os.chdir('../debug/')
for app, size in testcases.items():
    exe_list = ['valgrind',
                '--tool=callgrind',
                '--callgrind-out-file='+app+'.prof',
                './'+app] + size
    subprocess.call(exe_list)

