#!/usr/bin/env python2.6

# get weird with it
import os
import sys
import time
import json
import pprint
from CMSYAAT.RequestManager import RequestManager

if len(sys.argv) == 2:
    jenkins = sys.argv[1]
else:
    jenkins = 'testing'

# TODO: these shouldprobably be command line options

mcSamples = [
        "/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM",
        #"/WJetsToLNu_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM",
        "/T_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "/Tbar_s-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "/T_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM",
        "/T_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v3/AODSIM",
        "/T_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "/ZJetToMuMu_Pt-0to15_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "/ZJetToMuMu_Pt-15to20_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "/ZJetToMuMu_Pt-20to30_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "/ZJetToMuMu_Pt-30to50_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "/ZJetToMuMu_Pt-50to80_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "/ZJetToMuMu_Pt-80to120_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "/ZJetToMuMu_Pt-120to170_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "/ZJetToMuMu_Pt-170to230_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",
        "/ZJetToMuMu_Pt-230to300_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM",
        "/ZJetToMuMu_Pt-300_TuneZ2star_8TeV_pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM",       
        ]

dataSamples = [ '/SingleMu/Run2012A-13Jul2012-v1/AOD',
                #'/SingleMu/Run2012A-recover-06Aug2012-v1/AOD',
                '/SingleMu/Run2012B-13Jul2012-v1/AOD',
                '/SingleMu/Run2012C-24Aug2012-v1/AOD',
                '/SingleMu/Run2012C-PromptReco-v2/AOD',
                '/SingleMu/Run2012C-EcalRecover_11Dec2012-v1/AOD',
                '/SingleMu/Run2012D-PromptReco-v1/AOD',
                '/MET/Run2012A-13Jul2012-v1/AOD',
                '/MET/Run2012A-recover-06Aug2012-v1/AOD',
                '/MET/Run2012B-13Jul2012-v1/AOD',
                '/MET/Run2012C-24Aug2012-v1/AOD',
                '/MET/Run2012C-PromptReco-v2/AOD',
                '/MET/Run2012C-EcalRecover_11Dec2012-v1/AOD',
                '/MET/Run2012D-PromptReco-v1/AOD']

reqmgr = RequestManager( 
                    endpoint = 'https://se9.accre.vanderbilt.edu:8443/reqmgr'
                 )

allSamples = []
#allSamples.extend(mcSamples)
allSamples.extend(dataSamples)

requestIDs = []

requestJSON = { "CMSSWVersion": "CMSSW_5_3_7_patch4",
            "AsyncDest": "T2_US_Vanderbilt",
            "GlobalTag": "START53_V7E::All",
            "MergedLFNBase" : "/store/user/meloam",
            "UnmergedLFNBase" : "/store/temp/user/meloam",
              "ForceUserOutput" : 1,
              "ForceUserStorage" : 1,
              "forceUserStorage" : 1,
            "RequestPriority": 100000,
            "TimePerEvent": 0.5,
            "EnableNewStageout": 1,
            "FilterEfficiency": 1,
            "ScramArch": "slc5_amd64_gcc462",
            "RequestType" : "MeloProcessing",
            "RequestNumEvents": 1,
            "inputMode": "couchDB",
            "CouchURL":"https://cmsweb.cern.ch/couchdb",
            "CouchDBName":"reqmgr_config_cache",
            "ConfigCacheID": "7ed1855e5a9e1bb01b5c7cb259450d9a",
            "EventsPerLumi": 1,
            "filterEfficiency": 1,
            "MCPileup": "",
            "FirstEvent": 1,
            "DataTier": "USER",
            "Memory": 2000000000,
            "SizePerEvent":102400000,
            "maxRSS": 4294967296,
            "maxVSize": 4294967296,
            "SoftTimeout": 36000,
            "FirstLumi": 1,
            "Requestor": "meloam",
            "Username": "meloam",
            "RequestorDN": "/DC=org/DC=doegrids/OU=People/CN=Andrew Malone Melo 788499",
            "Group": "testing",
            "TotalTime": 14400,
            "Team" : "PriorityTeam",
            "userSandbox" : "root://xrootd.unl.edu:1094//store/user/meloam/sandboxes/edmntuple-sandbox.tgz",
            "ValidStatus" : "VALID"
}

# MC   - b63b1d4634d28520e53f6b5941d33bcb
# DATA - 025b9c1b6853f78ac3bdf7091e2bc1fd
requestList = []
now = time.strftime("%Y%m%d%H%M%S", time.gmtime()) 
for sample in allSamples:
    if sample in mcSamples:
        requestJSON['ConfigCacheID'] = 'b63b1d4634d28520e53f6b5941d33bcb'
        requestJSON['GlobalTag'] = 'START53_V7E::All'
        lumiFilename = 'mc_test_wmagent.json'
        requestJSON['StdJobSplitArgs'] = {'lumis_per_job': 10}
        acqHelper = ''
        #if sample.startswith('/ZJ'):
        #    # If you have to ask, you can't afford it
        #    requestJSON['StdJobSplitArgs']['lumis'] = '1,30'
    else:
        requestJSON['ConfigCacheID'] = '025b9c1b6853f78ac3bdf7091e2bc1fd'
        requestJSON['GlobalTag'] = 'GR_P_V40_AN1::All'
        lumiFilename = 'data_all_wmagent.json'
        acqHelper = "_" + sample.split('/')[2].replace('-','_')

    lumiMask = json.loads(open(lumiFilename,'r').read())
    requestJSON['StdJobSplitArgs'] = { 'lumis_per_job' : 10,
                                       'splitOnRun' : False }
    requestJSON['StdJobSplitArgs']['runs'] = lumiMask['runs']
    requestJSON['StdJobSplitArgs']['lumis'] = lumiMask['lumis']
    requestJSON['StdJobSplitAlgo'] = 'EventAwareLumiBased'
    requestJSON["RequestString"]  = "melo_oneoff_feb12"
    requestJSON['AcquisitionEra'] = 'meloam_feb12_tlbsm53x2' + acqHelper
    requestJSON['ProcessingVersion'] = now
    requestJSON['InputDataset'] = sample
    newRequest = reqmgr.newRequest()
    newRequest.setRequestDict( requestJSON )
    print "Doing %s" % sample
    reqmgr.submitRequest( newRequest )
    print newRequest.getWorkflowName()
    requestList.append(newRequest)
