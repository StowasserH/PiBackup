#!/usr/bin/env python

import sys
from pibackup import PiBackup


def main():
    args = sys.argv[1:]

#    print('count of args :: {}'.format(len(args)))
#    for arg in args:
#        print('passed argument :: {}'.format(arg))
    bkup=PiBackup()
    bkup.do_backup()

#    print "done."

if __name__ == '__main__':
    main()