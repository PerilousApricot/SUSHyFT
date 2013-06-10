#! /usr/bin/env python
import os
import glob
from math import sqrt

from optparse import OptionParser


parser = OptionParser()

# Input files to use. This is in "glob" format, so you can use wildcards.
# If you get a "cannot find file" type of error, be sure to use "\*" instead
# of "*" to make sure you don't confuse the shell. 
parser.add_option('--files', metavar='F', type='string', action='store',
                  dest='files',
                  help='Input files')


# Output file name
parser.add_option('--outfile', metavar='F', type='string', action='store',
                  dest='outfile',
                  default='TTJets_pdfunc.root',
                  help='Ouptut file name')


# This will use the loose selections, and negate the isolation
# criteria
parser.add_option('--useLoose', metavar='F', action='store_true',
                  default=False,
                  dest='useLoose',
                  help='use loose leptons (exclusive from tight)')



(options, args) = parser.parse_args()

argv = []

# Import everything from ROOT
import ROOT
ROOT.gROOT.Macro("rootlogon.C")

# Import stuff from FWLite
import sys
from DataFormats.FWLite import Events, Handle

print 'Getting files from this dir: ' + options.files

# Get the file list. 
files = glob.glob( options.files )
print files


events = Events (files)

# Make the entirety of the handles required for the
# analysis. 
postfix = ""
if options.useLoose :
    postfix = "Loose"

jetPtHandle         = Handle( "std::vector<float>" )
jetPtLabel    = ( "pfShyftTupleJets" + postfix,   "pt" )
jetEtaHandle         = Handle( "std::vector<float>" )
jetEtaLabel    = ( "pfShyftTupleJets" + postfix,   "eta" )
jetPhiHandle         = Handle( "std::vector<float>" )
jetPhiLabel    = ( "pfShyftTupleJets" + postfix,   "phi" )
jetMassHandle         = Handle( "std::vector<float>" )
jetMassLabel    = ( "pfShyftTupleJets" + postfix,   "mass" )
jetSecvtxMassHandle         = Handle( "std::vector<float>" )
jetSecvtxMassLabel    = ( "pfShyftTupleJets" + postfix,   "secvtxMass" )
jetSSVHEHandle         = Handle( "std::vector<float>" )
jetSSVHELabel    = ( "pfShyftTupleJets" + postfix,   "ssvhe" )
jetFlavorHandle         = Handle( "std::vector<float>" )
jetFlavorLabel    = ( "pfShyftTupleJets" + postfix,   "flavor" )

muonPtHandle         = Handle( "std::vector<float>" )
muonPtLabel    = ( "pfShyftTupleMuons" + postfix,   "pt" )
muonEtaHandle         = Handle( "std::vector<float>" )
muonEtaLabel    = ( "pfShyftTupleMuons" + postfix,   "eta" )
muonPhiHandle         = Handle( "std::vector<float>" )
muonPhiLabel    = ( "pfShyftTupleMuons" + postfix,   "phi" )
muonPfisoHandle         = Handle( "std::vector<float>" )
muonPfisoLabel    = ( "pfShyftTupleMuons" + postfix,   "pfiso" )

electronPtHandle         = Handle( "std::vector<float>" )
electronPtLabel    = ( "pfShyftTupleElectrons" + postfix,   "pt" )
electronEtaHandle         = Handle( "std::vector<float>" )
electronEtaLabel    = ( "pfShyftTupleElectrons" + postfix,   "eta" )
electronPhiHandle         = Handle( "std::vector<float>" )
electronPhiLabel    = ( "pfShyftTupleElectrons" + postfix,   "phi" )
electronPfisoHandle         = Handle( "std::vector<float>" )
electronPfisoLabel    = ( "pfShyftTupleElectrons" + postfix,   "pfiso" )

metHandle = Handle( "std::vector<float>" )
metLabel = ("pfShyftTupleMET" + postfix,   "pt" )

pdfHandle = Handle("std::vector<double>")
pdfLabel = ( 'pdfWeightProducer', "pdfWeights")


outfile = ROOT.TFile(options.outfile, 'RECREATE')
outfile.cd()
nJetsHists = []
nEigenvectors = 44
for ieig in range(0,nEigenvectors) :
    nJetsHists.append( ROOT.TH1F('nJets' + str(ieig), 'N Jets, Eigenvector = ' + str(ieig), 5, 0, 5 ) )

# Sum of weights
weightUp = 0.0
weightDown = 0.0
nWeights = 0

# loop over events
count = 0
ntotal = events.size()
percentDone = 0.0
ipercentDone = 0
ipercentDoneLast = -1
print "Start looping"
for event in events:
    ipercentDone = int(percentDone)
    if ipercentDone != ipercentDoneLast :
        ipercentDoneLast = ipercentDone
        print 'Processing {0:10.0f}/{1:10.0f} : {2:5.0f}%'.format(
            count, ntotal, ipercentDone )
    count = count + 1
    percentDone = float(count) / float(ntotal) * 100.0
    

    #Require exactly one lepton (e or mu)

    lepType = 0 # Let 0 = muon, 1 = electron    
    event.getByLabel (muonPtLabel, muonPtHandle)
    if not muonPtHandle.isValid():
        continue
    muonPts = muonPtHandle.product()

    
    event.getByLabel (electronPtLabel, electronPtHandle)
    if not electronPtHandle.isValid():
        continue
    electronPts = electronPtHandle.product()

    nMuonsVal = 0
    for imuonPt in range(0,len(muonPts)):
        muonPt = muonPts[imuonPt]
        if muonPt > 45.0 :
            if options.useLoose :
                if muonPfisos[imuonPt] / muonPt < 0.2 :
                    continue
                else :
                    nMuonsVal += 1
                    lepType = 0
            else :
                nMuonsVal += 1
                lepType = 0                
                    
    event.getByLabel (electronPtLabel, electronPtHandle)
    electronPts = electronPtHandle.product()

    nElectronsVal = 0
    if nMuonsVal == 0 :
        for ielectronPt in range(0,len(electronPts)):
            electronPt = electronPts[ielectronPt]
            if electronPt > 45.0 :
                if options.useLoose :
                    if electronPfisos[ielectronPt] / electronPt < 0.2 :
                        continue
                    else :
                        nElectronsVal += 1
                        lepType = 1
                else :
                    nElectronsVal += 1
                    lepType = 1
                        

    # Require exactly one lepton
    if nMuonsVal + nElectronsVal != 1 :
        continue

    # Now get the number of jets
    event.getByLabel( jetPtLabel, jetPtHandle )
    jetPts = jetPtHandle.product()

    njets = 0
    for jetPt in jetPts :
        if jetPt > 30.0 :
            njets += 1


    if njets < 1 :
        continue

    iweightUp = 0.0
    iweightDown = 0.0
    nWeights = nWeights + 1

    
    event.getByLabel( pdfLabel, pdfHandle )

    pdfs = pdfHandle.product()
    ipdf = 0
    for pdf in pdfs[0::2] :
        iweightUp = iweightUp + pdf*pdf
        nJetsHists[ipdf].Fill( njets, pdf )
        ipdf += 2
    ipdf = 1
    for pdf in pdfs[1::2] :
        iweightDown = iweightDown + pdf*pdf
        nJetsHists[ipdf].Fill( njets, pdf )
        ipdf += 2


    iweightUp = iweightUp / (len(pdfs) * 0.5)
    iweightDown = iweightDown / (len(pdfs) * 0.5)
    
    weightUp = weightUp + sqrt(iweightUp)
    weightDown = weightDown + sqrt(iweightDown)


print 'PDF Weight up   = ' + str( weightUp)
print 'PDF Weight down = ' + str( weightDown) 
print 'nEvents = ' + str(nWeights)

print 'PDF Sys    up   = ' + str( weightUp / nWeights)
print 'PDF Sys    down = ' + str( weightDown / nWeights) 



outfile.cd()
outfile.Write()
outfile.Close()
