#!/usr/bin/env python

import Datasets2012
import subprocess
import json

datasetInfo = Datasets2012.getInputPAT()
fileDict = {}
for filesetName in datasetInfo['datasetNames'].values():
    cmdLine = './das.py --query="file dataset=%s" --limit=0' % filesetName
    print "Examining %s" % filesetName
    print "  cmdline: %s" % cmdLine
    subproc = subprocess.Popen( \
                args=cmdLine,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
    fileout, err = subproc.communicate()
    print "  stderr: %s" % err

    fileDict[filesetName] = []
    for line in fileout.splitlines():
        fileDict[filesetName].append(line)

fh = open('fileList.json', 'w')
fh.write( json.dumps( fileDict ) )
fh.close()

