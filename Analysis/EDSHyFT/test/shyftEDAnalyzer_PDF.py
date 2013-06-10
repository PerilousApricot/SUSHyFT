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
                 'top',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Sample name to give histograms")

options.parseArguments()

print options

import sys

if options.useFlavorHistory > 0 :
    useFlavorHistory = True
else :
    useFlavorHistory = False


inputSampleName = options.sampleNameInput

## Source
if len(options.inputFiles) == 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbar/shyft_38xOn35x_v4/10de90d53f51d470a59d10c8f54ad479/shyft_382_mc_1_1_VM0.root'
#                                    'dcap:///pnfs/cms/WAX/11/store/user/rappocc/TTbarJets-madgraph/shyft_38xOn35x_v2/b8014e49c41bd22a9b4664626194b599/shyft_382_mc_1_1_fU1.root'
                                    )
                                )
else :
    filelist = open( options.inputFiles[0], 'r' )
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                    filelist.readlines()
                                    )
                                )

## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

from Analysis.SHyFT.shyftAnalysis_cfi import shyftAnalysis as inputShyftAnalysis


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("shyftStudies_PDF.root")
                                   )


process.caloShyftAna = cms.EDAnalyzer('EDSHyFT',
                                      shyftAnalysis = inputShyftAnalysis.clone(
                                          jetPtMin = cms.double(30.0),
                                          minJets = cms.int32(1),
                                          heavyFlavour = cms.bool( useFlavorHistory ),
                                          doMC = cms.bool( True),
                                          sampleName = cms.string(inputSampleName),
                                          reweightPDF = cms.bool(False),
                                          btaggerString = cms.string('simpleSecondaryVertexBJetTags'),
                                          identifier = cms.string('CALO')
                                          )                                      
                                      )




process.p = cms.Path(
    process.caloShyftAna
    )

for ipdf in range(0, 3) :

    setattr( process, 'caloShyftAnaPDF' + str(ipdf),  process.caloShyftAna.clone(
        shyftAnalysis = process.caloShyftAna.shyftAnalysis.clone(
            reweightPDF = cms.bool(True),
            pdfToUse = cms.string('cteq66.LHgrid'),
            pdfEigenToUse = cms.int32( ipdf ),
            identifier=cms.string('CALO_PDF_' + str(ipdf))
            )
        )
             )
    process.p *= cms.Sequence( getattr( process, 'caloShyftAnaPDF' + str(ipdf) ) )



process.MessageLogger.cerr.FwkReport.reportEvery = 10000
