#!/usr/bin/python
import os
import sys


def extract(input):
    output = os.path.dirname(input)
    #os.chdir(directory)
    file = open(input)
    #name = input.split('/')[-1]
    #name = name.split('.')[0]
    #if not os.path.exists(output):
    #    os.makedirs(output)
    #print output
    f = open('.foo', 'w')
    param_prev = ''
    for line in file:
        if ':' not in line:
            continue
        param_cur = line.split(':')[0]
        num = line.split(':')[1].strip()
        if(param_cur != param_prev):
            f.close()
            f = open(os.path.join(output, param_cur+'.txt'), 'w')
        param_prev = param_cur
        f.write(num + '\n')
    os.remove('.foo')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "You should specify input file"
        exit(-1)
    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        print 'Error: '+input_file+': No such file'
        exit(-1)
    extract(input_file)