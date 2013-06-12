#! /bin/python

from string import *
import subprocess

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputCfg', metavar='C', type='string', action='store',
                  default='crab_dummy_anashyft_ele_fit.cfg',
                  dest='inputCfg',
                  help='input config tag to be used')

parser.add_option('--outLabel', metavar='L', type='string', action='store',
                  default='_ttbsm_424_v9',
                  dest='outLabel',
                  help='output tag to be used')

parser.add_option('--data', metavar='D', type='int', action='store',
                  default = '0',
                  dest='data',
                  help='submit data jobs')
                 
(options, args) = parser.parse_args()
if options.data == 1:
  
   inputCMSSW = 'shyftEDAnalyzer_mu_kinfit.py'
   outputLable = '_ttbsm_424_v9'
   crabFileStrs = [
      ['/SingleMu/vasquez-ttbsm_v9_Run2011A-May10ReReco-f8e845a0332c56398831da6c30999af1/USER', 60, 0, 'Data', 0,
       'HLT_Mu30_v1', '160431-163261', 'P1', 'Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.txt'],

      ['/SingleMu/vasquez-ttbsm_v9_Run2011A-May10ReReco-f8e845a0332c56398831da6c30999af1/USER', 60, 0, 'Data', 0,
       'HLT_Mu30_v2', '163270-163869', 'P2', 'Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.txt'],
      
      ['/SingleMu/vasquez-ttbsm_v9_Run2011A-PromptReco-v4-f8e845a0332c56398831da6c30999af1/USER', 60, 0, 'Data', 0,
       'HLT_Mu30_v3', '165088-166164', 'P3a', 'Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt'],

      ['/SingleMu/vasquez-ttbsm_v9_Run2011A-PromptReco-v4-f8e845a0332c56398831da6c30999af1/USER', 60, 0, 'Data', 0,
       'HLT_Mu30_v3', '166374-167043', 'P3b', 'Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt'],

      ['/SingleMu/vasquez-ttbsm_v9_Run2011A-PromptReco-v4-f8e845a0332c56398831da6c30999af1/USER', 60, 0, 'Data', 0,
       'HLT_Mu30_v4', '166346-166346', 'P4', 'Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt'],

      ['/SingleMu/vasquez-ttbsm_v9_Run2011A-PromptReco-v4-f8e845a0332c56398831da6c30999af1/USER', 60, 0, 'Data', 0,
       'HLT_Mu30_v5', '167078-167913', 'P5', 'Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt'],

      ['/SingleMu/vasquez-ttbsm_v9_Run2011A-05Aug2011-f8e845a0332c56398831da6c30999af1/USER', 60, 0, 'Data', 0,       
       'HLT_Mu30_v7', '170826-173198', 'P6a', 'Cert_170249-172619_7TeV_ReReco5Aug_Collisions11_JSON_v3.txt'],##Data ends at run 172619
        
      ['/SingleMu/yumiceva-ttbsm_v9_Run2011A-PromptReco-v6-f8e845a0332c56398831da6c30999af1/USER', 60, 0, 'Data', 0,
       'HLT_Mu30_v7', '170826-173198', 'P6b', 'Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt'], ##Data starts from run 172620

      ['/SingleMu/yumiceva-ttbsm_v9_Run2011A-PromptReco-v6-f8e845a0332c56398831da6c30999af1/USER', 60, 0, 'Data', 0,
       'HLT_Mu40_eta2p1_v1', '173236-175770', 'P7a', 'Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt'], 
      
      ['/SingleMu/guragain-ttbsm_v9_Run2011B-PromptReco-v1_160404-179434-f8e845a0332c56398831da6c30999af1/USER',  60, 0, 'Data', 0,
       'HLT_Mu40_eta2p1_v1', '175832-178380', 'P7b', 'Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt'],

      ['/SingleMu/guragain-ttbsm_v9_Run2011B-PromptReco-v1_178162_180252-f8e845a0332c56398831da6c30999af1/USER',  60, 0, 'Data', 0,
       'HLT_Mu40_eta2p1_v4', '178420-179889', 'P8', 'Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt'],

      ['/SingleMu/guragain-ttbsm_v9_Run2011B-PromptReco-v1_178162_180252-f8e845a0332c56398831da6c30999af1/USER',  60, 0, 'Data', 0,
       'HLT_Mu40_eta2p1_v5', '179959-180252', 'P9', 'Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt'],
      
      
      ]
else:
   inputCMSSW = 'shyftEDAnalyzer_allsys_mu_kinfit_rw.py'
   outputLable = '_ttbsm_424_v9' 
   crabFileStrs = [
      
##SIGNAL MC for Bprime->tW
## ##       ['/BprimeBprimeToTWTWinc_M-350_7TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M350_7TeVSummer11_PU_S4_START42_V11v2_AA-bf57a985b107a689982b667a3f2f23c7/USER',
## ##        15, 0, 'BPrime_350',    1],
##        ['/BprimeBprimeToTWTWinc_M-375_7TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M375_7TeVmadgraphFall11_PU_S6_START42_V14Bv1CC-bf57a985b107a689982b667a3f2f23c7/USER',
##         15, 0, 'Fall11',    1],
## ##       ['/BprimeBprimeToTWTWinc_M-400_7TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M400_7TeVSummer11_PU_S4_START42_V11v2_AA-bf57a985b107a689982b667a3f2f23c7/USER',
## ##        15, 0, 'BPrime_400',    1],           
##        ['/BprimeBprimeToTWTWinc_M-425_7TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M425_7TeVmadgraphFall11_PU_S6_START42_V14Bv1DD-bf57a985b107a689982b667a3f2f23c7/USER',
##         15, 0, 'Fall11',    1],    
## ##       ['/BprimeBprimeToTWTWinc_M-450_7TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M450_7TeVSummer11_PU_S4_START42_V11v1-bf57a985b107a689982b667a3f2f23c7/USER',
## ##        15, 0, 'BPrime_450',    1],
## ##       ['/BprimeBprimeToTWTWinc_M-500_7TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M500_7TeVSummer11_PU_S4_START42_V11v2-bf57a985b107a689982b667a3f2f23c7/USER',
## ##        15, 0, 'BPrime_500',    1],
##        ['/BprimeBprimeToTWTWinc_M-525_7TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M525_7TeVmadgraphFall11PU_S6_START42_V14Bv1-bf57a985b107a689982b667a3f2f23c7/USER',
##         15, 0, 'Fall11',    1],
## ##       ['/BprimeBprimeToTWTWinc_M-550_7TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M550_7TeVSummer11_PU_S4_START42_V11v2-bf57a985b107a689982b667a3f2f23c7/USER',
## ##        15, 0, 'BPrime_550',    1],
##        ['/BprimeBprimeToTWTWinc_M-575_7TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M575_7TeVmadgraphFall11_PU_S6_START42_V14Bv1-bf57a985b107a689982b667a3f2f23c7/USER',
##         15, 0, 'Fall11',    1],
## ##       ['/BprimeBprimeToTWTWinc_M-600_7TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M600_7TeVSummer11_PU_S4_START42_V11v2-bf57a985b107a689982b667a3f2f23c7/USER',
## ##        15, 0, 'BPrime_600',    1],
##        ['/BprimeBprimeToTWTWinc_M-625_7TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M625_7TeVmadgraphFall11_PU_S6_START42_V14Bv1-bf57a985b107a689982b667a3f2f23c7/USER',
##         15, 0, 'Fall11',    1],
##        ['/BprimeBprimeToTWTWinc_M-650_7TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M650_7TeVmadgraphFall11_PU_S6_START42_V14Bv1-bf57a985b107a689982b667a3f2f23c7/USER',
##          15, 0, 'Fall11',    1],
##        ['/BprimeBprimeToTWTWinc_M-675_7TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M675_7TeVmadgraphFall11_PU_S6_START42_V14Bv1-bf57a985b107a689982b667a3f2f23c7/USER',
##         15, 0, 'Fall11',    1],
##        ['/BprimeBprimeToTWTWinc_M-700_7TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M700_7TeVmadgraphFall11_PU_S6_START42_V14Bv1-bf57a985b107a689982b667a3f2f23c7/USER',
##          15, 0, 'Fall11',    1],
##        ['/BprimeBprimeToTWTWinc_M-725_7TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M725_7TeVmadgraphFall11_PU_S6_START42_V14Bv1_CCC-bf57a985b107a689982b667a3f2f23c7/USER',
##          15, 0, 'Fall11',    1],
##        ['/BprimeBprimeToTWTWinc_M-750_7TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M750_7TeVmadgraphFall11_PU_S6_START42_V14Bv1_BBB-bf57a985b107a689982b667a3f2f23c7/USER',
##          15, 0, 'Fall11',    1],
##        ['/BprimeBprimeToTWTWinc_M-775_7TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M775_7TeVmadgraphFall11_PU_S6_START42_V14Bv1-bf57a985b107a689982b667a3f2f23c7/USER',
##         15, 0, 'Fall11',    1],
##        ['/BprimeBprimeToTWTWinc_M-800_7TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M800_7TeVmadgraphFall11_PU_S6_START42_V14Bv1-bf57a985b107a689982b667a3f2f23c7/USER',
##          15, 0, 'Fall11',    1],
      
## ##Signal Samples for LQToTNuTau
##       ['/LQToTNutau_M-200_7TeV-pythia6/cjenkins-LQToTNutauM200_7TeVpythia6Sum11PU_S4_START42_V11v1_v9-bf57a985b107a689982b667a3f2f23c7/USER',   15, 0, 'LQ_200',  1],
##       ['/LQToTNutau_M-250_7TeV-pythia6/cjenkins-LQToTNutauM250_7TeVpythia6Sum11PU_S4_START42_V11v1_v9_A-bf57a985b107a689982b667a3f2f23c7/USER', 15, 0, 'LQ_250',  1],
##       ['/LQToTNutau_M-300_7TeV-pythia6/cjenkins-LQToTNutauM300_7TeVpythia6Sum11PU_S4_START42_V11v1_v9-bf57a985b107a689982b667a3f2f23c7/USER',   15, 0, 'LQ_300',  1],
##       ['/LQToTNutau_M-350_7TeV-pythia6/cjenkins-LQToTNutauM350_7TeVpythia6Sum11PU_S4_START42_V11v1_v9-bf57a985b107a689982b667a3f2f23c7/USER',   15, 0, 'LQ_350',  1],
##       ['/LQToTNutau_M-400_7TeV-pythia6/cjenkins-LQToTNutauM400_7TeVpythia6Sum11PU_S4_START42_V11v1_v9_A-bf57a985b107a689982b667a3f2f23c7/USER', 15, 0, 'LQ_400',  1],
##       ['/LQToTNutau_M-450_7TeV-pythia6/cjenkins-LQToTNutauM450_7TeVpythia6Sum11PU_S4_START42_V11v1_v9-bf57a985b107a689982b667a3f2f23c7/USER',   15, 0, 'LQ_450',  1],
##       ['/LQToTNutau_M-500_7TeV-pythia6/cjenkins-LQToTNutauM500_7TeVpythia6Sum11PU_S4_START42_V11v1_v9-bf57a985b107a689982b667a3f2f23c7/USER',   15, 0, 'LQ_500',  1],
##       ['/LQToTNutau_M-550_7TeV-pythia6/cjenkins-LQToTNutauM550_7TeVpythia6Sum11PU_S4_START42_V11v1_v9_A-bf57a985b107a689982b667a3f2f23c7/USER', 15, 0, 'LQ_550',  1],
##       ['/LQToTNutau_M-600_7TeV-pythia6/cjenkins-LQToTNutauM600_7TeVpythia6Sum11PU_S4_START42_V11v1_v9-bf57a985b107a689982b667a3f2f23c7/USER',   15, 0, 'LQ_600',  1],
##       ['/LQToTNutau_M-650_7TeV-pythia6/cjenkins-LQToTNutauM650_7TeVpythia6Sum11PU_S4_START42_V11v1_v9-bf57a985b107a689982b667a3f2f23c7/USER',   15, 0, 'LQ_650',  1],

###t'->tW
##          ['/TprimeTprimeToBWBWinc_M-400_7TeV-madgraph/cjenkins-TprimeTprimeToBWBWinc_M400_7TeVSummer11_PU_S4_START42_V11_v2_BB-bf57a985b107a689982b667a3f2f23c7/USER',
##          11, 0, 'TPrime_400',  1],
##         ['/TprimeTprimeToBWBWinc_M-450_7TeV-madgraph/cjenkins-TprimeTprimeToBWBWinc_M450_7TeVSummer11_PU_S4_START42_V11_v2_AA-bf57a985b107a689982b667a3f2f23c7/USER',
##          11, 0, 'TPrime_450',  1],
##         ['/TprimeTprimeToBWBWinc_M-500_7TeV-madgraph/cjenkins-TprimeTprimeToBWBWinc_M500_7TeVSummer11_PU_S4_START42_V11_v2_AA-bf57a985b107a689982b667a3f2f23c7/USER',
##          11, 0, 'TPrime_500',  1],
##         ['/TprimeTprimeToBWBWinc_M-550_7TeV-madgraph/cjenkins-TprimeTprimeToBWBWinc_M550_7TeVSummer11_PU_S4_START42_V11_v2_AA-bf57a985b107a689982b667a3f2f23c7/USER',
##          11, 0, 'TPrime_550',  1],
##         ['/TprimeTprimeToBWBWinc_M-600_7TeV-madgraph/cjenkins-TprimeTprimeToBWBWinc_M600_7TeVSummer11_PU_S4_START42_V11_v2_AA-bf57a985b107a689982b667a3f2f23c7/USER',
##          11, 0, 'TPrime_600',  1],
        
##         ['/tprime425_bWbW_Summer11MG7TeV_JackLHE_atFermilab/vasquez-ttbsm_v9_Summer11MG7TeV_JackLHE_atFermilab-bf57a985b107a689982b667a3f2f23c7/USER',
##          11, 0, 'TPrime_425', 1],
##         ['/tprime475_bWbW_Summer11MG7TeV_JackLHE_atFermilab/vasquez-ttbsm_v9_Summer11MG7TeV_JackLHE_atFermilab-bf57a985b107a689982b667a3f2f23c7/USER',
##          11, 0, 'TPrime_475', 1],
##         ['/tprime525_bWbW_Summer11MG7TeV_JackLHE_atFermilab/vasquez-ttbsm_v9_Summer11MG7TeV_JackLHE_atFermilab-bf57a985b107a689982b667a3f2f23c7/USER',
##          11, 0, 'TPrime_525', 1],
##         ['/tprime525_bWbW_Summer11MG7TeV_JackLHE_atFermilab/vasquez-ttbsm_v9_Summer11MG7TeV_JackLHE_atFermilab-bf57a985b107a689982b667a3f2f23c7/USER',
##          11, 0, 'TPrime_525', 1],
##         ['/tprime575_bWbW_Summer11MG7TeV_JackLHE_atFermilab/vasquez-ttbsm_v9_Summer11MG7TeV_JackLHE_atFermilab-bf57a985b107a689982b667a3f2f23c7/USER',
##          11, 0, 'TPrime_575', 1],
##         ['/tprime625_bWbW_Summer11MG7TeV_JackLHE_atFermilab/vasquez-ttbsm_v9_Summer11MG7TeV_JackLHE_atFermilab-bf57a985b107a689982b667a3f2f23c7/USER',
##          11, 0, 'TPrime_625', 1],

 ##T->tZ
       ##  ['/TprimeTprimeToTZTZinc_M-350_7TeV-madgraph/cjenkins-TprimeTprimeToTZTZinc_M350_7TeVmadgraphSummer11_PU_S4_START42_V11v2_AAA-bf57a985b107a689982b667a3f2f23c7/USER',
##          11, 0, 'TPrimeTZ_350', 1],
##         ['/TprimeTprimeToTZTZinc_M-400_7TeV-madgraph/cjenkins-TprimeTprimeToTZTZinc_M400_7TeVmadgraphSummer11_PU_S4_START42_V11v1_AAA-bf57a985b107a689982b667a3f2f23c7/USER',
##          11, 0, 'TPrimeTZ_400', 1],
##         ['/TprimeTprimeToTZTZinc_M-450_7TeV-madgraph/cjenkins-TprimeTprimeToTZTZinc_M450_7TeVmadgraphSummer11_PU_S4_START42_V11v2_AAA-bf57a985b107a689982b667a3f2f23c7/USER',
##          11, 0, 'TPrimeTZ_450', 1],
##         ['/TprimeTprimeToTZTZinc_M-500_7TeV-madgraph/cjenkins-TprimeTprimeToTZTZinc_M500_7TeVmadgraphSummer11_PU_S4_START42_V11v2_BBB-bf57a985b107a689982b667a3f2f23c7/USER',
##          11, 0, 'TPrimeTZ_500', 1],
##         ['/TprimeTprimeToTZTZinc_M-550_7TeV-madgraph/cjenkins-TprimeTprimeToTZTZinc_M550_7TeVmadgraphSummer11_PU_S4_START42_V11v2_BBB-bf57a985b107a689982b667a3f2f23c7/USER',
##          11, 0, 'TPrimeTZ_550', 1],
##         ['/TprimeTprimeToTZTZinc_M-600_7TeV-madgraph/cjenkins-TprimeTprimeToTZTZinc_M600_7TeVmadgraphSummer11_PU_S4_START42_V11v2_AAA-bf57a985b107a689982b667a3f2f23c7/USER',
##          11, 0, 'TPrimeTZ_600', 1],
##        ['/TprimeTprimeToTZTZinc_M650_7TeV_madgraph_GEN_SIM_privateSample_B/cjenkins-TprimeTprimeToTZTZinc_M650_7TeVmadgraphSummer11_PU_S4_START42_PrivateSample_E-bf57a985b107a689982b667a3f2f23c7/USER', 11, 0, 'TPrimeTZ_650', 1],

## ## Background central samples
##         ['/TTJets_TuneZ2_7TeV-madgraph-tauola/srappocc-ttbsm_v9_Summer11-PU_S4_START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',  80, 0, 'Top',           1],
##       ['/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/dstrom-prod_2011_10_05_17_14_11-bf57a985b107a689982b667a3f2f23c7/USER',              50, 0, 'Wjets',         1],
##       ['/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/samvel-prod_2011_10_04_10_32_11-bf57a985b107a689982b667a3f2f23c7/USER',         40, 0, 'Zjets',         1],
##       ['/T_TuneZ2_t-channel_7TeV-powheg-tauola/samvel-prod_2011_10_03_17_24_02-bf57a985b107a689982b667a3f2f23c7/USER',               40, 0, 'SingleTopT',    1],
##       ['/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/samvel-prod_2011_10_03_17_25_57-bf57a985b107a689982b667a3f2f23c7/USER',            40, 0, 'SingleTopbarT', 1],
##       ['/T_TuneZ2_s-channel_7TeV-powheg-tauola/samvel-prod_2011_10_03_17_19_46-bf57a985b107a689982b667a3f2f23c7/USER',               40, 0, 'SingleTopS',    1],
##       ['/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/samvel-prod_2011_10_03_17_22_26-bf57a985b107a689982b667a3f2f23c7/USER',            40, 0, 'SingleTopbarS', 1],
##       ['/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/samvel-prod_2011_10_03_17_15_48-bf57a985b107a689982b667a3f2f23c7/USER',           40, 0, 'SingleToptW',   1],
##       ['/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/samvel-prod_2011_10_03_17_18_26-bf57a985b107a689982b667a3f2f23c7/USER',        40, 0, 'SingleTopbartW',1],
##       ['/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/weizou-ttbsm_v9_Summer11-PU_S4_-START42_V11-v1_new-bf57a985b107a689982b667a3f2f23c7/USER',  40, 0, 'QCD_Mu',1],
##       ['/WZ_TuneZ2_7TeV_pythia6_tauola/weizou-ttbsm_v9_Summer11-PU_S4_-START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',  40, 0, 'WZ',1],
##       ['/WW_TuneZ2_7TeV_pythia6_tauola/weizou-ttbsm_v9_Summer11-PU_S4_-START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',  40, 0, 'WW',1],
##       ['/ZZ_TuneZ2_7TeV_pythia6_tauola/skhalil-ttbsm_v9_Summer11-PU_S4_START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',  40, 0, 'ZZ',1],
      

## ## systematic samples
##       ['/TTjets_TuneZ2_scaledown_7TeV-madgraph-tauola/weizou-ttbsm_v9_Summer11-PU_S4_-START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',     25, 0, 'TopDown',       1],
##       ['/TTjets_TuneZ2_scaleup_7TeV-madgraph-tauola/weizou-ttbsm_v9_Summer11-PU_S4_-START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',       25, 0, 'TopUp',         1],
##       ['/WJetsToLNu_TuneZ2_scaleup_7TeV-madgraph-tauola/skhalil-ttbsm_v9_Summer11-PU_S4_START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',   25, 0, 'WJetsUp',       1],
##       ['/WJetsToLNu_TuneZ2_scaledown_7TeV-madgraph-tauola/skhalil-ttbsm_v9_Summer11-PU_S4_START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER', 25, 0, 'WJetsDown',     1],
##       ['/TTjets_TuneZ2_matchingdown_7TeV-madgraph-tauola/weizou-ttbsm_v9_Summer11-PU_S4_-START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',  25, 0, 'TopMatchDown',  1],
##       ['/TTjets_TuneZ2_matchingup_7TeV-madgraph-tauola/weizou-ttbsm_v9_Summer11-PU_S4_-START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',    25, 0, 'TopMatchUp',    1],
##       ['/TT_TuneZ2_7TeV-powheg-tauola/weizou-ttbsm_v9_Summer11-PU_S4_-START42_V11-v1_new-bf57a985b107a689982b667a3f2f23c7/USER',     120, 0, 'Top_powheg',    1],
##       ['/TTjets_TuneZ2_matchingup_7TeV-madgraph-tauola/vasquez-ttbsm_v9_Fall11-PU_S4_START42_V14B-v2-bf57a985b107a689982b667a3f2f23c7/USER',   25, 0, 'Fall11',   1],
##       ['/TTJets_TuneZ2_7TeV-madgraph-tauola/vasquez-ttbsm_v9_Fall11-PU_S4_START42_V14B-v2-bf57a985b107a689982b667a3f2f23c7/USER', 50, 0, 'Fall11',   1],
         ['/TT_TuneZ2_7TeV-pythia6-tauola/vasquez-ttbsm_v9_Summer11-PU_S3_START42_V11-v2-bf57a985b107a689982b667a3f2f23c7/USER', 50, 0, 'TTbar',   1],
        ]

for crabFileStr in crabFileStrs :
    print '------------------------- Operating on sample ' + crabFileStr[0] + ' ---------------------------'
    f = open(options.inputCfg, 'r')
    instring = f.read()

    # Get the dataset name, without the user-level stuff
    baseList = crabFileStr[0].split('/')
    
    if options.data == 1:
       outname = baseList[1] + options.outLabel+'_'+str(crabFileStr[7])
       outlocation = '/uscms_data/d2/skhalil/BPrimeEDM/Data_Apr30/'+baseList[1] + outputLable+'_'+str(crabFileStr[7])
    else:
       outname = baseList[1] + options.outLabel
       outlocation = '/uscms_data/d2/skhalil/BPrimeEDM/MC_Apr30/'+baseList[1] + outputLable+'_'+str(crabFileStr[3])
    
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


