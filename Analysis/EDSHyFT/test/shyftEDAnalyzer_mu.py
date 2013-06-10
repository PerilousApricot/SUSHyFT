import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

#input stuff for Run/Lumi selection with the "JSON"-formatted files from the PVT group
import FWCore.PythonUtilities.LumiList as LumiList


## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('useFlavorHistory',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Flavor History Mode")

options.register ('doMC',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Use MC truth")

options.register ('sampleNameInput',
                  'top',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "Sample name to give histograms")

options.register ('outputRootFile',
                  'shyftStudies.root',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "Output root file name")

options.register('ignoreTrigger',
                 0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")

options.register('triggerName',
                 'HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v1',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Electron/Muon trigger to run")

options.register('ttbsmPAT',
                 1,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "If running on ttbsm PAT tuples"
                 )
options.register('use42X',
                 1,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "PAT tuplese done in 4_2_2"
                 )

options.parseArguments()

print options

import sys

if options.useFlavorHistory > 0 :
    useFlavorHistory = True
else :
    useFlavorHistory = False

if options.doMC > 0 :
    inputDoMC = True
else :
    inputDoMC = False
    # get JSON file correctly parced
    JSONfile = 'Cert_160404-167913_7TeV_PromptReco_Collisions11_JSON.txt'
    myList = LumiList.LumiList (filename = JSONfile).getCMSSWString().split(',')


inputSampleName = options.sampleNameInput

inputCutsToIgnore = []
if options.ignoreTrigger == 1 :
    inputCutsToIgnore.append( 'Trigger' )

## Source
if len(options.inputFiles) == 0  and options.ttbsmPAT > 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
				'/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v8_Run2011-PromptReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_223_2_BE0.root',
        '/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v8_Run2011-PromptReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_9_1_Pba.root',
        '/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v8_Run2011-PromptReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_99_1_J5T.root',
        '/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v8_Run2011-PromptReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_98_1_w0Q.root',
        '/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v8_Run2011-PromptReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_97_1_cw1.root',
        '/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v8_Run2011-PromptReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_96_1_uJW.root',
        '/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v8_Run2011-PromptReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_95_1_qrp.root',
        '/store/user/lpctlbsm/srappocc/SingleMu/ttbsm_v8_Run2011-PromptReco/0d3d9a54f3a29af186ad87df2a0c3ce1/ttbsm_42x_data_94_2_J6v.root'
        )
                                )
    
elif len(options.inputFiles) == 0  and options.ttbsmPAT == 0 and not options.use42X :  
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_9_1_drw.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_96_1_0fn.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_95_1_JQ3.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_94_1_58x.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_93_1_2Y9.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_92_1_ezw.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_91_1_iUf.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_90_1_JGA.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_8_1_d1I.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_89_1_eod.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_88_1_zha.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_87_1_odL.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_86_1_jGO.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_85_1_kNr.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_84_1_mnY.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_83_1_LnL.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_82_1_9tr.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_81_1_1f1.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_80_1_tyX.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_7_1_JR7.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_79_1_RRB.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_78_1_0Cw.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_77_1_mBd.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_76_1_WRY.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_75_1_svK.root',
        '/store/user/skhalil/SingleElectron/SingleElectron_Run2011A-PromptReco_shyft_414_v1/6d0f840ee9d905cf3aa2d7f7eaf89508/shyft_414patch1_mu_74_1_7zu.root',
        )
                                )
else :
    filelist = open( options.inputFiles[0], 'r' )
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
        filelist.readlines()
        )
                                )
    
if inputDoMC == False :
    process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange( myList )

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )


## Geometry and Detector Conditions (needed for a few patTuple production steps)
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'GR_R_42_V12::All'
process.load("Configuration.StandardSequences.MagneticField_cff")

# run the trigger on the fly
process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff')

payloads = [
    'Jec12_V1_L1FastJet_AK5PFchs.txt',
    'Jec12_V1_L2Relative_AK5PFchs.txt',
    'Jec12_V1_L3Absolute_AK5PFchs.txt',
    'Jec12_V1_L2L3Residual_AK5PFchs.txt',
    'Jec12_V1_Uncertainty_AK5PFchs.txt'
]

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(options.outputRootFile)
                                   )
if options.ttbsmPAT > 0 and options.use42X > 0:
    process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                        shyftAnalysis = inputShyftAnalysis.clone(
        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
        metSrc = cms.InputTag('patMETsPFlow'),
        jetSrc = cms.InputTag('goodPatJetsPFlow'),
        ePlusJets = cms.bool( False ),
        muPlusJets = cms.bool( True ),
        eleTrig = cms.string(options.triggerName),	
        pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
        jetPtMin = cms.double(30.0),##
        minJets = cms.int32(5),
        metMin = cms.double(30.0),
	muPtMin = cms.double(35.0),
	muTrig = cms.string(options.triggerName),
        use42X  = cms.bool(True),
        useData = cms.bool( not inputDoMC ),       
        heavyFlavour = cms.bool( useFlavorHistory ),
        doMC = cms.bool( inputDoMC),
        sampleName = cms.string(inputSampleName),
        identifier = cms.string('PF'),
        cutsToIgnore=cms.vstring(inputCutsToIgnore),
        jecPayloads = cms.vstring( payloads )
        
        )
                                        )
    process.pfShyftAnaLooseNoMETWithD0 = process.pfShyftAna.clone(
  	shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
  	muonSrc = cms.InputTag('selectedPatMuonsLoosePFlow'),
       	metMin = cms.double(0.0),
       	identifier = cms.string('PF Loose no MET with D0 Cut'),
       	muonIdTight = process.pfShyftAna.shyftAnalysis.muonIdTight.clone(
                    cutsToIgnore=cms.vstring('PFIso')
                                     ),
    )
)
    
elif options.ttbsmPAT == 0 and options.use42X == 0:
    process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
        metSrc = cms.InputTag('patMETsPFlow'),
        jetSrc = cms.InputTag('selectedPatJetsPFlow'),
        ePlusJets = cms.bool( False ),
        muPlusJets = cms.bool( True ),
        eleTrig = cms.string(options.triggerName),	
        useEleMC = cms.bool(False),
        useAntiSelection = cms.bool(False),
        jetPtMin = cms.double(30.0),##
        minJets = cms.int32(5),
        metMin = cms.double(30.0),
        useData = cms.bool( not inputDoMC ),
        heavyFlavour = cms.bool( useFlavorHistory ),
        doMC = cms.bool( inputDoMC),
        useTTBSMPat = cms.bool(False),
        sampleName = cms.string(inputSampleName),
        identifier = cms.string('PF'),
        cutsToIgnore=cms.vstring(inputCutsToIgnore),
        )                                    
                                        )
    
process.pfShyftAnaNoMET = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    identifier = cms.string('PF no MET')
    )
    )

process.pfShyftAnaMETMax20 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    metMax = cms.double(20.),
    identifier = cms.string('PF MET < 20')
    )
    )

process.p = cms.Path(
    process.patTriggerDefaultSequence*
    process.pfShyftAna*
    process.pfShyftAnaNoMET*              
#    process.pfShyftAnaMETMax20
    process.pfShyftAnaLooseNoMETWithD0
    )

#suppress the L1 trigger error messages
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.suppressWarning.append('patTrigger')
process.MessageLogger.cerr.FwkJob.limit=1
process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit =
cms.untracked.int32(0) )
