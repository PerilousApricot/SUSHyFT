#!/usr/bin/env python

import sys, os, subprocess, shutil, string, re
from optparse import OptionParser


def main():
  # usage description
  usage = "Usage: cleanUpCrabOutput.py [options] \nExample: ./cleanUpCrabOutput.py -w CRAB_Jobs"

  # input parameters
  parser = OptionParser(usage=usage)

  parser.add_option("-w", "--main_workdir", dest="main_workdir",
                    help="Main working directory",
                    metavar="MAIN_WORKDIR")

  (options, args) = parser.parse_args()

  # make sure all necessary input parameters are provided
  if not options.main_workdir:
    print usage
    sys.exit()

  main_workdir = options.main_workdir

  # redefine main_workdir as an absolute path (if not defined in such form already)
  if not re.search("^/", main_workdir):
    main_workdir = os.path.join(os.getcwd(),main_workdir)

  # open and read the dataset_list file
  dataset_list_file = open(os.path.join(main_workdir,'datasetList.txt'),'r')
  dataset_list_lines = dataset_list_file.readlines()

  print 'Starting cleanup...'

  # loop over datasets
  for line in dataset_list_lines:
   
    line_elements = line.split()
    if (len(line_elements)==0 or line_elements[0][0]=='#'): continue

    workdir = line_elements[0].lstrip('/').replace('/','__')
    print 'Removing ' + workdir

    # delete subdirectories inside the working directory
    cmd = 'rm -rf ' + os.path.join(main_workdir,workdir)
    proc = subprocess.Popen( cmd, shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
    output = proc.communicate()[0]
    if proc.returncode != 0:
      print output
      sys.exit(1)

  print 'Done'


if __name__ == "__main__":
  main()

