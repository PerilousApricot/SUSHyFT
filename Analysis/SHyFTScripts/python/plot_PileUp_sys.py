#!/bin/python



from ROOT import *
from array import *

from optparse import OptionParser
        
        
parser = OptionParser()

parser.add_option('--region', metavar = 'R',  type='string', action='store',
                  default='eleEB',
                  dest='region',
                  help='barrel or endcap')
        
(options, args) = parser.parse_args()
        
argv = []

gROOT.Macro("~/rootlogon.C")

gStyle.SetOptStat(000000)
f_nominal = TFile('TTJets_TuneD6T_7TeV-madgraph-tauola_shyftana_387_v1.root')
f_up= TFile('TTJets_TuneD6T_7TeV-madgraph-tauola_pileup_shyftana_387_v1.root')

hist_tag   = 'pfRecoShyftAnaMC' + '/' + options.region + '/Top_secvtxMass_'

hists_tag_nominal = []
hists_tag_up = []


c1 = TCanvas('c1', 'c1')

# > 1jets, >1 tags
for ijet in range(1,6) :
    print 'working tags : ijet = ' + str(ijet)
    for itag in range(1, min(ijet,2) + 1) :
        print 'working tags : itag = ' + str(itag)
        print 'Getting ' + hist_tag + str(ijet) + 'j_' + str(itag) + 't'
        hist_tag_nominal = f_nominal.Get( hist_tag + str(ijet) + 'j_' + str(itag) + 't' ).Clone()
        hists_tag_nominal.append( hist_tag_nominal )
        
        hist_tag_up = f_up.Get( hist_tag + str(ijet) + 'j_' + str(itag) + 't' ).Clone()
        hists_tag_up.append( hist_tag_up )
        
      

hist_tag_nominal_sum = hists_tag_nominal[0]
for hist in range(1,len(hists_tag_nominal)):
    hist_tag_nominal_sum.Add( hists_tag_nominal[hist] )

hist_tag_nominal_sum.Sumw2()
hist_tag_nominal_sum.Scale( 1.0 / hist_tag_nominal_sum.GetEntries() )
hist_tag_nominal_sum.SetLineColor(1)
hist_tag_nominal_sum.SetTitle('Electron ' + options.region + ' SVM, Systematics for pileup ;Mass (GeV);Number (arbs)')
hist_tag_nominal_sum.Draw('hist')


hist_tag_up_sum = hists_tag_up[0]
for hist in range(1,len(hists_tag_up)):
    hist_tag_up_sum.Add( hists_tag_up[hist] )

hist_tag_up_sum.Sumw2()
hist_tag_up_sum.Scale( 1.0 / hist_tag_up_sum.GetEntries() )
hist_tag_up_sum.SetLineColor(2)
hist_tag_up_sum.Draw('same hist')


leg = TLegend(0.6, 0.6, 0.84, 0.84)
leg.SetBorderSize(0)
leg.SetFillColor(0)

leg.AddEntry(hist_tag_up_sum, 'Pile Up', 'l')
leg.AddEntry(hist_tag_nominal_sum, 'Nominal', 'l')
leg.Draw()

c1.Print('pileup_sys_mass_ele_EB.png', 'png')
c1.Print('pileup_sys_mass_ele_EB.pdf', 'pdf')
