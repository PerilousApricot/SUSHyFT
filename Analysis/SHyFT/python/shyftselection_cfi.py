import FWCore.ParameterSet.Config as cms

#from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector as pvSel
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
from PhysicsTools.SelectorUtils.pfMuonSelector_cfi import pfMuonSelector
from PhysicsTools.SelectorUtils.pfElectronSelector_cfi import pfElectronSelector
from Analysis.SHyFT.cutbasedIDSelector_cfi import cutbasedIDSelector

wplusjetsAnalysis = cms.PSet(
    
    electronIdVeto = cutbasedIDSelector.clone(
    version = cms.string('VETO')
    ),
    
    # Primary vertex
    pvSelector = cms.PSet(
    pvSrc = cms.InputTag('goodOfflinePrimaryVertices'),
    minNdof = cms.double(4.0),
    maxZ = cms.double(24.0),
    maxRho = cms.double(2.0),
    NPV = cms.int32(1),
    ),
    
    # input parameter sets
    muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
    electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
    jetSrc = cms.InputTag('goodPatJetsPFlow'),
    metSrc = cms.InputTag('patMETsPFlow'),
    trigSrc = cms.InputTag('patTriggerEvent'),
    muTrig = cms.string('HLT_Mu9'),
    eleTrig = cms.string('HLT_Ele10_LW_L1R'),
    pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
    rhoSrc  = cms.InputTag('kt6PFJets', 'rho'),
    rhoIsoSrc = cms.InputTag("kt6PFJetsForIsolation", 'rho'),
    pfEleSrc  = cms.InputTag("particleFlow"),
    useNoPFIso = cms.bool(False),
    useNoID  = cms.bool(False),
    
    # kinematic cuts
    minJets        = cms.int32( 1 ),
    muPlusJets     = cms.bool( True ),
    ePlusJets      = cms.bool( False ),
    muPtMin        = cms.double( 30.0 ),
    muEtaMax       = cms.double( 2.1 ),
    eleEtMin       = cms.double( 20.0 ),
    eleEtaMax      = cms.double( 2.4 ),
    muPtMinLoose   = cms.double( 10.0 ),#mu pt to be vetoed in mu+jets
    muEtaMaxLoose  = cms.double( 2.5 ), #mu eta to be vetoed in mu+jets
    eleEtMinLoose  = cms.double( 15.0 ),#ele pt to be vetoed in muon
    eleEtaMaxLoose = cms.double( 2.5 ), #eta to be vetoed in muon
    elDist         = cms.double( 0.02 ),
    elDcot         = cms.double( 0.02 ),
    eRelIso        = cms.double( 0.1 ),
    eEt            = cms.double( 30. ),
    muRelIso       = cms.double( 0.125),
    vertexCut      = cms.double( 1.),
    dxy            = cms.double( 0.02),
    jetPtMin       = cms.double( 30.0 ),
    jetEtaMax      = cms.double( 2.4 ),
    jetScale       = cms.double( 0.0 ),
    jetUncertainty = cms.double( 0.0 ),
    jetSmear       = cms.double( 0.0 ),
    ePtScale       = cms.double( 0.0 ),
    ePtUncertaintyEE = cms.double( 0.025), 
    unclMetScale   = cms.double( 0.0 ),
    muJetDR        = cms.double( 0.3 ),
    eleJetDR       = cms.double( 0.5 ),
    rawJetPtCut    = cms.double( 0.0 ),
    useData        = cms.bool(False),
    pfCandidateMap = cms.InputTag('particleFlow:electrons'),
    jecPayloads    = cms.vstring([
    'Jec12_V2_L1FastJet_AK5PFchs.txt',
    'Jec12_V2_L2Relative_AK5PFchs.txt',
    'Jec12_V2_L3Absolute_AK5PFchs.txt',
    'Jec12_V2_L2L3Residual_AK5PFchs.txt',
    'Jec12_V2_Uncertainty_AK5PFchs.txt', ])
   
    #jecPayload     = cms.string('Jec12_V2_AK5PFchs_Uncertainty.txt')
)
