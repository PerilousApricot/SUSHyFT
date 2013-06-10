#! /bin/python

from string import *
import subprocess

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputCfg', metavar='C', type='string', action='store',
                  default='crab_dummy_anashyft_allsys.cfg',
                  dest='inputCfg',
                  help='input config tag to be used')

parser.add_option('--inputCMSSW', metavar='C', type='string', action='store',
                  default='shyftEDAnalyzer_prettyplots.py',
                  dest='inputCMSSW',
                  help='input CMSSW py to be used')

parser.add_option('--outLabel', metavar='L', type='string', action='store',
                  default='_shyftana_387_v4_prettyplots',
                  dest='outLabel',
                  help='output tag to be used')

(options, args) = parser.parse_args()


crabFileStrs = [
['/TTJets_TuneD6T_7TeV-madgraph-tauola/srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4/USER',            15, 0, 'Top', 0],
['/WJetsToLNu_TuneD6T_7TeV-madgraph-tauola/srappocc-shyft_387_v1-9a4f16815707934fe8e1e1334c342e5c/USER',        15, 0, 'Wjets', 0],
['/DYJetsToLL_TuneD6T_M-50_7TeV-madgraph-tauola/srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4/USER',   15, 0, 'Zjets', 0],
## ['/VQQJetsToLL_TuneD6T_7TeV-madgraph-tauola/srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4/USER',       15, 1, 'Vqq', 0],
## ['/VQQJetsToLL_TuneD6T_scaledown_7TeV-madgraph-tauola/srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4/USER',     15, 1, 'Vqq', 1],
## ['/VQQJetsToLL_TuneD6T_scaleup_7TeV-madgraph-tauola/srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4/USER',       15, 1, 'Vqq', 1],
## ['/WJets_TuneD6T_scaledown_7TeV-madgraph-tauola/srappocc-shyft_387_v1-9a4f16815707934fe8e1e1334c342e5c/USER',           80, 1, 'Wjets', 1],
## ['/WJets_TuneD6T_scaleup_7TeV-madgraph-tauola/srappocc-shyft_387_v1-9a4f16815707934fe8e1e1334c342e5c/USER',             80, 1, 'Wjets', 1],
['/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/srappocc-shyft_387_v1-9a4f16815707934fe8e1e1334c342e5c/USER',        15, 0, 'SingleToptW', 1],
['/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4/USER',         15, 0, 'SingleTopT', 1],
['/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4/USER',         15, 0, 'SingleTopS', 1],
##['/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/srappocc-shyft_387_v1-2f94777c47687658400e9bd1c4f72c89/USER',  50, 0, 'QCD', 1],
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
    a6 = a5.replace( 'DUMMY_IGNORETRIGGER', str(crabFileStr[4]) )

    # Dump the contents of the crab config to the screen
    print '------ Config : ------- '
    print a6


    # open the output file
    crabName = 'crab_' + outname + '.cfg'
    fout = open( crabName, 'w')
    # write the text to the output file
    fout.write( a6 )
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

