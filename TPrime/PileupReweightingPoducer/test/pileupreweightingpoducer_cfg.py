import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register('sampleNameInput',
                 'T_TuneZ2_t-channel_7TeV-powheg-tauola_ttbsm_424_v9.root',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Sample name to give histograms")

options.parseArguments()
print options.sampleNameInput

inputSampleName = 'file:/data1/vasquez/BPrimeEDM_Ntuples_MC_Nov23/' + options.sampleNameInput
outputSampleName = '/data1/vasquez/BPrimeEDM_Ntuples_MC_Nov23_reweightedTEST/' + options.sampleNameInput

print "output name: " , outputSampleName
process = cms.Process("OWNPARTICLES")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(500)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        inputSampleName
    )
)

process.myProducerLabel = cms.EDProducer("PileupReweightingPoducer",
                                         FirstTime = cms.untracked.bool(False),
                                         PileupMCFile = cms.untracked.string('PUMC_dist_flat10.root'),
                                         PileupDataFile = cms.untracked.string('PUData_finebin_dist.root')
)

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string(outputSampleName),
                               outputCommands = cms.untracked.vstring('drop *')
                               )

process.out.outputCommands += ['keep *_*_*_*'] 

process.p = cms.Path(process.myProducerLabel)

process.e = cms.EndPath(process.out)
