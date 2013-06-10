import FWCore.ParameterSet.Config as cms
#from PhysicsTools.PatAlgos.patTemplate_cfg import *
#from PhysicsTools.PatAlgos.tools.coreTools import *

process = cms.Process("KinFit")

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

options.register('sampleNameInput',
                 'Wjets',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Sample name to give histograms")

options.register('ignoreTrigger',
                 1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")

options.register('runLoose',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Run extra sequence(1) for loose selction or ignore them (0)")

options.parseArguments()

print options

import sys

inputDoMC=True
inputSampleName = options.sampleNameInput


inputCutsToIgnore = []
if options.ignoreTrigger == 1 :
    inputCutsToIgnore.append( 'Trigger' )

## Source
if len(options.inputFiles) == 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
        '/store/user/lpctlbsm/samvel/T_TuneZ2_s-channel_7TeV-powheg-tauola/prod_2011_10_03_17_19_46/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_9_1_3hF.root',
        '/store/user/lpctlbsm/samvel/T_TuneZ2_s-channel_7TeV-powheg-tauola/prod_2011_10_03_17_19_46/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_8_1_h4D.root',
        '/store/user/lpctlbsm/samvel/T_TuneZ2_s-channel_7TeV-powheg-tauola/prod_2011_10_03_17_19_46/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_7_1_wtz.root',
        '/store/user/lpctlbsm/samvel/T_TuneZ2_s-channel_7TeV-powheg-tauola/prod_2011_10_03_17_19_46/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_6_1_j9k.root',
        '/store/user/lpctlbsm/samvel/T_TuneZ2_s-channel_7TeV-powheg-tauola/prod_2011_10_03_17_19_46/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_5_1_uuM.root',
        '/store/user/lpctlbsm/samvel/T_TuneZ2_s-channel_7TeV-powheg-tauola/prod_2011_10_03_17_19_46/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_4_1_leZ.root',
        '/store/user/lpctlbsm/samvel/T_TuneZ2_s-channel_7TeV-powheg-tauola/prod_2011_10_03_17_19_46/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_3_1_47a.root',
        '/store/user/lpctlbsm/samvel/T_TuneZ2_s-channel_7TeV-powheg-tauola/prod_2011_10_03_17_19_46/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_2_1_ynz.root',
        '/store/user/lpctlbsm/samvel/T_TuneZ2_s-channel_7TeV-powheg-tauola/prod_2011_10_03_17_19_46/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_1_1_DUD.root',
        '/store/user/lpctlbsm/samvel/T_TuneZ2_s-channel_7TeV-powheg-tauola/prod_2011_10_03_17_19_46/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_11_1_YQG.root',
        '/store/user/lpctlbsm/samvel/T_TuneZ2_s-channel_7TeV-powheg-tauola/prod_2011_10_03_17_19_46/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_10_1_7UM.root',
        )
                                )                           

payloads = [
  
    'Jec12_V1_L1FastJet_AK5PFchs.txt',
    'Jec12_V1_L2Relative_AK5PFchs.txt',
    'Jec12_V1_L3Absolute_AK5PFchs.txt',
    'Jec12_V1_L2L3Residual_AK5PFchs.txt',
    'Jec12_V1_Uncertainty_AK5PFchs.txt',    
]
## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

#_________________________________Pileup___________________________________
## process.pileupReweightingProducer = cms.EDProducer("PileupReweightingPoducer",
##                                          FirstTime = cms.untracked.bool(False),
##                                          PileupMCFile = cms.untracked.string('PUMC_dist_flat10.root'),
##                                          PileupDataFile = cms.untracked.string('PUData_finebin_dist.root')
## )

process.pileupReweightingProducer = cms.EDProducer("PileupReweightingPoducer",
                                         FirstTime = cms.untracked.bool(False),
                                         oneDReweighting = cms.untracked.bool(True),
                                         PileupMCFile = cms.untracked.string('PUMC_dist_flat10.root'),
                                         PileupDataFile = cms.untracked.string('PUData_finebin_dist.root')
)

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis

#_______________________________BTagging SF______________________________________________
process.load("CondCore.DBCommon.CondDBCommon_cfi")
#Data measurements from Summer11
process.load ("RecoBTag.PerformanceDB.BTagPerformanceDB1107")
process.load ("RecoBTag.PerformanceDB.PoolBTagPerformanceDB1107")

process.goodPatJetsPFlowSF = cms.EDProducer("BTaggingSFProducer",
                                            jetSource = cms.InputTag('goodPatJetsPFlow'),
                                            Tagger = cms.string('combinedSecondaryVertexBJetTags'),
                                            DiscriminantValue = cms.double(0.679)
                                            )

#_____________________________________PF__________________________________________________

process.pfShyftSkim =  cms.EDFilter('EDWPlusJetsSelector',
                                    inputShyftAnalysis.clone(
    muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
    electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
    metSrc = cms.InputTag('patMETsPFlow'),
    jetSrc = cms.InputTag('goodPatJetsPFlowSF'),
    pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
    ePlusJets = cms.bool( False ),
    muPlusJets = cms.bool( True ),
    jetPtMin = cms.double(35.0),##
    minJets = cms.int32(4),##
    metMin = cms.double(0.0),
    muPtMin = cms.double(35.0),
    identifier = cms.string('PFMu'),
    cutsToIgnore=cms.vstring( inputCutsToIgnore ),
    reweightPU = cms.bool(False),
    useData = cms.bool( not inputDoMC ),
    sampleName = cms.string(inputSampleName),
    doMC = cms.bool( inputDoMC),
    jetAlgo = cms.string("pf"),
    jetSmear = cms.double(0.1),
    jecPayloads = cms.vstring( payloads )
    )
                                    )

#____________________JES up and down _______________________

process.pfShyftSkimJES095 = process.pfShyftSkim.clone()
process.pfShyftSkimJES095.jetScale = cms.double(-1.0)
process.pfShyftSkimJES095.jetUncertainty = cms.double(0.0)
process.pfShyftSkimJES095.identifier = cms.string('PFJES095')

process.pfShyftSkimJES105 = process.pfShyftSkim.clone()
process.pfShyftSkimJES105.jetScale = cms.double(1.0)
process.pfShyftSkimJES105.jetUncertainty = cms.double(0.0)
process.pfShyftSkimJES105.identifier = cms.string('PFJES105')


#________________ JER up and down__________________

process.pfShyftSkimJER000 = process.pfShyftSkim.clone()
process.pfShyftSkimJER000.jetSmear = cms.double(0.00)
process.pfShyftSkimJER000.identifier = cms.string('PFJER000')

process.pfShyftSkimJER020 = process.pfShyftSkim.clone()
process.pfShyftSkimJER020.jetSmear = cms.double(0.20)
process.pfShyftSkimJER020.identifier = cms.string('PFJER020')
    


############################
## adding KinFitter stuff
############################

from TopQuarkAnalysis.TopObjectResolutions.stringResolutions_etEtaPhi_cff import *

# original version /TopQuarkAnalysis/TopKinFitter/python/TtSemiLepKinFitProducer_Electrons_cfi.p
# using CSVMnoSF b-tagger
process.kinFitTtSemiLepEventCSVMnoSF = cms.EDProducer("TtSemiLepKinFitProducerMuon",
    jets = cms.InputTag("pfShyftSkim:jets"),
    leps = cms.InputTag("pfShyftSkim:muons"),
    mets = cms.InputTag("pfShyftSkim:met"),

    # ------------------------------------------------
    # maximum number of jets to be considered in the
    # jet combinatorics (has to be >= 4, can be set to
    # -1 if you want to take all)
    # ------------------------------------------------
    maxNJets = cms.int32(5),

    #-------------------------------------------------
    # maximum number of jet combinations finally
    # written into the event, starting from the "best"
    # (has to be >= 1, can be set to -1 if you want to 
    # take all)
    #-------------------------------------------------
    maxNComb = cms.int32(2),

    # ------------------------------------------------
    # option to take only a given jet combination
    # instead of going through the full combinatorics
    # ------------------------------------------------
    match = cms.InputTag(""),
    useOnlyMatch = cms.bool(False),

    # ------------------------------------------------
    # option to use b-tagging
    # ------------------------------------------------
    bTagAlgo          = cms.string("combinedSecondaryVertexBJetTags"),
    minBDiscBJets     = cms.double(0.679),
    maxBDiscLightJets = cms.double(0.679),
    useBTagging       = cms.bool(True),

    # ------------------------------------------------
    # option to use the btagger of choice: -1 -- ignore, 1 -- right out of the box,
    # 2 -- Nominal SF, 4 -- SF up, 8 -- SF down.
    # ------------------------------------------------                                                                                                    
    btaggingIncludingSF = cms.int32(-1),                                                      
    # ------------------------------------------------
    # settings for the KinFitter
    # ------------------------------------------------    
    maxNrIter = cms.uint32(500),
    maxDeltaS = cms.double(5e-05),
    maxF      = cms.double(0.0001),
    # ------------------------------------------------
    # select parametrisation
    # 0: EMom, 1: EtEtaPhi, 2: EtThetaPhi
    # ------------------------------------------------
    jetParametrisation = cms.uint32(1),
    lepParametrisation = cms.uint32(1),
    metParametrisation = cms.uint32(1),

    jetEnergyResolutionSmearFactor = cms.double(1.0),
    # ------------------------------------------------
    # set constraints
    # 1: Whad-mass, 2: Wlep-mass, 3: thad-mass,
    # 4: tlep-mass, 5: nu-mass, 6: equal t-masses,
    # by default: Px conservation and Py conservation
    # ------------------------------------------------                                   
    constraints = cms.vuint32(1, 2, 6),

    # ------------------------------------------------
    # set mass values used in the constraints
    # ------------------------------------------------    
    mW   = cms.double(80.4),
    mTop = cms.double(173.),
                                              
    # using new object resolutions
    udscResolutions             = udscResolutionPF.functions,
    bResolutions                = bjetResolutionPF.functions,
    lepResolutions              = elecResolution.functions,
    metResolutions              = metResolutionPF.functions,
                                        )


process.tprimeNtupleDumperCSVMnoSF = cms.EDProducer("TprimeNtupleDumper",
                                                    do_MC = cms.bool(False),
                                                    resonanceId = cms.int32(6), 
                                                    kinFitterLabel = cms.string("kinFitTtSemiLepEventCSVMnoSF"),
                                                    selectorLabel  = cms.string("pfShyftSkim"),
                                                    )
# add pure min Chi2 with CSVM for comparison
process.kinFitTtSemiLepEventCHI2 = process.kinFitTtSemiLepEventCSVMnoSF.clone()
process.kinFitTtSemiLepEventCHI2.useBTagging = False

process.tprimeNtupleDumperCHI2 = process.tprimeNtupleDumperCSVMnoSF.clone()
process.tprimeNtupleDumperCHI2.kinFitterLabel = cms.string("kinFitTtSemiLepEventCHI2")

# add the use of CSVM tagger with SF included
process.kinFitTtSemiLepEventCSVM = process.kinFitTtSemiLepEventCSVMnoSF.clone()
process.kinFitTtSemiLepEventCSVM.useBTagging = True
# ------------------------------------------------
# option to use the btagger of choice: 1 -- right out of the box,
# 2 -- Nominal SF, 4 -- SF up, 8 -- SF down.
# ------------------------------------------------
process.kinFitTtSemiLepEventCSVM.btaggingIncludingSF = 2

process.tprimeNtupleDumperCSVM = process.tprimeNtupleDumperCSVMnoSF.clone()
process.tprimeNtupleDumperCSVM.kinFitterLabel = cms.string("kinFitTtSemiLepEventCSVM")

################################################
#_______________Systematics__________________
#################################################

# CSVM b-tagging
# --------------
# btagging up
process.kinFitTtSemiLepEventCSVMBTagSFup = process.kinFitTtSemiLepEventCSVM.clone()
process.kinFitTtSemiLepEventCSVMBTagSFup.btaggingIncludingSF = 4 #4 -- SF up

process.tprimeNtupleDumperCSVMBTagSFup = process.tprimeNtupleDumperCSVM.clone()
process.tprimeNtupleDumperCSVMBTagSFup.kinFitterLabel = cms.string("kinFitTtSemiLepEventCSVMBTagSFup")
process.tprimeNtupleDumperCSVMBTagSFup.selectorLabel  = cms.string("pfShyftSkimBTagSFup")

# btagging down
process.kinFitTtSemiLepEventCSVMBTagSFdown = process.kinFitTtSemiLepEventCSVM.clone()
process.kinFitTtSemiLepEventCSVMBTagSFdown.btaggingIncludingSF = 8 #8 -- SF down

process.tprimeNtupleDumperCSVMBTagSFdown = process.tprimeNtupleDumperCSVM.clone()
process.tprimeNtupleDumperCSVMBTagSFdown.kinFitterLabel = cms.string("kinFitTtSemiLepEventCSVMBTagSFdown")
process.tprimeNtupleDumperCSVMBTagSFdown.selectorLabel  = cms.string("pfShyftSkimBTagSFdown")

# JER up
process.kinFitTtSemiLepEventCSVMJER000 = process.kinFitTtSemiLepEventCSVM.clone()
process.kinFitTtSemiLepEventCSVMJER000.jets = cms.InputTag("pfShyftSkimJER000:jets")
process.kinFitTtSemiLepEventCSVMJER000.leps = cms.InputTag("pfShyftSkimJER000:muons")
process.kinFitTtSemiLepEventCSVMJER000.mets = cms.InputTag("pfShyftSkimJER000:met")

process.tprimeNtupleDumperCSVMJER000 = process.tprimeNtupleDumperCSVM.clone()
process.tprimeNtupleDumperCSVMJER000.kinFitterLabel = cms.string("kinFitTtSemiLepEventCSVMJER000")
process.tprimeNtupleDumperCSVMJER000.selectorLabel  = cms.string("pfShyftSkimJER000")

# JER down
process.kinFitTtSemiLepEventCSVMJER020 = process.kinFitTtSemiLepEventCSVM.clone()
process.kinFitTtSemiLepEventCSVMJER020.jets = cms.InputTag("pfShyftSkimJER020:jets")
process.kinFitTtSemiLepEventCSVMJER020.leps = cms.InputTag("pfShyftSkimJER020:muons")
process.kinFitTtSemiLepEventCSVMJER020.mets = cms.InputTag("pfShyftSkimJER020:met")

process.tprimeNtupleDumperCSVMJER020 = process.tprimeNtupleDumperCSVM.clone()
process.tprimeNtupleDumperCSVMJER020.kinFitterLabel = cms.string("kinFitTtSemiLepEventCSVMJER020")
process.tprimeNtupleDumperCSVMJER020.selectorLabel  = cms.string("pfShyftSkimJER020")

# JES up
process.kinFitTtSemiLepEventCSVMJES095 = process.kinFitTtSemiLepEventCSVM.clone()
process.kinFitTtSemiLepEventCSVMJES095.jets = cms.InputTag("pfShyftSkimJES095:jets")
process.kinFitTtSemiLepEventCSVMJES095.leps = cms.InputTag("pfShyftSkimJES095:muons")
process.kinFitTtSemiLepEventCSVMJES095.mets = cms.InputTag("pfShyftSkimJES095:met")

process.tprimeNtupleDumperCSVMJES095 = process.tprimeNtupleDumperCSVM.clone()
process.tprimeNtupleDumperCSVMJES095.kinFitterLabel = cms.string("kinFitTtSemiLepEventCSVMJES095")
process.tprimeNtupleDumperCSVMJES095.selectorLabel  = cms.string("pfShyftSkimJES095")

# JES down
process.kinFitTtSemiLepEventCSVMJES105 = process.kinFitTtSemiLepEventCSVM.clone()
process.kinFitTtSemiLepEventCSVMJES105.jets = cms.InputTag("pfShyftSkimJES105:jets")
process.kinFitTtSemiLepEventCSVMJES105.leps = cms.InputTag("pfShyftSkimJES105:muons")
process.kinFitTtSemiLepEventCSVMJES105.mets = cms.InputTag("pfShyftSkimJES105:met")

process.tprimeNtupleDumperCSVMJES105 = process.tprimeNtupleDumperCSVM.clone()
process.tprimeNtupleDumperCSVMJES105.kinFitterLabel = cms.string("kinFitTtSemiLepEventCSVMJES105")
process.tprimeNtupleDumperCSVMJES105.selectorLabel  = cms.string("pfShyftSkimJES105")

# minimum Chi2:
#-------------
# JES up
process.kinFitTtSemiLepEventCHI2JES095 = process.kinFitTtSemiLepEventCHI2.clone()
process.kinFitTtSemiLepEventCHI2JES095.jets = cms.InputTag("pfShyftSkimJES095:jets")
process.kinFitTtSemiLepEventCHI2JES095.leps = cms.InputTag("pfShyftSkimJES095:muons")
process.kinFitTtSemiLepEventCHI2JES095.mets = cms.InputTag("pfShyftSkimJES095:met")

process.tprimeNtupleDumperCHI2JES095 = process.tprimeNtupleDumperCHI2.clone()
process.tprimeNtupleDumperCHI2JES095.kinFitterLabel = cms.string("kinFitTtSemiLepEventCHI2JES095")
process.tprimeNtupleDumperCHI2JES095.selectorLabel  = cms.string("pfShyftSkimJES095")

# JES down
process.kinFitTtSemiLepEventCHI2JES105 = process.kinFitTtSemiLepEventCHI2.clone()
process.kinFitTtSemiLepEventCHI2JES105.jets = cms.InputTag("pfShyftSkimJES105:jets")
process.kinFitTtSemiLepEventCHI2JES105.leps = cms.InputTag("pfShyftSkimJES105:muons")
process.kinFitTtSemiLepEventCHI2JES105.mets = cms.InputTag("pfShyftSkimJES105:met")

process.tprimeNtupleDumperCHI2JES105 = process.tprimeNtupleDumperCHI2.clone()
process.tprimeNtupleDumperCHI2JES105.kinFitterLabel = cms.string("kinFitTtSemiLepEventCHI2JES105")
process.tprimeNtupleDumperCHI2JES105.selectorLabel  = cms.string("pfShyftSkimJES105")

################################################

process.p0 = cms.Path( process.pileupReweightingProducer * process.goodPatJetsPFlowSF )

process.p1 = cms.Path( process.pfShyftSkim * (process.kinFitTtSemiLepEventCHI2 * process.tprimeNtupleDumperCHI2 +
                                              process.kinFitTtSemiLepEventCSVM * process.tprimeNtupleDumperCSVM +
                                              process.kinFitTtSemiLepEventCSVMBTagSFup * process.tprimeNtupleDumperCSVMBTagSFup +
                                              process.kinFitTtSemiLepEventCSVMBTagSFdown * process.tprimeNtupleDumperCSVMBTagSFdown 
                                            )
                       )

process.p2 = cms.Path( process.pfShyftSkimJES095 * (process.kinFitTtSemiLepEventCSVMJES095 * process.tprimeNtupleDumperCSVMJES095
                                                    )
                       )

process.p3 = cms.Path( process.pfShyftSkimJES105 * (process.kinFitTtSemiLepEventCSVMJES105 * process.tprimeNtupleDumperCSVMJES105
                                                    )
                       )

process.p4 = cms.Path( process.pfShyftSkimJER020 * (process.kinFitTtSemiLepEventCSVMJER020 * process.tprimeNtupleDumperCSVMJER020
                                                    )
                       )

process.p5 = cms.Path( process.pfShyftSkimJER000 * (process.kinFitTtSemiLepEventCSVMJER000 * process.tprimeNtupleDumperCSVMJER000
                                                   )
                       )


process.out = cms.OutputModule("PoolOutputModule",
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring( 'p1','p2','p3','p4','p5') ),
                               )



process.out.fileName =  cms.untracked.string('ttTest_mu.root')
process.out.outputCommands = cms.untracked.vstring('drop *')


process.out.outputCommands += ['keep *_kinFitTtSemiLepEvent*_*_*',
                               'keep *_pfShyftSkim*_*_*',
                               'keep *_tprimeNtupleDumper*_*_*',
                               'keep PileupSummaryInfos_*_*_*',
                               'keep *_goodOfflinePrimaryVertices_*_*',
                               'keep *_prunedGenParticles_*_*',
                               'keep *_*_pileupWeights_*'
                               ]


#process.out.dropMetaData = cms.untracked.string("DROPPED")

## output path
process.outpath = cms.EndPath(process.out)

## process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
## process.MessageLogger.suppressWarning.append('patTrigger')
## process.MessageLogger.cerr.FwkJob.limit=1
## process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) )

open('junk.py','w').write(process.dumpPython())
