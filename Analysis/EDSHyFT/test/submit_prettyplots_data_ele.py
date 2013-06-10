#! /bin/python

from string import *
import subprocess

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputCfg', metavar='C', type='string', action='store',
                  default='crab_dummy_anashyft_data.cfg',
                  dest='inputCfg',
                  help='input config tag to be used')

parser.add_option('--inputCMSSW', metavar='C', type='string', action='store',
                  default='shyftEDAnalyzer_prettyplots_data_ele.py',
                  dest='inputCMSSW',
                  help='input CMSSW py to be used')

parser.add_option('--outLabel', metavar='L', type='string', action='store',
                  default='_shyftana_387_v4_prettyplots',
                  dest='outLabel',
                  help='output tag to be used')

(options, args) = parser.parse_args()


crabFileStrs = [
['/EG/skhalil-Run2010A-Nov4ReReco_135821to139980_shyft_387_v1-a4be05aebb80039c1242697b9afc0270/USER',       10, 0, 'data', 0, 'HLT_Ele10_LW_L1R'],   
['/EG/skhalil-Run2010A-Nov4ReReco_140058to143962_shyft_387_v1-8eebe5049fea5334352bacc0b041e3da/USER',       20, 0, 'data', 0, 'HLT_Ele15_SW_L1R'],
['/EG/skhalil-Run2010A-Nov4ReReco_144010to144114_shyft_387_v1-7a3bb29e2c6856bcccbb636170c4af7d/USER',       20, 0, 'data', 0, 'HLT_Ele15_SW_CaloEleId_L1R'],
['/Electron/skhalil-Run2010B-Nov4ReReco_146428to147116_shyft_387_v1-ece428603ab6a4df794bc7cec474f8f5/USER', 20, 0, 'data', 0, 'HLT_Ele17_SW_CaloEleId_L1R'],
['/Electron/skhalil-Run2010B-Nov4ReReco_147196to148058_shyft_387_v1-6972ed86d39f1862f7c0481864fa398d/USER', 20, 0, 'data', 0, 'HLT_Ele17_SW_TightEleId_L1R'],
['/Electron/skhalil-Run2010B-Nov4ReReco_148819to149063_shyft_387_v1-34867acba19f8e4efd85e03a183a4b00/USER', 20, 0, 'data', 0, 'HLT_Ele22_SW_TighterEleId_L1R_v2'],
['/Electron/skhalil-Run2010B-Nov4ReReco_149181to149442_shyft_387_v1-3ea0376194d6ff8faf5a3ccff3084893/USER', 20, 0, 'data', 0, 'HLT_Ele22_SW_TighterEleId_L1R_v3'],
    ]

for crabFileStr in crabFileStrs :
    print '------------------------- Operating on sample ' + crabFileStr[0] + ' ---------------------------'
    f = open(options.inputCfg, 'r')
    instring = f.read()

    # Get the dataset name, without the user-level stuff
    baseList = crabFileStr[0].split('/')
    runList  = crabFileStr[0].split('_')
    # baseList contains, e.g. ['', 'TTJets_TuneD6T_7TeV-madgraph-tauola', 'srappocc-shyft_387_v1-806866a699de2045917e2f88bbb597f4', 'USER']
    # so we want baseList[1]
    outname = baseList[1] + '_' + runList[1] + options.outLabel
    outlocation = '/uscms_data/d2/skhalil/ShyftTemplates3/'+outname
    # now do all of the substitutions
    a0 = instring.replace( 'DUMMY_DATASET', crabFileStr[0] )
    a1 = a0.replace( 'DUMMY_UI_DIR', outlocation)
    a2 = a1.replace( 'DUMMY_NJOBS', str(crabFileStr[1]) )    
    a3 = a2.replace( 'DUMMY_CMSSW', options.inputCMSSW )
    a4 = a3.replace( 'DUMMY_USEFLAVORHISTORY', str(crabFileStr[2]) )
    a5 = a4.replace( 'DUMMY_SAMPLENAMEINPUT', crabFileStr[3] )
    a6 = a5.replace( 'DUMMY_IGNORETRIGGER', str(crabFileStr[4]) )
    a7 = a6.replace( 'DUMMY_TRIGGER', str(crabFileStr[5]))

    # Dump the contents of the crab config to the screen
    print '------ Config : ------- '
    print a7


    # open the output file
    crabName = 'crab_' + outname + '.cfg'
    fout = open( crabName, 'w')
    # write the text to the output file
    fout.write( a7 )
    fout.close()
    print '------ CRAB starting up! ------'
    # now create the job:
    #s = 'crab -create -cfg ' + crabName
    #print s
    # and submit:
    #subprocess.call( [s], shell=True )
    #s = 'crab -submit -c ' + outlocation
    #print s
    #subprocess.call( [s], shell=True )

