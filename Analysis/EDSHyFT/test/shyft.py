

# SHyFT configuration
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *


###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('useData',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run this on real data")

options.register ('hltProcess',
                  'HLT',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "HLT process name to use.")

options.register ('useMuon',
                  1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Use muons (1) or electrons (0)")

options.register ('slimOutput',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Remove several heavy collections for systematic samples")

options.parseArguments()

print options

import sys

# Set to true for running on data
useData = options.useData
# muons
useMuon = options.useMuon

if options.useData == False :
    # Make sure to NOT apply L2L3Residual to MC
    corrections = ['L1Offset', 'L2Relative', 'L3Absolute']
    # global tag for 384 MC
    process.GlobalTag.globaltag = cms.string('START311_V2::All')
else :
    # Make sure to apply L2L3Residual to data
    corrections = ['L1Offset', 'L2Relative', 'L3Absolute', 'L2L3Residual']
    # global tag for 386 data
    process.GlobalTag.globaltag = cms.string('GR_R_311_V2::All')


# require HLT_Mu9 trigger
from HLTrigger.HLTfilters.hltHighLevel_cfi import *


# HB + HE noise filtering
process.load('CommonTools/RecoAlgos/HBHENoiseFilter_cfi')

# add the flavor history
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")

 
# get the 7 TeV jet corrections
from PhysicsTools.PatAlgos.tools.jetTools import *



# require physics declared
process.load('HLTrigger.special.hltPhysicsDeclared_cfi')
process.hltPhysicsDeclared.L1GtReadoutRecordTag = 'gtDigis'

# require scraping filter
process.scrapingVeto = cms.EDFilter("FilterOutScraping",
                                    applyfilter = cms.untracked.bool(True),
                                    debugOn = cms.untracked.bool(False),
                                    numtrack = cms.untracked.uint32(10),
                                    thresh = cms.untracked.double(0.2)
                                    )


# switch on PAT trigger
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
switchOnTrigger( process )
process.patTriggerEvent.processName = cms.string( options.hltProcess )
process.patTrigger.processName = cms.string( options.hltProcess )


process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
                                           vertexCollection = cms.InputTag('offlinePrimaryVertices'),
                                           minimumNDOF = cms.uint32(4) ,
                                           maxAbsZ = cms.double(24.0), 
                                           maxd0 = cms.double(2) 
                                           )

# Now add the two PF sequences, one for the tight leptons, the other for the loose.
# For both, do the fastjet area calculation for possible pileup subtraction correction. 

from PhysicsTools.PatAlgos.tools.pfTools import *
postfix = "PFlow"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC= not useData, postfix=postfix) 

postfixLoose = "PFlowLoose"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC= not useData, postfix=postfixLoose)

# We'll be using a lot of AOD so re-run b-tagging to get the
# tag infos which are dropped in AOD
switchJetCollection(process,cms.InputTag('ak5PFJets'),
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = ('AK5PF', cms.vstring(corrections)),
                 doType1MET   = True,
                 genJetCollection=cms.InputTag("ak5GenJets"),
                 doJetID      = True
                 )

# tcMET
from PhysicsTools.PatAlgos.tools.metTools import *
addPfMET(process, 'PF')





# Selection
process.selectedPatJetsPFlow.cut = cms.string('pt > 20 & abs(eta) < 2.4')
process.selectedPatJetsPFlowLoose.cut = cms.string('pt > 20 & abs(eta) < 2.4')
process.selectedPatJets.cut = cms.string('pt > 20 & abs(eta) < 2.4')


process.patJets.addTagInfos = True
process.patJetsPFlow.addTagInfos = True
process.patJetsPFlowLoose.addTagInfos = True
process.patJets.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAOD")
    )
process.patJetsPFlow.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAOD" + postfix)
    )
process.patJetsPFlowLoose.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAOD" + postfixLoose)
    )


#remove isolation from the PFlow
process.patMuonsPFlowLoose.pfMuonSource = 'pfAllMuonsPFlowLoose'
process.patMuonsPFlowLoose.isoDeposits = cms.PSet()
process.patMuonsPFlowLoose.isolationValues = cms.PSet()
process.patElectronsPFlowLoose.pfElectronSource = 'pfAllElectronsPFlowLoose'
process.patElectronsPFlowLoose.isoDeposits = cms.PSet()
process.patElectronsPFlowLoose.isolationValues = cms.PSet()

#Muons
process.selectedPatMuons.cut = cms.string("pt > 10")
process.selectedPatMuonsPFlow.cut = cms.string("pt > 10")
process.selectedPatMuonsPFlowLoose.cut = cms.string("pt > 10")
process.patMuons.usePV = False
process.patMuonsPFlow.usePV = False
process.patMuonsPFlowLoose.usePV = False

process.patMuons.embedTrack = True
process.patMuonsPFlow.embedTrack = True
process.patMuonsPFlowLoose.embedTrack = True

#Electrons
#process.selectedPatElectrons.cut = cms.string("pt > 10")
#process.selectedPatElectronsPFlow.cut = cms.string("pt > 10")
#process.selectedPatElectronsPFlowLoose.cut = cms.string("pt > 10")
process.patElectrons.usePV = False
process.patElectronsPFlow.usePV = False
process.patElectronsPFlowLoose.usePV = False

process.patElectrons.embedTrack = True
process.patElectronsPFlow.embedTrack = True
process.patElectronsPFlowLoose.embedTrack = True

#turn to false when running on data
if useData :
    removeMCMatching(process, ['All'])
    removeMCMatching(process, ['METs'], postfix='PF')    

#insert partner track info, dist and dcot for conversion rejection
process.patElectronsUserData = cms.EDProducer(
    "PATElectronUserData",
    src = cms.InputTag("patElectrons"),
	useData = cms.bool(useData==1)
)	

process.patElectronsPFlowUserData = cms.EDProducer(
    "PATElectronUserData",
    src = cms.InputTag("patElectronsPFlow"),
	useData = cms.bool(useData==1)
)

process.patElectronsPFlowLooseUserData = cms.EDProducer(
    "PATElectronUserData",
    src = cms.InputTag("patElectronsPFlowLoose"),
	useData = cms.bool(useData==1)
)

#Embed the user data process into the PAT sequence and tell selectedPatElectrons(PFlow) to use the new user collection as input
process.patDefaultSequence.replace(getattr(process,"patElectrons"),getattr(process,"patElectrons")*process.patElectronsUserData)
process.selectedPatElectrons.src = "patElectronsUserData"
process.selectedPatElectrons.cut = cms.string("et > 20 & abs(eta)<3")

process.patDefaultSequencePFlow.replace(getattr(process,"patElectronsPFlow"),getattr(process,"patElectronsPFlow")*process.patElectronsPFlowUserData)
process.selectedPatElectronsPFlow.src = "patElectronsPFlowUserData"
process.selectedPatElectronsPFlow.cut = cms.string("et > 20 & abs(eta)<3")

process.patDefaultSequencePFlowLoose.replace(getattr(process,"patElectronsPFlowLoose"),getattr(process,"patElectronsPFlowLoose")*process.patElectronsPFlowLooseUserData)
process.selectedPatElectronsPFlowLoose.src = "patElectronsPFlowLooseUserData"
process.selectedPatElectronsPFlowLoose.cut = cms.string("et > 20 & abs(eta)<3")


#secvtxMass as user data
process.patJets.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJets.userData.userFunctionLabels = cms.vstring('secvtxMass')


process.patJetsPFlow.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJetsPFlow.userData.userFunctionLabels = cms.vstring('secvtxMass')


process.patJetsPFlowLoose.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJetsPFlowLoose.userData.userFunctionLabels = cms.vstring('secvtxMass')


process.patTaus.isoDeposits = cms.PSet()
process.patTausPFlow.isoDeposits = cms.PSet()
process.patTausPFlowLoose.isoDeposits = cms.PSet()

process.patJets.embedPFCandidates = True
process.patJets.embedCaloTowers = True
process.patJetsPFlow.embedCaloTowers = True
process.patJetsPFlow.embedPFCandidates = True
process.patJetsPFlowLoose.embedCaloTowers = True
process.patJetsPFlowLoose.embedPFCandidates = True




# prune gen particles
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")


process.prunedGenParticles = cms.EDProducer("GenParticlePruner",
                                            src = cms.InputTag("genParticles"),
                                            select = cms.vstring(
                                                "drop  *",
                                                "keep status = 3", #keeps all particles from the hard matrix element
                                                "+keep (abs(pdgId) = 11 | abs(pdgId) = 13) & status = 1" #keeps all stable muons and electrons and their (direct) mothers.
                                                )
                                            )


# Add the files 
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()

if useData :

    if useMuon:
        readFiles.extend( [
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/329/C6BB9308-2F4E-E011-BDB2-0030487A17B8.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/377/FA349E81-0C4F-E011-918A-0030487CD6B4.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/379/508FB370-0C4F-E011-93DC-0030487CD7B4.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/383/DC057254-0D4F-E011-B6D7-0030487CD77E.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/384/02891170-084F-E011-AFA5-0030487C6090.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/386/486860D1-0A4F-E011-B826-0030487CD6DA.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/403/48410433-364F-E011-8F0C-001D09F23D1D.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/404/823DE1A5-374F-E011-A5C0-0030487CD906.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/405/4642D954-D64F-E011-8280-003048F024DE.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/406/50A4D30B-5A4F-E011-AAD8-0030487CD906.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/406/CC18CBF0-5F4F-E011-915F-0030487C6A66.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/406/CEDF54F6-574F-E011-BF5D-0030487CD6E8.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/410/46231D2E-604F-E011-8355-0030487C2B86.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/413/048A81DD-EA4F-E011-B73D-0030487CD6D2.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/413/2CCB00F3-924F-E011-85E7-0030487A1884.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/413/32E839DD-974F-E011-A15D-0030487CD76A.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/413/58B9EE73-964F-E011-A1A3-0030487A1884.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/413/740EDDCC-9C4F-E011-AF2B-0030487CD14E.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/413/A4AC1A65-944F-E011-A96B-003048F024FA.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/413/BC6DCF3D-924F-E011-BE4A-0030487CD180.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/413/C23AB560-A24F-E011-A764-0030487CD7EE.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/413/D0F29DA7-934F-E011-98CB-003048F1183E.root',
            '/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/413/D6401F96-984F-E011-BCBE-0030487CD7EE.root',
            ] );
    else:    
        readFiles.extend( [
            '/store/data/Run2011A/SingleElectron/AOD/PromptReco-v1/000/161/217/08AE9834-1B57-E011-981D-003048F11C28.root',
            '/store/data/Run2011A/SingleElectron/AOD/PromptReco-v1/000/161/217/1296A997-0557-E011-8B99-0030487A18A4.root',
            '/store/data/Run2011A/SingleElectron/AOD/PromptReco-v1/000/161/217/32726183-ED56-E011-9633-001617E30CC8.root',
            '/store/data/Run2011A/SingleElectron/AOD/PromptReco-v1/000/161/217/7C68821E-F156-E011-9B0C-000423D94494.root',
            '/store/data/Run2011A/SingleElectron/AOD/PromptReco-v1/000/161/217/82073D07-1C57-E011-B045-003048F110BE.root',
            '/store/data/Run2011A/SingleElectron/AOD/PromptReco-v1/000/161/217/AEE73320-1957-E011-A4B1-003048F1BF68.root',
            '/store/data/Run2011A/SingleElectron/AOD/PromptReco-v1/000/161/217/B241F3D0-FF56-E011-8214-003048F1BF68.root',
            '/store/data/Run2011A/SingleElectron/AOD/PromptReco-v1/000/161/217/BA2F0A7E-EB56-E011-ACD9-000423D94908.root',
            '/store/data/Run2011A/SingleElectron/AOD/PromptReco-v1/000/161/217/C6FD8EAE-1057-E011-8E6F-000423D94908.root',
            '/store/data/Run2011A/SingleElectron/AOD/PromptReco-v1/000/161/217/D69EE709-0B57-E011-996D-000423D9A212.root',
            '/store/data/Run2011A/SingleElectron/AOD/PromptReco-v1/000/161/217/E6D98922-1957-E011-A491-003048F11C5C.root',
            '/store/data/Run2011A/SingleElectron/AOD/PromptReco-v1/000/161/217/F4729787-0E57-E011-A5C9-003048F118AC.root',
            '/store/data/Run2011A/SingleElectron/AOD/PromptReco-v1/000/161/217/F823151E-0B5A-E011-B1FA-003048F117EC.root',
            ] );
else : 
    readFiles.extend( [
        '/store/relval/CMSSW_4_1_3/RelValTTbar/GEN-SIM-RECO/START311_V2-v1/0037/648B6AA5-C751-E011-8208-001A928116C6.root',
        '/store/relval/CMSSW_4_1_3/RelValTTbar/GEN-SIM-RECO/START311_V2-v1/0038/12763BEE-5A52-E011-8988-003048679048.root'
        ] );
    
    
process.source.fileNames = readFiles


# let it run

#print
#print "============== Warning =============="
#print "technical trigger filter:    DISABLED"
#print "physics declare bit filter:  DISABLED"
#print "primary vertex filter:       DISABLED"

process.patseq = cms.Sequence(
#    process.step1*
    process.scrapingVeto*
    process.primaryVertexFilter*
    process.HBHENoiseFilter*
    process.patDefaultSequence* 
    getattr(process,"patPF2PATSequence"+postfix)*
    getattr(process,"patPF2PATSequence"+postfixLoose)*    
    process.flavorHistorySeq *
    process.prunedGenParticles
)

if useData :
    process.patseq.remove( process.flavorHistorySeq )
    process.patseq.remove( process.prunedGenParticles )
else :
    process.patseq.remove( process.scrapingVeto )
    process.patseq.remove( process.primaryVertexFilter )
    process.patseq.remove( process.HBHENoiseFilter )    


process.p1 = cms.Path(
    process.patseq
    )

process.out.SelectEvents.SelectEvents = cms.vstring('p1')


# rename output file
if useData :
    if useMuon:
        process.out.fileName = cms.untracked.string('shyft_414patch1_mu.root')
    else:
        process.out.fileName = cms.untracked.string('shyft_414patch1_ele.root')
else :
    process.out.fileName = cms.untracked.string('shyft_414patch1_mc.root')

# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)

# process all the events
process.maxEvents.input = options.maxEvents
process.options.wantSummary = True
process.out.dropMetaData = cms.untracked.string("DROPPED")

from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning
from PhysicsTools.PatAlgos.patEventContent_cff import patExtraAodEventContent
from PhysicsTools.PatAlgos.patEventContent_cff import patTriggerEventContent
#process.out.outputCommands = patEventContentNoCleaning
#process.out.outputCommands += patExtraAodEventContent
#process.out.outputCommands += patTriggerEventContent
process.out.outputCommands = [
    'keep GenRunInfoProduct_generator_*_*',
    'keep GenEventInfoProduct_generator_*_*',
    'keep *_flavorHistoryFilter_*_*',
    'keep *_prunedGenParticles_*_*',
#    'keep *_decaySubset_*_*',
#    'keep *_initSubset_*_*',
    'drop *_cleanPat*_*_*',
    'keep *_selectedPat*_*_*',
    'keep *_patMETs*_*_*',
#    'keep recoPFCandidates_particleFlow_*_*',
    'keep *_offlineBeamSpot_*_*',
    'keep *_offlinePrimaryVertices_*_*',
    'keep recoTracks_generalTracks_*_*',
    'drop patPFParticles_*_*_*',
#    'keep patTriggerObjects_patTrigger_*_*',
#    'keep patTriggerFilters_patTrigger_*_*',
    'keep patTriggerPaths_patTrigger_*_*',
    'keep patTriggerEvent_patTriggerEvent_*_*',
#    'keep *_cleanPatPhotonsTriggerMatch_*_*',
#    'keep *_cleanPatElectronsTriggerMatch_*_*',
#    'keep *_cleanPatMuonsTriggerMatch_*_*',
#    'keep *_cleanPatTausTriggerMatch_*_*',
#    'keep *_cleanPatJetsTriggerMatch_*_*',
#    'keep *_patMETsTriggerMatch_*_*',
    'drop *_MEtoEDMConverter_*_*'
    ]

if options.slimOutput :
    process.out.outputCommands += [ 'drop recoTracks_generalTracks_*_*',
                                    'drop patTriggerPaths_patTrigger_*_*',
                                    'drop patTriggerEvent_patTriggerEvent_*_*',
                                    'drop GenRunInfoProduct_generator_*_*',
                                    'drop GenEventInfoProduct_generator_*_*'
                                    ]

if useData :
    process.out.outputCommands.append( 'keep LumiSummary_lumiProducer_*_*' )
#    process.out.outputCommands.append( 'keep *_towerMaker_*_*' )
