import subprocess, os, ConfigParser


dummy_config_name = 'crab_dummy_anashyft_ele.cfg'

dummy_config = ConfigParser.RawConfigParser()
dummy_config.read(dummy_config_name)

pset = 'shyftTupleDump2_cfg.py'
working_dir = os.environ['HOME'] + '/nobackup/ntuplesShyft/Jan18/'
dir_suffix = '_ttbsm_v9'

# one pset for all jobs
dummy_config.set('CMSSW','pset',pset)

joblist = [
##    # ==========  MC  =========
#    {'datasetpath':'/TTJets_TuneZ2_7TeV-madgraph-tauola/srappocc-ttbsm_v9_Summer11-PU_S4_START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',
#      'number_of_jobs':'15', 'pycfg_params':'useData=0', '#sample_name': 'Top' },
#    {'datasetpath':'/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/dstrom-prod_2011_10_05_17_14_11-bf57a985b107a689982b667a3f2f23c7/USER',
#     'number_of_jobs':'25', 'pycfg_params':'useData=0', '#sample_name': 'Wjets' },
#    {'datasetpath':'/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/samvel-prod_2011_10_04_10_32_11-bf57a985b107a689982b667a3f2f23c7/USER',
#     'number_of_jobs':'10', 'pycfg_params':'useData=0', '#sample_name': 'ZJets' },
#    {'datasetpath':'/T_TuneZ2_t-channel_7TeV-powheg-tauola/samvel-prod_2011_10_03_17_24_02-bf57a985b107a689982b667a3f2f23c7/USER',
#     'number_of_jobs':'5', 'pycfg_params':'useData=0', '#sample_name': 'SingleTopT' },
#    {'datasetpath':'/Tbar_TuneZ2_t-channel_7TeV-powheg-tauola/samvel-prod_2011_10_03_17_25_57-bf57a985b107a689982b667a3f2f23c7/USER',
#     'number_of_jobs':'5', 'pycfg_params':'useData=0', '#sample_name': 'SingleTopbarT' },
#    {'datasetpath':'/T_TuneZ2_s-channel_7TeV-powheg-tauola/samvel-prod_2011_10_03_17_19_46-bf57a985b107a689982b667a3f2f23c7/USER',
#     'number_of_jobs':'5', 'pycfg_params':'useData=0', '#sample_name': 'SingleTopS' },
#    {'datasetpath':'/Tbar_TuneZ2_s-channel_7TeV-powheg-tauola/samvel-prod_2011_10_03_17_22_26-bf57a985b107a689982b667a3f2f23c7/USER',
#     'number_of_jobs':'5', 'pycfg_params':'useData=0', '#sample_name': 'SingleTopbarS' },
#    {'datasetpath':'/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/samvel-prod_2011_10_03_17_15_48-bf57a985b107a689982b667a3f2f23c7/USER',
#     'number_of_jobs':'5', 'pycfg_params':'useData=0', '#sample_name': 'SingleToptW' },
#    {'datasetpath':'/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola/samvel-prod_2011_10_03_17_18_26-bf57a985b107a689982b667a3f2f23c7/USER',
#     'number_of_jobs':'5', 'pycfg_params':'useData=0', '#sample_name': 'SingleTopbartW' },
    
    # adding loose electron selection for electron QCD MC
##     {'datasetpath':'/GJets_TuneZ2_40_HT_100_7TeV-madgraph/skhalil-ttbsm_v9_Summer11-PU_S4_START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',
##      'number_of_jobs':'20', 'pycfg_params':'useData=0 useLooseElectrons=1', '#sample_name': 'PhoJet40100' },
##     {'datasetpath':'/GJets_TuneZ2_100_HT_200_7TeV-madgraph/skhalil-ttbsm_v9_Summer11-PU_S4_START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',
##      'number_of_jobs':'20', 'pycfg_params':'useData=0 useLooseElectrons=1', '#sample_name': 'PhoJet100200' },
##     {'datasetpath':'/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/skhalil-ttbsm_v9_Summer11-PU_S4_START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',
##      'number_of_jobs':'20', 'pycfg_params':'useData=0 useLooseElectrons=1', '#sample_name': 'PhoJet200Inf' },
##     {'datasetpath':'/QCD_Pt-20to30_BCtoE_TuneZ2_7TeV-pythia6/samvel-prod_2011_10_02_09_36_51-bf57a985b107a689982b667a3f2f23c7/USER',
##      'number_of_jobs':'5', 'pycfg_params':'useData=0 useLooseElectrons=1', '#sample_name': 'BCtoE2030' },
##     {'datasetpath':'/QCD_Pt-30to80_BCtoE_TuneZ2_7TeV-pythia6/samvel-prod_2011_10_02_09_39_46-bf57a985b107a689982b667a3f2f23c7/USER',
##      'number_of_jobs':'5', 'pycfg_params':'useData=0 useLooseElectrons=1', '#sample_name': 'BCtoE3080' },
##     {'datasetpath':'/QCD_Pt-80to170_BCtoE_TuneZ2_7TeV-pythia/samvel-prod_2011_10_02_09_41_02-bf57a985b107a689982b667a3f2f23c7/USER',
##      'number_of_jobs':'5', 'pycfg_params':'useData=0 useLooseElectrons=1', '#sample_name': 'BCtoE80170' },
##     {'datasetpath':'/QCD_Pt-20to30_EMEnriched_TuneZ2_7TeV-pythia6/samvel-tlbsm_v9_Summer11-PU_S4_START42_V11-v1_2011_10_07_15_34_09-bf57a985b107a689982b667a3f2f23c7/USER',
##      'number_of_jobs':'15', 'pycfg_params':'useData=0 useLooseElectrons=1', '#sample_name': 'EMEn2030' },
##     {'datasetpath':'/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia/samvel-ltbsm_v9_Summer11-PU_S4_START42_V11-v1_2011_10_07_12_56_15-bf57a985b107a689982b667a3f2f23c7/USER',
##      'number_of_jobs':'35', 'pycfg_params':'useData=0 useLooseElectrons=1', '#sample_name': 'EMEn3080' },
##     {'datasetpath':'/QCD_Pt-80to170_EMEnriched_TuneZ2_7TeV-pythia6/samvel-tlbsm_v9_Summer11-PU_S4_START42_V11-v1_2011_10_07_16_06_41-bf57a985b107a689982b667a3f2f23c7/USER',
##      'number_of_jobs':'5', 'pycfg_params':'useData=0 useLooseElectrons=1', '#sample_name': 'EMEn80170' },

##     # adding the top mass samples
##        {'datasetpath':'/TTJets_TuneZ2_mass161_5_7TeV-madgraph-tauola/meloam-ttbsm_v9_TTJets_TuneZ2_mass161_5_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v3-bf57a985b107a689982b667a3f2f23c7/USER',        'number_of_jobs':'20', 'pycfg_params':'useData=0', '#sample_name': 'Mass161_5' },
##        {'datasetpath':'/TTJets_TuneZ2_mass163_5_7TeV-madgraph-tauola/meloam-ttbsm_v9_TTJets_TuneZ2_mass163_5_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v3-bf57a985b107a689982b667a3f2f23c7/USER',        'number_of_jobs':'20', 'pycfg_params':'useData=0', '#sample_name': 'Mass163_5' },
##        {'datasetpath':'/TTJets_TuneZ2_mass166_5_7TeV-madgraph-tauola/meloam-ttbsm_v9_TTJets_TuneZ2_mass166_5_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v3-bf57a985b107a689982b667a3f2f23c7/USER',        'number_of_jobs':'20', 'pycfg_params':'useData=0', '#sample_name': 'Mass166_5' },
##        {'datasetpath':'/TTJets_TuneZ2_mass169_5_7TeV-madgraph-tauola/meloam-ttbsm_v9_TTJets_TuneZ2_mass169_5_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v3-bf57a985b107a689982b667a3f2f23c7/USER',        'number_of_jobs':'20', 'pycfg_params':'useData=0', '#sample_name': 'Mass169_5' },
          {'datasetpath':'/TTJets_TuneZ2_mass175_5_7TeV-madgraph-tauola/meloam-ttbsm_v9_TTJets_TuneZ2_mass175_5_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v3-bf57a985b107a689982b667a3f2f23c7/USER',        'number_of_jobs':'20', 'pycfg_params':'useData=0', '#sample_name': 'Mass175_5' },
##        {'datasetpath':'/TTJets_TuneZ2_mass178_5_7TeV-madgraph-tauola/meloam-ttbsm_v9_TTJets_TuneZ2_mass178_5_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v3-bf57a985b107a689982b667a3f2f23c7/USER',        'number_of_jobs':'20', 'pycfg_params':'useData=0', '#sample_name': 'Mass178_5' },
##        {'datasetpath':'/TTJets_TuneZ2_mass181_5_7TeV-madgraph-tauola/meloam-ttbsm_v9_TTJets_TuneZ2_mass181_5_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v3-bf57a985b107a689982b667a3f2f23c7/USER',        'number_of_jobs':'20', 'pycfg_params':'useData=0', '#sample_name': 'Mass181_5' },
##        {'datasetpath':'/TTJets_TuneZ2_mass184_5_7TeV-madgraph-tauola/meloam-ttbsm_v9_TTJets_TuneZ2_mass184_5_7TeV_madgraph_tauola_Summer11_PU_S4_START42_V11_v3-bf57a985b107a689982b667a3f2f23c7/USER',        'number_of_jobs':'20', 'pycfg_params':'useData=0', '#sample_name': 'Mass184_5' },

##    ##  # adding muon QCD MC
##     {'datasetpath':'/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/weizou-ttbsm_v9_Summer11-PU_S4_-START42_V11-v1_new-bf57a985b107a689982b667a3f2f23c7/USER',
##      'number_of_jobs':'20', 'pycfg_params':'useData=0', '#sample_name': 'Mu_QCD'},
    
## ##      # adding systematics samples
##     {'datasetpath':'/WJetsToLNu_TuneZ2_scaleup_7TeV-madgraph-tauola/skhalil-ttbsm_v9_Summer11-PU_S4_START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',
##      'number_of_jobs':'15', 'pycfg_params':'useData=0', '#sample_name': 'WjetsDown' },
##     {'datasetpath':'/WJetsToLNu_TuneZ2_scaledown_7TeV-madgraph-tauola/skhalil-ttbsm_v9_Summer11-PU_S4_START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',
##      'number_of_jobs':'15', 'pycfg_params':'useData=0', '#sample_name': 'WjetsUp' },
##     {'datasetpath':'/TTjets_TuneZ2_matchingdown_7TeV-madgraph-tauola/weizou-ttbsm_v9_Summer11-PU_S4_-START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',
##      'number_of_jobs':'15', 'pycfg_params':'useData=0', '#sample_name': 'TopMatchDown' },
##     {'datasetpath':'/TTjets_TuneZ2_matchingup_7TeV-madgraph-tauola/weizou-ttbsm_v9_Summer11-PU_S4_-START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',
##      'number_of_jobs':'15', 'pycfg_params':'useData=0', '#sample_name': 'TopMatchUp' },
##       {'datasetpath':'/TTjets_TuneZ2_scaledown_7TeV-madgraph-tauola/weizou-ttbsm_v9_Summer11-PU_S4_-START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',
##        'number_of_jobs':'15', 'pycfg_params':'useData=0', '#sample_name': 'TopDown' },
##       {'datasetpath':'/TTjets_TuneZ2_scaleup_7TeV-madgraph-tauola/weizou-ttbsm_v9_Summer11-PU_S4_-START42_V11-v1-bf57a985b107a689982b667a3f2f23c7/USER',
##        'number_of_jobs':'15', 'pycfg_params':'useData=0', '#sample_name': 'TopUp' },
    

## ##    # ==========  electron data  ==========
    ## {'datasetpath':'/SingleElectron/vasquez-ttbsm_v9_Run2011A-May10ReReco-f8e845a0332c56398831da6c30999af1/USER',
##      'number_of_jobs':'10', 'pycfg_params':'useData=1 triggerName=HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v1',
##      'runselection':'160431-161176' ,'lumi_mask':'Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.txt' ,'#sample_name': 'DataP1' },

##     {'datasetpath':'/SingleElectron/vasquez-ttbsm_v9_Run2011A-May10ReReco-f8e845a0332c56398831da6c30999af1/USER',
##      'number_of_jobs':'10', 'pycfg_params':'useData=1 triggerName=HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v2',
##      'runselection':'161217-163261' ,'lumi_mask':'Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.txt' ,'#sample_name': 'DataP2' },

##     {'datasetpath':'/SingleElectron/vasquez-ttbsm_v9_Run2011A-May10ReReco-f8e845a0332c56398831da6c30999af1/USER',
##      'number_of_jobs':'25', 'pycfg_params':'useData=1 triggerName=HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v3',
##      'runselection':'163270-163869' ,'lumi_mask':'Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.txt' ,'#sample_name': 'DataP3' },
    
##     {'datasetpath':'/SingleElectron/vasquez-ttbsm_v9_Run2011A-PromptReco-v4-f8e845a0332c56398831da6c30999af1/USER',
##      'number_of_jobs':'25', 'pycfg_params':'useData=1 triggerName=HLT_Ele32_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v3',
##      'runselection':'165088-165633' ,'lumi_mask':'Cert_160404-178078_7TeV_PromptReco_Collisions11_JSON.txt' ,'#sample_name': 'DataP4' },
    
##     {'datasetpath':'/SingleElectron/vasquez-ttbsm_v9_Run2011A-PromptReco-v4-f8e845a0332c56398831da6c30999af1/USER',
##      'number_of_jobs':'45', 'pycfg_params':'useData=1 triggerName=HLT_Ele32_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v4',
##      'runselection':'165970-166967' ,'lumi_mask':'Cert_160404-178078_7TeV_PromptReco_Collisions11_JSON.txt' ,'#sample_name': 'DataP5' },

##     # end of single electron triggers
##     {'datasetpath':'/ElectronHad/samvel-tlbsm_v9_Run2011A-PromptReco-v4_2011_10_14_06_42_11-f8e845a0332c56398831da6c30999af1/USER',
##      'number_of_jobs':'55', 'pycfg_params':'useData=1 triggerName=HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralJet30_v2',
##      'runselection':'167039-167913' ,'lumi_mask':'Cert_160404-178078_7TeV_PromptReco_Collisions11_JSON.txt' ,'#sample_name': 'DataP6' },
    
##     {'datasetpath':'/ElectronHad/samvel-tlbsm_v9_Run2011A-05Aug2011-v1_2011_10_14_06_37_36-f8e845a0332c56398831da6c30999af1/USER',
##      'number_of_jobs':'55', 'pycfg_params':'useData=1 triggerName=HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralJet30_v4',
##      'runselection':'170826-172619' ,'lumi_mask':'Cert_170249-172619_7TeV_ReReco5Aug_Collisions11_JSON_v3.txt' ,'#sample_name': 'DataP7a' },

##     {'datasetpath':'/ElectronHad/samvel-tlbsm_v9_Run2011A-PromptReco-v6_2011_10_13_15_49_05-f8e845a0332c56398831da6c30999af1/USER',
##      'number_of_jobs':'55', 'pycfg_params':'useData=1 triggerName=HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralJet30_v4',
##      'runselection':'172620-173198' ,'lumi_mask':'Cert_160404-178078_7TeV_PromptReco_Collisions11_JSON.txt' ,'#sample_name': 'DataP7b' },

##     {'datasetpath':'/ElectronHad/samvel-tlbsm_v9_Run2011A-PromptReco-v6_2011_10_13_15_49_05-f8e845a0332c56398831da6c30999af1/USER',
##      'number_of_jobs':'55', 'pycfg_params':'useData=1 triggerName=HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralJet30_v5',
##      'runselection':'173236-173692' ,'lumi_mask':'Cert_160404-178078_7TeV_PromptReco_Collisions11_JSON.txt' ,'#sample_name': 'DataP8a' },##173236-175770
    

## ##    # ==========  muon data  ==========
##     {'datasetpath':'/SingleMu/vasquez-ttbsm_v9_Run2011A-May10ReReco-f8e845a0332c56398831da6c30999af1/USER',
##      'number_of_jobs':'10', 'pycfg_params':'useData=1 triggerName=HLT_Mu30_v1 useLooseMuons=1',
##      'runselection':'160431-163261' ,'lumi_mask':'Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.txt' ,'#sample_name': 'DataP1' },

##     {'datasetpath':'/SingleMu/vasquez-ttbsm_v9_Run2011A-May10ReReco-f8e845a0332c56398831da6c30999af1/USER',
##      'number_of_jobs':'10', 'pycfg_params':'useData=1 triggerName=HLT_Mu30_v2 useLooseMuons=1',
##      'runselection':'163270-163869' ,'lumi_mask':'Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.txt' ,'#sample_name': 'DataP2' },

##     {'datasetpath':'/SingleMu/vasquez-ttbsm_v9_Run2011A-PromptReco-v4-f8e845a0332c56398831da6c30999af1/USER',
##      'number_of_jobs':'10', 'pycfg_params':'useData=1 triggerName=HLT_Mu30_v3 useLooseMuons=1',
##      'runselection':'165088-166164' ,'lumi_mask':'Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt' ,'#sample_name': 'DataP3a' },

##     {'datasetpath':'/SingleMu/vasquez-ttbsm_v9_Run2011A-PromptReco-v4-f8e845a0332c56398831da6c30999af1/USER',
##      'number_of_jobs':'10', 'pycfg_params':'useData=1 triggerName=HLT_Mu30_v3 useLooseMuons=1',
##      'runselection':'166374-167043' ,'lumi_mask':'Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt' ,'#sample_name': 'DataP3b' },

##     {'datasetpath':'/SingleMu/vasquez-ttbsm_v9_Run2011A-PromptReco-v4-f8e845a0332c56398831da6c30999af1/USER',
##      'number_of_jobs':'10', 'pycfg_params':'useData=1 triggerName=HLT_Mu30_v4 useLooseMuons=1',
##      'runselection':'166346-166346' ,'lumi_mask':'Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt' ,'#sample_name': 'DataP4' },

##     {'datasetpath':'/SingleMu/vasquez-ttbsm_v9_Run2011A-PromptReco-v4-f8e845a0332c56398831da6c30999af1/USER',
##      'number_of_jobs':'10', 'pycfg_params':'useData=1 triggerName=HLT_Mu30_v5 useLooseMuons=1',
##      'runselection':'167078-167913' ,'lumi_mask':'Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt' ,'#sample_name': 'DataP5' },

##     {'datasetpath':'/SingleMu/vasquez-ttbsm_v9_Run2011A-05Aug2011-f8e845a0332c56398831da6c30999af1/USER',
##      'number_of_jobs':'10', 'pycfg_params':'useData=1 triggerName=HLT_Mu30_v7 useLooseMuons=1',
##      'runselection':'170826-172619' ,'lumi_mask':'Cert_170249-172619_7TeV_ReReco5Aug_Collisions11_JSON_v3.txt' ,'#sample_name': 'DataP6a' },

##     {'datasetpath':'/SingleMu/yumiceva-ttbsm_v9_Run2011A-PromptReco-v6-f8e845a0332c56398831da6c30999af1/USER',
##      'number_of_jobs':'10', 'pycfg_params':'useData=1 triggerName=HLT_Mu30_v7 useLooseMuons=1',
##      'runselection':'172620-173198' ,'lumi_mask':'Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt' ,'#sample_name': 'DataP6b' },

##     {'datasetpath':'/SingleMu/yumiceva-ttbsm_v9_Run2011A-PromptReco-v6-f8e845a0332c56398831da6c30999af1/USER',
##      'number_of_jobs':'10', 'pycfg_params':'useData=1 triggerName=HLT_Mu30_v8 useLooseMuons=1',
##      'runselection':'173236-173692' ,'lumi_mask':'Cert_160404-180252_7TeV_PromptReco_Collisions11_JSON.txt' ,'#sample_name': 'DataP7' },

    ]

for job in joblist:
    config = dummy_config
    
    # for MC we don't need this
    config.remove_option('CMSSW','runselection')
    config.remove_option('CMSSW','lumi_mask')

    # plug for data
    if 'Data' in job['#sample_name']:
        config.remove_option('CMSSW','total_number_of_events')
        config.set('CMSSW','total_number_of_lumis','-1')
    
    for p in job:
        config.set('CMSSW', p, job[p])
    #ui_working_dir = working_dir + job['datasetpath'].split('/')[1] + '_' + job['#sample_name'] + dir_suffix
    ui_working_dir = working_dir + job['datasetpath'].split('/')[1] + dir_suffix +'_'+ job['#sample_name']
    config.set('USER','ui_working_dir',ui_working_dir)
    
    # write cfg file and run crab
    cfgname = 'crab_'+job['#sample_name']+'.cfg'
    with open(cfgname, 'wb') as configfile:
        config.write(configfile)
       
    s = 'crab -create -cfg ' + cfgname
    print s
    subprocess.call( [s], shell=True )

    s = 'crab -submit -c ' + ui_working_dir
    print s
    subprocess.call( [s], shell=True )
