
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
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Use muons (1) or electrons (0)")

options.register ('slimOutput',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Remove several heavy collections for systematic samples")

options.register ('useLooseLeptonPresel',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Select events with reliso cut < 0.2")

options.register ('useRange135821to139980',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Selected run range 135821-139980 for HLT_Ele10_LW_L1R")

options.register ('useRange140058to143962',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Selected run range 140058_143962 for HLT_Ele15_SW_L1R")

options.register ('useRange144010to146421',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Selected run range 144010_146421 for HLT_Ele15_SW_CaloEleId_L1R")

options.register ('useRange146428to147116',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Selected run range 146428_147116 for HLT_Ele17_SW_CaloEleId_L1R")

options.register ('useRange147196to148058',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Selected run range 147196_148058 for HLT_Ele17_SW_TightEleId_L1R")

options.register ('useRange148819to149063',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Selected run range 148819_149063 for HLT_Ele22_SW_TighterEleId_L1R_v2")

options.register ('useRange149181to149442',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Selected run range 149181_149442 for HLT_Ele22_SW_TighterEleId_L1R_v3")

options.parseArguments()

print options

import sys

# Set to true for running on data
useData = options.useData
# muons
useMuon = options.useMuon
# run the loose W+Jets selector filter
useLooseLeptonPresel = options.useLooseLeptonPresel
# check electron triggers for different run era
useRange135821to139980 = options.useRange135821to139980
useRange140058to143962 = options.useRange140058to143962
useRange144010to146421 = options.useRange144010to146421
useRange146428to147116 = options.useRange146428to147116
useRange147196to148058 = options.useRange147196to148058
useRange148819to149063 = options.useRange148819to149063
useRange149181to149442 = options.useRange149181to149442

if options.useData == False :
    # Make sure to NOT apply L2L3Residual to MC
    corrections = ['L2Relative', 'L3Absolute']
    # global tag for 384 MC
    process.GlobalTag.globaltag = cms.string('START38_V14::All')
else :
    # Make sure to apply L2L3Residual to data
    corrections = ['L2Relative', 'L3Absolute', 'L2L3Residual']
    # global tag for 386 data
    process.GlobalTag.globaltag = cms.string('GR_R_38X_V15::All')



# Add the L1 JPT offset correction for JPT jets
jptcorrections = ['L1JPTOffset']
jptcorrections += corrections 

# require HLT_Mu9 trigger
from HLTrigger.HLTfilters.hltHighLevel_cfi import *

triggerFilter = ""

if useMuon :
    process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::" + options.hltProcess, HLTPaths = ["HLT_Mu9", "HLT_Mu15*"])
else :
    if useRange135821to139980 :
        process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::" + options.hltProcess, HLTPaths = ["HLT_Ele10_LW_L1R"])
        triggerFilter = "hltL1NonIsoHLTNonIsoSingleElectronLWEt10PixelMatchFilter"
		
    elif useRange140058to143962 :
        process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::" + options.hltProcess, HLTPaths = ["HLT_Ele15_SW_L1R"])
        triggerFilter = "hltL1NonIsoHLTNonIsoSingleElectronEt15PixelMatchFilter"
 		
    elif useRange144010to146421 :
        process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::" + options.hltProcess, HLTPaths = ["HLT_Ele15_SW_CaloEleId_L1R"])
        triggerFilter = "hltL1NonIsoHLTNonIsoSingleElectronEt15CaloEleIdPixelMatchFilter"
        
    elif useRange146428to147116 :
        process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::" + options.hltProcess, HLTPaths = ["HLT_Ele17_SW_CaloEleId_L1R"])
        triggerFilter = "hltL1NonIsoHLTNonIsoSingleElectronEt17CaloEleIdPixelMatchFilter"
		
    elif useRange147196to148058 :
        process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::" + options.hltProcess, HLTPaths = ["HLT_Ele17_SW_TightEleId_L1R"])
        triggerFilter = "hltL1NonIsoHLTNonIsoSingleElectronEt17TightEleIdDphiFilter"
		
    elif useRange148819to149063 :
        process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::" + options.hltProcess, HLTPaths = ["HLT_Ele22_SW_TighterEleId_L1R_v2"])
        triggerFilter = "hltL1NonIsoHLTNonIsoSingleElectronEt22TighterEleIdDphiFilter"
        
    elif useRange149181to149442  :
        process.step1 =  hltHighLevel.clone(TriggerResultsTag = "TriggerResults::" + options.hltProcess, HLTPaths = ["HLT_Ele22_SW_TighterEleId_L1R_v3"])
        triggerFilter = "hltL1NonIsoHLTNonIsoSingleElectronEt22TighterEleIdDphiFilter"
        
    else :
        process.step1 = hltHighLevel.clone(TriggerResultsTag = "TriggerResults::" + options.hltProcess, HLTPaths = ["*"])
        triggerFilter = ""
            
process.step1.throw = True

# HB + HE noise filtering
process.load('CommonTools/RecoAlgos/HBHENoiseFilter_cfi')

# add the flavor history
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")
 
# get the 7 TeV jet corrections
from PhysicsTools.PatAlgos.tools.jetTools import *

# require physics declared
process.load('HLTrigger.special.hltPhysicsDeclared_cfi')
process.hltPhysicsDeclared.L1GtReadoutRecordTag = 'gtDigis'

#Use only for electron data	
process.HLTFilter = cms.EDFilter("HLTSummaryFilter",
                                 summary = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
                                 member  = cms .InputTag(triggerFilter,"","HLT"),
                                 cut     = cms.string(""),
                                 minN    = cms.int32(1)
                                 )

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


# turn to false when running on data
if useData :
    removeMCMatching(process, ['All'])



# We'll be using a lot of AOD so re-run b-tagging to get the
# tag infos which are dropped in AOD
switchJetCollection(process,cms.InputTag('ak5CaloJets'),
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = ('AK5Calo', cms.vstring(corrections)),
                 doType1MET   = True,
                 genJetCollection=cms.InputTag("ak5GenJets"),
                 doJetID      = True
                 )


# Add the other 6,000 jet collections that someone might hypothetically
# maybe someday think about possibly including as a cross check. 



addJetCollection(process,cms.InputTag('JetPlusTrackZSPCorJetAntiKt5'),
                 'AK5', 'JPT',
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = ('AK5JPT', cms.vstring(jptcorrections)),
                 doType1MET   = False,
                 doL1Cleaning = False,
                 doL1Counters = True,                 
                 genJetCollection = cms.InputTag("ak5GenJets"),
                 doJetID      = True,
                 jetIdLabel   = "ak5"
                 )


# PF from RECO and not using PF2PAT
addJetCollection(process,cms.InputTag('ak5PFJets'),
                 'AK5', 'PF',
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = ('AK5PF',corrections),
                 doType1MET   = False,
                 doL1Cleaning = False,
                 doL1Counters = False,                 
                 genJetCollection = cms.InputTag("ak5GenJets"),
                 doJetID      = False,
                 jetIdLabel   = "ak5"
                 )


# tcMET
from PhysicsTools.PatAlgos.tools.metTools import *
addTcMET(process, 'TC')
addPfMET(process, 'PF')





# Selection
process.selectedPatJetsPFlow.cut = cms.string('pt > 20 & abs(eta) < 2.4')
process.selectedPatJetsPFlowLoose.cut = cms.string('pt > 20 & abs(eta) < 2.4')
process.selectedPatJetsAK5JPT.cut = cms.string('pt > 20 & abs(eta) < 2.4')
process.selectedPatJetsAK5PF.cut = cms.string('pt > 20 & abs(eta) < 2.4')
process.selectedPatJets.cut = cms.string('pt > 20 & abs(eta) < 2.4')
process.patJets.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAOD")
    )
process.patJetsPFlow.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAOD" + postfix)
    )
process.patJetsPFlowLoose.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAOD" + postfixLoose)
    )
process.patJetsAK5JPT.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAK5JPT")
    )
process.patJetsAK5PF.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAK5PF")
    )

#remove isolation from the PFlow 
process.patMuonsPFlowLoose.pfMuonSource = 'pfAllMuonsPFlowLoose'
process.patMuonsPFlowLoose.isoDeposits = cms.PSet()
process.patMuonsPFlowLoose.isolationValues = cms.PSet()
process.patElectronsPFlowLoose.pfElectronSource = 'pfAllElectronsPFlowLoose'
process.patElectronsPFlowLoose.isoDeposits = cms.PSet()
process.patElectronsPFlowLoose.isolationValues = cms.PSet()

##Muons
process.selectedPatMuons.cut = cms.string("pt > 10")
process.selectedPatMuonsPFlow.cut = cms.string("pt > 10")
process.selectedPatMuonsPFlowLoose.cut = cms.string("pt > 10")
process.patMuons.usePV = False
process.patMuonsPFlow.usePV = False
process.patMuonsPFlowLoose.usePV = False

process.patMuons.embedTrack = True
process.patMuonsPFlow.embedTrack = True
process.patMuonsPFlowLoose.embedTrack = True

##Electrons
process.patElectrons.usePV = False
process.patElectronsPFlow.usePV = False
process.patElectronsPFlowLoose.usePV = False

process.patElectrons.embedTrack = True
process.patElectronsPFlow.embedTrack = True
process.patElectronsPFlowLoose.embedTrack = True

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
process.makePatElectrons.replace(getattr(process,"patElectrons"),getattr(process,"patElectrons")*process.patElectronsUserData)
process.selectedPatElectrons.src = "patElectronsUserData"
process.selectedPatElectrons.cut = cms.string("et > 20 & abs(eta)<3")

process.makePatElectronsPFlow.replace(getattr(process,"patElectronsPFlow"),getattr(process,"patElectronsPFlow")*process.patElectronsPFlowUserData)
process.selectedPatElectronsPFlow.src = "patElectronsPFlowUserData"
process.selectedPatElectronsPFlow.cut = cms.string("et > 20 & abs(eta)<3")

process.makePatElectronsPFlowLoose.replace(getattr(process,"patElectronsPFlowLoose"),getattr(process,"patElectronsPFlowLoose")*process.patElectronsPFlowLooseUserData)
process.selectedPatElectronsPFlowLoose.src = "patElectronsPFlowLooseUserData"
process.selectedPatElectronsPFlowLoose.cut = cms.string("et > 20 & abs(eta)<3")


#secvtxVertex as user data
process.patJets.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJets.userData.userFunctionLabels = cms.vstring('secvtxMass')


process.patJetsPFlow.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJetsPFlow.userData.userFunctionLabels = cms.vstring('secvtxMass')


process.patJetsPFlowLoose.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJetsPFlowLoose.userData.userFunctionLabels = cms.vstring('secvtxMass')


process.patJetsAK5PF.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJetsAK5PF.userData.userFunctionLabels = cms.vstring('secvtxMass')

process.patJetsAK5JPT.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJetsAK5JPT.userData.userFunctionLabels = cms.vstring('secvtxMass')


process.patTaus.isoDeposits = cms.PSet()
process.patTausPFlow.isoDeposits = cms.PSet()
process.patTausPFlowLoose.isoDeposits = cms.PSet()

process.patJets.embedPFCandidates = True
process.patJets.embedCaloTowers = True
process.patJetsPFlow.embedCaloTowers = True
process.patJetsPFlow.embedPFCandidates = True
process.patJetsPFlowLoose.embedCaloTowers = True
process.patJetsPFlowLoose.embedPFCandidates = True
process.patJetsAK5PF.embedCaloTowers = True
process.patJetsAK5PF.embedPFCandidates = True
process.patJetsAK5JPT.embedCaloTowers = True
process.patJetsAK5JPT.embedPFCandidates = True


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
            '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/0A82F71C-57EA-DF11-80A2-E0CB4E55365F.root',
            '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/0A78BF54-84EA-DF11-A0CD-485B39800BCA.root',
            '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/0A77B760-B9E9-DF11-B2F8-90E6BA442F2B.root',
            '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/0A777C9D-02EA-DF11-B982-90E6BA0D09E2.root',
            '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/0A69BA60-0FEA-DF11-9879-90E6BA442F3B.root',
            '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/0A292691-A8EA-DF11-908E-E0CB4E29C4D5.root',
            '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/0A1C4CCB-0FEA-DF11-9642-001EC9D8D08D.root',
            '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/08E0BEAD-EEE9-DF11-80B2-90E6BA442EEE.root',
            '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/083FAA15-28EA-DF11-96C1-90E6BA442EF2.root',
            '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/06F1A9FA-36EC-DF11-AE50-001EC9D8D08D.root',
            '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/06CC3F83-08EA-DF11-A05B-E0CB4E29C4CA.root',
            '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/06A53695-A8EA-DF11-BAE4-485B39800C2B.root',
            '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/0683478B-0FEA-DF11-9729-00261834B575.root',
            '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0000/066D7924-0FEA-DF11-8ED7-E0CB4E55367A.root'
            ] );
    else: #useRange146428to147116
         readFiles.extend( [
             '/store/data/Run2010B/Electron/AOD/Nov4ReReco_v1/0150/FE495F95-6CED-DF11-826E-0018F3D09700.root',
             '/store/data/Run2010B/Electron/AOD/Nov4ReReco_v1/0150/F43CC38E-6CED-DF11-82FF-0026189437F2.root',
             '/store/data/Run2010B/Electron/AOD/Nov4ReReco_v1/0150/DE7ED294-6CED-DF11-9CAF-0018F3D095F2.root',
             '/store/data/Run2010B/Electron/AOD/Nov4ReReco_v1/0150/C0CA698E-6CED-DF11-8846-0026189437EC.root',
             '/store/data/Run2010B/Electron/AOD/Nov4ReReco_v1/0150/C06F3D98-6CED-DF11-965A-003048679228.root',
             '/store/data/Run2010B/Electron/AOD/Nov4ReReco_v1/0150/BA0BDE93-6CED-DF11-8C7D-00261894383E.root',
             '/store/data/Run2010B/Electron/AOD/Nov4ReReco_v1/0150/B2A79494-6CED-DF11-9BF9-002618943916.root',
             '/store/data/Run2010B/Electron/AOD/Nov4ReReco_v1/0150/9218EE99-6CED-DF11-8EAC-0018F3D096AA.root',
             '/store/data/Run2010B/Electron/AOD/Nov4ReReco_v1/0150/76660295-6CED-DF11-A4CF-001A928116B4.root',
             '/store/data/Run2010B/Electron/AOD/Nov4ReReco_v1/0150/6006DA92-6CED-DF11-805E-00248C55CC97.root',
             '/store/data/Run2010B/Electron/AOD/Nov4ReReco_v1/0150/1C737394-6CED-DF11-AC4F-0018F3D0966C.root',
             '/store/data/Run2010B/Electron/AOD/Nov4ReReco_v1/0150/18391B99-6CED-DF11-A88E-002618FDA287.root',
             '/store/data/Run2010B/Electron/AOD/Nov4ReReco_v1/0150/14C3939A-6CED-DF11-962F-001A92971B0E.root', 
             ]);

else : 
    readFiles.extend( [
        '/store/mc/Fall10/QCD_Pt-20to30_BCtoE_TuneZ2_7TeV-pythia6/AODSIM/START38_V12-v1/0006/FC66B410-78C9-DF11-A289-002481FFD0CC.root',

       #'/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/AODSIM/START38_V12-v1/0034/4E13F346-89CC-DF11-A639-001A92810AD0.root',
       # '/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/AODSIM/START38_V12-v1/0034/30CFC3B1-BECC-DF11-8EDE-002618FDA259.root',
       # '/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/AODSIM/START38_V12-v1/0033/F2D852D4-4CCB-DF11-8085-002618943900.root',
       # '/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/AODSIM/START38_V12-v1/0033/F22B100C-4BCB-DF11-84A6-003048678B92.root',
       # '/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/AODSIM/START38_V12-v1/0033/EAA1A008-4BCB-DF11-9737-002618943900.root',
       # '/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/AODSIM/START38_V12-v1/0033/E8BB73B4-05CA-DF11-AABA-003048679048.root',
       # '/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/AODSIM/START38_V12-v1/0033/DC52F7EE-42CB-DF11-AFCE-001A92810AB8.root',
       # '/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/AODSIM/START38_V12-v1/0033/DA1AD6FF-4BCB-DF11-9EA0-001A9281172A.root',
       # '/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/AODSIM/START38_V12-v1/0033/D6A23149-4BCB-DF11-A1F6-001A92810AAA.root',
       # '/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/AODSIM/START38_V12-v1/0033/D274A804-46CB-DF11-9CBC-002618FDA248.root',
       # '/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/AODSIM/START38_V12-v1/0033/CA98476E-49CB-DF11-9553-001A92971B48.root',

       ## '/store/mc/Fall10/QCD_Pt-20to30_BCtoE_TuneZ2_7TeV-pythia6/GEN-SIM-RECO/START38_V12-v1/0006/DCE8DBEC-62C9-DF11-BE9E-001F29C4A3A0.root',
##        '/store/mc/Fall10/QCD_Pt-20to30_BCtoE_TuneZ2_7TeV-pythia6/GEN-SIM-RECO/START38_V12-v1/0006/BAA34038-74C9-DF11-8C9D-00237DA16692.root',

       #  '/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/GEN-SIM-RECO/START38_V12-v1/0034/46CB78A7-A3CB-DF11-8133-0018F3D09696.root',
         
        #'/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/GEN-SIM-RECO/START38_V12-v1/0017/38A3E2DC-14C9-DF11-97C5-0026189438C0.root',
        #'/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/GEN-SIM-RECO/START38_V12-v1/0034/52D613E5-B7CC-DF11-8D4A-0026189438D8.root',
        #'/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/GEN-SIM-RECO/START38_V12-v1/0034/46CB78A7-A3CB-DF11-8133-0018F3D09696.root',###
##         '/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/GEN-SIM-RECO/START38_V12-v1/0034/1A52400B-AECC-DF11-88F8-00261894393C.root',
##         '/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/GEN-SIM-RECO/START38_V12-v1/0033/FE903370-43CB-DF11-ACA2-001A928116EC.root',
##         '/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/GEN-SIM-RECO/START38_V12-v1/0033/FE399F62-50CB-DF11-A21E-0026189438F5.root',
##         '/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/GEN-SIM-RECO/START38_V12-v1/0033/FC6ADC11-35CB-DF11-854B-002618943986.root',
##         '/store/mc/Fall10/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6/GEN-SIM-RECO/START38_V12-v1/0033/FA4EC6E9-4ACB-DF11-9A6C-001A92811744.root',

        
##        '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0009/E8B2CA4D-42E7-DF11-988C-90E6BA442F16.root',
##        '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0009/E847D402-12E7-DF11-97C5-003048D4EF1D.root',
##        '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0009/6EE559BE-11E7-DF11-B575-00145E5513C1.root',
##        '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/DC4963A1-E0E5-DF11-807E-00D0680BF898.root',
##        '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/D8F33E3F-58E5-DF11-9FCC-0026B9548CB5.root',
##        '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/B2D39D4C-63E6-DF11-8CFA-003048CEB070.root',
##        '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/B28EE7AE-48E5-DF11-9F45-001F29651428.root',
##        '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/9C7AD216-ACE5-DF11-BE50-001517255D36.root',
##        '/store/mc/Fall10/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/START38_V12-v2/0008/788BCB6C-ACE5-DF11-A13C-90E6BA442F1F.root',

        ] );

    
process.source.fileNames = readFiles


# let it run

#print
#print "============== Warning =============="
#print "technical trigger filter:    DISABLED"
#print "physics declare bit filter:  DISABLED"
#print "primary vertex filter:       DISABLED"

process.patseq = cms.Sequence(
    process.step1*
    process.scrapingVeto*
    process.primaryVertexFilter*
    process.HBHENoiseFilter*
    process.HLTFilter*
    process.patDefaultSequence* 
    getattr(process,"patPF2PATSequence"+postfix)*
    getattr(process,"patPF2PATSequence"+postfixLoose)*    
    process.flavorHistorySeq *
    process.prunedGenParticles
)

process.isolatedPatElectrons = cms.EDFilter("PATElectronSelector",
                                            src = cms.InputTag("selectedPatElectrons"),
                                            cut = cms.string("(dr03TkSumPt+dr03EcalRecHitSumEt+dr03HcalTowerSumEt)/et < 0.2"),
                                            filter=cms.bool(True)                                       
                                            )

if useData :
    process.patseq.remove( process.flavorHistorySeq )
    process.patseq.remove( process.prunedGenParticles )
    if useMuon:
        process.patseq.remove( process.HLTFilter )
        
else :
    #if not useMuon:
    process.patseq.remove( process.step1)
    process.patseq.remove( process.scrapingVeto )
    process.patseq.remove( process.primaryVertexFilter )
    process.patseq.remove( process.HBHENoiseFilter )    
    process.patseq.remove( process.HLTFilter )

process.p1 = cms.Path(
    process.patseq
    )

process.p2 = cms.Path(
    process.patseq *
    process.isolatedPatElectrons
    )
    
if not useLooseLeptonPresel:
    process.out.SelectEvents.SelectEvents = cms.vstring('p1')
    
else:
    process.out.SelectEvents.SelectEvents = cms.vstring('p2')
# rename output file
if useData :
    process.out.fileName = cms.untracked.string('shyft_386.root')
else :
    process.out.fileName = cms.untracked.string('shyft_386_mc.root')

# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

# process all the events
process.maxEvents.input = 200
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
