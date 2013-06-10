import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

#input stuff for Run/Lumi selection with the "JSON"-formatted files from the PVT group
import FWCore.PythonUtilities.LumiList as LumiList
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(                                'dcap:///pnfs/cms/WAX/11/store/user/rappocc/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/shyft_387_v1/2f94777c47687658400e9bd1c4f72c89/shyft_386_mc_1_1_AoD.root'
                            ))

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )



from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector

process.muonInJet = cms.EDFilter('EDMuonInJetSelector',
                                   muonSrc = cms.InputTag('selectedPatMuonsPFlowLoose'),
                                   jetSrc = cms.InputTag('selectedPatJetsPFlowLoose'),
                                   jetPtMin = cms.double(25.0),
                                   jetEtaMax = cms.double(2.4),
                                   muPtMin = cms.double(10.0),
                                   muEtaMax = cms.double(2.1),
                                   muJetDR = cms.double(0.5),
                                   btagDisc1 = cms.string('simpleSecondaryVertexHighEffBJetTags'),
                                   btagDisc2 = cms.string('simpleSecondaryVertexHighEffBJetTags'),
                                   btagDiscCut1 = cms.double(1.74),
                                   btagDiscCut2 = cms.double(1.74),
                                   muonId = cms.PSet(
                                       version = cms.string('FALL10'),
                                       Chi2 = cms.double(10.0),
                                       D0 = cms.double(0.02),
                                       ED0 = cms.double(999.0),
                                       SD0 = cms.double(999.0),
                                       NHits = cms.int32(11),
                                       NValMuHits = cms.int32(0),
                                       ECalVeto = cms.double(999.0),
                                       HCalVeto = cms.double(999.0),
                                       RelIso = cms.double(0.05),
                                       LepZ = cms.double(1.0),
                                       nPixelHits = cms.int32(1),
                                       nMatchedStations=cms.int32(1),
                                       cutsToIgnore = cms.vstring('ED0', 'SD0', 'ECalVeto', 'HCalVeto', 'RelIso', 'D0'),
                                       RecalcFromBeamSpot = cms.bool(False),
                                       beamLineSrc = cms.InputTag("offlineBeamSpot"),
                                       pvSrc = cms.InputTag("offlinePrimaryVertices"),
                                       ),
                                   pfjetId = pfJetIDSelector.clone() 
                                   )



process.jetsDump = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("muonInJet", "jets"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("jet"),
    variables = cms.VPSet(

    cms.PSet(
    tag = cms.untracked.string("Pt"),
    quantity = cms.untracked.string("pt")
    ),
    cms.PSet(
    tag = cms.untracked.string("Eta"),
    quantity = cms.untracked.string("eta")
    ),
   
        cms.PSet(
    tag = cms.untracked.string("Phi"),
    quantity = cms.untracked.string("phi")
    ),


        cms.PSet(
    tag = cms.untracked.string("SimpleSecondaryVertexHighEff"),
    quantity = cms.untracked.string("bDiscriminator('SimpleSecondaryVertexHighEff')")
    ),

        cms.PSet(
    tag = cms.untracked.string("SimpleSecondaryVertexHighPur"),
    quantity = cms.untracked.string("bDiscriminator('SimpleSecondaryVertexHighPur')")
    ),

        cms.PSet(
    tag = cms.untracked.string("SecvtxMass"),
    quantity = cms.untracked.string("userFloat('secvtxMass')")
    ),


    ),

    )



process.p = cms.Path(
    process.muonInJet*
    process.jetsDump
    )


process.MessageLogger.cerr.FwkReport.reportEvery = 1000



process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string("muonInJet.root"),
                               SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
                               outputCommands = cms.untracked.vstring('drop *',
#                                                                      'keep *_muonInJet_*_*',
                                                                      'keep *_jetsDump_*_*' ) 
                               )
process.outpath = cms.EndPath(process.out)
