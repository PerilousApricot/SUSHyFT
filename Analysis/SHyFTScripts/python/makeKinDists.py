#!/bin/python


# ===================================================
#             makeKinDists.py
#
# ===================================================
# ===================================================

from SummedKinHist import *

from ROOT import *

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputTextFile', metavar='F', type='string', action='store',
                  default='mu12_ele12_v2.txt',
                  dest='inputTextFile',
                  help='input text file tag to be used that contains the event counts per jet/tag bin')

parser.add_option('--verbose',action='store_true',
                  default=False,
                  dest='verbose',
                  help='verbose switch')

parser.add_option('--inputTag', metavar='T', type='string', action='store',
                  default='shyftana_387_v4_prettyplots',
                  dest='inputTag',
                  help='Input string that is used to ID the input root files')

parser.add_option('--var', metavar='T', type='string', action='store',
                  default='hT',
                  dest='var',
                  help='variable to plot')


parser.add_option('--rebin', metavar='T', type='int', action='store',
                  default=None,
                  dest='rebin',
                  help='rebin x axes to this')


parser.add_option('--minJets', metavar='D', type='int', action='store',
                  default=3,
                  dest='minJets',
                  help='Minimum number of jets for plots')

parser.add_option('--maxJets', metavar='D', type='int', action='store',
                  default=6,
                  dest='maxJets',
                  help='Minimum number of jets for plots')


parser.add_option('--minTags', metavar='D', type='int', action='store',
                  default=1,
                  dest='minTags',
                  help='Minimum number of tags for plots')

parser.add_option('--maxTags', metavar='D', type='int', action='store',
                  default=3,
                  dest='maxTags',
                  help='Minimum number of tags for plots')


(options, args) = parser.parse_args()

argv = []

gROOT.Macro("rootlogon.C")

from string import Template

inputNamesMC = [
    [ 'Zjets',      TColor.kAzure-2, Template('DYJetsToLL_TuneD6T_M-50_7TeV-madgraph-tauola_${tag}_${lep}.root')],
    [ 'Wjets',      TColor.kGreen-3, Template('WJetsToLNu_TuneD6T_7TeV-madgraph-tauola_${tag}_${lep}.root')],
#    [ 'SingleToptW', Template('TToBLNu_TuneZ2_tW-channel_7TeV-madgraph_${tag}_${lep}.root')],
    [ 'SingleTopT', TColor.kMagenta, Template('TToBLNu_TuneZ2_t-channel_7TeV-madgraph_${tag}_${lep}.root')],
    [ 'Top',        TColor.kRed+1,   Template('TTJets_TuneD6T_7TeV-madgraph-tauola_${tag}_${lep}.root')],
#    [ 'SingleTopS',  Template('TToBLNu_TuneZ2_s-channel_7TeV-madgraph_${tag}_${lep}.root')]
]


ffs = dict( {'Electrons':'Ele_Nov4ReReco_shyft_387_v1_shyftana_v5.root', 'Muons':'Mu_Nov4ReReco_shyft_387_v2_shyftana_v9.root', } ) 
inputNamesData = [ ['Data', ffs] ]

histNames = [ 'hT', 'MET', 'wMT']
histTitles = dict( {'hT':';H_{T} (GeV);Number in 36 pb^{-1}',
                    'MET':';#slash{E}_{T} (GeV);Number in 36 pb^{-1}',
                    'wMT':';M_{T}^{W} (GeV);Number in 36 pb^{-1}',              
              })

if options.var not in histNames :
    quit()

dirsMu = dict( {histNames[0]:['pfShyftAnaMC'],
                histNames[1]:['pfShyftAnaMC'],
                histNames[2]:['pfShyftAnaMC']
                }
               )
dirsE = dict( {histNames[0]:['pfShyftAnaMC/eleEE', 'pfShyftAnaMC/eleEB'],
               histNames[1]:['pfShyftAnaMC/eleEE', 'pfShyftAnaMC/eleEB'],
               histNames[2]:['pfShyftAnaMC/eleEE', 'pfShyftAnaMC/eleEB'],
               }
              )

dirs = dict ({'Electrons':dirsE, 'Muons':dirsMu})


qcdDirsMu = dict( {histNames[0]:[['pfShyftAnaLooseWithD0','pfShyftAna']],
                   histNames[1]:[['pfShyftAnaLooseWithD0','pfShyftAna']],
                   histNames[2]:[['pfShyftAnaLooseWithD0','pfShyftAna']],
                }
               )
qcdDirsE = dict( {histNames[0]:['pfShyftAnaDataQCDLoose/eleEE', 'pfShyftAnaDataQCDLoose/eleEB'],
                  histNames[1]:['pfShyftAnaDataQCDLoose/eleEE', 'pfShyftAnaDataQCDLoose/eleEB'],
                  histNames[2]:['pfShyftAnaDataQCDLoose/eleEE', 'pfShyftAnaDataQCDLoose/eleEB'],
                  }
              )

qcdDirs = dict ({'Electrons':qcdDirsE, 'Muons':qcdDirsMu})


dataDirsMu = dict( {histNames[0]:['pfShyftAna'],
                    histNames[1]:['pfShyftAna'],
                    histNames[2]:['pfShyftAna'],
                }
               )
dataDirsE = dict( {histNames[0]:['pfShyftAna/eleEB','pfShyftAna/eleEE'],
                   histNames[1]:['pfShyftAna/eleEB','pfShyftAna/eleEE'],
                   histNames[2]:['pfShyftAna/eleEB','pfShyftAna/eleEE'],
                }
               )

dataDirs = dict ({'Electrons':dataDirsE, 'Muons':dataDirsMu})


hists = []

bkgsMuon = []
dataMuon = []

bkgsElectron = []
dataElectron = []

gStyle.SetOptStat(000000)


for iname in inputNamesData :
    prepend = iname[0]
    color = TColor.kYellow
    fnameMuon = iname[1]['Muons']
    histMuon = SummedKinQCDHist(prepend, "HT",
                                options.minJets, options.maxJets,
                                options.minTags, options.maxTags,
                                options.inputTextFile, fnameMuon, qcdDirs['Muons'][options.var], prepend, options.var, 'Muons', 'QCD')
    histMuon.form()
    hMuon = histMuon.getHist()
    if options.rebin is not None:
        hMuon.Rebin(options.rebin)
    hMuon.SetFillColor(color)
    bkgsMuon.append( hMuon )

    hists.append( histMuon )


for iname in inputNamesData:
    prepend = iname[0]
    color = TColor.kYellow
    fnameElectron = iname[1]['Electrons']
    histElectron = SummedKinMCHist(prepend, "HT",
                                   options.minJets, options.maxJets,
                                   options.minTags, options.maxTags,
                                   options.inputTextFile, fnameElectron, qcdDirs['Electrons'][options.var], prepend, options.var, 'Electrons', 'QCD')
    histElectron.form()
    hElectron = histElectron.getHist()
    if options.rebin is not None:
        hElectron.Rebin(options.rebin)    
    hElectron.SetFillColor(color)
    bkgsElectron.append( hElectron )

    hists.append( histElectron )







for iname in inputNamesData :
    prepend = iname[0]
    fnameMuon = iname[1]['Muons']
    histMuon = SummedKinDataHist(prepend, "HT",
                                 options.minJets, options.maxJets,
                                 options.minTags, options.maxTags,
                                 options.inputTextFile, fnameMuon, dataDirs['Muons'][options.var], prepend, options.var, 'Muons', None)
    histMuon.form()
    hMuon = histMuon.getHist()
    if options.rebin is not None:
        hMuon.Rebin(options.rebin)    
    hMuon.SetMarkerStyle(21)
    dataMuon.append( hMuon )

    hists.append( histMuon )
    
    prepend = iname[0]
    fnameElectron = iname[1]['Electrons']
    histElectron = SummedKinDataHist(prepend, "HT",
                                     options.minJets, options.maxJets,
                                     options.minTags, options.maxTags,
                                     options.inputTextFile, fnameElectron, dataDirs['Electrons'][options.var], prepend, options.var, 'Electrons', None)
    histElectron.form()
    hElectron = histElectron.getHist()
    if options.rebin is not None:
        hElectron.Rebin(options.rebin)        
    hElectron.SetMarkerStyle(21)
    dataElectron.append( hElectron )

    hists.append( histElectron )    



for iname in inputNamesMC :
    prepend = iname[0]
    color = iname[1]
    fnameMuon = iname[2].substitute( tag=options.inputTag, lep='muon' )
    histMuon = SummedKinMCHist(prepend, histTitles[options.var],
                               options.minJets, options.maxJets,
                               options.minTags, options.maxTags,
                               options.inputTextFile, fnameMuon, dirs['Muons'][options.var], prepend, options.var, 'Muons', prepend)
    histMuon.form()
    hMuon = histMuon.getHist()
    if options.rebin is not None:
        hMuon.Rebin(options.rebin)        
    hMuon.SetFillColor(color)
    bkgsMuon.append( hMuon )

    fnameElectron = iname[2].substitute( tag=options.inputTag, lep='electron' )
    histElectron = SummedKinMCHist(prepend, "HT",
                                   options.minJets, options.maxJets,
                                   options.minTags, options.maxTags,
                                   options.inputTextFile, fnameElectron, dirs['Electrons'][options.var], prepend, options.var, 'Electrons', prepend)
    histElectron.form()
    hElectron = histElectron.getHist()
    if options.rebin is not None:
        hElectron.Rebin(options.rebin)        
    hElectron.SetFillColor(color)
    bkgsElectron.append( hElectron )

    hists.append( histMuon )
    hists.append( histElectron ) 

bkgMuonHS = THStack('hs_muon' + options.var, histTitles[options.var])
for bkgm in bkgsMuon:
    bkgMuonHS.Add( bkgm )
    
bkgElectronHS = THStack('hs_electron' + options.var, histTitles[options.var])
for bkge in bkgsElectron:
    bkgElectronHS.Add( bkge )
    

leg = TLegend(0.5, 0.5, 0.8, 0.8)
leg.SetFillColor(0)
leg.SetBorderSize(0)

leg.AddEntry( dataMuon[0], 'Data', 'p')
leg.AddEntry( bkgsMuon[4], 't#bar{t}', 'f')
leg.AddEntry( bkgsMuon[3], 'Single-Top', 'f')
leg.AddEntry( bkgsMuon[2], 'W#rightarrowl#nu', 'f')
leg.AddEntry( bkgsMuon[1], 'Z/#gamma*#rightarrowl^{+}l^{-}', 'f')
leg.AddEntry( bkgsMuon[0], 'QCD', 'f')



if options.var == 'wMT' :
    dataMuon[0].GetXaxis().SetRangeUser(0.0,300.0)
    dataElectron[0].GetXaxis().SetRangeUser(0.0,300.0)


tex=TLatex()
tex.SetNDC()

c1 = TCanvas('c1', 'c1')
dataMuon[0].SetTitle( histTitles[options.var] )
dataMuon[0].Draw('e')
bkgMuonHS.Draw('hist same')
dataMuon[0].Draw('e same')
leg.Draw()
tex.DrawLatex(0.2, 0.88, 'CMS, #sqrt{s} = 7 TeV, 36 pb^{-1} of Muon Data')
c1.Print('prettyplots_mu_' + options.var + '.png', 'png')
c1.Print('prettyplots_mu_' + options.var + '.pdf', 'pdf')


c2 = TCanvas('c2', 'c2')
dataElectron[0].SetTitle( histTitles[options.var] )
dataElectron[0].Draw('e')
bkgElectronHS.Draw('hist same')
dataElectron[0].Draw('e same')
leg.Draw()
tex.DrawLatex(0.2, 0.88, 'CMS, #sqrt{s} = 7 TeV, 36 pb^{-1} of Electron Data')
c2.Print('prettyplots_el_' + options.var + '.png', 'png')
c2.Print('prettyplots_el_' + options.var + '.pdf', 'pdf')
