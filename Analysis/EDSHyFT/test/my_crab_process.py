#!/bin/python

import subprocess
import sys
import glob


from optparse import OptionParser


parser = OptionParser()

parser.add_option('--files', metavar='F', type='string', action='store',
                  dest='files',
                  help='Input files')

parser.add_option('--command', metavar = 'C', type='string', action='store',
                  dest='command',
                  default='status',
                  help='CRAB command to run')

(options, args) = parser.parse_args()


argv = []

dirs = glob.glob( options.files )

for idir in dirs :
    print '--------------------------------'
    print '--------------------------------'
    print '--------------------------------'    
    s = "crab -" + options.command + " -c " + idir
    print s
    subprocess.call( [s, ""], shell=True )
