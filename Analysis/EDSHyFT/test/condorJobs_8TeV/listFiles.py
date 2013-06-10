#!/usr/bin/python

import sys
import os, re
from optparse import OptionParser


def make_filenamelist(inputDir):
    if not os.path.isdir(inputDir):
        print ('%s is not a directory'%(inputDir))
        sys.exit(1)

    filenamelist = []
    for filename in os.listdir(inputDir):
        if not os.path.isfile(os.path.join(inputDir,filename)):
            continue
        filenamelist.append(filename)

    return filenamelist


def process_input_dir(inputDir, filelist):
    inputDir = inputDir.rstrip('/')+'/'
    filenamelist = make_filenamelist(inputDir)

    path = inputDir;
    name = ''
    jobdict = {}

    for filename in filenamelist:
        if( not re.search('.root$', filename) ):
            continue
        m1 = re.search('_\d+_\d+_\w+.root', filename)
        if name=='':
            name = re.split('_\d+_\d+_\w+.root', filename)[0]
        jobstring = filename[m1.start():].lstrip('_').replace('.root','').split('_')
        job = int(jobstring[0])
        if job not in jobdict.keys():
            jobdict[job] = []
            jobdict[job].append([int(jobstring[1])])
            jobdict[job].append([jobstring[2]])
        else:
            jobdict[job][0].append(int(jobstring[1]))
            jobdict[job][1].append(jobstring[2])

    jobs = jobdict.keys()
    if( len(jobs)==0 ):
        print 'No .root files found'
        sys.exit()

    jobs.sort()
    for job in jobs:
        maxsub = max(jobdict[job][0])
        filename = (path+name+'_%i_%i_%s.root')%(job, maxsub, jobdict[job][1][jobdict[job][0].index(maxsub)])
        filelist.append(filename)

    return


def main():

  parser = OptionParser()

  parser.add_option('--path', metavar='F', type='string', action='store',
                    default = '/pnfs/cms/WAX/11/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-650_TuneZ2star_8TeV-madgraph/BPrimeEDMNtuples_53x_v1_sv1/492787f5dd5ca403ce99ce9536ef4dbc',
                    dest='path',
                    help='Input path')

  parser.add_option('--outputText', metavar='F', type='string', action='store',
                    default = "outputText",
                    dest='outputText',
                    help='output file')

  # Parse and get arguments
  (options, args) = parser.parse_args()

  #path = sys.argv[1]
  path = options.path
  textName = options.outputText

  f = open(textName+'.txt', 'w')

  filelist = []
  process_input_dir(path, filelist)

  for i in filelist:
      #print i
      f.write(i+'\n')


if __name__ == '__main__':
    main()
