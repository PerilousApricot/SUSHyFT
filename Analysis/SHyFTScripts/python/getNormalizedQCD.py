#!/bin/pytho
from ROOT import *
from array import *
#from sys import argv
#import sys
#import re
from addTagHistos import *
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

parser.add_option('--mcQCDDir', metavar='MTD', type='string',
                  default='pfShyftAnaQCDWP95',
                  dest='mcQCDDir',
                  help='Main directory from which mc qcd is extracted')

parser.add_option('--mcQCDSubDir', metavar='MTD', type='string',
                  default='NULL',
                  dest='mcQCDSubDir',
                  help='sub directory from which mc qcd is extracted')

parser.add_option('--outputDir', metavar='MTD', type='string',
                  default='plots_772',
                  dest='outputDir',
                  help='Directory to store output histos')

parser.add_option('--filePath', metavar='MTD', type='string',
                  default='../RootFiles_v5',
                  dest='filePath',
                  help='Path to the root histograms')

parser.add_option('--verbose',action='store_true',
                  default=False,
                  dest='verbose',
                  help='verbose switch')

(options,args) = parser.parse_args()

# ==========end: options =============
   
Path          = options.filePath
mcQCDSubDir   = options.mcQCDSubDir
mcQCDDir      = options.mcQCDDir
verbose       = options.verbose
lum           = '{0:1.0f}'.format( options.Lumi)

if mcQCDSubDir == "NULL":
    qcdDir = mcQCDDir
else:
    qcdDir = mcQCDDir+'/'+mcQCDSubDir


f_emen2030    = TFile(Path+'/QCD_Pt-20to30_EMEnriched_TuneZ2_7TeV-pythia6_tlbsm_415_v7.root')
f_emen3080    = TFile(Path+'/QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6_tlbsm_415_v7.root')
f_emen80170   = TFile(Path+'/QCD_Pt-80to170_EMEnriched_TuneZ2_7TeV-pythia6_tlbsm_415_v7.root')
f_bc2e2030    = TFile(Path+'/QCD_Pt-20to30_BCtoE_TuneZ2_7TeV-pythia6_tlbsm_415_v7.root')
f_bc2e3080    = TFile(Path+'/QCD_Pt-30to80_BCtoE_TuneZ2_7TeV-pythia6_tlbsm_415_v7.root')
f_bc2e80170   = TFile(Path+'/QCD_Pt-80to170_BCtoE_TuneZ2_7TeV-pythia6_tlbsm_415_v7.root')
f_gjet40100   = TFile(Path+'/GJets_TuneD6T_HT-40To100_7TeV-madgraph_tlbsm_415_v7.root')
f_gjet100200  = TFile(Path+'/GJets_TuneD6T_HT-100To200_7TeV-madgraph_tlbsm_415_v7.root')
f_gjet200Inf  = TFile(Path+'/GJets_TuneD6T_HT-200_7TeV-madgraph_tlbsm_415_v7.root')

#==== Assumed luminosity (pb-1)=====
lumi = options.Lumi
globalSF = options.globalSF


#===== cross sections (pb)==========
xs_emen2030   =  2454400.0 * globalSF
xs_emen3080   =  3866200.0 * globalSF
xs_emen80170  =  139500.0 * globalSF
xs_bc2e2030   =  132160.0 * globalSF
xs_bc2e3080   =  136804.0 * globalSF
xs_bc2e80170  =  9360.0 * globalSF
xs_gjet40100  =  23620.0 * globalSF
xs_gjet100200 =  3476.0 * globalSF
xs_gjet200Inf =  485.0 * globalSF

#===== Number of generated events ======
n_emen2030    =  36136246
n_emen3080    =  70708892
n_emen80170   =  8069591
n_bc2e2030    =  2243439
n_bc2e3080    =  1995502
n_bc2e80170   =  1043390
n_gjet40100   =  2196870
n_gjet100200  =  1065691
n_gjet200Inf  =  1142171

# ====variables of interest======

names = [
    'MET',        # for 0-tag
    'secvtxMass', # for 1-tag
    'secvtxMass', # for 2-tag
    ]

pretagMET =[
    'MET',        # for 0-tag
    'MET',        # for 1-tag
    'MET',        # for 2-tag
    ]

pretagCentrality =[
    'Central',        # for 0-tag
    'Central',        # for 1-tag
    'Central',        # for 2-tag
    ]

pretagJetEt =[
    'jetEt',        # for 0-tag
    'jetEt',        # for 1-tag
    'jetEt',        # for 2-tag
    ]
pretagEta =[
    'lepEta',        # for 0-tag
    'lepEta',        # for 1-tag
    'lepEta',        # for 2-tag
    ]
pretagSVM = [
    'secvtxMass', # for 1-tag
    'secvtxMass', # for 2-tag
    ]
#'dijetMass'
preLabel = 'pre_'
noLabel  = ''
qcdLabel = 'qcd_'
preMETHists = []
preJetEtHists = []
preCentHists = []
preSVMHists = []
preEtaHists = []
dijetHists = []
allHists = []

# === prepare the inputs ===========

qcdSamples = [
    ['EMEn2030_',     f_emen2030,   xs_emen2030,   n_emen2030,  lumi],
    ['EMEn3080_',     f_emen3080,   xs_emen3080,   n_emen3080,  lumi],
    ['EMEn80170_',    f_emen80170,  xs_emen80170,  n_emen80170, lumi],
    ['BCtoE2030_',    f_bc2e2030,   xs_bc2e2030,   n_bc2e2030,  lumi],
    ['BCtoE3080_',    f_bc2e3080,   xs_bc2e3080,   n_bc2e3080,  lumi],
    ['BCtoE80170_',   f_bc2e80170,  xs_bc2e80170,  n_bc2e80170, lumi],
    ['PhoJet40100_',  f_gjet40100,  xs_gjet40100,  n_gjet40100, lumi],
    ['PhoJet100200_', f_gjet100200, xs_gjet100200, n_gjet100200,lumi],
    ['PhoJet200Inf_', f_gjet200Inf, xs_gjet200Inf, n_gjet200Inf,lumi],
    ]

maxJets = 6
maxTags = 3

h1 = TH1F("h1","h1", 120, 0, 300) ##Dummy for MET
h2 = TH1F("h2","h2", 40,  0, 10)  ##Dummy for secvtxMass
h3 = TH1F("h3","h3", 100, 0, 1000)##Dummy for jetEt
h4 = TH1F("h4","h4", 120, 0, 1.2) ##Dummy for centrality
h5 = TH1F("h5", "h5", 30, 0, 3)   ##Dummy for eta
#======= get 0+1+2 MET histos  ============
for ijet in range(1,maxJets) :
    for itag in range(0,maxTags) :
        if itag > ijet :
            continue
        pMET = pretagMET[itag]
        hist = addHistos( noLabel, qcdDir, pMET+'_'+str(ijet)+'j_'+str(itag)+'t', qcdSamples, 220, verbose)
        #hist.Print()
        h1.Add(hist)
    #h1.Print()    
    h1.SetName(preLabel+pMET+'_'+str(ijet)+'j')    
    preMETHists.append(h1.Clone())
    h1.Reset()
    
#======= get 0+1+2 JetEt histos  ============
for ijet in range(1,maxJets) :
    for itag in range(0,maxTags) :
        if itag > ijet :
            continue
        pJetEt = pretagJetEt[itag]
        hist = addHistos( noLabel, qcdDir, pJetEt+'_'+str(ijet)+'j_'+str(itag)+'t', qcdSamples, 220, verbose)
        #hist.Print()
        h3.Add(hist)
    #h3.Print()    
    h3.SetName(preLabel+pJetEt+'_'+str(ijet)+'j')    
    preJetEtHists.append(h3.Clone())
    h3.Reset()

#======= get 0+1+2 Centrality histos  ============
for ijet in range(1,maxJets) :
    for itag in range(0,maxTags) :
        if itag > ijet :
            continue
        pCent = pretagCentrality[itag]
        hist = addHistos( noLabel, qcdDir, pCent+'_'+str(ijet)+'j_'+str(itag)+'t', qcdSamples, 220, verbose)
        #hist.Print()
        h4.Add(hist)
    #h4.Print()    
    h4.SetName(preLabel+pCent+'_'+str(ijet)+'j')    
    preCentHists.append(h4.Clone())
    h4.Reset()

#======= get 0+1+2 Centrality histos  ============
for ijet in range(1,maxJets) :
    for itag in range(0,maxTags) :
        if itag > ijet :
            continue
        pEta = pretagEta[itag]
        hist = addHistos( noLabel, qcdDir, pEta+'_'+str(ijet)+'j_'+str(itag)+'t', qcdSamples, 220, verbose)
        #hist.Print()
        h5.Add(hist)
    #h5.Print()    
    h5.SetName(preLabel+pCent+'_'+str(ijet)+'j')    
    preEtaHists.append(h5.Clone())
    h5.Reset()    
    
#======= get 1+2 tag secvtxMass histos  ============
for ijet in range(1,maxJets) :
    for itag in range(1,maxTags) :
        if itag > ijet :
            continue
        pSVM = pretagSVM[itag-1]
        hist = addHistos( noLabel, qcdDir, pSVM+'_'+str(ijet)+'j_'+str(itag)+'t', qcdSamples, 220, verbose) 
        #hist.Print()
        h2.Add(hist)
    h2.SetName(preLabel+pSVM+'_'+str(ijet)+'j')    
    preSVMHists.append(h2.Clone())
    h2.Reset()
    
#====== special addition for dijetMass ======
for ijet in range(4,maxJets):
     hist = addHistos( qcdLabel, qcdDir, 'dijetMass_'+str(ijet)+'j_2t', qcdSamples, 220, verbose)
     hist.Print()
     dijetHists.append(hist)
     
#======= get each tag bin histos for any mixture of 0-tag variables and 1+2 tags  ============
for ijet in range(1,maxJets) :
    for itag in range(0,maxTags) :
        if itag > ijet :
            continue
        name = names[itag]
        hist = addHistos( qcdLabel, qcdDir, name+'_'+str(ijet)+'j_'+str(itag)+'t', qcdSamples, 220, verbose)
        allHists.append(hist)
        

#===== fit results ====
if mcQCDSubDir == "NULL":
    pretagScales = {
        '1j_0t' : 6807.729, 
        '2j_0t' : 2408.297, 
        '3j_0t' : 538.115, 
        '4j_0t' : 124.712, 
        '5j_0t' : 56.030, 
        '1j_1t' : 282.896, 
        '2j_1t' : 192.293, 
        '3j_1t' : 56.215, 
        '4j_1t' : 23.130, 
        '5j_1t' : 26.928, 
        '2j_2t' : 11.374, 
        '3j_2t' : 9.941, 
        '4j_2t' : 11.334, 
        '5j_2t' : 5.336,
    }
elif mcQCDSubDir == "eleEB_plus":
    pretagScales ={
        '1j_0t' : 1506.779, 
        '2j_0t' : 529.323, 
        '3j_0t' : 133.197, 
        '4j_0t' : 40.365, 
        '5j_0t' : 7.166, 
        '1j_1t' : 57.882, 
        '2j_1t' : 47.240, 
        '3j_1t' : 10.175, 
        '4j_1t' : 2.121, 
        '5j_1t' : 5.354, 
        '2j_2t' : 5.840, 
        '3j_2t' : 2.447, 
        '4j_2t' : 8.087, 
        '5j_2t' : 0.157,
        }
elif mcQCDSubDir == "eleEB_minus":
    pretagScales = {
        '1j_0t' : 1652.132, 
        '2j_0t' : 525.385, 
        '3j_0t' : 176.738, 
        '4j_0t' : 28.527, 
        '5j_0t' : 8.091, 
        '1j_1t' : 82.012, 
        '2j_1t' : 33.034, 
        '3j_1t' : 11.149, 
        '4j_1t' : 5.002, 
        '5j_1t' : 0.000, 
        '2j_2t' : 8.337, 
        '3j_2t' : 6.820, 
        '4j_2t' : 0.000, 
        '5j_2t' : 6.908, 
        }
elif mcQCDSubDir == "eleEE_plus":
    pretagScales ={
        '1j_0t' : 4321.328, 
        '2j_0t' : 742.686, 
        '3j_0t' : 120.644, 
        '4j_0t' : 100.077, 
        '5j_0t' : 3.251, 
        '1j_1t' : 87.666, 
        '2j_1t' : 64.289, 
        '3j_1t' : 19.411, 
        '4j_1t' : 10.487, 
        '5j_1t' : 3.868, 
        '2j_2t' : 0.000, 
        '3j_2t' : 2.022, 
        '4j_2t' : 1.123, 
        '5j_2t' : 1.791,
        }
elif mcQCDSubDir == "eleEE_minus":
    pretagScales ={
        '1j_0t' : 1909.310, 
        '2j_0t' : 598.251, 
        '3j_0t' : 134.653, 
        '4j_0t' : 41.932, 
        '5j_0t' : 5.589, 
        '1j_1t' : 63.309, 
        '2j_1t' : 49.008, 
        '3j_1t' : 15.332, 
        '4j_1t' : 2.580, 
        '5j_1t' : 1.374, 
        '2j_2t' : 2.788, 
        '3j_2t' : 0.893, 
        '4j_2t' : 1.855, 
        '5j_2t' : 0.000,
        }
newhists={}

for ihist in preMETHists:
    #ihist.Print()
    for PS in pretagScales:
        if ihist.GetName()[-2:] in PS:
            #if '0t' in PS:
            newhists['h_qcd_MET_'+PS]=ihist.Clone()
            newhists['h_qcd_MET_'+PS].SetName('h_qcd_MET_'+PS)
            if newhists['h_qcd_MET_'+PS].Integral()!=0:
                newhists['h_qcd_MET_'+PS].Scale(pretagScales[PS]/newhists['h_qcd_MET_'+PS].Integral())

for ihist in preJetEtHists:
    #ihist.Print()
    for PS in pretagScales:
        if ihist.GetName()[-2:] in PS:
            #if '0t' in PS:
            newhists['h_qcd_jetEt_'+PS]=ihist.Clone()
            newhists['h_qcd_jetEt_'+PS].SetName('h_qcd_jetEt_'+PS)
            if newhists['h_qcd_jetEt_'+PS].Integral()!=0:
                newhists['h_qcd_jetEt_'+PS].Scale(pretagScales[PS]/newhists['h_qcd_jetEt_'+PS].Integral())

for ihist in preCentHists:
    ihist.Print()
    for PS in pretagScales:
        if ihist.GetName()[-2:] in PS:
            #if '0t' in PS:
            newhists['h_qcd_Central_'+PS]=ihist.Clone()
            newhists['h_qcd_Central_'+PS].SetName('h_qcd_Central_'+PS)
            if newhists['h_qcd_Central_'+PS].Integral()!=0:
                newhists['h_qcd_Central_'+PS].Scale(pretagScales[PS]/newhists['h_qcd_Central_'+PS].Integral())

for ihist in dijetHists:
    ihist.Print()
    for PS in pretagScales:
        if ihist.GetName()[-5:] in PS:
            if '4j_2t' or '5j_2t' in PS:
                newhists['h_qcd_dijetMass_'+PS]=ihist.Clone()
                newhists['h_qcd_dijetMass_'+PS].SetName('h_qcd_dijetMass_'+PS)
                if newhists['h_qcd_dijetMass_'+PS].Integral()!=0:
                    newhists['h_qcd_dijetMass_'+PS].Scale(pretagScales[PS]/newhists['h_qcd_dijetMass_'+PS].Integral())
                
for ihist in preSVMHists:
    ihist.Print()
    for PS in pretagScales:
        if ihist.GetName()[-2:] in PS:
             if '1t' in PS or '2t' in PS:
                 #print 'will try to scale histogram ', ihist.GetName(), 'by ',pretagScales[PS]
                 #print ihist.GetName()[:-2]+PS
                 #print 'the name of the histogram will be ','h_qcd_secvtxMass_'+PS
                 newhists['h_qcd_secvtxMass_'+PS]=ihist.Clone()
                 newhists['h_qcd_secvtxMass_'+PS].SetName('h_qcd_secvtxMass_'+PS)
                 if newhists['h_qcd_secvtxMass_'+PS].Integral()!=0:
                     newhists['h_qcd_secvtxMass_'+PS].Scale(pretagScales[PS]/newhists['h_qcd_secvtxMass_'+PS].Integral())
                 
#print newhists
outFile = TFile.Open ('qcd_'+mcQCDSubDir+'_'+lum+'.root', "RECREATE")
for h in newhists:
    print 'name ', h, 'integral ', newhists[h].Integral()
    newhists[h].Write()

outFile.Close()


