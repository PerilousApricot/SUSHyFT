#! /bin/python

from string import *
import subprocess

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputCfg', metavar='C', type='string', action='store',
                  default='crab_dummy.cfg',
                  dest='inputCfg',
                  help='input config tag to be used')

parser.add_option('--inputCMSSW', metavar='C', type='string', action='store',
                  default='shyft.py',
                  dest='inputCMSSW',
                  help='input CMSSW py to be used')

parser.add_option('--outLabel', metavar='L', type='string', action='store',
                  default='shyft_414_v1',
                  dest='outLabel',
                  help='output tag to be used')



(options, args) = parser.parse_args()


crabFileStrs = [
#['/SingleMu/Run2011A-PromptReco-v1/AOD',                                                'condor', 0, 400, 1, 'HLT'        ],
#['/SingleElectron/Run2011A-PromptReco-v1/AOD',                                          'condor', 0, 400, 1, 'HLT'        ],
['/WJetsToLNu_TuneD6T_7TeV-madgraph-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM',      'condor', 0, 50,  0, 'REDIGI311X' ],
['/DYJetsToLL_TuneD6T_M-50_7TeV-madgraph-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM', 'condor', 0, 50,  0, 'REDIGI311X'],
['/TTJets_TuneD6T_7TeV-madgraph-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM',          'condor', 0, 50,  0, 'REDIGI311X' ],
['/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph/Spring11-PU_S1_START311_V1G1-v1/AODSIM',      'condor', 0, 50,  0, 'REDIGI311X' ],
['/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/Spring11-PU_S1_START311_V1G1-v1/AODSIM',       'condor', 0, 50,  0, 'REDIGI311X' ],
['/TToBLNu_TuneZ2_t-channel_7TeV-madgraph/Spring11-PU_S1_START311_V1G1-v1/AODSIM',       'condor', 0, 50,  0, 'REDIGI311X' ],

    ]

for crabFileStr in crabFileStrs :
    print '------------------------- Operating on sample ' + crabFileStr[0] + ' ---------------------------'
    f = open(options.inputCfg, 'r')
    instring = f.read()

    # Get the dataset name, without the user-level stuff
    baseList = crabFileStr[0].split('/')
    outname = baseList[1] + '_' + baseList[2] + '_' + options.outLabel
    outlocation = '/uscms_data/d2/skhalil/ShyftCrab2011/'+outname
    # now do all of the substitutions
    
    a0 = instring.replace( 'DUMMY_DATASET',    crabFileStr[0]      )
    a1 = a0.replace(       'DUMMY_SCHEDULER',  crabFileStr[1]      )
    a2 = a1.replace(       'DUMMY_USE_SERVER', str(crabFileStr[2]) )
    a3 = a2.replace(       'DUMMY_CMSSW',      options.inputCMSSW  )
    a4 = a3.replace(       'DUMMY_NJOBS',      str(crabFileStr[3]) )
    a5 = a4.replace(       'DUMMY_YES_DATA',   str(crabFileStr[4]) )
    a6 = a5.replace(       'DUMMY_OUTDIR',     options.outLabel    )        
    a7 = a6.replace(       'DUMMY_UI_DIR',     outlocation         )
    a8 = a7.replace(       'DUMMY_HLT',        crabFileStr[5]      )

    if  str(crabFileStr[4]) == '1':
        a9 = a8.replace( 'total_number_of_events', 'total_number_of_lumis')
    
    else:
        a9 = a8.replace( 'lumi_mask=json_DCSONLY.txt', '')

    # Dump the contents of the crab config to the screen
    print '------ Config : ------- '
    print a9


    # open the output file
    crabName = 'crab_' + outname + '.cfg'
    fout = open( crabName, 'w')
    # write the text to the output file
    fout.write( a9 )
    fout.close()
    print '------ CRAB starting up! ------'
    # now create the job:
    s = 'crab -create -cfg ' + crabName
    print s
    # and submit:
    subprocess.call( [s], shell=True )
    s = 'crab -submit -c ' + outlocation
    print s
    subprocess.call( [s], shell=True )

