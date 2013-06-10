#! /usr/bin/env python
import os
import glob

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--files', metavar='F', type='string', action='store',
                  dest='files',
                  help='Input files')



parser.add_option('--outname', metavar='F', type='string', action='store',
                  default='TTSemilepAnalyzer_antibtag_w_mucut',
                  dest='outname',
                  help='output name')

parser.add_option('--minTags', metavar='N', type='int', action='store',
                  default=1,
                  dest='minTags',
                  help='minimum number of tags to consider')


parser.add_option('--muOnly', metavar='F', action='store_true',
                  default=False,
                  dest='muOnly',
                  help='use only muons')

parser.add_option('--sideband', metavar='F', action='store_true',
                  default=False,
                  dest='sideband',
                  help='use loose leptons (exclusive from tight)')


parser.add_option('--printEvents', metavar='F', action='store_true',
                  default=False,
                  dest='printEvents',
                  help='print events')

(options, args) = parser.parse_args()

argv = []


import ROOT
ROOT.gROOT.Macro("rootlogon.C")


import sys
from DataFormats.FWLite import Events, Handle

print 'Getting these files : ' + options.files

files = glob.glob( options.files )
print files

f = ROOT.TFile(options.outname + ".root", "recreate")
f.cd()

goodEvents = []

print "Creating histograms"

nJets = ROOT.TH1F("nJets",         "Number of Jets, p_{T} > 30 GeV;N_{Jets};Number",               20, -0.5, 19.5 )
nMuons = ROOT.TH1F("nMuons",         "Number of Muons, p_{T} > 45 GeV;N_{Muons};Number",               5, -0.5, 4.5 )
nElectrons = ROOT.TH1F("nElectrons",         "Number of Electrons, p_{T} > 60 GeV;N_{Jets};Number",               5, -0.5, 4.5 )

ptMu = ROOT.TH1F("ptMu", "p_{T} of Muon", 200, 0., 200.)
ptLep0 = ROOT.TH1F("ptLep0", "p_{T} of Lepon", 200, 0., 200.)
ptLep1 = ROOT.TH1F("ptLep1", "p_{T} of Lepon", 200, 0., 200.)
ptLep2 = ROOT.TH1F("ptLep2", "p_{T} of Lepon", 200, 0., 200.)
ptLep3 = ROOT.TH1F("ptLep3", "p_{T} of Lepon", 200, 0., 200.)
ptLep4 = ROOT.TH1F("ptLep4", "p_{T} of Lepon", 200, 0., 200.)
ptLep5 = ROOT.TH1F("ptLep5", "p_{T} of Lepon", 200, 0., 200.)
ptLep6 = ROOT.TH1F("ptLep6", "p_{T} of Lepon", 200, 0., 200.)

ptMET0 = ROOT.TH1F("ptMET0", "MET", 200, 0., 200.)
ptMET1 = ROOT.TH1F("ptMET1", "MET", 200, 0., 200.)
ptMET2 = ROOT.TH1F("ptMET2", "MET", 200, 0., 200.)
ptMET3 = ROOT.TH1F("ptMET3", "MET", 200, 0., 200.)
ptMET4 = ROOT.TH1F("ptMET4", "MET", 200, 0., 200.)
ptMET5 = ROOT.TH1F("ptMET5", "MET", 200, 0., 200.)
htLep0 = ROOT.TH1F("htLep0", "H_{T}^{Lep}", 300, 0., 600.)
htLep1 = ROOT.TH1F("htLep1", "H_{T}^{Lep}", 300, 0., 600.)
htLep2 = ROOT.TH1F("htLep2", "H_{T}^{Lep}", 300, 0., 600.)
htLep3 = ROOT.TH1F("htLep3", "H_{T}^{Lep}", 300, 0., 600.)
htLep4 = ROOT.TH1F("htLep4", "H_{T}^{Lep}", 300, 0., 600.)
htLep5 = ROOT.TH1F("htLep5", "H_{T}^{Lep}", 300, 0., 600.)
ptJet0 = ROOT.TH1F("ptJet0", "p_{T} Of Leading Jet", 300, 0., 600.)
ptJet1 = ROOT.TH1F("ptJet1", "p_{T} Of Leading Jet", 300, 0., 600.)
ptJet2 = ROOT.TH1F("ptJet2", "p_{T} Of Leading Jet", 300, 0., 600.)
ptJet3 = ROOT.TH1F("ptJet3", "p_{T} Of Leading Jet", 300, 0., 600.)
ptJet4 = ROOT.TH1F("ptJet4", "p_{T} Of Leading Jet", 300, 0., 600.)
ptJet5 = ROOT.TH1F("ptJet5", "p_{T} Of Leading Jet", 300, 0., 600.)
ptJet6 = ROOT.TH1F("ptJet6", "p_{T} Of Leading Jet", 300, 0., 600.)



muHistType2 = ROOT.TH1F("muHistType2", "#mu", 300, 0, 1.0)
mWCandType2 = ROOT.TH1F("mWCandType2",         "Mass of W Candidate from Hadronic Jets;Mass;Number",  200, 0., 200. )
mTopCandType2 = ROOT.TH1F("mTopCandType2",         "Mass of Top Candidate from Hadronic Jets;Mass;Number",  300, 0., 600. )
mWCandVsMuCutType2 = ROOT.TH2F("mWCandVsMuCutType2", "Mass of W candidate versus #mu cut", 20, 0, 200, 10, 0, 1.0)
mWCandVsMTopCandType2 = ROOT.TH2F("mWCandVsMTopCandType2","WCand+bJet Mass vs WCand mass",200,0.,200.,600,0.,600.)

topMassHist = ROOT.TH1F("topMass", "Top Mass Histogram", 250, 0., 500.)
minMassHist0 = ROOT.TH1F("minMass0", "Min Mass Histogram", 100, 0., 200.)
minMassHist1 = ROOT.TH1F("minMass1", "Min Mass Histogram After Top Mass Cut", 100, 0., 200.)

ptRelVsDRMin = ROOT.TH2F("ptRelVsDRMin", "Mass of W candidate versus #mu cut", 40, 0, 200, 15, 0, 1.5)

events = Events (files)

postfix = "Loose"


jetPtHandle         = Handle( "std::vector<float>" )
jetPtLabel    = ( "pfShyftTupleJets" + postfix + "TopTag",   "pt" )
jetEtaHandle         = Handle( "std::vector<float>" )
jetEtaLabel    = ( "pfShyftTupleJets" + postfix + "TopTag",   "eta" )
jetPhiHandle         = Handle( "std::vector<float>" )
jetPhiLabel    = ( "pfShyftTupleJets" + postfix + "TopTag",   "phi" )
jetMassHandle         = Handle( "std::vector<float>" )
jetMassLabel    = ( "pfShyftTupleJets" + postfix + "TopTag",   "mass" )
jetTopMassHandle         = Handle( "std::vector<float>" )
jetTopMassLabel    = ( "pfShyftTupleJets" + postfix + "TopTag",   "topMass" )
jetMinMassHandle         = Handle( "std::vector<float>" )
jetMinMassLabel    = ( "pfShyftTupleJets" + postfix + "TopTag",   "minMass" )


prunedJetPtHandle         = Handle( "std::vector<float>" )
prunedJetPtLabel    = ( "pfShyftTupleJets" + postfix,   "pt" )
prunedJetEtaHandle         = Handle( "std::vector<float>" )
prunedJetEtaLabel    = ( "pfShyftTupleJets" + postfix,   "eta" )
prunedJetPhiHandle         = Handle( "std::vector<float>" )
prunedJetPhiLabel    = ( "pfShyftTupleJets" + postfix,   "phi" )
prunedJetMassHandle         = Handle( "std::vector<float>" )
prunedJetMassLabel    = ( "pfShyftTupleJets" + postfix,   "mass" )
prunedJetDa0MassHandle         = Handle( "std::vector<float>" )
prunedJetDa0MassLabel    = ( "pfShyftTupleJets" + postfix,   "da0Mass" )
prunedJetDa1MassHandle         = Handle( "std::vector<float>" )
prunedJetDa1MassLabel    = ( "pfShyftTupleJets" + postfix,   "da1Mass" )
prunedJetSSVHEHandle         = Handle( "std::vector<float>" )
prunedJetSSVHELabel    = ( "pfShyftTupleJets" + postfix,   "ssvhe" )

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

cutFlow = [0,0,0,0,0,0,0,0,0,0]

# loop over events
count = 0
print "Start looping"
for event in events:
    count = count + 1
    if count % 10000 == 0 :
      print  '--------- Processing Event ' + str(count)
    cutFlow[0] += 1

    #Require exactly one lepton (e or mu)

    lepType = 0 # Let 0 = muon, 1 = electron    
    event.getByLabel (muonPtLabel, muonPtHandle)
    if not muonPtHandle.isValid():
        continue
    muonPts = muonPtHandle.product()


    nMuonsVal = 0
    for imuonPt in range(0,len(muonPts)):
        muonPt = muonPts[imuonPt]
        if muonPt > 45.0 :
            nMuonsVal += 1
            lepType = 0
                
    nMuons.Fill( nMuonsVal )

    if nMuonsVal < 1 :
        continue

    # Plot the number of muons with pt > 25.
    # Require at least one.
    ptMu.Fill( muonPts[0] )


    # Plot the number of jets with pt > 25.
    # Require at least two
    event.getByLabel (jetPtLabel, jetPtHandle)
    jetPts = jetPtHandle.product()

    nJetsVal = 0
    for ijet in range(0,len(jetPts)) :
        if jetPts[ijet] > 25.0 :
            nJetsVal += 1  
    # Require >= 2 jets above 30 GeV
    if nJetsVal < 2 :
        continue


    # Now look at the rest of the lepton information.
    # We will classify jets based on hemispheres, defined
    # by the lepton.

    lepMass = 0.0
    event.getByLabel (muonEtaLabel, muonEtaHandle)
    muonEtas = muonEtaHandle.product()
    event.getByLabel (muonPhiLabel, muonPhiHandle)
    muonPhis = muonPhiHandle.product()



    event.getByLabel (jetEtaLabel, jetEtaHandle)
    jetEtas = jetEtaHandle.product()
    event.getByLabel (jetPhiLabel, jetPhiHandle)
    jetPhis = jetPhiHandle.product()
    event.getByLabel (jetMassLabel, jetMassHandle)
    jetMasss = jetMassHandle.product()
    event.getByLabel (jetTopMassLabel, jetTopMassHandle)
    jetTopMasss = jetTopMassHandle.product()
    event.getByLabel (jetMinMassLabel, jetMinMassHandle)
    jetMinMasss = jetMinMassHandle.product()    

    # Break the jets up by hemisphere.
    # Also compute the 2d cut parameters
    # (dR between the lepton and the nearest jet,
    # and the ptRel between the lepton and the nearest jet)
    hadJets = []
    hadJetsMu = []
    hadJetsBDisc = []
    hadJetsTopMass = []
    hadJetsMinMass = []
    lepJets = []
    lepPt = muonPts[0]
    lepEta = muonEtas[0]
    lepPhi = muonPhis[0]
    lepMass = 0.105
    lepP4 = ROOT.TLorentzVector()
    lepP4.SetPtEtaPhiM( lepPt, lepEta, lepPhi, lepMass )
    dRMin = 999.0
    ptRel = -1.0
    nJetsVal = 0
    for ijet in range(0,len(jetPts)) :
        if jetPts[ijet] > 25.0 :
            jet = ROOT.TLorentzVector()
            jet.SetPtEtaPhiM( jetPts[ijet], jetEtas[ijet], jetPhis[ijet], jetMasss[ijet] )
            dR = jet.DeltaR( lepP4 )
            if dR > ROOT.TMath.Pi() / 2.0 :
                hadJets.append( jet )
                hadJetsTopMass.append( jetTopMasss[ijet] )
                hadJetsMinMass.append( jetMinMasss[ijet] )
            else :
                if dR < dRMin :
                    #print 'dR = ' + str(dR)
                    #print 'jet = {0:6.2f}, {1:6.2f}, {2:6.2f}, {3:6.2f}'.format( jetPts[ijet], jetEtas[ijet], jetPhis[ijet], jetMasss[ijet] )
                    #print 'lep = {0:6.2f}, {1:6.2f}, {2:6.2f}, {3:6.2f}'.format( lepPt, lepEta, lepPhi, lepMass )
                    dRMin = dR
                    ptRel = jet.Perp( lepP4.Vect() )
                lepJets.append( jet )

    # Fill the njets plot
    nJets.Fill( nJetsVal )             
    # Fill the 2D cut plot
    ptRelVsDRMin.Fill( ptRel, dRMin )

    # Compute htLep and fill plots
    event.getByLabel (metLabel, metHandle)
    mets = metHandle.product()
    met = mets[0]

    htLepVal = met + lepP4.Perp()

    cutFlow[1] += 1
    htLep0.Fill( htLepVal )
    ptMET0.Fill( met )
    ptLep0.Fill( muonPts[0] )
    ptJet0.Fill( jetPts[0] )

    # Compute the 2d cut
    pass2D = dRMin > 0.5 or ptRel > 25.0


    # If using signal selection ( not loose ), then
    # require the 2d cut to continue.
    # Otherwise, you're using the loose selection,
    # so require failure of the 2d cut for a sideband
    if not options.sideband :
        if not pass2D :
            continue
    else :
        if pass2D :
            continue


    # Plot HTLep and MET for this stage of the selection.
    # Also plot the leading jet PT before we cut on it.
    cutFlow[2] += 1        
    htLep1.Fill( htLepVal )
    ptMET1.Fill( met )
    ptLep1.Fill( muonPts[0] )
    ptJet1.Fill( jetPts[0] )

    # Require leading jet pt to be pt > 200 GeV
    if len(hadJets) < 1 or hadJets[0].Perp() < 250.0 :
        continue


    # Plot HTLep and MET for this stage of the selection.
    cutFlow[3] += 1
    htLep2.Fill( htLepVal )
    ptMET2.Fill( met )
    ptLep2.Fill( muonPts[0] )
    ptJet2.Fill( jetPts[0] )

    if htLepVal < 150.0 :
      continue

    # Plot HTLep and MET for this stage of the selection.
    cutFlow[4] += 1
    htLep3.Fill( htLepVal )
    ptMET3.Fill( met )
    ptLep3.Fill( muonPts[0] )
    ptJet3.Fill( jetPts[0] )

    highestMassJetIndex = -1
    highestJetMass = -1.0
    for ijet in range(0,len(hadJetsTopMass) ):
      if hadJetsTopMass[ijet] > highestJetMass :
        highestJetMass = hadJetsTopMass[ijet]
        highestMassJetIndex = ijet
      
    topMassHist.Fill( hadJetsTopMass[highestMassJetIndex] )
    minMassHist0.Fill( hadJetsMinMass[highestMassJetIndex] )
    topMassTagged = hadJetsTopMass[highestMassJetIndex] > 100.0 and hadJetsTopMass[highestMassJetIndex] < 250.
    topMinMassTagged = False
    if topMassTagged :
      minMassHist1.Fill( hadJetsMinMass[highestMassJetIndex] )
      topMinMassTagged = hadJetsMinMass[highestMassJetIndex] > 50.0

    topTagged = topMassTagged and topMinMassTagged

    if topTagged :
      cutFlow[5] += 1
      htLep4.Fill( htLepVal )
      ptMET4.Fill( met )
      ptLep4.Fill( muonPts[0] )
      ptJet4.Fill( jetPts[0] )
      goodEvents.append( [ event.object().id().run(), event.object().id().luminosityBlock(), event.object().id().event(), 1 ] )


    if not topTagged :


      event.getByLabel (prunedJetPtLabel, prunedJetPtHandle)
      prunedJetPts = prunedJetPtHandle.product()
      event.getByLabel (prunedJetEtaLabel, prunedJetEtaHandle)
      prunedJetEtas = prunedJetEtaHandle.product()
      event.getByLabel (prunedJetPhiLabel, prunedJetPhiHandle)
      prunedJetPhis = prunedJetPhiHandle.product()
      event.getByLabel (prunedJetMassLabel, prunedJetMassHandle)
      prunedJetMasss = prunedJetMassHandle.product()
      event.getByLabel (prunedJetSSVHELabel, prunedJetSSVHEHandle)
      prunedJetSSVHEs = prunedJetSSVHEHandle.product()
      event.getByLabel (prunedJetDa0MassLabel, prunedJetDa0MassHandle)
      prunedJetDa0Masses = prunedJetDa0MassHandle.product()
      event.getByLabel (prunedJetDa1MassLabel, prunedJetDa1MassHandle)
      prunedJetDa1Masses = prunedJetDa1MassHandle.product()
    

      ptRel = -1.0
      hadPrunedJets = []
      hadPrunedJetsMu = []
      hadPrunedJetsBDisc = []
      for iprunedJet in range(0,len(prunedJetPts)) :
          if prunedJetPts[iprunedJet] > 25.0 :
            prunedJet = ROOT.TLorentzVector()
            prunedJet.SetPtEtaPhiM( prunedJetPts[iprunedJet], prunedJetEtas[iprunedJet], prunedJetPhis[iprunedJet], prunedJetMasss[iprunedJet] )
            dR = prunedJet.DeltaR( lepP4 )
            if dR > ROOT.TMath.Pi() / 2.0 :
              hadPrunedJets.append( prunedJet )
              hadPrunedJetsBDisc.append( prunedJetSSVHEs[iprunedJet] )
              mu0 = prunedJetDa0Masses[iprunedJet] / prunedJetMasss[iprunedJet]
              mu1 = prunedJetDa1Masses[iprunedJet] / prunedJetMasss[iprunedJet]
              mu = mu0
              if mu1 > mu0 :
                mu = mu1
              hadPrunedJetsMu.append( mu )



        # Select the hadronic W and b candidates in the "type 2" hemisphere:
        #   W candidate: 
        #     - b-tag veto
        #     - highest mass prunedJet in hadronic hemisphere
        #   b candidate:
        #     - Leading pt tagged prunedJet in the hadronic hemisphere
      highestMassPrunedJetIndex = -1
      highestPrunedJetMass = -1.0
      bPrunedJetCandIndex = -1
      for iprunedJet in range(0,len(hadPrunedJets)):
        if hadPrunedJets[iprunedJet].M() > highestPrunedJetMass  and hadPrunedJetsBDisc[iprunedJet] < 2.74 :
          highestPrunedJetMass = hadPrunedJets[iprunedJet].M()
          highestMassPrunedJetIndex = iprunedJet
        if hadPrunedJetsBDisc[iprunedJet] > 2.74 and bPrunedJetCandIndex == -1 :
          bPrunedJetCandIndex = iprunedJet


        # Now select on mu cut, and select type 2 top candidate
      type2Top = False
      if highestPrunedJetMass >= 0 :
        muHistType2.Fill( hadPrunedJetsMu[highestMassPrunedJetIndex] )
        mWCandVsMuCutType2.Fill( highestPrunedJetMass, hadPrunedJetsMu[highestMassPrunedJetIndex] )
        if hadPrunedJetsMu[highestMassPrunedJetIndex] < 0.4 :
          mWCandType2.Fill( highestPrunedJetMass )
          if bPrunedJetCandIndex >= 0 :
            topCandP4 = hadPrunedJets[highestMassPrunedJetIndex] + hadPrunedJets[bPrunedJetCandIndex]
            mWCandVsMTopCandType2.Fill( highestPrunedJetMass, topCandP4.M() )
            if abs(highestPrunedJetMass - 80.4) < 20 :
              mTopCandType2.Fill( topCandP4.M() )
              if topCandP4.M() > 100. and topCandP4.M() < 250. :
                type2Top = True


      if type2Top :
        cutFlow[6] += 1
        htLep5.Fill( htLepVal )
        ptMET5.Fill( met )
        ptLep5.Fill( muonPts[0] )
        ptJet5.Fill( jetPts[0] )
        goodEvents.append( [ event.object().id().run(), event.object().id().luminosityBlock(), event.object().id().event(), 2] )


f.cd()
f.Write()
f.Close()


print '------Cut flow:-------'
for icut in cutFlow :
  print '{0:12.0f}'.format(icut),

if options.printEvents :
    for goodEvent in goodEvents :
        print '{0:12.0f}:{1:12.0f}:{2:12.0f},    {3:4.0f}'.format(
            goodEvent[0], goodEvent[1], goodEvent[2], goodEvent[3]
        )

