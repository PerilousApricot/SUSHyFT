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

options.register('sampleNameInput',
                 'Wjets',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Sample name to give histograms")

options.register ('allSys',
                  1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run all systematics (1) or just the central one (0)")

options.register('ignoreTrigger',
                 1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Ignore trigger in selection")

options.register('eleEt',
                  30.,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.float,
                 "electron et threshold")

options.register('ttbsmPAT',
                 1,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "If running on ttbsm PAT tuples"
                 )
options.register('use42X',
                 0,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "PAT tuplese done in 4_2_2"
                 )
options.register('pileupDataFile',
				 'PUData_dist.root',
				 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
				 "Data pileup distribution file name")
options.register('pileupMCFile',
				 'PUMC_dist.root',
				 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
				 "MC pileup distribution file name")


options.parseArguments()

print options

import sys

if options.useFlavorHistory > 0 :
    useFlavorHistory = True
else :
    useFlavorHistory = False

if options.use42X > 0:
   use42XMC = True
else: use42XMC = False

inputDoMC=True

inputSampleName = options.sampleNameInput

pileupDataFile = options.pileupDataFile

pileupMCFile = options.pileupMCFile

inputCutsToIgnore = []
if options.ignoreTrigger == 1 :
    inputCutsToIgnore.append( 'Trigger' )

## Source
if len(options.inputFiles) == 0 and options.ttbsmPAT > 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
		'/store/user/lpctlbsm/srappocc/TTJets_TuneZ2_7TeV-madgraph-tauola/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_100_1_5nQ.root',
#        '/store/user/deisher/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/ttbsm_v8_Summer11-PU_S4_START42_V11-v1/87037ef7c828ea57e128f1ace23a632e/ttbsm_42x_mc_9_1_jQj.root',
#        '/store/user/deisher/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/ttbsm_v8_Summer11-PU_S4_START42_V11-v1/87037ef7c828ea57e128f1ace23a632e/ttbsm_42x_mc_99_1_ubf.root',
#        '/store/user/deisher/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/ttbsm_v8_Summer11-PU_S4_START42_V11-v1/87037ef7c828ea57e128f1ace23a632e/ttbsm_42x_mc_98_1_Wy2.root',
#        '/store/user/deisher/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/ttbsm_v8_Summer11-PU_S4_START42_V11-v1/87037ef7c828ea57e128f1ace23a632e/ttbsm_42x_mc_97_1_3yL.root',
#        '/store/user/deisher/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/ttbsm_v8_Summer11-PU_S4_START42_V11-v1/87037ef7c828ea57e128f1ace23a632e/ttbsm_42x_mc_96_2_KxX.root',
#        '/store/user/deisher/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/ttbsm_v8_Summer11-PU_S4_START42_V11-v1/87037ef7c828ea57e128f1ace23a632e/ttbsm_42x_mc_95_1_R09.root',
#        '/store/user/deisher/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/ttbsm_v8_Summer11-PU_S4_START42_V11-v1/87037ef7c828ea57e128f1ace23a632e/ttbsm_42x_mc_94_1_fV1.root',
#        '/store/user/deisher/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/ttbsm_v8_Summer11-PU_S4_START42_V11-v1/87037ef7c828ea57e128f1ace23a632e/ttbsm_42x_mc_93_1_Hkr.root',
#        '/store/user/deisher/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/ttbsm_v8_Summer11-PU_S4_START42_V11-v1/87037ef7c828ea57e128f1ace23a632e/ttbsm_42x_mc_92_1_qsn.root',
#        '/store/user/deisher/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/ttbsm_v8_Summer11-PU_S4_START42_V11-v1/87037ef7c828ea57e128f1ace23a632e/ttbsm_42x_mc_91_1_UPo.root',
#        '/store/user/deisher/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/ttbsm_v8_Summer11-PU_S4_START42_V11-v1/87037ef7c828ea57e128f1ace23a632e/ttbsm_42x_mc_90_1_kqT.root',
#        '/store/user/deisher/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/ttbsm_v8_Summer11-PU_S4_START42_V11-v1/87037ef7c828ea57e128f1ace23a632e/ttbsm_42x_mc_8_1_KfN.root',
#        '/store/user/deisher/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/ttbsm_v8_Summer11-PU_S4_START42_V11-v1/87037ef7c828ea57e128f1ace23a632e/ttbsm_42x_mc_89_1_GZl.root',
#        '/store/user/deisher/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/ttbsm_v8_Summer11-PU_S4_START42_V11-v1/87037ef7c828ea57e128f1ace23a632e/ttbsm_42x_mc_88_1_uYP.root',
#        '/store/user/deisher/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/ttbsm_v8_Summer11-PU_S4_START42_V11-v1/87037ef7c828ea57e128f1ace23a632e/ttbsm_42x_mc_87_1_H05.root',
        )
                                )                           
elif len(options.inputFiles) == 0 and options.ttbsmPAT == 0:
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
        '/store/user/skhalil/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/shyft_414_v1/c43141acf8ecb16bf2b2a65d482d5d16/shyft_414patch1_mc_9_2_eVJ.root',
        '/store/user/skhalil/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/shyft_414_v1/c43141acf8ecb16bf2b2a65d482d5d16/shyft_414patch1_mc_8_2_oT0.root',
        '/store/user/skhalil/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/shyft_414_v1/c43141acf8ecb16bf2b2a65d482d5d16/shyft_414patch1_mc_7_1_J25.root',
        '/store/user/skhalil/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/shyft_414_v1/c43141acf8ecb16bf2b2a65d482d5d16/shyft_414patch1_mc_6_1_xjJ.root',
        '/store/user/skhalil/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/shyft_414_v1/c43141acf8ecb16bf2b2a65d482d5d16/shyft_414patch1_mc_5_1_SOs.root',
        '/store/user/skhalil/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/shyft_414_v1/c43141acf8ecb16bf2b2a65d482d5d16/shyft_414patch1_mc_51_1_Ghi.root',
        '/store/user/skhalil/TToBLNu_TuneZ2_s-channel_7TeV-madgraph/shyft_414_v1/c43141acf8ecb16bf2b2a65d482d5d16/shyft_414patch1_mc_50_1_jHG.root',
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

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("shyftStudies.root")
                                   )

payloads = [
    'Jec12_V1_L1FastJet_AK5PFchs.txt',
    'Jec12_V1_L2Relative_AK5PFchs.txt',
    'Jec12_V1_L3Absolute_AK5PFchs.txt',
    'Jec12_V1_L2L3Residual_AK5PFchs.txt',
    'Jec12_V1_Uncertainty_AK5PFchs.txt'
]
#_____________________________________PF__________________________________________________

if options.ttbsmPAT > 0:
    
    process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                        shyftAnalysis = inputShyftAnalysis.clone(
        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
        metSrc = cms.InputTag('patMETsPFlow'),
        jetSrc = cms.InputTag('goodPatJetsPFlow'),
        pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
        ePlusJets = cms.bool( False ),
        muPlusJets = cms.bool( True ),        
        jetPtMin = cms.double(30.0),##
        minJets = cms.int32(5),
        metMin = cms.double(30.0),
	muPtMin = cms.double(35.0),
#        eEtCut = cms.double(options.eleEt),
        use42X  = cms.bool(use42XMC),
        heavyFlavour = cms.bool( useFlavorHistory ),
        doMC = cms.bool( inputDoMC),
        sampleName = cms.string(inputSampleName),
        identifier = cms.string('PF'),
        jetAlgo = cms.string("pf"),
        simpleSFCalc = cms.bool(False),                                        
        reweightBTagEff = cms.bool(True),
        weightSFCalc = cms.bool(True),                                        
        useCustomPayload = cms.bool(False),
        bcEffScale = cms.double(1.00),
        lfEffScale = cms.double(1.00),
        jetSmear = cms.double(0.1),
		cutsToIgnore=cms.vstring(inputCutsToIgnore),
		reweightPU = cms.bool(False),
		reweightPU3D = cms.bool(True),
		pileupData = cms.string( pileupDataFile ),
		pileupMC = cms.string( pileupMCFile ),
        jecPayloads = cms.vstring( payloads )

        
        )                                    
                                        )

    
elif options.ttbsmPAT == 0 :    
    process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                        shyftAnalysis = inputShyftAnalysis.clone(
        muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
        electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
        metSrc = cms.InputTag('patMETsPFlow'),
        jetSrc = cms.InputTag('selectedPatJetsPFlow'),
        ePlusJets = cms.bool(False),
        muPlusJets = cms.bool(True),
        jetPtMin = cms.double(30.0),##
        minJets = cms.int32(5),
        metMin = cms.double(30.0),
        eEtCut = cms.double(options.eleEt),
        heavyFlavour = cms.bool( useFlavorHistory ),
        doMC = cms.bool( inputDoMC),
        sampleName = cms.string(inputSampleName),
        identifier = cms.string('PF'),
        jetAlgo = cms.string("pf"),
        simpleSFCalc = cms.bool(False),                                        
        reweightBTagEff = cms.bool(True),
        weightSFCalc = cms.bool(True),                                        
        useCustomPayload = cms.bool(False),
        useTTBSMPat = cms.bool(False),
        bcEffScale = cms.double(1.00),
        lfEffScale = cms.double(1.00),
        jetSmear = cms.double(0.1),
        cutsToIgnore=cms.vstring(inputCutsToIgnore)
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

#___________Special case of MET < 20 GeV_________________
process.pfShyftAnaMETMax20 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MET <20'),
    metMin = cms.double(0.0),
    metMax = cms.double(20.0),
    )
    )
    
#_____________QCD WP95_______________________
process.pfShyftAnaQCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    eRelIso = cms.double(0.15),
    identifier = cms.string('PF MET, WP95')
    )
    )

process.pfShyftAnaMETMax20QCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MET <20, WP95'),
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    metMin = cms.double(0.0),
    metMax = cms.double(20.0),
    eRelIso = cms.double(0.15),
    )
    )
#___________no MET cut________________
process.pfShyftAnaNoMET = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    identifier = cms.string('PF no MET')
    )
    )

process.pfShyftAnaQCDWP95NoMET = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    eRelIso = cms.double(0.15),
    identifier = cms.string('PF no MET, WP95')
    )
    )

#______________To extract secvtx shapes and >=3 tag jets count _____________________

process.pfShyftAnaMC = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC'),
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
	reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    )
    )

process.pfShyftAnaMCNoMET = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC no MET'),
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
    reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    metMin = cms.double(0.0),
    )
    )


process.pfShyftAnaMCQCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC WP95'),
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
	reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    eRelIso = cms.double(0.15),
    )
    )

process.pfShyftAnaMCQCDWP95NoMET = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC WP95, NoMET'),
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
	reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    eRelIso = cms.double(0.15),
    metMin = cms.double(0.0),
    )
    )

process.pfShyftAnaMCMETMax20 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC MET < 20'),
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
    reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    metMin = cms.double(0.0),
    metMax = cms.double(20.0),
    )
    )
process.pfShyftAnaMCMETMax20QCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    identifier = cms.string('PF MC MET < 20, WP95'),
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
    reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    eRelIso = cms.double(0.15),
    metMin = cms.double(0.0),
    metMax = cms.double(20.0),
    )
    )






################################################
#_______________Systematics__________________
#################################################

#________________________btagging Systematics ____________________________

##HF

process.pfShyftAnaReweightedBTag080 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 080'),
        bcEffScale = cms.double(0.80),        
        )
    )

process.pfShyftAnaReweightedBTag090 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 090'),
        bcEffScale = cms.double(0.90),
        )
    )


process.pfShyftAnaReweightedBTag110 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 110'),
        bcEffScale = cms.double(1.10),
        )
    )

process.pfShyftAnaReweightedBTag120 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted BTag 120'),
        bcEffScale = cms.double(1.20),
        )
    )


##LF

process.pfShyftAnaReweightedLFTag080 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 080'),
        lfEffScale = cms.double(0.80),
        )
    )

process.pfShyftAnaReweightedLFTag090 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 090'),        
        lfEffScale = cms.double(0.90),
        )
    )

process.pfShyftAnaReweightedLFTag110 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 110'),     
        lfEffScale = cms.double(1.10),
        )
    )

process.pfShyftAnaReweightedLFTag120 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        identifier = cms.string('PF Reweighted LFTag 120'),
        lfEffScale = cms.double(1.20)
        )
    )

#____________________JES up and down _______________________

process.pfShyftAnaJES095 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(-1.0),
        jetUncertainty = cms.double(0.00),
        identifier = cms.string('PFJES095')
        )
    )

process.pfShyftAnaJES105 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        jetScale = cms.double(1.0),
        jetUncertainty = cms.double(0.00),
        identifier = cms.string('PFJES105')
        )
    )

#____________________JER _______________________
process.pfShyftAnaJER000 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        jetSmear = cms.double(0.00),
        identifier = cms.string('PFJER000')
        )
    )

process.pfShyftAnaJER020 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        jetSmear = cms.double(0.20),
        identifier = cms.string('PFJER020')
        )
    )

#____________________Pileup _______________________
process.pfShyftAnaPUup = process.pfShyftAna.clone(
	shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
		puUp = cms.bool(True),
		identifier = cms.string('PFPUup')
		)
	)

process.pfShyftAnaPUdown = process.pfShyftAna.clone(
	shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
		puDn = cms.bool(True),
		identifier = cms.string('PFPUdown')
		)
	)

process.pfShyftAnaNoPUReweight = process.pfShyftAna.clone(
	shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
		reweightPU = cms.bool(False),
		reweightPU3D = cms.bool(False),
		identifier = cms.string('PFNoPUReweighting')
		)
	)

#____________________MET Resolution _______________________
process.pfShyftAnaMETRES090 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        unclMetScale = cms.double( 0.90 ),
        identifier = cms.string('PFMETRES090')
        )
    )

process.pfShyftAnaMETRES110 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        unclMetScale = cms.double( 1.10 ),
        identifier = cms.string('PFMETRES110')
        )
    )

process.pfShyftAnaEleEEPt125 =  process.pfShyftAna.clone(
     shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        ePtScale = cms.double(1.0),
        ePtUncertaintyEE = cms.double( 0.025),
        identifier = cms.string('PFEleEEPt125')
        )
    )

process.pfShyftAnaEleEEPt075 =  process.pfShyftAna.clone(
     shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
        ePtScale = cms.double(-1.0),
        ePtUncertaintyEE = cms.double( 0.025),
        identifier = cms.string('PFEleEEPt075')
        )
    )

process.s = cms.Sequence(
   process.pfShyftAna*                 
   process.pfShyftAnaLooseNoMETWithD0*
   process.pfShyftAnaNoMET*
   
   process.pfShyftAnaJES095*    
   process.pfShyftAnaJES105*
   process.pfShyftAnaMETRES090*
   process.pfShyftAnaMETRES110*
   process.pfShyftAnaJER000*
	process.pfShyftAnaJER020*
	process.pfShyftAnaPUup*
	process.pfShyftAnaPUdown*
	process.pfShyftAnaNoPUReweight*
#   process.pfShyftAnaEleEEPt125*
#   process.pfShyftAnaEleEEPt075*
   process.pfShyftAnaMC*
   process.pfShyftAnaMCNoMET*   
#   process.pfShyftAnaMETMax20*
#   process.pfShyftAnaMCMETMax20*
   process.pfShyftAnaReweightedBTag080*
   process.pfShyftAnaReweightedBTag090*
   process.pfShyftAnaReweightedBTag110*
   process.pfShyftAnaReweightedBTag120*
   process.pfShyftAnaReweightedLFTag080*
   process.pfShyftAnaReweightedLFTag090*
   process.pfShyftAnaReweightedLFTag110*
   process.pfShyftAnaReweightedLFTag120
   
#   process.pfShyftAnaQCDWP95*
#   process.pfShyftAnaQCDWP95NoMET*
#   process.pfShyftAnaMCQCDWP95*
#   process.pfShyftAnaMCQCDWP95NoMET*
#   process.pfShyftAnaMETMax20QCDWP95*
#   process.pfShyftAnaMCMETMax20QCDWP95
   )

process.p = cms.Path(
    process.pfShyftAna*
    process.pfShyftAnaMC
    )

if options.allSys == 1 :
    process.p *= process.s

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
