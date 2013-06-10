import subprocess, os, ConfigParser


dummy_config_name = 'crab_dummy_anashyft_ele.cfg'

dummy_config = ConfigParser.RawConfigParser()
dummy_config.read(dummy_config_name)

pset = 'edmNtupleMaker.py'
working_dir = os.environ['HOME'] + '/nobackup/BPrimeEDM_8TeV/Jan15/'
dir_suffix = '_tlbsm_53x_v2'

# one pset for all jobs
dummy_config.set('CMSSW','pset',pset)

joblist = [
   # ==========  MC ==========

##      {'datasetpath':'/BprimeBprimeToBZTWinc_M-450_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-450_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_450', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet'},

##        {'datasetpath':'/BprimeBprimeToBZTWinc_M-500_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_500', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'BprimeBprimeToBZTWinc_M-500_TuneZ2star_8TeV-madgraph'},

##        {'datasetpath':'/BprimeBprimeToBZTWinc_M-550_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-550_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_550', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'BprimeBprimeToBZTWinc_M-550_TuneZ2star_8TeV-madgraph'},
    
##      {'datasetpath':'/BprimeBprimeToBZTWinc_M-600_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBZTWinc_M-600_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2_A-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_600', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##      {'datasetpath':'/BprimeBprimeToBZTWinc_M-650_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBZTWinc_M-650_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_650', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##      {'datasetpath':'/BprimeBprimeToBZTWinc_M-700_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBZTWinc_M-700_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2_A-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_700', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##      {'datasetpath':'/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_750', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##      {'datasetpath':'/BprimeBprimeToBZTWinc_M-800_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBZTWinc_M-800_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_800', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

#      {'datasetpath':'/BprimeBprimeToBZTWinc_M-900_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-900_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_900', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'BprimeBprimeToBZTWinc_M-900_TuneZ2star_8TeV-madgraph'},

#      {'datasetpath':'/BprimeBprimeToBZTWinc_M-1000_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-1000_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_1000', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'BprimeBprimeToBZTWinc_M-1000_TuneZ2star_8TeV-madgraph'},
      
#      {'datasetpath':'/BprimeBprimeToBZTWinc_M-1100_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZTWinc_M-1100_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7C-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZTW_1100', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', ''btag_map':'BprimeBprimeToBZTWinc_M-1100_TuneZ2star_8TeV-madgraph'},
       
##      {'datasetpath':'/BprimeBprimeToTWTWinc_M-450_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToTWTWinc_M-450_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToTWTW_450', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

#      {'datasetpath':'/BprimeBprimeToTWTWinc_M-500_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToTWTW_500', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet'},

##      {'datasetpath':'/BprimeBprimeToTWTWinc_M-550_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToTWTWinc_M-550_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToTWTW_550', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##        {'datasetpath':'/BprimeBprimeToTWTWinc_M-600_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToTWTWinc_M-600_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToTWTW_600', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'BprimeBprimeToTWTWinc_M-600_TuneZ2star_8TeV-madgraph'},
       
##      {'datasetpath':'/BprimeBprimeToTWTWinc_M-650_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToTWTWinc_M-650_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2_B-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToTWTW_650', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##      {'datasetpath':'/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2_B-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToTWTW_700', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##      {'datasetpath':'/BprimeBprimeToTWTWinc_M-750_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToTWTWinc_M-750_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToTWTW_750', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##      {'datasetpath':'/BprimeBprimeToTWTWinc_M-800_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToTWTWinc_M-800_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToTWTW_800', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##      {'datasetpath': '/BprimeBprimeToBHBHinc_M-450_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHBHinc_M-450_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBH_450', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBHBHinc_M-500_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHBHinc_M-500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBH_500', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBHBHinc_M-550_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHBHinc_M-550_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBH_550', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBHBHinc_M-600_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHBHinc_M-600_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBH_600', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBHBHinc_M-650_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHBHinc_M-650_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBH_650', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBHBHinc_M-700_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHBHinc_M-700_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBH_700', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBHBHinc_M-750_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHBHinc_M-750_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBH_750', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBHBHinc_M-800_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHBHinc_M-800_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBH_800', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

#      {'datasetpath': '/BprimeBprimeToBHBZinc_M-450_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHBZinc_M-450_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBZ_450', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet', 'btag_map':'BprimeBprimeToBHBZinc_M-450_TuneZ2star_8TeV-madgraph' },

##      {'datasetpath': '/BprimeBprimeToBHBZinc_M-500_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHBZinc_M-500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBZ_500', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBHBZinc_M-550_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHBZinc_M-550_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBZ_550', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBHBZinc_M-600_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHBZinc_M-600_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBZ_600', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBHBZinc_M-650_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHBZinc_M-650_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBZ_650', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBHBZinc_M-700_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHBZinc_M-700_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBZ_700', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBHBZinc_M-750_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHBZinc_M-750_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBZ_750', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBHBZinc_M-800_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHBZinc_M-800_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHBZ_800', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##       {'datasetpath': '/BprimeBprimeToBHTWinc_M-450_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHTWinc_M-450_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_450', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'BprimeBprimeToBHTWinc_M-450_TuneZ2star_8TeV-madgraph' },

##        {'datasetpath': '/BprimeBprimeToBHTWinc_M-500_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHTWinc_M-500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_500', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'BprimeBprimeToBHTWinc_M-500_TuneZ2star_8TeV-madgraph' },

##       {'datasetpath': '/BprimeBprimeToBHTWinc_M-550_TuneZ2star_8TeV-madgraph/cjenkins-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_550', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'BprimeBprimeToBHTWinc_M-550_TuneZ2star_8TeV-madgraph' },
    
##      {'datasetpath': '/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_600', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBHTWinc_M-650_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHTWinc_M-650_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_650', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },        
##      {'datasetpath': '/BprimeBprimeToBHTWinc_M-700_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHTWinc_M-700_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_700', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBHTWinc_M-750_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBHTWinc_M-750_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_750', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },
      
##       {'datasetpath': '/BprimeBprimeToBHTWinc_M-800_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBHTWinc_M-800_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBHTW_800', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'BprimeBprimeToBHTWinc_M-800_TuneZ2star_8TeV-madgraph' },
    
##      {'datasetpath': '/BprimeBprimeToBZBZinc_M-450_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBZBZinc_M-450_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZBZ_450', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBZBZinc_M-500_TuneZ2star_8TeV-madgraph/cjenkins-BprimeBprimeToBZBZinc_M-500_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZBZ_500', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'BprimeBprimeToBZBZinc_M-550_TuneZ2star_8TeV-madgraph' },
    
##      {'datasetpath': '/BprimeBprimeToBZBZinc_M-550_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBZBZinc_M-550_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZBZ_550', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBZBZinc_M-600_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBZBZinc_M-600_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZBZ_600', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBZBZinc_M-650_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBZBZinc_M-650_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZBZ_650', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBZBZinc_M-700_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBZBZinc_M-700_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZBZ_700', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBZBZinc_M-750_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBZBZinc_M-750_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZBZ_750', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##      {'datasetpath': '/BprimeBprimeToBZBZinc_M-800_TuneZ2star_8TeV-madgraph/StoreResults-BprimeBprimeToBZBZinc_M-800_TuneZ2star_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'BBToBZBZ_800', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

#### ========= To be submitted =============

##    {'datasetpath': '/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'200', 'pycfg_params':'runData=0', '#sample_name': 'Top', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##    {'datasetpath': '/T_s-channel_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'SingleTopS', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##    {'datasetpath': '/T_t-channel_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'SingleTopT', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##    {'datasetpath': '/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'SingleToptW', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##    {'datasetpath': '/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'SingleTopbarS', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##    {'datasetpath': '/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'SingleTopbarT', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##    {'datasetpath': '/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'SingleTopbartW', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##    {'datasetpath': '/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'300','pycfg_params':'runData=0', '#sample_name': 'ZJets', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##    {'datasetpath': '/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v2_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'150', 'pycfg_params':'runData=0', '#sample_name': 'WJets_v2', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##    {'datasetpath': '/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'WJets_v1', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' }, #not urgent

##    {'datasetpath': '/TTWJets_8TeV-madgraph/avetisya-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'TopWJets', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

##    {'datasetpath': '/TTZJets_8TeV-madgraph_v2/mmhl-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'TopZJets', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet' },

##    {'datasetpath': '/WW_TuneZ2star_8TeV_pythia6_tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'WW', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##    {'datasetpath': '/ZZ_TuneZ2star_8TeV_pythia6_tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'ZZ', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##    {'datasetpath': '/WZ_TuneZ2star_8TeV_pythia6_tauola/malik-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-3abcc3b1cd74b7b45c7ed2df0ee1e03c/USER', 'number_of_jobs':'50', 'pycfg_params':'runData=0', '#sample_name': 'WZ', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'WZ_TuneZ2star_8TeV_pythia6_tauola' },

##    {'datasetpath': '/TT_8TeV-mcatnlo/galank-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'450', 'pycfg_params':'runData=0', '#sample_name': 'Top_mcatnlo', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'TT_8TeV-mcatnlo' },

##    {'datasetpath': '/TT_CT10_TuneZ2star_8TeV-powheg-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v2_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'300', 'pycfg_params':'runData=0', '#sample_name': 'Top_powheg', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet', 'btag_map':'TT_CT10_TuneZ2star_8TeV-powheg-tauola' },

##    {'datasetpath': '/TTJets_matchingdown_TuneZ2star_8TeV-madgraph-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0', '#sample_name': 'TopMatchdn', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##    {'datasetpath': '/TTJets_matchingup_TuneZ2star_8TeV-madgraph-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0', '#sample_name': 'TopMatchup', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##    {'datasetpath': '/TTJets_scaledown_TuneZ2star_8TeV-madgraph-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2_bugfix_v1-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0', '#sample_name': 'TopScaledn', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

##    {'datasetpath': '/TTJets_scaleup_TuneZ2star_8TeV-madgraph-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0', '#sample_name': 'TopScaleup', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },
 
##     {'datasetpath': '/QCD_Pt_20_30_BCtoE_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runEleQCDSamples=1', '#sample_name': 'QCD_Pt_20_30_BCtoE', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet', 'btag_map':'QCD_Pt_20_30_BCtoE_TuneZ2star_8TeV_pythia6' },
    
##     {'datasetpath': '/QCD_Pt_30_80_BCtoE_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runEleQCDSamples=1', '#sample_name': 'QCD_Pt_30_80_BCtoE', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet', 'btag_map':'QCD_Pt_30_80_BCtoE_TuneZ2star_8TeV_pythia6' },

##     {'datasetpath': '/QCD_Pt_80_170_BCtoE_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt_80_170_BCtoE_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runEleQCDSamples=1', '#sample_name': 'QCD_Pt_80_170_BCtoE', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'QCD_Pt_80_170_BCtoE_TuneZ2star_8TeV_pythia6'},
  
##     {'datasetpath': '/QCD_Pt_170_250_BCtoE_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt_170_250_BCtoE_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runEleQCDSamples=1', '#sample_name': 'QCD_Pt_170_250_BCtoE', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'QCD_Pt_170_250_BCtoE_TuneZ2star_8TeV_pythia6' },
    
##     {'datasetpath': '/QCD_Pt_250_350_BCtoE_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt_250_350_BCtoE_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runEleQCDSamples=1', '#sample_name': 'QCD_Pt_250_350_BCtoE', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet','btag_map':'QCD_Pt_250_350_BCtoE_TuneZ2star_8TeV_pythia6' },

##     {'datasetpath': '/QCD_Pt_350_BCtoE_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v2_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runEleQCDSamples=1', '#sample_name': 'QCD_Pt_350_BCtoE', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet', 'btag_map':'QCD_Pt_350_BCtoE_TuneZ2star_8TeV_pythia6' },

##     {'datasetpath': '/QCD_Pt_20_30_EMEnriched_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runEleQCDSamples=1', '#sample_name': 'QCD_Pt_20_30_EMEnriched', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet', 'btag_map':'QCD_Pt_20_30_EMEnriched_TuneZ2star_8TeV_pythia6' },

    {'datasetpath': '/QCD_Pt_30_80_EMEnriched_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt_30_80_EMEnriched_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runEleQCDSamples=1', '#sample_name': 'QCD_Pt_30_80_EMEnriched', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'QCD_Pt_30_80_EMEnriched_TuneZ2star_8TeV_pythia6' },

    {'datasetpath': '/QCD_Pt_80_170_EMEnriched_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runEleQCDSamples=1', '#sample_name': 'QCD_Pt_80_170_EMEnriched', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet', 'btag_map':'QCD_Pt_80_170_EMEnriched_TuneZ2star_8TeV_pythia6' },

    {'datasetpath': '/QCD_Pt_170_250_EMEnriched_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runEleQCDSamples=1', '#sample_name': 'QCD_Pt_170_250_EMEnriched', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet', 'btag_map':'QCD_Pt_170_250_EMEnriched_TuneZ2star_8TeV_pythia6' },

    {'datasetpath': '/QCD_Pt_250_350_EMEnriched_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runEleQCDSamples=1', '#sample_name': 'QCD_Pt_250_350_EMEnriched', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet', 'btag_map':'QCD_Pt_250_350_EMEnriched_TuneZ2star_8TeV_pythia6' },

    {'datasetpath': '/QCD_Pt_350_EMEnriched_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runEleQCDSamples=1', '#sample_name': 'QCD_Pt_350_EMEnriched', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet', 'btag_map':'QCD_Pt_350_EMEnriched_TuneZ2star_8TeV_pythia6' },

    {'datasetpath': '/GJets_HT-200To400_8TeV-madgraph/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runEleQCDSamples=1', '#sample_name': 'GJets_HT-200To400', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet', 'btag_map':'GJets_HT-200To400_8TeV-madgraph' },

    {'datasetpath': '/GJets_HT-400ToInf_8TeV-madgraph/cjenkins-GJets_HT-400ToInf_8TeV-madgraph-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runEleQCDSamples=1', '#sample_name': 'GJets_HT-400ToInf', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'GJets_HT-400ToInf_8TeV-madgraph' },

    {'datasetpath': '/QCD_Pt-15to20_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt-15to20_MuEnrichedPt5_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v2_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runMuonQCDSamples=1', '#sample_name': 'QCD_Pt-15to20_MuEnrichedPt5', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'QCD_Pt-15to20_MuEnrichedPt5_TuneZ2star_8TeV_pythia6' },

    {'datasetpath': '/QCD_Pt-20to30_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runMuonQCDSamples=1', '#sample_name': 'QCD_Pt-20to30_MuEnrichedPt5', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet', 'btag_map':'QCD_Pt-20to30_MuEnrichedPt5_TuneZ2star_8TeV_pythia6' },
    
    {'datasetpath': '/QCD_Pt-30to50_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runMuonQCDSamples=1', '#sample_name': 'QCD_Pt-30to50_MuEnrichedPt5', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet', 'btag_map':'QCD_Pt-30to50_MuEnrichedPt5_TuneZ2star_8TeV_pythia6' },

    {'datasetpath': 'QCD_Pt-50to80_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt-50to80_MuEnrichedPt5_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runMuonQCDSamples=1', '#sample_name': 'QCD_Pt-50to80_MuEnrichedPt5', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'QCD_Pt-50to80_MuEnrichedPt5_TuneZ2star_8TeV_pythia6' },

    {'datasetpath': '/QCD_Pt-80to120_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runMuonQCDSamples=1', '#sample_name': 'QCD_Pt-80to120_MuEnrichedPt5', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet', 'btag_map':'QCD_Pt-80to120_MuEnrichedPt5_TuneZ2star_8TeV_pythia6' },

    {'datasetpath': '/QCD_Pt-120to170_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt-120to170_MuEnrichedPt5_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runMuonQCDSamples=1', '#sample_name': 'QCD_Pt-120to170_MuEnrichedPt5', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'QCD_Pt-120to170_MuEnrichedPt5_TuneZ2star_8TeV_pythia6' },

    {'datasetpath': '/QCD_Pt-170to300_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt-170to300_MuEnrichedPt5_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runMuonQCDSamples=1', '#sample_name': 'QCD_Pt-170to300_MuEnrichedPt5', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'QCD_Pt-170to300_MuEnrichedPt5_TuneZ2star_8TeV_pythia6' },

    {'datasetpath': '/QCD_Pt-300to470_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt-300to470_MuEnrichedPt5_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runMuonQCDSamples=1', '#sample_name': 'QCD_Pt-300to470_MuEnrichedPt5', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'QCD_Pt-300to470_MuEnrichedPt5_TuneZ2star_8TeV_pythia6' },

    {'datasetpath': '/QCD_Pt-470to600_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/cjenkins-QCD_Pt-470to600_MuEnrichedPt5_TuneZ2star_8TeV_pythia6-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runMuonQCDSamples=1', '#sample_name': 'QCD_Pt-470to600_MuEnrichedPt5', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet', 'btag_map':'QCD_Pt-470to600_MuEnrichedPt5_TuneZ2star_8TeV_pythia6' },

    {'datasetpath': '/QCD_Pt-600to800_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runMuonQCDSamples=1', '#sample_name': 'QCD_Pt-600to800_MuEnrichedPt5', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet', 'btag_map':'QCD_Pt-600to800_MuEnrichedPt5_TuneZ2star_8TeV_pythia6' },

    {'datasetpath': '/QCD_Pt-800to1000_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/USER', 'number_of_jobs':'100', 'pycfg_params':'runData=0 runMuonQCDSamples=1', '#sample_name': 'QCD_Pt-800to1000_MuEnrichedPt5', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet', 'btag_map':'QCD_Pt-800to1000_MuEnrichedPt5_TuneZ2star_8TeV_pythia6' },
     

# ========== Data Electron ==========
   
##     {'datasetpath':'/SingleElectron/StoreResults-Run2012A-13Jul2012-v1_TLBSM_53x_v2-e3fb55b810dc7a0811f4c66dfa2267c9/USER',
##      'number_of_jobs':'50', 'pycfg_params':'runData=1','runselection':'190450-193621' ,'lumi_mask':'Cert_190456-196531_8TeV_13Jul2012ReReco_Collisions12_JSON_v2.txt' ,
##      '#sample_name': 'Data-Run2012A-13Jul2012-v1','dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##     {'datasetpath':'/SingleElectron/StoreResults-Run2012A-recover-06Aug2012-v1_TLBSM_53x_v2-e3fb55b810dc7a0811f4c66dfa2267c9/USER',
##      'number_of_jobs':'30', 'pycfg_params':'runData=1','runselection':'190782-190949' ,'lumi_mask':'Cert_190782-190949_8TeV_06Aug2012ReReco_Collisions12_JSON.txt' ,
##      '#sample_name': 'Data-Run2012A-06Aug2012-v1','dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},
    
##     {'datasetpath':'/SingleElectron/StoreResults-Run2012B-13Jul2012-v1_TLBSM_53x_v2-e3fb55b810dc7a0811f4c66dfa2267c9/USER',
##      'number_of_jobs':'300', 'pycfg_params':'runData=1', 'runselection':'193834-196531', 'lumi_mask':'Cert_190456-196531_8TeV_13Jul2012ReReco_Collisions12_JSON_v2.txt' ,
##      '#sample_name': 'Data_Run2012B-13Jul2012-v1', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global//servlet/DBSServlet'},
    
##     {'datasetpath':'/SingleElectron/StoreResults-Run2012C-24Aug2012-v1_TLBSM_53x_v2-e3fb55b810dc7a0811f4c66dfa2267c9/USER',
##      'number_of_jobs':'50', 'pycfg_params':'runData=1','runselection':'198022-198523' ,'lumi_mask':'Cert_198022-198523_8TeV_24Aug2012ReReco_Collisions12_JSON.txt' ,
##      '#sample_name': 'Data-Run2012C-24Aug2012-v1', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##      {'datasetpath':'/SingleElectron/StoreResults-Run2012C-PromptReco-v2_TLBSM_53x_v2-e3fb55b810dc7a0811f4c66dfa2267c9/USER',
##      'number_of_jobs':'150', 'pycfg_params':'runData=1','runselection':'198934-203755' ,'lumi_mask':'Cert_190456-203002_8TeV_PromptReco_Collisions12_JSON_v2.txt' ,
##      '#sample_name': 'Data-Run2012C-PromptReco-v2-a', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##      {'datasetpath':'/SingleElectron/StoreResults-Run2012C-PromptReco-v2_TLBSM_53x_v2_extension_v1-e3fb55b810dc7a0811f4c66dfa2267c9/USER',
##      'number_of_jobs':'80', 'pycfg_params':'runData=1','runselection':'198934-203755' ,'lumi_mask':'Cert_190456-203002_8TeV_PromptReco_Collisions12_JSON_v2.txt' ,
##      '#sample_name': 'Data-Run2012C-PromptReco-v2-b', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},


##     {'datasetpath':'/SingleElectron/cjenkins-Run2012C-EcalRecover_11Dec2012-v1_TLBSM_53x_v2-e3fb55b810dc7a0811f4c66dfa2267c9/USER',
##      'number_of_jobs':'5', 'pycfg_params':'runData=1','runselection':'201191-201191' ,'lumi_mask':'Cert_201191-201191_8TeV_11Dec2012ReReco-recover_Collisions12_JSON.txt' ,
##      '#sample_name': 'Data-Run2012C-EcalRecover_11Dec2012-v1', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet'},
    
##      {'datasetpath':'/SingleElectron/StoreResults-Run2012D-PromptReco-v1_TLBSM_53x_v2_bugfix-e3fb55b810dc7a0811f4c66dfa2267c9/USER',
##      'number_of_jobs':'300', 'pycfg_params':'runData=1','runselection':'203773-209465' ,'lumi_mask':'Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.txt' ,
##      '#sample_name': 'Data-Run2012D-PromptReco-v1-a', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##      {'datasetpath':'/SingleElectron/StoreResults-Run2012D-PromptReco-v1_TLBSM_53x_v2_extension_v1-e3fb55b810dc7a0811f4c66dfa2267c9/USER',
##      'number_of_jobs':'100', 'pycfg_params':'runData=1','runselection':'203773-209465' ,'lumi_mask':'Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.txt' ,
##      '#sample_name': 'Data-Run2012D-PromptReco-v1-b', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},
      

##=========== Data Muon ===============

##     {'datasetpath':'/SingleMu/StoreResults-SingleMu_Run2012A-13Jul2012-v1_TLBSM_53x_v2_jsonfix-e3fb55b810dc7a0811f4c66dfa2267c9/USER',
##      'number_of_jobs':'40', 'pycfg_params':'runData=1','runselection':'190456-193621','lumi_mask':'Cert_190456-196531_8TeV_13Jul2012ReReco_Collisions12_JSON_MuonPhys_v3.txt' ,
##      '#sample_name': 'Data-Run2012A-13Jul2012-v1', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##     {'datasetpath':'/SingleMu/StoreResults-Run2012A-recover-06Aug2012-v1_TLBSM_53x_v2-e3fb55b810dc7a0811f4c66dfa2267c9/USER',
##      'number_of_jobs':'50', 'pycfg_params':'runData=1','runselection':'190782-190949','lumi_mask':'Cert_190782-190949_8TeV_06Aug2012ReReco_Collisions12_JSON_MuonPhys.txt' ,
##      '#sample_name': 'Data-Run2012A-06Aug2012-v1', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##     {'datasetpath':'/SingleMu/StoreResults-Run2012B-13Jul2012-v1_TLBSM_53x_v2-e3fb55b810dc7a0811f4c66dfa2267c9/USER',
##      'number_of_jobs':'300', 'pycfg_params':'runData=1','runselection':'193834-196531','lumi_mask':'Cert_190456-196531_8TeV_13Jul2012ReReco_Collisions12_JSON_MuonPhys_v3.txt' ,
##      '#sample_name': 'Data-Run2012B-13Jul2012-v1', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##     {'datasetpath':'/SingleMu/StoreResults-Run2012C-24Aug2012-v1_TLBSM_53x_v2-e3fb55b810dc7a0811f4c66dfa2267c9/USER',
##      'number_of_jobs':'50', 'pycfg_params':'runData=1','runselection':'197770-198913','lumi_mask':'Cert_198022-198523_8TeV_24Aug2012ReReco_Collisions12_JSON_MuonPhys.txt' ,
##      '#sample_name': 'Data-Run2012C-24Aug2012-v1', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##     {'datasetpath':'/SingleMu/StoreResults-Run2012C-PromptReco-v2_TLBSM_53x_v2-e3fb55b810dc7a0811f4c66dfa2267c9/USER',
##      'number_of_jobs':'150', 'pycfg_params':'runData=1','runselection':'198934-203755','lumi_mask':'Cert_190456-203002_8TeV_PromptReco_Collisions12_JSON_MuonPhys_v2.txt' ,
##      '#sample_name': 'Data-Run2012C-PromptReco-v2-a', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##     {'datasetpath':'/SingleMu/StoreResults-Run2012C-PromptReco-v2_TLBSM_53x_v2-646f7563e9ae6f48814faa1c250f042a/USER',
##      'number_of_jobs':'150', 'pycfg_params':'runData=1','runselection':'198934-203755','lumi_mask':'Cert_190456-203002_8TeV_PromptReco_Collisions12_JSON_MuonPhys_v2.txt' ,
##      '#sample_name': 'Data-Run2012C-PromptReco-v2-b', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'},

##     {'datasetpath':'/SingleMu/StoreResults-Run2012C-PromptReco-v2_TLBSM_53x_v2_extension_v1-e3fb55b810dc7a0811f4c66dfa2267c9/USER',
##      'number_of_jobs':'50', 'pycfg_params':'runData=1','runselection':'198934-203755','lumi_mask':'Cert_190456-203002_8TeV_PromptReco_Collisions12_JSON_MuonPhys_v2.txt' ,
##      '#sample_name': 'Data-Run2012C-PromptReco-v2-c', 'dbs_url':'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet' },

    ]

for job in joblist:
    config = dummy_config

    # common input files
    config.set('USER', 'additional_input_files', 'Jec12_V3_L1FastJet_AK5PFchs.txt,Jec12_V3_L2Relative_AK5PFchs.txt,Jec12_V3_L3Absolute_AK5PFchs.txt,Jec12_V3_L2L3Residual_AK5PFchs.txt,Jec12_V3_Uncertainty_AK5PFchs.txt,Jec12_V3_MC_L1FastJet_AK5PFchs.txt,Jec12_V3_MC_L2Relative_AK5PFchs.txt,Jec12_V3_MC_L3Absolute_AK5PFchs.txt,Jec12_V3_MC_L2L3Residual_AK5PFchs.txt,Jec12_V3_MC_Uncertainty_AK5PFchs.txt,PUMC_dist_flat10.root,PUData_finebin_dist.root')
 
    # for MC we don't need this
    config.remove_option('CMSSW','runselection')
    config.remove_option('CMSSW','lumi_mask')

    # plug for data
    if 'Data' in job['#sample_name']:
        config.remove_option('CMSSW','total_number_of_events')
        config.set('CMSSW','total_number_of_lumis','-1')

    # set the CMSSW parameters
    for p in job:
        config.set('CMSSW', p, job[p])
        #if 'cms_dbs_prod_global'in job[p]:
        #config.set('CRAB', 'scheduler', 'remoteGlidein')

    if 'Data' not in job['#sample_name']:
        btagMap = job['datasetpath'].split('/')[1]
        if 'btag_map' in job.keys():
            btagMap = job['btag_map']

        config.set('CMSSW', 'pycfg_params', config.get('CMSSW', 'pycfg_params')+" btagMap="+btagMap)


    # specify the name in case of data and signal
    if 'Data' in job['#sample_name'] or 'Bprime' in job['#sample_name']:
        ui_working_dir = working_dir + job['datasetpath'].split('/')[1] + '_' + job['#sample_name'] + dir_suffix
        if 'Data' in job['#sample_name']:
            publish_data_name = 'BPrimeEDMNtuples_53x_v2_'+job['#sample_name']
    elif 'WJets_v2' in job['#sample_name']:
        publish_data_name = 'BPrimeEDMNtuples_53x_v2_WJets_v2'
        ui_working_dir = working_dir + job['datasetpath'].split('/')[1] + '_v2'+ dir_suffix
    elif 'WJets_v1' in job['#sample_name']:
        publish_data_name = 'BPrimeEDMNtuples_53x_v2_WJets_v1'
        ui_working_dir = working_dir + job['datasetpath'].split('/')[1] + '_v1'+ dir_suffix
    else:
        ui_working_dir = working_dir + job['datasetpath'].split('/')[1] + dir_suffix
        publish_data_name = 'BPrimeEDMNtuples_53x_v2'
    config.set('USER','ui_working_dir',ui_working_dir)
    config.set('USER','publish_data_name',publish_data_name)

    print 'ui', ui_working_dir
    print 'pub name',  publish_data_name
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
