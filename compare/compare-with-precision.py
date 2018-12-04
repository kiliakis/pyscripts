#!/usr/bin/python

import sys
import re


def hasNumber(string):
    return re.findall(r'[-+]?\d*\.\d+(?:[Ee][-+]?\d+)?|\d+(?:[Ee][-+]?\d+)?', string)


def check_precision(f1, f2, prec):
    errors = 0
    file1 = open(f1)
    file2 = open(f2)
    stderr = open('errors.txt', 'w')
    for l1, l2 in zip(file1, file2):
        # skipe empty lines
        while (not l1):
            l1 = f1.next()
        while (not l2):
            l2 = f2.next()
        list1 = hasNumber(l1)
        list2 = hasNumber(l2)
        #print list1, list2
        if(list1 or list2):
            for x, y in zip(list1, list2):
                dif = abs(float(x) - float(y))
                if dif > prec * max(abs(float(x)), abs(float(y))):
                    errors += 1
                    stderr.write(l1+l2)
                    #stderr.write(x + '\t' + y + '\t' + str(dif) + '\n')
                #else:
                    #print dif / 0
        else:
            if(l1 != l2):
                "Error:\nl1:%sl2:%s" % (l1, l2)
    print "%d Errors found" % errors


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "You should specify two input files to " + \
            "compare and a float for the precision"
        exit(-1)
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    prec = float(sys.argv[3])
    check_precision(f1, f2, prec)
