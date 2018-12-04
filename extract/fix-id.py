#!/usr/bin/python
import os
import sys


def fix_id(input):
    output = os.path.dirname(input)
    file = open(input, 'r')
    f = open('foo', 'w')
    for line in file:
        if float(line) > 0:
            f.write('1\n')
        else:
            f.write('0\n')
    os.rename('foo', input)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "You should specify input file"
        exit(-1)
    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        print 'Error: '+input_file+': No such file'
        exit(-1)
    fix_id(input_file)