# Returns the datasets for this analysis

def getInputPAT():
    datasetDict = { 
        'Tbar_tW' : '/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
        'Tbar_t' : '/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
        'Tbar_s' : '/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
        'T_tW'   : '/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
        'T_t'    : '/T_t-channel_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
        'T_s'    : '/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
        'TTJets' :
    '/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
        'DYJetsLL' :
    '/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
        'DY1JetsLL' : '/DY1JetsToLL_M-50_TuneZ2Star_8TeV-madgraph/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
        'WJets_lnu' :
        '/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v2_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER',
    'DoubleMu-2012A':
    '/DoubleMu/StoreResults-Run2012A-13Jul2012-v1_TLBSM_53x_v2-e3fb55b810dc7a0811f4c66dfa2267c9/USER',
    'SingleMu-2012B':'/SingleMu/StoreResults-Run2012B-13Jul2012-v1_TLBSM_53x_v2-e3fb55b810dc7a0811f4c66dfa2267c9/USER',
    'SingleEle-2012A':
    '/SingleElectron/StoreResults-Run2012A-13Jul2012-v1_TLBSM_53x_v2-e3fb55b810dc7a0811f4c66dfa2267c9/USER' }

    return { 'datasetNames' : datasetDict }
