#!/bin/pytho
from ROOT import *
from array import *
#from sys import argv
#import sys
#import re
from addHistos import *
from weightHisto import *
gROOT.Macro("~/rootlogon.C")
gStyle.SetOptStat(000000)

# ===============
# options
# ===============
from optparse import OptionParser
parser = OptionParser()
parser.add_option('--Lumi', metavar='D', type='float', action='store',
                  default=771.5,
                  dest='Lumi',
                  help='Data Luminosity')

parser.add_option('--globalSF', metavar='SF', type='float',
                  default=1.0,
                  dest='globalSF',
                  help='Global lepton SF (%default default)')

parser.add_option('--rebin', metavar='T', type='int', action='store',
                  default=3,
                  dest='rebin',
                  help='rebin x axes to this')

parser.add_option('--templateDir', metavar='MTD', type='string',
                  default='pfShyftAna',
                  dest='templateDir',
                  help='Directory from which to get different config')

parser.add_option('--mcQCDDir', metavar='MTD', type='string',
                  default='pfShyftAnaQCDWP95',
                  dest='mcQCDDir',
                  help='Directory from which mc qcd is extracted')

parser.add_option('--outputDir', metavar='MTD', type='string',
                  default='plots_772',
                  dest='outputDir',
                  help='Directory to store output histos')

parser.add_option('--filePath', metavar='MTD', type='string',
                  default='../RootFiles_v5',
                  dest='filePath',
                  help='Path to the root histograms')

parser.add_option('--var', metavar='MTD', type='string',
                  default='jet1Pt',
                  dest='var',
                  help='variable of interest')

parser.add_option('--nBin', metavar='D', type='int', action='store',
                  default=40,
                  dest='nBin',
                  help='Number of x-axis bin to display')

parser.add_option('--verbose',action='store_true',
                  default=False,
                  dest='verbose',
                  help='verbose switch')

(options,args) = parser.parse_args()

# ==========end: options =============
   
Path          = options.filePath
tempDir       = options.templateDir
qcdDir        = options.mcQCDDir
var           = options.var
verbose       = options.verbose
lum           = '{0:1.0f}'.format( options.Lumi)

f_data        = TFile(Path+'/SingleElectron_tlbsm_424_v8.root')
#f_tprime400   = TFile(Path+'/tprime400_bWbW_Fall10MG7TeV_AlexisLHE_v1_ttbsm_415_v7.root')
f_ttbar       = TFile(Path+'/TTJets_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8.root')
f_wjets       = TFile(Path+'/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8.root')
f_zjets       = TFile(Path+'/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola_tlbsm_424_v8.root')
f_sToptW      = TFile(Path+'/TToBLNu_TuneZ2_tW-channel_7TeV-madgraph_tlbsm_415_v7.root')
f_sTopt       = TFile(Path+'/TToBLNu_TuneZ2_t-channel_7TeV-madgraph_tlbsm_415_v7.root')
f_sTops       = TFile(Path+'/TToBLNu_TuneZ2_s-channel_7TeV-madgraph_tlbsm_415_v7.root')
f_emen2030    = TFile(Path+'/QCD_Pt-20to30_EMEnriched_TuneZ2_7TeV-pythia6_tlbsm_415_v7.root')
f_emen3080    = TFile(Path+'/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6_tlbsm_415_v7.root')
f_emen80170   = TFile(Path+'/QCD_Pt-80to170_EMEnriched_TuneZ2_7TeV-pythia6_tlbsm_415_v7.root')
f_bc2e2030    = TFile(Path+'/QCD_Pt-20to30_BCtoE_TuneZ2_7TeV-pythia6_tlbsm_415_v7.root')
f_bc2e3080    = TFile(Path+'/QCD_Pt-30to80_BCtoE_TuneZ2_7TeV-pythia6_tlbsm_415_v7.root')
f_bc2e80170   = TFile(Path+'/QCD_Pt-80to170_BCtoE_TuneZ2_7TeV-pythia6_tlbsm_415_v7.root')
f_gjet40100   = TFile(Path+'/GJets_TuneD6T_HT-200_7TeV-madgraph_tlbsm_415_v7.root')
f_gjet100200  = TFile(Path+'/GJets_TuneD6T_HT-40To100_7TeV-madgraph_tlbsm_415_v7.root')
f_gjet200Inf  = TFile(Path+'/GJets_TuneD6T_HT-100To200_7TeV-madgraph_tlbsm_415_v7.root')

#==== Assumed luminosity (pb-1)=====
lumi = options.Lumi
globalSF = options.globalSF


#===== cross sections (pb)==========
xs_ttbar      =  157.5 * globalSF
xs_wjets      =  31314.0 * globalSF
xs_zjets      =  3048.0 * globalSF
xs_sToptW     =  10.6 * globalSF
xs_sTopt      =  20.93 * globalSF
xs_sTops      =  4.6/3.0 * globalSF
xs_emen2030   =  2454400.0 * globalSF
xs_emen3080   =  3866200.0 * globalSF
xs_emen80170  =  139500.0 * globalSF
xs_bc2e2030   =  132160.0 * globalSF
xs_bc2e3080   =  136804.0 * globalSF
xs_bc2e80170  =  9360.0 * globalSF
xs_gjet40100  =  23620.0 * globalSF
xs_gjet100200 =  3476.0 * globalSF
xs_gjet200Inf =  485.0 * globalSF
#xs_tprime400  =  1.30 * globalSF * 5

#===== Number of generated events ======
n_ttbar       =  3688248
n_wjets       =  49484941
n_zjets       =  32512091
n_sToptW      =  489417
n_sTopt       =  484060
n_sTops       =  494967
n_emen2030    =  36136246
n_emen3080    =  70708892
n_emen80170   =  8069591
n_bc2e2030    =  2243439
n_bc2e3080    =  1995502
n_bc2e80170   =  1043390
n_gjet40100   =  2196870
n_gjet100200  =  1065691
n_gjet200Inf  =  1142171
#n_tprime400   =  205202

# ====variables of interest======
names = [
    var,
    ]

# === prepare the inputs ===========
dataLabel     = 'Data_'
#tprimeLabel   = 'TPrime400_'
topLabel      = 'Top_'
wjetsLabel    = 'Wjets_'
zjetsLabel    = 'Zjets_'
sTopLabel     = 'STop_'
qcdLabel      = 'QCD_'

allHists     = []

dataSample   = [f_data,      1.0 ,         1.0,         1.0 ]
#tprimeSample = [f_tprime400, xs_tprime400, n_tprime400, lumi]
topSample    = [f_ttbar,     xs_ttbar,     n_ttbar,     lumi]
wjetSample   = [f_wjets,     xs_wjets,     n_wjets,     lumi]
zjetSample   = [f_zjets,     xs_zjets,     n_zjets,     lumi]

singleTopSamples = [
    [f_sToptW,    xs_sToptW,   n_sToptW,  lumi],
    [f_sTopt,     xs_sTopt,    n_sTopt,   lumi],
    [f_sTops,     xs_sTops,    n_sTops,   lumi],
    ]

qcdSamples = [
    [f_emen2030,   xs_emen2030,   n_emen2030,  lumi],
    [f_emen3080,   xs_emen3080,   n_emen3080,  lumi],
    [f_emen80170,  xs_emen80170,  n_emen80170, lumi],
    [f_bc2e2030,   xs_bc2e2030,   n_bc2e2030,  lumi],
    [f_bc2e3080,   xs_bc2e3080,   n_bc2e3080,  lumi],
    [f_bc2e80170,  xs_bc2e80170,  n_bc2e80170, lumi],
    [f_gjet40100,  xs_gjet40100,  n_gjet40100, lumi],
    [f_gjet100200, xs_gjet100200, n_gjet100200,lumi],
    [f_gjet200Inf, xs_gjet200Inf, n_gjet200Inf,lumi],
    ]

#======= add the qcd and singleTop histos and apply weights to all ============
for ivar in range(0, len(names)) :
    name = names[ivar]
    hist_data  = weightHisto( dataLabel,   tempDir, name, dataSample,    kBlack, verbose)
    #hist_tp    = weightHisto( tprimeLabel, tempDir, name, tprimeSample,  6,      verbose)
    hist_top   = weightHisto( topLabel,    tempDir, name, topSample,     206,    verbose)
    hist_wjets = weightHisto( wjetsLabel,  tempDir, name, wjetSample,    210,    verbose)
    hist_zjets = weightHisto( zjetsLabel,  tempDir, name, zjetSample,    215,    verbose)   
    hist_sTop  = addHistos( sTopLabel,   tempDir, name, singleTopSamples,95,     verbose)
    hist_qcd   = addHistos( qcdLabel,    tempDir, name, qcdSamples,      220,    verbose)
    
    print 'data area', hist_data.Integral()
    allHists.append(hist_data)
    allHists.append(hist_qcd)
    allHists.append(hist_sTop)
    allHists.append(hist_zjets)
    allHists.append(hist_wjets)
    allHists.append(hist_top)
    #allHists.append(hist_tp)
    
# ============= PLOT ==================
hs = THStack("nEvents","nEvents")
for ihist in allHists[1:]:
    ihist.Rebin(options.rebin)
    hs.Add(ihist)
    ihist.Print()

if var == 'nJets':
   xtitle = "number of jets"
if var == 'nTags':
   xtitle = "number of b-tag jets"   
if var == 'm3':
    xtitle = "M3"
if var == 'm3_2t':
    xtitle = "M3 with at least 2tag jets"
if var == 'm3_1t':
    xtitle = "M3 with at least 1tag jet"
if var == 'm3_0t':
    xtitle = "M3 with 0tag jet"    
if var == 'jet1Pt':
    xtitle = "leading jet pt (GeV)"
if var == 'jet2Pt':
    xtitle = "second leading jet pt (GeV)"
if var == 'jet3Pt':
    xtitle = "third leading jet pt (GeV)"
if var == 'jet4Pt':
    xtitle = "fourth leading jet pt (GeV)"
if var == 'jet4Mass':
    xtitle = "fourth leading jet mass (GeV)"
if var == 'jet4Phi':
    xtitle = "fourth leading jet #phi"
if var == 'discriminator':
    xtitle = "b-tagging discriminator (SSVHEM)"
if var == 'lepRelIso':
    xtitle = "electron relative isolation"
if var == 'lepEta':
    xtitle = "electron #eta"
if var == 'lepPhi':
    xtitle = "electron $phi"
if var == 'lepJetdR':
    xtitle = "dR b/w electron and jets"
if var == 'nPrimVertices':
    xtitle = "Number of Primary vertices"    
else:
    xtitle = ""
    
# draw
if allHists[0].GetMaximum() > hs.GetMaximum() :
    hs.SetMaximum(allHists[0].GetMaximum())

c1 = TCanvas('c1', 'c1')
allHists[0].Rebin(options.rebin)
allHists[0].SetMarkerStyle(8)
allHists[0].error = "e"
hs.Draw("HIST")
allHists[0].Draw("esame")

xs = hs.GetXaxis()
xs.SetTitle(xtitle)
#xs.SetRangeUser(0.,options.nBin)
#xs.SetRangeUser(0.,200)
gPad.RedrawAxis()

#legend		
leg = TLegend(0.65,0.8,0.99,0.99)
leg.AddEntry(allHists[0],"Data (194pb^{-1})","pl")
#leg.AddEntry(allHists[6],"#acute{t} #bar{#acute{t}}, 400GeV, 5*#sigma_{th}","f")
leg.AddEntry(allHists[5],"t #bar{t}","f")
leg.AddEntry(allHists[4],"W+jets","f")
leg.AddEntry(allHists[3],"Z+jets","f")
leg.AddEntry(allHists[2],"SingleTop","f")
leg.AddEntry(allHists[1],"QCD","f")

Ysize = max(4, len(allHists))
leg.SetY1(1-0.05*Ysize)
leg.SetBorderSize(1)
leg.SetFillColor(10)
#leg.Draw()

c1.SetLogy(1)
c1.SaveAs(options.outputDir+"/"+options.var+"_"+lum+"_log.gif")
c1.SaveAs(options.outputDir+"/"+options.var+"_"+lum+"_log.eps")
gROOT.ProcessLine(".!epstopdf "+options.outputDir+"/"+options.var+"_"+lum+"_log.eps")

c1.SetLogy(0)
c1.SaveAs(options.outputDir+"/"+options.var+"_"+lum+".gif")
c1.SaveAs(options.outputDir+"/"+options.var+"_"+lum+".eps")
gROOT.ProcessLine(".!epstopdf "+options.outputDir+"/"+options.var+"_"+lum+".eps")
