#! /bin/python

from string import *
import subprocess

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputCfg', metavar='C', type='string', action='store',
                  default='crab_dummy_anashyft_simplesys.cfg',
                  dest='inputCfg',
                  help='input config tag to be used')

parser.add_option('--inputCMSSW', metavar='C', type='string', action='store',
                  default='shyftEDAnalyzer_allsys.py',
                  dest='inputCMSSW',
                  help='input CMSSW py to be used')

parser.add_option('--outLabel', metavar='L', type='string', action='store',
                  default='_shyftana_387_v1_simplesys',
                  dest='outLabel',
                  help='output tag to be used')

(options, args) = parser.parse_args()


crabFileStrs = [
['/VQQJetsToLL_TuneD6T_scaleup_7TeV-madgraph-tauola/srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4/USER',   15, 1, 'Vqq'],
['/VQQJetsToLL_TuneD6T_scaledown_7TeV-madgraph-tauola/srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4/USER', 15, 1, 'Vqq'],
['/TTJets_TuneD6T_7TeV-madgraph-tauola/srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4/USER',            15, 0, 'Top'],
['/TTJets_TuneZ2_7TeV-madgraph-tauola/srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4/USER',                 15, 0, 'Top'],
['/TTJets_TuneD6T_smallerISRFSR_7TeV-madgraph-tauola/srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4/USER',  15, 0, 'Top'],
['/TTJets_TuneD6T_scaleup_7TeV-madgraph-tauola/srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4/USER',        15, 0, 'Top'],
['/TTJets_TuneD6T_scaledown_7TeV-madgraph-tauola/srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4/USER',      15, 0, 'Top'],
['/TTJets_TuneD6T_matchingup_7TeV-madgraph-tauola/srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4/USER',     15, 0, 'Top'],
['/TTJets_TuneD6T_matchingdown_7TeV-madgraph-tauola/srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4/USER',   15, 0, 'Top'],
['/TTJets_TuneD6T_largerISRFSR_7TeV-madgraph-tauola/srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4/USER',   15, 0, 'Top'],
    ]

for crabFileStr in crabFileStrs :
    print '------------------------- Operating on sample ' + crabFileStr[0] + ' ---------------------------'
    f = open(options.inputCfg, 'r')
    instring = f.read()

    # Get the dataset name, without the user-level stuff
    baseList = crabFileStr[0].split('/')

    # baseList contains, e.g. ['', 'TTJets_TuneD6T_7TeV-madgraph-tauola', 'srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4', 'USER']
    # so we want baseList[1]
    outname = baseList[1] + options.outLabel
    # now do all of the substitutions
    a0 = instring.replace( 'DUMMY_DATASET', crabFileStr[0] )
    a1 = a0.replace( 'DUMMY_UI_DIR', outname)
    a2 = a1.replace( 'DUMMY_NJOBS', str(crabFileStr[1]) )    
    a3 = a2.replace( 'DUMMY_CMSSW', options.inputCMSSW )
    a4 = a3.replace( 'DUMMY_USEFLAVORHISTORY', str(crabFileStr[2]) )
    a5 = a4.replace( 'DUMMY_SAMPLENAMEINPUT', crabFileStr[3] )

    # Dump the contents of the crab config to the screen
    print '------ Config : ------- '
    print a5


    # open the output file
    crabName = 'crab_' + outname + '.cfg'
    fout = open( crabName, 'w')
    # write the text to the output file
    fout.write( a5 )
    fout.close()
    print '------ CRAB starting up! ------'
    # now create the job:
    s = 'crab -create -cfg ' + crabName
    print s
    # and submit:
    subprocess.call( [s], shell=True )
    s = 'crab -submit -c ' + outname
    print s
    subprocess.call( [s], shell=True )

