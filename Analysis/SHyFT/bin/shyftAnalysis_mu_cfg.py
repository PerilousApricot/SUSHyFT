import FWCore.ParameterSet.Config as cms

process = cms.Process("FWLitePlots")
import string
import sys

filesin = sys.argv[2]
outfile = sys.argv[3]
#outfile = 'wjets_ttbsm.root'
#filesin = 'wjets_ttbsm.txt'

#prepend = 'dcap:///pnfs/cms/WAX/11'
prepend = ''

print 'Input files from ' + filesin
print 'Output file = ' + outfile

infilenames = cms.vstring()
txtfile = open(filesin)
for line in txtfile.readlines():
   infilenames.append( prepend + string.replace(line,'\n',''))

print infilenames

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis

process.shyftAnalysis = inputShyftAnalysis.clone(
    muonSrc = cms.InputTag('selectedPatMuonsPFlow'),
    electronSrc = cms.InputTag('selectedPatElectronsPFlow'),
    metSrc = cms.InputTag('patMETsPFlow'),
    jetSrc = cms.InputTag('goodPatJetsPFlow'),
    pvSrc   = cms.InputTag('goodOfflinePrimaryVertices'),
    jetPtMin = cms.double(30.0),
    minJets = cms.int32(5),
    ePlusJets = cms.bool(False),
    muPlusJets = cms.bool(True),
    metMin = cms.double(0.),
    cutsToIgnore=cms.vstring('Trigger'),
    #useTTBSMPat = cms.bool(False),
    jetScale = cms.double(1.0),
    
    #metMax = cms.double(25.),
    #***********Uncomment if want to test on WJets, ZJets, Vqq, WcJets******************
    #sampleName="Wjets",
    #sampleName = "Top",
    #doMC = True,
    #heavyFlavour = True,   
    )

process.inputs = cms.PSet (
    fileNames = infilenames,
    maxEvents = cms.int32(5000)
)


process.outputs = cms.PSet (
    outputName = cms.string(outfile)
)
