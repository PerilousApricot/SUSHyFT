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
                  35.,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.float,
                 "electron et threshold")

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

inputDoMC=True

inputSampleName = options.sampleNameInput

pileupDataFile = options.pileupDataFile

pileupMCFile = options.pileupMCFile

inputCutsToIgnore = []
if options.ignoreTrigger == 1 :
    inputCutsToIgnore.append( 'Trigger' )

## Source
if len(options.inputFiles) == 0:
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
        '/store/user/lpctlbsm/srappocc/TTJets_TuneZ2_7TeV-madgraph-tauola/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_100_1_5nQ.root',
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
    
process.pfShyftAna = cms.EDAnalyzer('EDSHyFT',
                                    shyftAnalysis = inputShyftAnalysis.clone(
    muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
    electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
    metSrc = cms.InputTag('patMETsPFlow'),
    jetSrc = cms.InputTag('goodPatJetsPFlow'),
    pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
    ePlusJets = cms.bool( True ),
    muPlusJets = cms.bool(False),
    usePFIso = cms.bool(True),
    eEtCut = cms.double(options.eleEt),
    useVBTFDetIso  = cms.bool(False),

    electronIdTight = cms.PSet(
    version = cms.string('SPRING11'),
    MVA = cms.double(-0.01),
    MaxMissingHits = cms.int32(0),
    D0 = cms.double(0.02),
    electronIDused = cms.string('eidHyperTight1MC'),
    ConversionRejection = cms.bool(True),
    PFIso = cms.double(0.1),
    cutsToIgnore = cms.vstring('MVA','MaxMissingHits', 'ConversionRejection'),
    ),
    
    jetPtMin = cms.double(30.0),##
    minJets = cms.int32(5),
    metMin = cms.double(20.0),      
    reweightPU = cms.bool(True),  
    heavyFlavour = cms.bool( useFlavorHistory ),
    doMC = cms.bool( inputDoMC),
    sampleName = cms.string(inputSampleName),   
    jetAlgo = cms.string("pf"),
    simpleSFCalc = cms.bool(False),                                            
    weightSFCalc = cms.bool(True),
    reweightBTagEff = cms.bool(True),
    useCustomPayload = cms.bool(False),
    bcEffScale = cms.double(1.00),
    lfEffScale = cms.double(1.00),
    jetSmear = cms.double(0.1),
    cutsToIgnore=cms.vstring(inputCutsToIgnore),
    reweightPU = cms.bool(False),
	reweightPU3D = cms.bool(True),
    pileupData = cms.string( pileupDataFile ),
    pileupMC = cms.string( pileupMCFile ),
    identifier = cms.string('PF'),
    jecPayloads = cms.vstring( payloads )
    )                                    
                                    )

process.pfShyftAnaMC = process.pfShyftAna.clone( #To extract secvtx shapes and >=3 tag jets count
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
	reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    identifier = cms.string('PF MC'),
    )
    )
#___________no MET cut________________
process.pfShyftAnaNoMET = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    identifier = cms.string('PF no MET')
    )
    )

process.pfShyftAnaMCNoMET = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0), 
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
    reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    identifier = cms.string('PF MC no MET'),
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
#_____________QCD WP95_______________________
process.pfShyftAnaQCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(    
    useWP95Selection = cms.bool(True),# if CiC ID loose, then pf reliso<0.2 is applied
    useWP70Selection = cms.bool(False),
    #eRelIso = cms.double(0.15),     
    #useVBTFDetIso  = cms.bool(True),
    identifier = cms.string('PF MET, WP95')
    )
    )

process.pfShyftAnaMCQCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
	reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    #eRelIso = cms.double(0.15),
    #useVBTFDetIso  = cms.bool(True),
    identifier = cms.string('PF MC WP95'),
    )
    )

#___________QCD WP95, no MET cut________________
process.pfShyftAnaQCDWP95NoMET = process.pfShyftAna.clone(
    shyftAnalysis=process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    #eRelIso = cms.double(0.15),
    #useVBTFDetIso  = cms.bool(True),
    identifier = cms.string('PF no MET, WP95')
    )
    )

process.pfShyftAnaMCQCDWP95NoMET = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
	reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    #eRelIso = cms.double(0.15),
    #useVBTFDetIso  = cms.bool(True),
    identifier = cms.string('PF MC WP95, NoMET'),
    )
    )

#___________QCD WP95, MET < 20 GeV ________________
process.pfShyftAnaMETMax20QCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(    
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    metMin = cms.double(0.0),
    metMax = cms.double(20.0),
    #eRelIso = cms.double(0.15),
    #useVBTFDetIso  = cms.bool(True),
    identifier = cms.string('PF MET <20, WP95'),
    )
    )

process.pfShyftAnaMCMETMax20QCDWP95 = process.pfShyftAna.clone(
    shyftAnalysis = process.pfShyftAna.shyftAnalysis.clone(
    metMin = cms.double(0.0),
    metMax = cms.double(20.0),
    useWP95Selection = cms.bool(True),
    useWP70Selection = cms.bool(False),
    weightSFCalc = cms.bool(False),
    simpleSFCalc = cms.bool(False),
    reweightBTagEff = cms.bool(False),
    useCustomPayload = cms.bool(False),
    #eRelIso = cms.double(0.15),
    #useVBTFDetIso  = cms.bool(True),
    identifier = cms.string('PF MC MET < 20, WP95'),
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
   process.pfShyftAnaNoMET*
   #process.pfShyftAnaMETMax20*
   
   #process.pfShyftAnaJES095*    
   #process.pfShyftAnaJES105*
   #process.pfShyftAnaMETRES090*
   #process.pfShyftAnaMETRES110*
   #process.pfShyftAnaJER000*
   #process.pfShyftAnaJER020*
   #process.pfShyftAnaPUup*
   #process.pfShyftAnaPUdown*
   #process.pfShyftAnaNoPUReweight*
   #process.pfShyftAnaEleEEPt125*
   #process.pfShyftAnaEleEEPt075*
   #process.pfShyftAnaReweightedBTag080*
   #process.pfShyftAnaReweightedBTag090*
   #process.pfShyftAnaReweightedBTag110*
   #process.pfShyftAnaReweightedBTag120*
   #process.pfShyftAnaReweightedLFTag080*
   #process.pfShyftAnaReweightedLFTag090*
   #process.pfShyftAnaReweightedLFTag110*
   #process.pfShyftAnaReweightedLFTag120*
    
   #process.pfShyftAnaQCDWP95*
   #process.pfShyftAnaQCDWP95NoMET*
   #process.pfShyftAnaMETMax20QCDWP95*

   process.pfShyftAnaMC*
   process.pfShyftAnaMCNoMET*
   #process.pfShyftAnaMCMETMax20*
   #process.pfShyftAnaMCQCDWP95*
   #process.pfShyftAnaMCQCDWP95NoMET*
   #process.pfShyftAnaMCMETMax20QCDWP95*
   #process.pfShyftAnaMETMax20QCDWP95
     
   )

process.p = cms.Path(
    process.pfShyftAna
    #process.pfShyftAnaMC
    )

if options.allSys == 1 :
    process.p *= process.s
process.MessageLogger.cerr.FwkReport.reportEvery = 10000
