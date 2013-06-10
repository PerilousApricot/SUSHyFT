#! /usr/bin/env python
import os
import glob
import math
import copy
import ROOT
ROOT.gROOT.Macro("~/rootlogon.C")
import sys
from DataFormats.FWLite import Events, Handle

def deltaR( eta1, phi1, eta2, phi2):
    deta = eta1 - eta2
    dphi = phi1 - phi2
    if dphi >= math.pi: dphi -= 2*math.pi
    elif dphi < -math.pi: dphi += 2*math.pi
    return math.sqrt(deta*deta + dphi*dphi)
    

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--files', metavar='F', type='string', action='store',
                  default = 'genOutputFile.root',
                  dest='files',
                  help='Input files')

parser.add_option('--outfile', metavar='F', type='string', action='store',
                  default = "test",
                  dest='outfile',
                  help='output file')

# Parse and get arguments
(options, args) = parser.parse_args()

print 'Getting files from this dir: ' + options.files

#Get the file list
files = glob.glob( options.files )
print "Getting files:", files

# Get the FWLite "Events"
events = Events (files)

HadTHandle   = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
HadTLabel    = ( "GenInfo",   "HadT")
WPart1Handle = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
WPart1Label  = ( "GenInfo",   "WPart1")
WPart2Handle = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
WPart2Label  = ( "GenInfo",   "WPart2")
HadTtoWHandle   = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
HadTtoWLabel    = ( "GenInfo",   "HadTtoW")
HadTtobHandle   = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
HadTtobLabel    = ( "GenInfo",   "HadTtob")

LepTHandle   = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
LepTLabel    = ( "GenInfo",   "LepT")
LepHandle    = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
LepLabel     = ( "GenInfo",   "Lep")
NuHandle     = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
NuLabel      = ( "GenInfo",   "Nu")
LepTtoWHandle   = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
LepTtoWLabel    = ( "GenInfo",   "LepTtoW")
LepTtobHandle   = Handle (  "ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> >"  )
LepTtobLabel    = ( "GenInfo",   "LepTtob")

f = ROOT.TFile( options.outfile + ".root", "recreate" )
f.cd()

print "Creating histograms"

dRWPart     = ROOT.TH1F("dR_Wqq", "dR(q,q)", 50, 0, 5)
dRWPart_Wpt = ROOT.TH2F("dR_Wqq_Wpt", "dR(q,q) Vs W pt(GeV)", 100, 0, 1000, 50, 0, 5)
dRtW        = ROOT.TH1F("dR_tW", "dR(t,W)", 50, 0, 5)
dRtW_Bpt    = ROOT.TH2F("dR_tW_Bpt", "dR(t,W) Vs b' pt(GeV)", 100, 0, 1000, 50, 0, 5)
dRbW        = ROOT.TH1F("dR_bW", "dR(b,W)", 50, 0, 5)
dRbW_Tpt    = ROOT.TH2F("dR_bW_Tpt", "dR(b,W) Vs t pt(GeV)", 100, 0, 1000, 50, 0, 5)

# loop over events
count = 0
ntotal = events.size()
print "Start looping"
for event in events:
    
    count = count + 1
    if count % 1000 == 0 :
        percentDone = float(count) / float(ntotal) * 100.0
        print 'Processing {0:10.0f}/{1:10.0f} : {2:5.2f} %'.format(
            count, ntotal, percentDone )
        
    if not event.object().isValid():
        continue
    
    event.getByLabel(WPart1Label, WPart1Handle)
    event.getByLabel(WPart2Label, WPart2Handle)
    event.getByLabel(HadTLabel, HadTHandle)
    event.getByLabel(HadTtoWLabel, HadTtoWHandle)
    event.getByLabel(HadTtobLabel, HadTtobHandle)

    WPart1 = WPart1Handle.product()
    WPart2 = WPart2Handle.product()
    HadT   = HadTHandle.product()
    HadTtoW = HadTtoWHandle.product()
    HadTtob = HadTtobHandle.product()
  
    skipHad = WPart1.Pt()==0 and WPart2.Pt()==0
    
    WPartP4 = WPart1 + WPart2
    BprimeP4 = WPartP4 + HadT
    TopP4 = HadTtoW + HadTtob

    #DeltaR b/w partons from W
    dR_qq = deltaR(WPart1.Eta(), WPart1.Phi(), WPart2.Eta(), WPart2.Phi())
    
    #DeltaR b/w t,W
    dR_tW = deltaR(WPartP4.Eta(), WPartP4.Phi(), HadT.Eta(), HadT.Phi())
    
    #DelatR b/w b,W
    dR_bW = deltaR(HadTtob.Eta(), HadTtob.Phi(), HadTtoW.Eta(), HadTtoW.Phi())
    
    
    #print "Had_Bprime_pt",  BprimeP4.Pt()
    #print "dR_qq ", dR_qq

    #print "WPart_Pt " , WPartP4.Pt()
    #print "dR_tW " , dR_tW

    # The two Tops are bit different, don't know why?
    #print "Top_Pt " , TopP4.Pt()
    #print "Top_Pt ", HadT.Pt()
    #print "dR_bW " , dR_bW
     
    #print "--------- \n",

    if not skipHad:
        dRWPart.Fill( dR_qq )
        dRWPart_Wpt.Fill (WPartP4.Pt(), dR_qq )
        dRtW.Fill( dR_tW )
        dRtW_Bpt.Fill( BprimeP4.Pt(), dR_tW )
        dRbW.Fill( dR_bW )
        dRbW_Tpt.Fill( TopP4.Pt(), dR_bW) 

f.cd()
f.Write()
f.Close()
