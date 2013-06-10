#!/usr/bin/env python

import Datasets2012
import subprocess
import json
import os, sys, os.path
from optparse import OptionParser

parser = OptionParser()

parser.add_option("--input", type='string', action='store',
                  default='fileList.json',
                  dest='inputFile',
                  help='File to convert to bare text files')

parser.add_option("--destDir", type='string', action='store',
                  default='fileList',
                  dest='destDir',
                  help='What directory to place these files')

parser.add_option('--prefix', type='string', action='store',
                  default='root://xrootd.unl.edu/',
                  dest='prefix',
                  help="Prefix for the LFNs (useful for xrootd)")

(options, args) = parser.parse_args()


if not os.path.exists( options.destDir ):
    os.mkdir( options.destDir )

fileDict = json.loads( open(options.inputFile, 'r').read() )
for dataset in fileDict.keys():
    print "Looking at dataset %s (%s vals)" % (dataset, len(fileDict[dataset]))
    targetName = os.path.join( options.destDir, 
                               dataset[1:].replace('/', '_') + ".txt" )
    fh = open( targetName, 'w' )
    
    for line in fileDict[dataset]:
        fh.write("%s%s\n" % ( options.prefix, line ) )

    fh.close()

