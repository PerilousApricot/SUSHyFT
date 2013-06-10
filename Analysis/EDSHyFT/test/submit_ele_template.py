#! /bin/python

from string import *
import subprocess

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputCfg', metavar='C', type='string', action='store',
                  default='crab_dummy_anashyft_ele.cfg',
                  dest='inputCfg',
                  help='input config tag to be used')

parser.add_option('--outLabel', metavar='L', type='string', action='store',
                  default='_ttbsm_424_v9',
                  dest='outLabel',
                  help='output tag to be used')

parser.add_option('--outLocation', metavar='L', type='string', action='store',
                  default='/uscms_data/d2/skhalil/ShyftTemplates13/',
                  dest='outLocation',
                  help='output location to create the crab directories')

parser.add_option('--data', metavar='D', type='int', action='store',
                  default = '0',
                  dest='data',
                  help='submit data jobs')

## parser.add_option('--summer11MC', metavar='M', type='int', action='store',
##                   default = '0',
##                   dest='summer11MC',
##                   help='submit summer 11 jobs')

## parser.add_option('--eleEtCut', metavar='EC', type='float', action='store',
##                   default = '35.0',
##                   dest='eleEtCut',
##                   help='electron Et threshold')

(options, args) = parser.parse_args()


##eleEt  = options.eleEtCut

if options.data == 1:
   inputCMSSW = 'shyftEDAnalyzer_ele.py'
   outputLable = '_tlbsm_424_v9'
   crabFileStrs = [
      ['/SingleElectron/vasquez-ttbsm_v9_Run2011A-May10ReReco-f8e845a0332c56398831da6c30999af1/USER', 60, 0, 'Data', 0,
       'HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v1', '160431-161176', 'P1', 'Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.txt'],
      
      ]
elif options.data == 0:
   inputCMSSW = 'shyftEDAnalyzer_allsys_ele.py'
   outputLable = '_tlbsm_424_v9'
   crabFileStrs = [
      ##       ## Background central samples
      ['/TTJets_TuneZ2_7TeV-madgraph-tauola/srappocc-ttbsm_v9_Summer11-PU_S4_START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',  80, 0, 'Top',           1],
      ['/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/dstrom-prod_2011_10_05_17_14_11-bf57a985b107a689982b667a3f2f23c7/USER',              50, 0, 'Wjets',         1],
      ['/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/samvel-prod_2011_10_04_10_32_11-bf57a985b107a689982b667a3f2f23c7/USER',         40, 0, 'Zjets',         1],
      ['/T_TuneZ2_t-channel_7TeV-powheg-tauola/samvel-prod_2011_10_03_17_24_02-bf57a985b107a689982b667a3f2f23c7/USER',               40, 0, 'SingleTopT',    1],
      ['/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/samvel-prod_2011_10_03_17_25_57-bf57a985b107a689982b667a3f2f23c7/USER',            40, 0, 'SingleTopbarT', 1],
      ['/T_TuneZ2_s-channel_7TeV-powheg-tauola/samvel-prod_2011_10_03_17_19_46-bf57a985b107a689982b667a3f2f23c7/USER',               40, 0, 'SingleTopS',    1],
      ['/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/samvel-prod_2011_10_03_17_22_26-bf57a985b107a689982b667a3f2f23c7/USER',            40, 0, 'SingleTopbarS', 1],
      ['/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/samvel-prod_2011_10_03_17_15_48-bf57a985b107a689982b667a3f2f23c7/USER',           40, 0, 'SingleToptW',   1],
      ['/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/samvel-prod_2011_10_03_17_18_26-bf57a985b107a689982b667a3f2f23c7/USER',        40, 0, 'SingleTopbartW',1],
      ['/GJets_TuneZ2_40_HT_100_7TeV-madgraph/skhalil-ttbsm_v9_Summer11-PU_S4_START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',                             25, 1, 'PhoJet40100',   1],
      ['/GJets_TuneZ2_100_HT_200_7TeV-madgraph/skhalil-ttbsm_v9_Summer11-PU_S4_START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',                            25, 1, 'PhoJet100200',  1],
      ['/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/skhalil-ttbsm_v9_Summer11-PU_S4_START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',                            25, 1, 'PhoJet200Inf',  1],
      ['/QCD_Pt-20to30_BCtoE_TuneZ2_7TeV-pythia6/samvel-prod_2011_10_02_09_36_51-bf57a985b107a689982b667a3f2f23c7/USER',                                         40, 1, 'BCtoE2030',     1],
      ['/QCD_Pt-30to80_BCtoE_TuneZ2_7TeV-pythia6/samvel-prod_2011_10_02_09_39_46-bf57a985b107a689982b667a3f2f23c7/USER',                                         40, 1, 'BCtoE3080',     1],
      ['/QCD_Pt-80to170_BCtoE_TuneZ2_7TeV-pythia/samvel-prod_2011_10_02_09_41_02-bf57a985b107a689982b667a3f2f23c7/USER',                                         40, 1, 'BCtoE80170',    1],
      ['/QCD_Pt-20to30_EMEnriched_TuneZ2_7TeV-pythia6/samvel-tlbsm_v9_Summer11-PU_S4_START42_V11-v1_2011_10_07_15_34_09-bf57a985b107a689982b667a3f2f23c7/USER',  40, 1, 'EMEn2030',      1],
      ['/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia/samvel-ltbsm_v9_Summer11-PU_S4_START42_V11-v1_2011_10_07_12_56_15-bf57a985b107a689982b667a3f2f23c7/USER',   40, 1, 'EMEn3080',      1],
      ['/QCD_Pt-80to170_EMEnriched_TuneZ2_7TeV-pythia6/samvel-tlbsm_v9_Summer11-PU_S4_START42_V11-v1_2011_10_07_16_06_41-bf57a985b107a689982b667a3f2f23c7/USER', 40, 1, 'EMEn80170',     1],

##       ## systematic samples
      ['/TTjets_TuneZ2_scaledown_7TeV-madgraph-tauola/weizou-ttbsm_v9_Summer11-PU_S4_-START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',                     25, 0, 'TopDown',       1],
      ['/TTjets_TuneZ2_scaleup_7TeV-madgraph-tauola/weizou-ttbsm_v9_Summer11-PU_S4_-START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',                       25, 0, 'TopUp',         1],
      ['/WJetsToLNu_TuneZ2_scaleup_7TeV-madgraph-tauola/skhalil-ttbsm_v9_Summer11-PU_S4_START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',                   25, 0, 'WJetsUp',       1],
      ['/WJetsToLNu_TuneZ2_scaledown_7TeV-madgraph-tauola/skhalil-ttbsm_v9_Summer11-PU_S4_START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',                 25, 0, 'WJetsDown',     1],
      ['/TTjets_TuneZ2_matchingdown_7TeV-madgraph-tauola/weizou-ttbsm_v9_Summer11-PU_S4_-START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',                  25, 0, 'TopMatchDown', 1 ],
      ['/TTjets_TuneZ2_matchingup_7TeV-madgraph-tauola/weizou-ttbsm_v9_Summer11-PU_S4_-START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',                    25, 0, 'TopMatchUp', 1 ],

      ]
   
for crabFileStr in crabFileStrs :
    print '------------------------- Operating on sample ' + crabFileStr[0] + ' ---------------------------'
    f = open(options.inputCfg, 'r')
    instring = f.read()

    # Get the dataset name, without the user-level stuff
    baseList = crabFileStr[0].split('/')

    if options.data == 1:
       outname = baseList[1] + options.outLabel+'_'+str(crabFileStr[7])
       outlocation = '/uscms_data/d2/skhalil/TPrimeEDM/TrigData_Dec29/'+baseList[1] + outputLable+'_'+str(crabFileStr[7])
    else:
       outname = baseList[1] + options.outLabel
       outlocation = '/uscms_data/d2/skhalil/TPrimeEDM/MC_Dec16/'+baseList[1] + outputLable

    # now do all of the substitutions
    a0 = instring.replace( 'DUMMY_DATASET', crabFileStr[0] )
    a1 = a0.replace( 'DUMMY_UI_DIR', outlocation)
    a2 = a1.replace( 'DUMMY_NJOBS', str(crabFileStr[1]) )
    a3 = a2.replace( 'DUMMY_CMSSW', inputCMSSW )
    a4 = a3.replace( 'DUMMY_RUNLOOSE', str(crabFileStr[2]) )
    a5 = a4.replace( 'DUMMY_SAMPLENAMEINPUT', crabFileStr[3] )
    a6 = a5.replace( 'DUMMY_IGNORETRIGGER', str(crabFileStr[4]) )
    if options.data == 1:
       a7 = a6.replace( 'DUMMY_JSON', str(crabFileStr[8]) )
       a8 = a7.replace('total_number_of_events = -1', 'total_number_of_lumis = -1')
       a9 = (a8.replace( 'DUMMY_TRIGGER', str(crabFileStr[5]) )).replace('DUMMY_RUNS', str(crabFileStr[6]) )
    else:
       a7 = a6.replace( 'lumi_mask=DUMMY_JSON', '')
       a8 = a7.replace(' triggerName=DUMMY_TRIGGER', '')
       a9 = a8.replace( 'runselection = DUMMY_RUNS', '')

    # Dump the contents of the crab config to the screen
    print '------ Config : ------- '
    print a9

    
    # open the output file
    crabName = 'crab_' + outname + '.cfg'
    fout = open( crabName, 'w')
    # write the text to the output file
    fout.write( a11 )
    fout.close()
    ## print '------ CRAB starting up! ------'
##     # now create the job:
##     s = 'crab -create -cfg ' + crabName
##     print s
##     # and submit:
##     subprocess.call( [s], shell=True )
##     s = 'crab -submit -c ' + outlocation
##     print s
##     subprocess.call( [s], shell=True )
