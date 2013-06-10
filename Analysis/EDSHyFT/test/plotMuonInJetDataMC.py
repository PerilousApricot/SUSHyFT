#!/bin/python


# ===================================================
#             doSys.py
#
#  Check acceptance (pretag, >=1-tag)
#  for a given systematic
# ===================================================
# ===================================================



from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputFileData', metavar='F', type='string', action='store',
                  default='plotSingleMuonInJetData.root',
                  dest='inputFileData',
                  help='input file tag to be used for data')

parser.add_option('--inputFileMC', metavar='F', type='string', action='store',
                  default='plotSingleMuonInJetMC.root',
                  dest='inputFileMC',
                  help='input file tag to be used for mc')

(options, args) = parser.parse_args()

argv = []



from ROOT import *
from array import *

gROOT.Macro("rootlogon.C")

f1 = TFile(options.inputFileData)
f2 = TFile(options.inputFileMC)

h1 = f1.Get('secvtxMass')
h2 = f2.Get('secvtxMass')

h1.Sumw2()
h2.Sumw2()

h1.Rebin(5)
h2.Rebin(5)

h1.Scale(1.0 / h1.Integral() )
h2.Scale(1.0 / h2.Integral() )

h1.SetMarkerStyle(20)
h2.SetFillColor(5)

gStyle.SetOptStat(000000)

h1.SetTitle('Secondary Vertex Mass;Secondary Vertex Mass (GeV/c^{2});Number (arbs)')
leg = TLegend(0.6, 0.6, 0.84, 0.84)
leg.AddEntry( h1, 'Data', 'p')
leg.AddEntry( h2, 'PYTHIA MC', 'f')
leg.SetFillColor(0)
leg.SetBorderSize(0)

c = TCanvas('c', 'c')
h1.Draw('e')
h2.Draw('hist same')
h1.Draw('e same')
leg.Draw()
h1.SetMinimum(0)
c.Print('compare_pure_secvtxmass.png', 'png')
c.Print('compare_pure_secvtxmass.pdf', 'pdf')
