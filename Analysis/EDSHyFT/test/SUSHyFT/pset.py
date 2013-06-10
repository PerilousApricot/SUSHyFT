import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.Config as cms

process = cms.Process("EDMNtuple")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/user/meloam/SingleMu/meloam_feb12_tlbsm53x2_Run2012C_24Aug2012_v1/20130212222033/00000/4463A7D0-9075-E211-95CC-003048F2E8C2.root')
)
process.cleanElectronTriggerMatchHLTEle27CaloIdVTCaloIsoTTrkIdTTrkIsoT = cms.EDProducer("PATTriggerMatcherDRDPtLessByR",
    matchedCuts = cms.string('path( "HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v*" )'),
    src = cms.InputTag("cleanPatElectrons"),
    maxDPtRel = cms.double(0.5),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = cms.double(0.5),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patTrigger")
)


process.cleanElectronTriggerMatchL1EGammaCollection = cms.EDProducer("PATTriggerMatcherDRLessByR",
    matchedCuts = cms.string('coll( "l1extraParticles:NonIsolated" ) || coll( "l1extraParticles:Isolated" )'),
    src = cms.InputTag("cleanPatElectrons"),
    maxDPtRel = cms.double(0.5),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.5),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patTrigger")
)


process.cleanJetTriggerMatchHLTJet240 = cms.EDProducer("PATTriggerMatcherDRLessByR",
    matchedCuts = cms.string('path( "HLT_Jet240_v*" )'),
    src = cms.InputTag("cleanPatJets"),
    maxDPtRel = cms.double(3.0),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = cms.double(0.4),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patTrigger")
)


process.cleanJetTriggerMatchHLTMu17CentralJet30 = cms.EDProducer("PATTriggerMatcherDRDPtLessByR",
    matchedCuts = cms.string('type( "TriggerJet" ) && path( "HLT_Mu17_CentralJet30_v*" )'),
    src = cms.InputTag("cleanPatJets"),
    maxDPtRel = cms.double(3.0),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = cms.double(0.4),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patTrigger")
)


process.cleanMuonTriggerMatchHLTDoubleMu6 = cms.EDProducer("PATTriggerMatcherDRDPtLessByR",
    matchedCuts = cms.string('path( "HLT_DoubleMu6_v*" )'),
    src = cms.InputTag("cleanPatMuons"),
    maxDPtRel = cms.double(0.5),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = cms.double(0.5),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patTrigger")
)


process.cleanMuonTriggerMatchHLTMu17CentralJet30 = cms.EDProducer("PATTriggerMatcherDRDPtLessByR",
    matchedCuts = cms.string('type( "TriggerMuon" ) && path( "HLT_Mu17_CentralJet30_v*" )'),
    src = cms.InputTag("cleanPatMuons"),
    maxDPtRel = cms.double(0.5),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = cms.double(0.5),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patTrigger")
)


process.cleanMuonTriggerMatchHLTMu20 = cms.EDProducer("PATTriggerMatcherDRDPtLessByR",
    matchedCuts = cms.string('path( "HLT_Mu20_v*" )'),
    src = cms.InputTag("cleanPatMuons"),
    maxDPtRel = cms.double(0.5),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = cms.double(0.5),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patTrigger")
)


process.cleanMuonTriggerMatchPDSingleMu = cms.EDProducer("PATTriggerMatcherDRDPtLessByR",
    matchedCuts = cms.string('path( "HLT_IsoMu12_v*" ) || path( "HLT_IsoMu15_v*" ) || path( "HLT_IsoMu17_v*" ) || path( "HLT_IsoMu24_v*" ) || path( "HLT_IsoMu30_v*" ) || path( "HLT_L1SingleMu10_v*" ) || path( "HLT_L1SingleMu20_v*" ) || path( "HLT_L2Mu10_v*" ) || path( "HLT_L2Mu20_v*" ) || path( "HLT_Mu3_v*" ) || path( "HLT_Mu5_v*" ) || path( "HLT_Mu8_v*" ) || path( "HLT_Mu12_v*" ) || path( "HLT_Mu15_v*" ) || path( "HLT_Mu20_v*" ) || path( "HLT_Mu24_v*" ) || path( "HLT_Mu30_v*" )'),
    src = cms.InputTag("cleanPatMuons"),
    maxDPtRel = cms.double(0.5),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = cms.double(0.5),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patTrigger")
)


process.cleanMuonTriggerMatchTriggerMuon = cms.EDProducer("PATTriggerMatcherDRDPtLessByR",
    matchedCuts = cms.string('type( "TriggerL1Mu" ) || type( "TriggerMuon" )'),
    src = cms.InputTag("cleanPatMuons"),
    maxDPtRel = cms.double(0.5),
    resolveByMatchQuality = cms.bool(False),
    maxDeltaR = cms.double(0.5),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patTrigger")
)


process.cleanPatElectronsTriggerMatch = cms.EDProducer("PATTriggerMatchElectronEmbedder",
    matches = cms.VInputTag("cleanElectronTriggerMatchHLTEle27CaloIdVTCaloIsoTTrkIdTTrkIsoT"),
    src = cms.InputTag("cleanPatElectrons")
)


process.cleanPatJetsTriggerMatch = cms.EDProducer("PATTriggerMatchJetEmbedder",
    matches = cms.VInputTag("cleanJetTriggerMatchHLTJet240"),
    src = cms.InputTag("cleanPatJets")
)


process.cleanPatMuonsTriggerMatch = cms.EDProducer("PATTriggerMatchMuonEmbedder",
    matches = cms.VInputTag("cleanMuonTriggerMatchHLTMu20", "cleanMuonTriggerMatchHLTDoubleMu6"),
    src = cms.InputTag("cleanPatMuons")
)


process.cleanPatPhotonsTriggerMatch = cms.EDProducer("PATTriggerMatchPhotonEmbedder",
    matches = cms.VInputTag("cleanPhotonTriggerMatchHLTPhoton26IsoVLPhoton18"),
    src = cms.InputTag("cleanPatPhotons")
)


process.cleanPatTausTriggerMatch = cms.EDProducer("PATTriggerMatchTauEmbedder",
    matches = cms.VInputTag("cleanTauTriggerMatchHLTDoubleIsoPFTau20Trk5"),
    src = cms.InputTag("cleanPatTaus")
)


process.cleanPhotonTriggerMatchHLTPhoton26IsoVLPhoton18 = cms.EDProducer("PATTriggerMatcherDRDPtLessByR",
    matchedCuts = cms.string('path( "HLT_Photon26_IsoVL_Photon18_v*" )'),
    src = cms.InputTag("cleanPatPhotons"),
    maxDPtRel = cms.double(0.5),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = cms.double(0.5),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patTrigger")
)


process.cleanTauTriggerMatchHLTDoubleIsoPFTau20Trk5 = cms.EDProducer("PATTriggerMatcherDRDPtLessByR",
    matchedCuts = cms.string('path( "HLT_DoubleIsoPFTau20_Trk5_v*" )'),
    src = cms.InputTag("cleanPatTaus"),
    maxDPtRel = cms.double(0.5),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = cms.double(0.5),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patTrigger")
)


process.metTriggerMatchHLTMET100 = cms.EDProducer("PATTriggerMatcherDRLessByR",
    matchedCuts = cms.string('path( "HLT_MET100_v*" )'),
    src = cms.InputTag("patMETs"),
    maxDPtRel = cms.double(3.0),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = cms.double(0.4),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patTrigger")
)


process.metTriggerMatchHLTMu20 = cms.EDProducer("PATTriggerMatcherDRLessByR",
    matchedCuts = cms.string('path( "HLT_Mu20_v*" )'),
    src = cms.InputTag("patMETs"),
    maxDPtRel = cms.double(0.5),
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = cms.double(0.5),
    resolveAmbiguities = cms.bool(True),
    matched = cms.InputTag("patTrigger")
)


process.patMETsTriggerMatch = cms.EDProducer("PATTriggerMatchMETEmbedder",
    matches = cms.VInputTag("metTriggerMatchHLTMET100"),
    src = cms.InputTag("patMETs")
)


process.patTrigger = cms.EDProducer("PATTriggerProducer",
    processName = cms.string('HLT'),
    onlyStandAlone = cms.bool(False)
)


process.patTriggerEvent = cms.EDProducer("PATTriggerEventProducer",
    patTriggerMatches = cms.VInputTag(),
    processName = cms.string('HLT')
)


process.pfTupleEle = cms.EDFilter("EDSHyFTSelector",
    matchByHand = cms.bool(False),
    shyftSelection = cms.PSet(
        muonSrc = cms.InputTag("selectedPatMuonsPFlow"),
        dxy = cms.double(0.02),
        eEt = cms.double(30.0),
        eleEtaMaxLoose = cms.double(2.5),
        tauTrig = cms.string('butz'),
        unclMetScale = cms.double(0.0),
        jecPayloads = cms.vstring('Jec12_V2_L1FastJet_AK5PFchs.txt', 
            'Jec12_V2_L2Relative_AK5PFchs.txt', 
            'Jec12_V2_L3Absolute_AK5PFchs.txt', 
            'Jec12_V2_L2L3Residual_AK5PFchs.txt', 
            'Jec12_V2_Uncertainty_AK5PFchs.txt'),
        muPtMin = cms.double(30.0),
        rawJetPtCut = cms.double(0.0),
        eleEtaMax = cms.double(2.4),
        useNoPFIso = cms.bool(True),
        elDcot = cms.double(0.02),
        rhoSrc = cms.InputTag("kt6PFJets","rho"),
        jetScale = cms.double(0.0),
        trigSrc = cms.InputTag("patTriggerEvent"),
        ePlusJets = cms.bool(True),
        metSrc = cms.InputTag("patMETs"),
        pfCandidateMap = cms.InputTag("particleFlow","electrons"),
        pvSelector = cms.PSet(
            maxZ = cms.double(24.0),
            minNdof = cms.double(4.0),
            NPV = cms.int32(1),
            maxRho = cms.double(2.0),
            pvSrc = cms.InputTag("goodOfflinePrimaryVertices")
        ),
        tauEtaMax = cms.double(2.4),
        elDist = cms.double(0.02),
        jetSmear = cms.double(0.0),
        tauPtMin = cms.double(20.0),
        useData = cms.bool(True),
        electronIdVeto = cms.PSet(
            vtxFitConv = cms.bool(True),
            sihih_EE = cms.double(0.03),
            sihih_EB = cms.double(0.01),
            ooemoop_EB = cms.double(0.05),
            ooemoop_EE = cms.double(0.05),
            d0_EB = cms.double(0.02),
            d0_EE = cms.double(0.02),
            version = cms.string('VETO'),
            deta_EB = cms.double(0.004),
            deta_EE = cms.double(0.005),
            rhoSrc = cms.InputTag("kt6PFJetsForIsolation","rho"),
            dZ_EB = cms.double(0.1),
            dphi_EB = cms.double(0.03),
            pvSrc = cms.InputTag("goodOfflinePrimaryVertices"),
            dZ_EE = cms.double(0.1),
            mHits = cms.int32(0),
            reliso_EE = cms.double(0.1),
            cutsToIgnore = cms.vstring(''),
            reliso_EB = cms.double(0.1),
            hoe_EE = cms.double(0.01),
            hoe_EB = cms.double(0.12),
            dphi_EE = cms.double(0.02)
        ),
        pfEleSrc = cms.InputTag("particleFlow"),
        cutsToIgnore = cms.vstring('Trigger', 
            'Dilepton Veto'),
        tauSrc = cms.InputTag("selectedPatTausPFlow"),
        muEtaMax = cms.double(2.1),
        muJetDR = cms.double(0.3),
        electronSrc = cms.InputTag("selectedPatElectronsPFlow"),
        eleEtMinLoose = cms.double(15.0),
        eleJetDR = cms.double(0.5),
        muPtMinLoose = cms.double(10.0),
        jetEtaMax = cms.double(2.4),
        muEtaMaxLoose = cms.double(2.5),
        useNoID = cms.bool(True),
        eleEtMin = cms.double(20.0),
        ePtScale = cms.double(0.0),
        muPlusJets = cms.bool(False),
        eRelIso = cms.double(0.1),
        vertexCut = cms.double(1.0),
        ePtUncertaintyEE = cms.double(0.025),
        rhoIsoSrc = cms.InputTag("kt6PFJetsForIsolation","rho"),
        eleTrig = cms.string('HLT_Ele10_LW_L1R'),
        muRelIso = cms.double(0.125),
        jetPtMin = cms.double(30.0),
        minJets = cms.int32(1),
        jetUncertainty = cms.double(0.0),
        muTrig = cms.string('HLT_Mu9'),
        jetSrc = cms.InputTag("goodPatJetsPFlow"),
        identifier = cms.string('AK5 PF'),
        pvSrc = cms.InputTag("goodOfflinePrimaryVertices")
    )
)


process.pfTupleEleCA8Pruned = cms.EDFilter("EDSHyFTSelector",
    matchByHand = cms.bool(True),
    shyftSelection = cms.PSet(
        muonSrc = cms.InputTag("selectedPatMuonsPFlow"),
        dxy = cms.double(0.02),
        eEt = cms.double(30.0),
        eleEtaMaxLoose = cms.double(2.5),
        tauTrig = cms.string('butz'),
        unclMetScale = cms.double(0.0),
        jecPayloads = cms.vstring('Jec12_V2_L1FastJet_AK5PFchs.txt', 
            'Jec12_V2_L2Relative_AK5PFchs.txt', 
            'Jec12_V2_L3Absolute_AK5PFchs.txt', 
            'Jec12_V2_L2L3Residual_AK5PFchs.txt', 
            'Jec12_V2_Uncertainty_AK5PFchs.txt'),
        muPtMin = cms.double(30.0),
        rawJetPtCut = cms.double(0.0),
        eleEtaMax = cms.double(2.4),
        useNoPFIso = cms.bool(True),
        elDcot = cms.double(0.02),
        rhoSrc = cms.InputTag("kt6PFJets","rho"),
        jetScale = cms.double(0.0),
        trigSrc = cms.InputTag("patTriggerEvent"),
        ePlusJets = cms.bool(True),
        metSrc = cms.InputTag("patMETs"),
        pfCandidateMap = cms.InputTag("particleFlow","electrons"),
        pvSelector = cms.PSet(
            maxZ = cms.double(24.0),
            minNdof = cms.double(4.0),
            NPV = cms.int32(1),
            maxRho = cms.double(2.0),
            pvSrc = cms.InputTag("goodOfflinePrimaryVertices")
        ),
        tauEtaMax = cms.double(2.4),
        elDist = cms.double(0.02),
        jetSmear = cms.double(0.0),
        tauPtMin = cms.double(20.0),
        useData = cms.bool(True),
        electronIdVeto = cms.PSet(
            vtxFitConv = cms.bool(True),
            sihih_EE = cms.double(0.03),
            sihih_EB = cms.double(0.01),
            ooemoop_EB = cms.double(0.05),
            ooemoop_EE = cms.double(0.05),
            d0_EB = cms.double(0.02),
            d0_EE = cms.double(0.02),
            version = cms.string('VETO'),
            deta_EB = cms.double(0.004),
            deta_EE = cms.double(0.005),
            rhoSrc = cms.InputTag("kt6PFJetsForIsolation","rho"),
            dZ_EB = cms.double(0.1),
            dphi_EB = cms.double(0.03),
            pvSrc = cms.InputTag("goodOfflinePrimaryVertices"),
            dZ_EE = cms.double(0.1),
            mHits = cms.int32(0),
            reliso_EE = cms.double(0.1),
            cutsToIgnore = cms.vstring(''),
            reliso_EB = cms.double(0.1),
            hoe_EE = cms.double(0.01),
            hoe_EB = cms.double(0.12),
            dphi_EE = cms.double(0.02)
        ),
        pfEleSrc = cms.InputTag("particleFlow"),
        cutsToIgnore = cms.vstring('Trigger', 
            'Dilepton Veto'),
        tauSrc = cms.InputTag("selectedPatTausPFlow"),
        muEtaMax = cms.double(2.1),
        muJetDR = cms.double(0.3),
        electronSrc = cms.InputTag("selectedPatElectronsPFlow"),
        eleEtMinLoose = cms.double(15.0),
        eleJetDR = cms.double(0.5),
        muPtMinLoose = cms.double(10.0),
        jetEtaMax = cms.double(2.4),
        muEtaMaxLoose = cms.double(2.5),
        useNoID = cms.bool(True),
        eleEtMin = cms.double(20.0),
        ePtScale = cms.double(0.0),
        muPlusJets = cms.bool(False),
        eRelIso = cms.double(0.1),
        vertexCut = cms.double(1.0),
        ePtUncertaintyEE = cms.double(0.025),
        rhoIsoSrc = cms.InputTag("kt6PFJetsForIsolation","rho"),
        eleTrig = cms.string('HLT_Ele10_LW_L1R'),
        muRelIso = cms.double(0.125),
        jetPtMin = cms.double(30.0),
        minJets = cms.int32(1),
        jetUncertainty = cms.double(0.0),
        muTrig = cms.string('HLT_Mu9'),
        jetSrc = cms.InputTag("goodPatJetsCA8PrunedPF"),
        identifier = cms.string('CA8 Prunded PF'),
        pvSrc = cms.InputTag("goodOfflinePrimaryVertices")
    ),
    ePlusJets = cms.bool(True),
    muPlusJuets = cms.bool(False)
)


process.pfTupleEleSelectedJets = cms.EDFilter("EDSHyFTSelector",
    matchByHand = cms.bool(True),
    shyftSelection = cms.PSet(
        muonSrc = cms.InputTag("selectedPatMuonsPFlow"),
        dxy = cms.double(0.02),
        eEt = cms.double(30.0),
        eleEtaMaxLoose = cms.double(2.5),
        tauTrig = cms.string('butz'),
        unclMetScale = cms.double(0.0),
        jecPayloads = cms.vstring('Jec12_V2_L1FastJet_AK5PFchs.txt', 
            'Jec12_V2_L2Relative_AK5PFchs.txt', 
            'Jec12_V2_L3Absolute_AK5PFchs.txt', 
            'Jec12_V2_L2L3Residual_AK5PFchs.txt', 
            'Jec12_V2_Uncertainty_AK5PFchs.txt'),
        muPtMin = cms.double(30.0),
        rawJetPtCut = cms.double(0.0),
        eleEtaMax = cms.double(2.4),
        useNoPFIso = cms.bool(True),
        elDcot = cms.double(0.02),
        rhoSrc = cms.InputTag("kt6PFJets","rho"),
        jetScale = cms.double(0.0),
        trigSrc = cms.InputTag("patTriggerEvent"),
        ePlusJets = cms.bool(True),
        metSrc = cms.InputTag("patMETs"),
        pfCandidateMap = cms.InputTag("particleFlow","electrons"),
        pvSelector = cms.PSet(
            maxZ = cms.double(24.0),
            minNdof = cms.double(4.0),
            NPV = cms.int32(1),
            maxRho = cms.double(2.0),
            pvSrc = cms.InputTag("goodOfflinePrimaryVertices")
        ),
        tauEtaMax = cms.double(2.4),
        elDist = cms.double(0.02),
        jetSmear = cms.double(0.0),
        tauPtMin = cms.double(20.0),
        useData = cms.bool(True),
        electronIdVeto = cms.PSet(
            vtxFitConv = cms.bool(True),
            sihih_EE = cms.double(0.03),
            sihih_EB = cms.double(0.01),
            ooemoop_EB = cms.double(0.05),
            ooemoop_EE = cms.double(0.05),
            d0_EB = cms.double(0.02),
            d0_EE = cms.double(0.02),
            version = cms.string('VETO'),
            deta_EB = cms.double(0.004),
            deta_EE = cms.double(0.005),
            rhoSrc = cms.InputTag("kt6PFJetsForIsolation","rho"),
            dZ_EB = cms.double(0.1),
            dphi_EB = cms.double(0.03),
            pvSrc = cms.InputTag("goodOfflinePrimaryVertices"),
            dZ_EE = cms.double(0.1),
            mHits = cms.int32(0),
            reliso_EE = cms.double(0.1),
            cutsToIgnore = cms.vstring(''),
            reliso_EB = cms.double(0.1),
            hoe_EE = cms.double(0.01),
            hoe_EB = cms.double(0.12),
            dphi_EE = cms.double(0.02)
        ),
        pfEleSrc = cms.InputTag("particleFlow"),
        cutsToIgnore = cms.vstring('Trigger', 
            'Dilepton Veto'),
        tauSrc = cms.InputTag("selectedPatTausPFlow"),
        muEtaMax = cms.double(2.1),
        muJetDR = cms.double(0.3),
        electronSrc = cms.InputTag("selectedPatElectronsPFlow"),
        eleEtMinLoose = cms.double(15.0),
        eleJetDR = cms.double(0.5),
        muPtMinLoose = cms.double(10.0),
        jetEtaMax = cms.double(2.4),
        muEtaMaxLoose = cms.double(2.5),
        useNoID = cms.bool(True),
        eleEtMin = cms.double(20.0),
        ePtScale = cms.double(0.0),
        muPlusJets = cms.bool(False),
        eRelIso = cms.double(0.1),
        vertexCut = cms.double(1.0),
        ePtUncertaintyEE = cms.double(0.025),
        rhoIsoSrc = cms.InputTag("kt6PFJetsForIsolation","rho"),
        eleTrig = cms.string('HLT_Ele10_LW_L1R'),
        muRelIso = cms.double(0.125),
        jetPtMin = cms.double(30.0),
        minJets = cms.int32(1),
        jetUncertainty = cms.double(0.0),
        muTrig = cms.string('HLT_Mu9'),
        jetSrc = cms.InputTag("goodPatJetsPFlow"),
        identifier = cms.string('Good PAT PF'),
        pvSrc = cms.InputTag("goodOfflinePrimaryVertices")
    ),
    ePlusJets = cms.bool(True),
    muPlusJuets = cms.bool(False)
)


process.pfTupleMuCA8Pruned = cms.EDFilter("EDSHyFTSelector",
    matchByHand = cms.bool(True),
    shyftSelection = cms.PSet(
        muonSrc = cms.InputTag("selectedPatMuonsPFlow"),
        dxy = cms.double(0.02),
        eEt = cms.double(30.0),
        eleEtaMaxLoose = cms.double(2.5),
        tauTrig = cms.string('butz'),
        unclMetScale = cms.double(0.0),
        jecPayloads = cms.vstring('Jec12_V2_L1FastJet_AK5PFchs.txt', 
            'Jec12_V2_L2Relative_AK5PFchs.txt', 
            'Jec12_V2_L3Absolute_AK5PFchs.txt', 
            'Jec12_V2_L2L3Residual_AK5PFchs.txt', 
            'Jec12_V2_Uncertainty_AK5PFchs.txt'),
        muPtMin = cms.double(30.0),
        rawJetPtCut = cms.double(0.0),
        eleEtaMax = cms.double(2.4),
        useNoPFIso = cms.bool(True),
        elDcot = cms.double(0.02),
        rhoSrc = cms.InputTag("kt6PFJets","rho"),
        jetScale = cms.double(0.0),
        trigSrc = cms.InputTag("patTriggerEvent"),
        ePlusJets = cms.bool(True),
        metSrc = cms.InputTag("patMETs"),
        pfCandidateMap = cms.InputTag("particleFlow","electrons"),
        pvSelector = cms.PSet(
            maxZ = cms.double(24.0),
            minNdof = cms.double(4.0),
            NPV = cms.int32(1),
            maxRho = cms.double(2.0),
            pvSrc = cms.InputTag("goodOfflinePrimaryVertices")
        ),
        tauEtaMax = cms.double(2.4),
        elDist = cms.double(0.02),
        jetSmear = cms.double(0.0),
        tauPtMin = cms.double(20.0),
        useData = cms.bool(True),
        electronIdVeto = cms.PSet(
            vtxFitConv = cms.bool(True),
            sihih_EE = cms.double(0.03),
            sihih_EB = cms.double(0.01),
            ooemoop_EB = cms.double(0.05),
            ooemoop_EE = cms.double(0.05),
            d0_EB = cms.double(0.02),
            d0_EE = cms.double(0.02),
            version = cms.string('VETO'),
            deta_EB = cms.double(0.004),
            deta_EE = cms.double(0.005),
            rhoSrc = cms.InputTag("kt6PFJetsForIsolation","rho"),
            dZ_EB = cms.double(0.1),
            dphi_EB = cms.double(0.03),
            pvSrc = cms.InputTag("goodOfflinePrimaryVertices"),
            dZ_EE = cms.double(0.1),
            mHits = cms.int32(0),
            reliso_EE = cms.double(0.1),
            cutsToIgnore = cms.vstring(''),
            reliso_EB = cms.double(0.1),
            hoe_EE = cms.double(0.01),
            hoe_EB = cms.double(0.12),
            dphi_EE = cms.double(0.02)
        ),
        pfEleSrc = cms.InputTag("particleFlow"),
        cutsToIgnore = cms.vstring('Trigger', 
            'Dilepton Veto'),
        tauSrc = cms.InputTag("selectedPatTausPFlow"),
        muEtaMax = cms.double(2.1),
        muJetDR = cms.double(0.3),
        electronSrc = cms.InputTag("selectedPatElectronsPFlow"),
        eleEtMinLoose = cms.double(15.0),
        eleJetDR = cms.double(0.5),
        muPtMinLoose = cms.double(10.0),
        jetEtaMax = cms.double(2.4),
        muEtaMaxLoose = cms.double(2.5),
        useNoID = cms.bool(True),
        eleEtMin = cms.double(20.0),
        ePtScale = cms.double(0.0),
        muPlusJets = cms.bool(False),
        eRelIso = cms.double(0.1),
        vertexCut = cms.double(1.0),
        ePtUncertaintyEE = cms.double(0.025),
        rhoIsoSrc = cms.InputTag("kt6PFJetsForIsolation","rho"),
        eleTrig = cms.string('HLT_Ele10_LW_L1R'),
        muRelIso = cms.double(0.125),
        jetPtMin = cms.double(30.0),
        minJets = cms.int32(1),
        jetUncertainty = cms.double(0.0),
        muTrig = cms.string('HLT_Mu9'),
        jetSrc = cms.InputTag("goodPatJetsCA8PrunedPF"),
        identifier = cms.string('CA8 Prunded PF'),
        pvSrc = cms.InputTag("goodOfflinePrimaryVertices")
    ),
    ePlusJets = cms.bool(False),
    muPlusJets = cms.bool(True)
)


process.pfTupleMuSelectedJets = cms.EDFilter("EDSHyFTSelector",
    matchByHand = cms.bool(True),
    shyftSelection = cms.PSet(
        muonSrc = cms.InputTag("selectedPatMuonsPFlow"),
        dxy = cms.double(0.02),
        eEt = cms.double(30.0),
        eleEtaMaxLoose = cms.double(2.5),
        tauTrig = cms.string('butz'),
        unclMetScale = cms.double(0.0),
        jecPayloads = cms.vstring('Jec12_V2_L1FastJet_AK5PFchs.txt', 
            'Jec12_V2_L2Relative_AK5PFchs.txt', 
            'Jec12_V2_L3Absolute_AK5PFchs.txt', 
            'Jec12_V2_L2L3Residual_AK5PFchs.txt', 
            'Jec12_V2_Uncertainty_AK5PFchs.txt'),
        muPtMin = cms.double(30.0),
        rawJetPtCut = cms.double(0.0),
        eleEtaMax = cms.double(2.4),
        useNoPFIso = cms.bool(True),
        elDcot = cms.double(0.02),
        rhoSrc = cms.InputTag("kt6PFJets","rho"),
        jetScale = cms.double(0.0),
        trigSrc = cms.InputTag("patTriggerEvent"),
        ePlusJets = cms.bool(True),
        metSrc = cms.InputTag("patMETs"),
        pfCandidateMap = cms.InputTag("particleFlow","electrons"),
        pvSelector = cms.PSet(
            maxZ = cms.double(24.0),
            minNdof = cms.double(4.0),
            NPV = cms.int32(1),
            maxRho = cms.double(2.0),
            pvSrc = cms.InputTag("goodOfflinePrimaryVertices")
        ),
        tauEtaMax = cms.double(2.4),
        elDist = cms.double(0.02),
        jetSmear = cms.double(0.0),
        tauPtMin = cms.double(20.0),
        useData = cms.bool(True),
        electronIdVeto = cms.PSet(
            vtxFitConv = cms.bool(True),
            sihih_EE = cms.double(0.03),
            sihih_EB = cms.double(0.01),
            ooemoop_EB = cms.double(0.05),
            ooemoop_EE = cms.double(0.05),
            d0_EB = cms.double(0.02),
            d0_EE = cms.double(0.02),
            version = cms.string('VETO'),
            deta_EB = cms.double(0.004),
            deta_EE = cms.double(0.005),
            rhoSrc = cms.InputTag("kt6PFJetsForIsolation","rho"),
            dZ_EB = cms.double(0.1),
            dphi_EB = cms.double(0.03),
            pvSrc = cms.InputTag("goodOfflinePrimaryVertices"),
            dZ_EE = cms.double(0.1),
            mHits = cms.int32(0),
            reliso_EE = cms.double(0.1),
            cutsToIgnore = cms.vstring(''),
            reliso_EB = cms.double(0.1),
            hoe_EE = cms.double(0.01),
            hoe_EB = cms.double(0.12),
            dphi_EE = cms.double(0.02)
        ),
        pfEleSrc = cms.InputTag("particleFlow"),
        cutsToIgnore = cms.vstring('Trigger', 
            'Dilepton Veto'),
        tauSrc = cms.InputTag("selectedPatTausPFlow"),
        muEtaMax = cms.double(2.1),
        muJetDR = cms.double(0.3),
        electronSrc = cms.InputTag("selectedPatElectronsPFlow"),
        eleEtMinLoose = cms.double(15.0),
        eleJetDR = cms.double(0.5),
        muPtMinLoose = cms.double(10.0),
        jetEtaMax = cms.double(2.4),
        muEtaMaxLoose = cms.double(2.5),
        useNoID = cms.bool(True),
        eleEtMin = cms.double(20.0),
        ePtScale = cms.double(0.0),
        muPlusJets = cms.bool(False),
        eRelIso = cms.double(0.1),
        vertexCut = cms.double(1.0),
        ePtUncertaintyEE = cms.double(0.025),
        rhoIsoSrc = cms.InputTag("kt6PFJetsForIsolation","rho"),
        eleTrig = cms.string('HLT_Ele10_LW_L1R'),
        muRelIso = cms.double(0.125),
        jetPtMin = cms.double(30.0),
        minJets = cms.int32(1),
        jetUncertainty = cms.double(0.0),
        muTrig = cms.string('HLT_Mu9'),
        jetSrc = cms.InputTag("goodPatJetsPFlow"),
        identifier = cms.string('Good PAT PF'),
        pvSrc = cms.InputTag("goodOfflinePrimaryVertices")
    ),
    ePlusJets = cms.bool(False),
    muPlusJets = cms.bool(True)
)


process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('edmTest.root'),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('p0', 
            'p1', 
            'p2', 
            'p3')
    ),
    outputCommands = cms.untracked.vstring('drop *', 
        'keep *_pfTuple*_*_*', 
        'keep *_patTriggerEvent_*_*', 
        'keep *_patTrigger_*_*', 
        'keep *_goodOfflinePrimaryVertices_*_*', 
        'keep *_caPrunedPFlow_SubJets_*')
)


process.patTriggerDefaultSequence = cms.Sequence(process.patTrigger+process.patTriggerEvent)


process.patTriggerMatchEmbedderDefaultSequence = cms.Sequence(process.cleanPatPhotonsTriggerMatch+process.cleanPatElectronsTriggerMatch+process.cleanPatMuonsTriggerMatch+process.cleanPatTausTriggerMatch+process.cleanPatJetsTriggerMatch+process.patMETsTriggerMatch)


process.triggerMatchingDefaultSequence = cms.Sequence(process.cleanMuonTriggerMatchHLTMu20+process.cleanMuonTriggerMatchHLTDoubleMu6+process.cleanPhotonTriggerMatchHLTPhoton26IsoVLPhoton18+process.cleanElectronTriggerMatchHLTEle27CaloIdVTCaloIsoTTrkIdTTrkIsoT+process.cleanTauTriggerMatchHLTDoubleIsoPFTau20Trk5+process.cleanJetTriggerMatchHLTJet240+process.metTriggerMatchHLTMET100+process.cleanMuonTriggerMatchHLTMu17CentralJet30+process.cleanJetTriggerMatchHLTMu17CentralJet30)


process.p0 = cms.Path(process.patTriggerDefaultSequence)


process.p1 = cms.Path(process.pfTupleEleCA8Pruned)


process.p2 = cms.Path(process.pfTupleMuCA8Pruned)


process.p3 = cms.Path()


process.p4 = cms.Path(process.pfTupleEleSelectedJets)


process.p5 = cms.Path(process.pfTupleMuSelectedJets)


process.outpath = cms.EndPath(process.out)


process.MessageLogger = cms.Service("MessageLogger",
    suppressInfo = cms.untracked.vstring(),
    debugs = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    suppressDebug = cms.untracked.vstring(),
    cout = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    cerr_stats = cms.untracked.PSet(
        threshold = cms.untracked.string('WARNING'),
        output = cms.untracked.string('cerr'),
        optionalPSet = cms.untracked.bool(True)
    ),
    warnings = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    default = cms.untracked.PSet(

    ),
    statistics = cms.untracked.vstring('cerr_stats'),
    cerr = cms.untracked.PSet(
        INFO = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        noTimeStamps = cms.untracked.bool(False),
        FwkReport = cms.untracked.PSet(
            reportEvery = cms.untracked.int32(100),
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(10000000)
        ),
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000)
        ),
        Root_NoDictionary = cms.untracked.PSet(
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(0)
        ),
        threshold = cms.untracked.string('INFO'),
        FwkJob = cms.untracked.PSet(
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(1)
        ),
        FwkSummary = cms.untracked.PSet(
            reportEvery = cms.untracked.int32(1),
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(10000000)
        ),
        optionalPSet = cms.untracked.bool(True),
        ERROR = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        )
    ),
    FrameworkJobReport = cms.untracked.PSet(
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        optionalPSet = cms.untracked.bool(True),
        FwkJob = cms.untracked.PSet(
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(10000000)
        )
    ),
    suppressWarning = cms.untracked.vstring('patTrigger'),
    errors = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    destinations = cms.untracked.vstring('warnings', 
        'errors', 
        'infos', 
        'debugs', 
        'cout', 
        'cerr'),
    debugModules = cms.untracked.vstring(),
    infos = cms.untracked.PSet(
        optionalPSet = cms.untracked.bool(True),
        Root_NoDictionary = cms.untracked.PSet(
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(0)
        ),
        placeholder = cms.untracked.bool(True)
    ),
    categories = cms.untracked.vstring('FwkJob', 
        'FwkReport', 
        'FwkSummary', 
        'Root_NoDictionary'),
    fwkJobReports = cms.untracked.vstring('FrameworkJobReport')
)


process.CSCGeometryESModule = cms.ESProducer("CSCGeometryESModule",
    appendToDataLabel = cms.string(''),
    useDDD = cms.bool(True),
    debugV = cms.untracked.bool(False),
    useGangedStripsInME1a = cms.bool(True),
    alignmentsLabel = cms.string(''),
    useOnlyWiresInME1a = cms.bool(False),
    useRealWireGeometry = cms.bool(True),
    useCentreTIOffsets = cms.bool(False),
    applyAlignment = cms.bool(True)
)


process.CaloGeometryBuilder = cms.ESProducer("CaloGeometryBuilder",
    SelectedCalos = cms.vstring('HCAL', 
        'ZDC', 
        'CASTOR', 
        'EcalBarrel', 
        'EcalEndcap', 
        'EcalPreshower', 
        'TOWER')
)


process.CaloTopologyBuilder = cms.ESProducer("CaloTopologyBuilder")


process.CaloTowerHardcodeGeometryEP = cms.ESProducer("CaloTowerHardcodeGeometryEP")


process.CastorDbProducer = cms.ESProducer("CastorDbProducer")


process.CastorHardcodeGeometryEP = cms.ESProducer("CastorHardcodeGeometryEP")


process.DTGeometryESModule = cms.ESProducer("DTGeometryESModule",
    appendToDataLabel = cms.string(''),
    fromDDD = cms.bool(True),
    applyAlignment = cms.bool(True),
    alignmentsLabel = cms.string('')
)


process.EcalBarrelGeometryEP = cms.ESProducer("EcalBarrelGeometryEP",
    applyAlignment = cms.bool(False)
)


process.EcalElectronicsMappingBuilder = cms.ESProducer("EcalElectronicsMappingBuilder")


process.EcalEndcapGeometryEP = cms.ESProducer("EcalEndcapGeometryEP",
    applyAlignment = cms.bool(False)
)


process.EcalLaserCorrectionService = cms.ESProducer("EcalLaserCorrectionService")


process.EcalPreshowerGeometryEP = cms.ESProducer("EcalPreshowerGeometryEP",
    applyAlignment = cms.bool(False)
)


process.EcalTrigTowerConstituentsMapBuilder = cms.ESProducer("EcalTrigTowerConstituentsMapBuilder",
    MapFile = cms.untracked.string('Geometry/EcalMapping/data/EndCap_TTMap.txt')
)


process.GlobalTrackingGeometryESProducer = cms.ESProducer("GlobalTrackingGeometryESProducer")


process.HcalHardcodeGeometryEP = cms.ESProducer("HcalHardcodeGeometryEP")


process.HcalTopologyIdealEP = cms.ESProducer("HcalTopologyIdealEP")


process.MuonDetLayerGeometryESProducer = cms.ESProducer("MuonDetLayerGeometryESProducer")


process.MuonNumberingInitialization = cms.ESProducer("MuonNumberingInitialization")


process.ParametrizedMagneticFieldProducer = cms.ESProducer("ParametrizedMagneticFieldProducer",
    version = cms.string('OAE_1103l_071212'),
    parameters = cms.PSet(
        BValue = cms.string('3_8T')
    ),
    label = cms.untracked.string('parametrizedField')
)


process.RPCGeometryESModule = cms.ESProducer("RPCGeometryESModule",
    useDDD = cms.untracked.bool(True),
    compatibiltyWith11 = cms.untracked.bool(True)
)


process.SiStripRecHitMatcherESProducer = cms.ESProducer("SiStripRecHitMatcherESProducer",
    ComponentName = cms.string('StandardMatcher'),
    NSigmaInside = cms.double(3.0)
)


process.StripCPEfromTrackAngleESProducer = cms.ESProducer("StripCPEESProducer",
    ComponentName = cms.string('StripCPEfromTrackAngle')
)


process.TrackerDigiGeometryESModule = cms.ESProducer("TrackerDigiGeometryESModule",
    appendToDataLabel = cms.string(''),
    fromDDD = cms.bool(True),
    applyAlignment = cms.bool(True),
    alignmentsLabel = cms.string('')
)


process.TrackerGeometricDetESModule = cms.ESProducer("TrackerGeometricDetESModule",
    fromDDD = cms.bool(True)
)


process.TrackerRecoGeometryESProducer = cms.ESProducer("TrackerRecoGeometryESProducer")


process.VolumeBasedMagneticFieldESProducer = cms.ESProducer("VolumeBasedMagneticFieldESProducer",
    scalingVolumes = cms.vint32(14100, 14200, 17600, 17800, 17900, 
        18100, 18300, 18400, 18600, 23100, 
        23300, 23400, 23600, 23800, 23900, 
        24100, 28600, 28800, 28900, 29100, 
        29300, 29400, 29600, 28609, 28809, 
        28909, 29109, 29309, 29409, 29609, 
        28610, 28810, 28910, 29110, 29310, 
        29410, 29610, 28611, 28811, 28911, 
        29111, 29311, 29411, 29611),
    scalingFactors = cms.vdouble(1, 1, 0.994, 1.004, 1.004, 
        1.005, 1.004, 1.004, 0.994, 0.965, 
        0.958, 0.958, 0.953, 0.958, 0.958, 
        0.965, 0.918, 0.924, 0.924, 0.906, 
        0.924, 0.924, 0.918, 0.991, 0.998, 
        0.998, 0.978, 0.998, 0.998, 0.991, 
        0.991, 0.998, 0.998, 0.978, 0.998, 
        0.998, 0.991, 0.991, 0.998, 0.998, 
        0.978, 0.998, 0.998, 0.991),
    overrideMasterSector = cms.bool(False),
    useParametrizedTrackerField = cms.bool(True),
    label = cms.untracked.string(''),
    version = cms.string('grid_1103l_090322_3_8t'),
    debugBuilder = cms.untracked.bool(False),
    paramLabel = cms.string('parametrizedField'),
    geometryVersion = cms.int32(90322),
    cacheLastVolume = cms.untracked.bool(True)
)


process.ZdcHardcodeGeometryEP = cms.ESProducer("ZdcHardcodeGeometryEP")


process.fakeForIdealAlignment = cms.ESProducer("FakeAlignmentProducer",
    appendToDataLabel = cms.string('fakeForIdeal')
)


process.hcal_db_producer = cms.ESProducer("HcalDbProducer",
    file = cms.untracked.string(''),
    dump = cms.untracked.vstring('')
)


process.idealForDigiCSCGeometry = cms.ESProducer("CSCGeometryESModule",
    appendToDataLabel = cms.string('idealForDigi'),
    useDDD = cms.bool(True),
    debugV = cms.untracked.bool(False),
    useGangedStripsInME1a = cms.bool(True),
    alignmentsLabel = cms.string('fakeForIdeal'),
    useOnlyWiresInME1a = cms.bool(False),
    useRealWireGeometry = cms.bool(True),
    useCentreTIOffsets = cms.bool(False),
    applyAlignment = cms.bool(False)
)


process.idealForDigiDTGeometry = cms.ESProducer("DTGeometryESModule",
    appendToDataLabel = cms.string('idealForDigi'),
    fromDDD = cms.bool(True),
    applyAlignment = cms.bool(False),
    alignmentsLabel = cms.string('fakeForIdeal')
)


process.idealForDigiTrackerGeometry = cms.ESProducer("TrackerDigiGeometryESModule",
    appendToDataLabel = cms.string('idealForDigi'),
    fromDDD = cms.bool(True),
    applyAlignment = cms.bool(False),
    alignmentsLabel = cms.string('fakeForIdeal')
)


process.siPixelQualityESProducer = cms.ESProducer("SiPixelQualityESProducer",
    ListOfRecordToMerge = cms.VPSet(cms.PSet(
        record = cms.string('SiPixelQualityFromDbRcd'),
        tag = cms.string('')
    ), 
        cms.PSet(
            record = cms.string('SiPixelDetVOffRcd'),
            tag = cms.string('')
        ))
)


process.siStripGainESProducer = cms.ESProducer("SiStripGainESProducer",
    printDebug = cms.untracked.bool(False),
    appendToDataLabel = cms.string(''),
    APVGain = cms.VPSet(cms.PSet(
        Record = cms.string('SiStripApvGainRcd'),
        NormalizationFactor = cms.untracked.double(1.0),
        Label = cms.untracked.string('')
    ), 
        cms.PSet(
            Record = cms.string('SiStripApvGain2Rcd'),
            NormalizationFactor = cms.untracked.double(1.0),
            Label = cms.untracked.string('')
        )),
    AutomaticNormalization = cms.bool(False)
)


process.siStripLorentzAngleDepESProducer = cms.ESProducer("SiStripLorentzAngleDepESProducer",
    LatencyRecord = cms.PSet(
        record = cms.string('SiStripLatencyRcd'),
        label = cms.untracked.string('')
    ),
    LorentzAngleDeconvMode = cms.PSet(
        record = cms.string('SiStripLorentzAngleRcd'),
        label = cms.untracked.string('deconvolution')
    ),
    LorentzAnglePeakMode = cms.PSet(
        record = cms.string('SiStripLorentzAngleRcd'),
        label = cms.untracked.string('peak')
    )
)


process.siStripQualityESProducer = cms.ESProducer("SiStripQualityESProducer",
    appendToDataLabel = cms.string(''),
    PrintDebugOutput = cms.bool(False),
    ThresholdForReducedGranularity = cms.double(0.3),
    UseEmptyRunInfo = cms.bool(False),
    ReduceGranularity = cms.bool(False),
    ListOfRecordToMerge = cms.VPSet(cms.PSet(
        record = cms.string('SiStripDetVOffRcd'),
        tag = cms.string('')
    ), 
        cms.PSet(
            record = cms.string('SiStripDetCablingRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('RunInfoRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadChannelRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadFiberRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadModuleRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadStripRcd'),
            tag = cms.string('')
        ))
)


process.sistripconn = cms.ESProducer("SiStripConnectivity")


process.GlobalTag = cms.ESSource("PoolDBESSource",
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string(''),
        enableReadOnlySessionOnUpdateConnection = cms.untracked.bool(False),
        idleConnectionCleanupPeriod = cms.untracked.int32(10),
        messageLevel = cms.untracked.int32(0),
        enablePoolAutomaticCleanUp = cms.untracked.bool(False),
        enableConnectionSharing = cms.untracked.bool(True),
        connectionRetrialTimeOut = cms.untracked.int32(60),
        connectionTimeOut = cms.untracked.int32(60),
        authenticationSystem = cms.untracked.int32(0),
        connectionRetrialPeriod = cms.untracked.int32(10)
    ),
    BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
    toGet = cms.VPSet(),
    connect = cms.string('frontier://FrontierProd/CMS_COND_31X_GLOBALTAG'),
    globaltag = cms.string('GR_P_V40_AN1::All')
)


process.XMLIdealGeometryESSource = cms.ESSource("XMLIdealGeometryESSource",
    geomXMLFiles = cms.vstring('Geometry/CMSCommonData/data/materials.xml', 
        'Geometry/CMSCommonData/data/rotations.xml', 
        'Geometry/CMSCommonData/data/normal/cmsextent.xml', 
        'Geometry/CMSCommonData/data/cms.xml', 
        'Geometry/CMSCommonData/data/cmsMother.xml', 
        'Geometry/CMSCommonData/data/cmsTracker.xml', 
        'Geometry/CMSCommonData/data/caloBase.xml', 
        'Geometry/CMSCommonData/data/cmsCalo.xml', 
        'Geometry/CMSCommonData/data/muonBase.xml', 
        'Geometry/CMSCommonData/data/cmsMuon.xml', 
        'Geometry/CMSCommonData/data/mgnt.xml', 
        'Geometry/CMSCommonData/data/beampipe.xml', 
        'Geometry/CMSCommonData/data/cmsBeam.xml', 
        'Geometry/CMSCommonData/data/muonMB.xml', 
        'Geometry/CMSCommonData/data/muonMagnet.xml', 
        'Geometry/TrackerCommonData/data/pixfwdMaterials.xml', 
        'Geometry/TrackerCommonData/data/pixfwdCommon.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq1x2.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq1x5.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq2x3.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq2x4.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPlaq2x5.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPanelBase.xml', 
        'Geometry/TrackerCommonData/data/pixfwdPanel.xml', 
        'Geometry/TrackerCommonData/data/pixfwdBlade.xml', 
        'Geometry/TrackerCommonData/data/pixfwdNipple.xml', 
        'Geometry/TrackerCommonData/data/pixfwdDisk.xml', 
        'Geometry/TrackerCommonData/data/pixfwdCylinder.xml', 
        'Geometry/TrackerCommonData/data/pixfwd.xml', 
        'Geometry/TrackerCommonData/data/pixbarmaterial.xml', 
        'Geometry/TrackerCommonData/data/pixbarladder.xml', 
        'Geometry/TrackerCommonData/data/pixbarladderfull.xml', 
        'Geometry/TrackerCommonData/data/pixbarladderhalf.xml', 
        'Geometry/TrackerCommonData/data/pixbarlayer.xml', 
        'Geometry/TrackerCommonData/data/pixbarlayer0.xml', 
        'Geometry/TrackerCommonData/data/pixbarlayer1.xml', 
        'Geometry/TrackerCommonData/data/pixbarlayer2.xml', 
        'Geometry/TrackerCommonData/data/pixbar.xml', 
        'Geometry/TrackerCommonData/data/tibtidcommonmaterial.xml', 
        'Geometry/TrackerCommonData/data/tibmaterial.xml', 
        'Geometry/TrackerCommonData/data/tibmodpar.xml', 
        'Geometry/TrackerCommonData/data/tibmodule0.xml', 
        'Geometry/TrackerCommonData/data/tibmodule0a.xml', 
        'Geometry/TrackerCommonData/data/tibmodule0b.xml', 
        'Geometry/TrackerCommonData/data/tibmodule2.xml', 
        'Geometry/TrackerCommonData/data/tibstringpar.xml', 
        'Geometry/TrackerCommonData/data/tibstring0ll.xml', 
        'Geometry/TrackerCommonData/data/tibstring0lr.xml', 
        'Geometry/TrackerCommonData/data/tibstring0ul.xml', 
        'Geometry/TrackerCommonData/data/tibstring0ur.xml', 
        'Geometry/TrackerCommonData/data/tibstring0.xml', 
        'Geometry/TrackerCommonData/data/tibstring1ll.xml', 
        'Geometry/TrackerCommonData/data/tibstring1lr.xml', 
        'Geometry/TrackerCommonData/data/tibstring1ul.xml', 
        'Geometry/TrackerCommonData/data/tibstring1ur.xml', 
        'Geometry/TrackerCommonData/data/tibstring1.xml', 
        'Geometry/TrackerCommonData/data/tibstring2ll.xml', 
        'Geometry/TrackerCommonData/data/tibstring2lr.xml', 
        'Geometry/TrackerCommonData/data/tibstring2ul.xml', 
        'Geometry/TrackerCommonData/data/tibstring2ur.xml', 
        'Geometry/TrackerCommonData/data/tibstring2.xml', 
        'Geometry/TrackerCommonData/data/tibstring3ll.xml', 
        'Geometry/TrackerCommonData/data/tibstring3lr.xml', 
        'Geometry/TrackerCommonData/data/tibstring3ul.xml', 
        'Geometry/TrackerCommonData/data/tibstring3ur.xml', 
        'Geometry/TrackerCommonData/data/tibstring3.xml', 
        'Geometry/TrackerCommonData/data/tiblayerpar.xml', 
        'Geometry/TrackerCommonData/data/tiblayer0.xml', 
        'Geometry/TrackerCommonData/data/tiblayer1.xml', 
        'Geometry/TrackerCommonData/data/tiblayer2.xml', 
        'Geometry/TrackerCommonData/data/tiblayer3.xml', 
        'Geometry/TrackerCommonData/data/tib.xml', 
        'Geometry/TrackerCommonData/data/tidmaterial.xml', 
        'Geometry/TrackerCommonData/data/tidmodpar.xml', 
        'Geometry/TrackerCommonData/data/tidmodule0.xml', 
        'Geometry/TrackerCommonData/data/tidmodule0r.xml', 
        'Geometry/TrackerCommonData/data/tidmodule0l.xml', 
        'Geometry/TrackerCommonData/data/tidmodule1.xml', 
        'Geometry/TrackerCommonData/data/tidmodule1r.xml', 
        'Geometry/TrackerCommonData/data/tidmodule1l.xml', 
        'Geometry/TrackerCommonData/data/tidmodule2.xml', 
        'Geometry/TrackerCommonData/data/tidringpar.xml', 
        'Geometry/TrackerCommonData/data/tidring0.xml', 
        'Geometry/TrackerCommonData/data/tidring0f.xml', 
        'Geometry/TrackerCommonData/data/tidring0b.xml', 
        'Geometry/TrackerCommonData/data/tidring1.xml', 
        'Geometry/TrackerCommonData/data/tidring1f.xml', 
        'Geometry/TrackerCommonData/data/tidring1b.xml', 
        'Geometry/TrackerCommonData/data/tidring2.xml', 
        'Geometry/TrackerCommonData/data/tid.xml', 
        'Geometry/TrackerCommonData/data/tidf.xml', 
        'Geometry/TrackerCommonData/data/tidb.xml', 
        'Geometry/TrackerCommonData/data/tibtidservices.xml', 
        'Geometry/TrackerCommonData/data/tibtidservicesf.xml', 
        'Geometry/TrackerCommonData/data/tibtidservicesb.xml', 
        'Geometry/TrackerCommonData/data/tobmaterial.xml', 
        'Geometry/TrackerCommonData/data/tobmodpar.xml', 
        'Geometry/TrackerCommonData/data/tobmodule0.xml', 
        'Geometry/TrackerCommonData/data/tobmodule2.xml', 
        'Geometry/TrackerCommonData/data/tobmodule4.xml', 
        'Geometry/TrackerCommonData/data/tobrodpar.xml', 
        'Geometry/TrackerCommonData/data/tobrod0c.xml', 
        'Geometry/TrackerCommonData/data/tobrod0l.xml', 
        'Geometry/TrackerCommonData/data/tobrod0h.xml', 
        'Geometry/TrackerCommonData/data/tobrod0.xml', 
        'Geometry/TrackerCommonData/data/tobrod1l.xml', 
        'Geometry/TrackerCommonData/data/tobrod1h.xml', 
        'Geometry/TrackerCommonData/data/tobrod1.xml', 
        'Geometry/TrackerCommonData/data/tobrod2c.xml', 
        'Geometry/TrackerCommonData/data/tobrod2l.xml', 
        'Geometry/TrackerCommonData/data/tobrod2h.xml', 
        'Geometry/TrackerCommonData/data/tobrod2.xml', 
        'Geometry/TrackerCommonData/data/tobrod3l.xml', 
        'Geometry/TrackerCommonData/data/tobrod3h.xml', 
        'Geometry/TrackerCommonData/data/tobrod3.xml', 
        'Geometry/TrackerCommonData/data/tobrod4c.xml', 
        'Geometry/TrackerCommonData/data/tobrod4l.xml', 
        'Geometry/TrackerCommonData/data/tobrod4h.xml', 
        'Geometry/TrackerCommonData/data/tobrod4.xml', 
        'Geometry/TrackerCommonData/data/tobrod5l.xml', 
        'Geometry/TrackerCommonData/data/tobrod5h.xml', 
        'Geometry/TrackerCommonData/data/tobrod5.xml', 
        'Geometry/TrackerCommonData/data/tob.xml', 
        'Geometry/TrackerCommonData/data/tecmaterial.xml', 
        'Geometry/TrackerCommonData/data/tecmodpar.xml', 
        'Geometry/TrackerCommonData/data/tecmodule0.xml', 
        'Geometry/TrackerCommonData/data/tecmodule0r.xml', 
        'Geometry/TrackerCommonData/data/tecmodule0s.xml', 
        'Geometry/TrackerCommonData/data/tecmodule1.xml', 
        'Geometry/TrackerCommonData/data/tecmodule1r.xml', 
        'Geometry/TrackerCommonData/data/tecmodule1s.xml', 
        'Geometry/TrackerCommonData/data/tecmodule2.xml', 
        'Geometry/TrackerCommonData/data/tecmodule3.xml', 
        'Geometry/TrackerCommonData/data/tecmodule4.xml', 
        'Geometry/TrackerCommonData/data/tecmodule4r.xml', 
        'Geometry/TrackerCommonData/data/tecmodule4s.xml', 
        'Geometry/TrackerCommonData/data/tecmodule5.xml', 
        'Geometry/TrackerCommonData/data/tecmodule6.xml', 
        'Geometry/TrackerCommonData/data/tecpetpar.xml', 
        'Geometry/TrackerCommonData/data/tecring0.xml', 
        'Geometry/TrackerCommonData/data/tecring1.xml', 
        'Geometry/TrackerCommonData/data/tecring2.xml', 
        'Geometry/TrackerCommonData/data/tecring3.xml', 
        'Geometry/TrackerCommonData/data/tecring4.xml', 
        'Geometry/TrackerCommonData/data/tecring5.xml', 
        'Geometry/TrackerCommonData/data/tecring6.xml', 
        'Geometry/TrackerCommonData/data/tecring0f.xml', 
        'Geometry/TrackerCommonData/data/tecring1f.xml', 
        'Geometry/TrackerCommonData/data/tecring2f.xml', 
        'Geometry/TrackerCommonData/data/tecring3f.xml', 
        'Geometry/TrackerCommonData/data/tecring4f.xml', 
        'Geometry/TrackerCommonData/data/tecring5f.xml', 
        'Geometry/TrackerCommonData/data/tecring6f.xml', 
        'Geometry/TrackerCommonData/data/tecring0b.xml', 
        'Geometry/TrackerCommonData/data/tecring1b.xml', 
        'Geometry/TrackerCommonData/data/tecring2b.xml', 
        'Geometry/TrackerCommonData/data/tecring3b.xml', 
        'Geometry/TrackerCommonData/data/tecring4b.xml', 
        'Geometry/TrackerCommonData/data/tecring5b.xml', 
        'Geometry/TrackerCommonData/data/tecring6b.xml', 
        'Geometry/TrackerCommonData/data/tecpetalf.xml', 
        'Geometry/TrackerCommonData/data/tecpetalb.xml', 
        'Geometry/TrackerCommonData/data/tecpetal0.xml', 
        'Geometry/TrackerCommonData/data/tecpetal0f.xml', 
        'Geometry/TrackerCommonData/data/tecpetal0b.xml', 
        'Geometry/TrackerCommonData/data/tecpetal3.xml', 
        'Geometry/TrackerCommonData/data/tecpetal3f.xml', 
        'Geometry/TrackerCommonData/data/tecpetal3b.xml', 
        'Geometry/TrackerCommonData/data/tecpetal6f.xml', 
        'Geometry/TrackerCommonData/data/tecpetal6b.xml', 
        'Geometry/TrackerCommonData/data/tecpetal8f.xml', 
        'Geometry/TrackerCommonData/data/tecpetal8b.xml', 
        'Geometry/TrackerCommonData/data/tecwheel.xml', 
        'Geometry/TrackerCommonData/data/tecwheela.xml', 
        'Geometry/TrackerCommonData/data/tecwheelb.xml', 
        'Geometry/TrackerCommonData/data/tecwheelc.xml', 
        'Geometry/TrackerCommonData/data/tecwheeld.xml', 
        'Geometry/TrackerCommonData/data/tecwheel6.xml', 
        'Geometry/TrackerCommonData/data/tecservices.xml', 
        'Geometry/TrackerCommonData/data/tecbackplate.xml', 
        'Geometry/TrackerCommonData/data/tec.xml', 
        'Geometry/TrackerCommonData/data/trackermaterial.xml', 
        'Geometry/TrackerCommonData/data/tracker.xml', 
        'Geometry/TrackerCommonData/data/trackerpixbar.xml', 
        'Geometry/TrackerCommonData/data/trackerpixfwd.xml', 
        'Geometry/TrackerCommonData/data/trackertibtidservices.xml', 
        'Geometry/TrackerCommonData/data/trackertib.xml', 
        'Geometry/TrackerCommonData/data/trackertid.xml', 
        'Geometry/TrackerCommonData/data/trackertob.xml', 
        'Geometry/TrackerCommonData/data/trackertec.xml', 
        'Geometry/TrackerCommonData/data/trackerbulkhead.xml', 
        'Geometry/TrackerCommonData/data/trackerother.xml', 
        'Geometry/EcalCommonData/data/eregalgo.xml', 
        'Geometry/EcalCommonData/data/ebalgo.xml', 
        'Geometry/EcalCommonData/data/ebcon.xml', 
        'Geometry/EcalCommonData/data/ebrot.xml', 
        'Geometry/EcalCommonData/data/eecon.xml', 
        'Geometry/EcalCommonData/data/eefixed.xml', 
        'Geometry/EcalCommonData/data/eehier.xml', 
        'Geometry/EcalCommonData/data/eealgo.xml', 
        'Geometry/EcalCommonData/data/escon.xml', 
        'Geometry/EcalCommonData/data/esalgo.xml', 
        'Geometry/EcalCommonData/data/eeF.xml', 
        'Geometry/EcalCommonData/data/eeB.xml', 
        'Geometry/HcalCommonData/data/hcalrotations.xml', 
        'Geometry/HcalCommonData/data/hcalalgo.xml', 
        'Geometry/HcalCommonData/data/hcalbarrelalgo.xml', 
        'Geometry/HcalCommonData/data/hcalendcapalgo.xml', 
        'Geometry/HcalCommonData/data/hcalouteralgo.xml', 
        'Geometry/HcalCommonData/data/hcalforwardalgo.xml', 
        'Geometry/HcalCommonData/data/average/hcalforwardmaterial.xml', 
        'Geometry/MuonCommonData/data/mbCommon.xml', 
        'Geometry/MuonCommonData/data/mb1.xml', 
        'Geometry/MuonCommonData/data/mb2.xml', 
        'Geometry/MuonCommonData/data/mb3.xml', 
        'Geometry/MuonCommonData/data/mb4.xml', 
        'Geometry/MuonCommonData/data/muonYoke.xml', 
        'Geometry/MuonCommonData/data/mf.xml', 
        'Geometry/ForwardCommonData/data/forward.xml', 
        'Geometry/ForwardCommonData/data/bundle/forwardshield.xml', 
        'Geometry/ForwardCommonData/data/brmrotations.xml', 
        'Geometry/ForwardCommonData/data/brm.xml', 
        'Geometry/ForwardCommonData/data/totemMaterials.xml', 
        'Geometry/ForwardCommonData/data/totemRotations.xml', 
        'Geometry/ForwardCommonData/data/totemt1.xml', 
        'Geometry/ForwardCommonData/data/totemt2.xml', 
        'Geometry/ForwardCommonData/data/ionpump.xml', 
        'Geometry/MuonCommonData/data/muonNumbering.xml', 
        'Geometry/TrackerCommonData/data/trackerStructureTopology.xml', 
        'Geometry/TrackerSimData/data/trackersens.xml', 
        'Geometry/TrackerRecoData/data/trackerRecoMaterial.xml', 
        'Geometry/EcalSimData/data/ecalsens.xml', 
        'Geometry/HcalCommonData/data/hcalsenspmf.xml', 
        'Geometry/HcalSimData/data/hf.xml', 
        'Geometry/HcalSimData/data/hfpmt.xml', 
        'Geometry/HcalSimData/data/hffibrebundle.xml', 
        'Geometry/HcalSimData/data/CaloUtil.xml', 
        'Geometry/MuonSimData/data/muonSens.xml', 
        'Geometry/DTGeometryBuilder/data/dtSpecsFilter.xml', 
        'Geometry/CSCGeometryBuilder/data/cscSpecsFilter.xml', 
        'Geometry/CSCGeometryBuilder/data/cscSpecs.xml', 
        'Geometry/RPCGeometryBuilder/data/RPCSpecs.xml', 
        'Geometry/ForwardCommonData/data/brmsens.xml', 
        'Geometry/HcalSimData/data/HcalProdCuts.xml', 
        'Geometry/EcalSimData/data/EcalProdCuts.xml', 
        'Geometry/EcalSimData/data/ESProdCuts.xml', 
        'Geometry/TrackerSimData/data/trackerProdCuts.xml', 
        'Geometry/TrackerSimData/data/trackerProdCutsBEAM.xml', 
        'Geometry/MuonSimData/data/muonProdCuts.xml', 
        'Geometry/ForwardSimData/data/ForwardShieldProdCuts.xml', 
        'Geometry/CMSCommonData/data/FieldParameters.xml'),
    rootNodeName = cms.string('cms:OCMS')
)


process.eegeom = cms.ESSource("EmptyESSource",
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('EcalMappingRcd'),
    firstValid = cms.vuint32(1)
)


process.es_hardcode = cms.ESSource("HcalHardcodeCalibrations",
    toGet = cms.untracked.vstring('GainWidths')
)


process.magfield = cms.ESSource("XMLIdealGeometryESSource",
    geomXMLFiles = cms.vstring('Geometry/CMSCommonData/data/normal/cmsextent.xml', 
        'Geometry/CMSCommonData/data/cms.xml', 
        'Geometry/CMSCommonData/data/cmsMagneticField.xml', 
        'MagneticField/GeomBuilder/data/MagneticFieldVolumes_1103l.xml', 
        'MagneticField/GeomBuilder/data/MagneticFieldParameters_07_2pi.xml', 
        'Geometry/CMSCommonData/data/materials.xml'),
    rootNodeName = cms.string('cmsMagneticField:MAGF')
)


process.prefer("magfield")

process.CondDBSetup = cms.PSet(
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string(''),
        enableReadOnlySessionOnUpdateConnection = cms.untracked.bool(False),
        idleConnectionCleanupPeriod = cms.untracked.int32(10),
        messageLevel = cms.untracked.int32(0),
        enablePoolAutomaticCleanUp = cms.untracked.bool(False),
        enableConnectionSharing = cms.untracked.bool(True),
        connectionRetrialTimeOut = cms.untracked.int32(60),
        connectionTimeOut = cms.untracked.int32(60),
        authenticationSystem = cms.untracked.int32(0),
        connectionRetrialPeriod = cms.untracked.int32(10)
    )
)

process.fieldScaling = cms.PSet(
    scalingVolumes = cms.vint32(14100, 14200, 17600, 17800, 17900, 
        18100, 18300, 18400, 18600, 23100, 
        23300, 23400, 23600, 23800, 23900, 
        24100, 28600, 28800, 28900, 29100, 
        29300, 29400, 29600, 28609, 28809, 
        28909, 29109, 29309, 29409, 29609, 
        28610, 28810, 28910, 29110, 29310, 
        29410, 29610, 28611, 28811, 28911, 
        29111, 29311, 29411, 29611),
    scalingFactors = cms.vdouble(1, 1, 0.994, 1.004, 1.004, 
        1.005, 1.004, 1.004, 0.994, 0.965, 
        0.958, 0.958, 0.953, 0.958, 0.958, 
        0.965, 0.918, 0.924, 0.924, 0.906, 
        0.924, 0.924, 0.918, 0.991, 0.998, 
        0.998, 0.978, 0.998, 0.998, 0.991, 
        0.991, 0.998, 0.998, 0.978, 0.998, 
        0.998, 0.991, 0.991, 0.998, 0.998, 
        0.978, 0.998, 0.998, 0.991)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

