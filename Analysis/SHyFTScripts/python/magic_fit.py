#!/usr/bin/python


# ===================================================================
#             magic_fit.py
#
#	Author: Andrew Ivanov
#
#   generic script to 
#	plot kinematic distributions using histograms
#
#	One need to edit "My Inputs" sections to specify root filenames
#	and histogram names
#
# The expected histogram name: "Process_Variable_Nj_Kt"
# Run using --simple option, in case Nj_Kt is not defined
# ====================================================================

from ROOT import *
gROOT.Macro("~/rootlogon.C")

# ===============
# options
# ===============
from optparse import OptionParser
parser = OptionParser()
parser.add_option('--verbose',action='store_true',
                  default=False,
                  dest='verbose',
                  help='verbose switch')				  
parser.add_option('--simple',action='store_true',
                  default=False,
                  dest='simple',
                  help='simple_mode')	
parser.add_option('--fit',action='store_true',
                  default=False,
                  dest='fit',
                  help='fitting_mode')
parser.add_option('--Lumi', metavar='D', type='float', action='store',
                  default=771.5,
                  dest='Lumi',
                  help='Data Luminosity')
parser.add_option('--var', metavar='T', type='string', action='store',
                  default='',
                  dest='var',
                  help='variable to plot')
parser.add_option('--rebin', metavar='T', type='int', action='store',
                  default=1,
                  dest='rebin',
                  help='rebin x axes to this')
parser.add_option('--minJets', metavar='D', type='int', action='store',
                  default=1,
                  dest='minJets',
                  help='Minimum number of jets for plots')
parser.add_option('--maxJets', metavar='D', type='int', action='store',
                  default=5,
                  dest='maxJets',
                  help='Minimum number of jets for plots')
parser.add_option('--nJets', metavar='D', type='int', action='store',
                  default=-1,
                  dest='nJets',
                  help='Exact number of jets for plots')
parser.add_option('--minTags', metavar='D', type='int', action='store',
                  default=0,
                  dest='minTags',
                  help='Minimum number of tags for plots')
parser.add_option('--maxTags', metavar='D', type='int', action='store',
                  default=2,
                  dest='maxTags',
                  help='Minimum number of tags for plots')
parser.add_option('--nTags', metavar='D', type='int', action='store',
                  default=-1,
                  dest='nTags',
                  help='Exact number of tags for plots')

parser.add_option('--templateDir', metavar='MTD', type='string',
                  default='pfShyftAnaNoMET',
                  dest='templateDir',
                  help='Directory from which to get high statistics templates')

parser.add_option('--qcdDir', metavar='MTD', type='string',
                  default='pfShyftAnaQCDWP95NoMET',
                  dest='qcdDir',
                  help='Directory from which to get qcd MC statistics')

parser.add_option('--subDir', metavar='MTD', type='string',
                  default='eleEB',
                  dest='subDir',
                  help='Directory from which to get EE or EB statistics')

parser.add_option('--outputDir', metavar='MTD', type='string',
                  default='plots_772_leg',
                  dest='outputDir',
                  help='Directory to store output histos')

parser.add_option('--pretagDir', metavar='MTD', type='string',
                  default='plots_pre',
                  dest='pretagDir',
                  help='Directory to store output pretag or some combination of histos')

parser.add_option('--nBin', metavar='D', type='int', action='store',
                  default=300,
                  dest='nBin',
                  help='Number of x-axis bin to display')

parser.add_option('--version', type='string', action='store',
                  default='v7',
                  dest='version',
                  help='root files version')

parser.add_option('--fixBin', metavar='D', type='int', action='store',
                  default=1000,
                  dest='fixBin',
                  help='x-bin range to be fitted')

parser.add_option('--printTable', type='string', action='store',
                  default='fitOut.txt',
                  dest='printTable',
                  help='print event counts to the file')


(options,args) = parser.parse_args()
# ==========end: options =============

# =====================================================
# class that contains all relevant plot quantities		
# =====================================================

class TDistribution:
		def __init__(self, name, var, *filenames, **hists):
			self.name = name
			self.legentry = "legentry"
			self.file = TFile(filenames[0]+".root")
			keys = sorted(hists.keys())
                        #print keys
			self.hist = self.file.Get(keys[0])
			print "opening ", filenames[0], ".root, accessing histogram ", keys[0]
                        self.hist.Sumw2
			self.hist.Scale(hists[keys[0]])
			for ihist in keys[1:] :
				histo = self.file.Get(ihist)
				try:	
					self.hist.Add(histo,hists[ihist])				
				except TypeError:
					if options.verbose :
						print "No histogram ", ihist, "in file", filenames[0], " ... skipping"
					continue					
			for filename in filenames[1:] :
				file = TFile(filename+".root")
				keys = sorted(hists.keys())
				for ihist in keys :
					histo = file.Get(ihist)
					try:
						self.hist.Add(histo,hists[ihist])
					except TypeError:
						if options.verbose :
							print "No histogram ", ihist, "in file", filenames[0], " ... skipping"
						continue
			if options.rebin > 1 :
				self.hist.Rebin(options.rebin)
# RooFit quantities:
			self.SF = RooRealVar(name+"SF",name+"SF",1.,0.,100.)
			self.norm = RooRealVar(name+"Norm",name+"Norm",self.hist.Integral())
			self.N = RooFormulaVar(name+"N",name+"SF*"+name+"Norm",RooArgList(self.norm,self.SF))
			if var != 0 :				
				self.set = RooDataHist(name+"Set",name+"Set",RooArgList(var),self.hist)
				self.pdf = RooHistPdf(name+"Pdf",name+"Pdf",RooArgSet(var), self.set)
                                 
# =========== end: class TDistribution =================
	
if options.verbose :
	print "script to create normalized plots"

dirMain     = "../RootFiles_v5/"
tempDir     = options.templateDir
qcdDir      = options.qcdDir
subDir      = options.subDir
reg         = subDir[-8:]
vx          =options.version

nJet = '{0:1.0f}'.format( options.nJets)
nTag = '{0:1.0f}'.format( options.nTags)
minJ = '{0:1.0f}'.format( options.minJets)
maxJ = '{0:1.0f}'.format( options.maxJets)
minT = '{0:1.0f}'.format( options.minTags)
maxT = '{0:1.0f}'.format( options.maxTags)
lum  = '{0:1.0f}'.format( options.Lumi)

#provide explanatory title for each variable name
##if options.var == "secvtxMass" :
##	xtitle = "Secondary Vertex Mass (GeV)," + nJet+"j_"+nTag+"t"
##elif options.var == "MET" :
##	xtitle = "Missing Transverse Energy (GeV)," + nJet+"j_"+nTag+"t"
##elif options.var == "wMT" :
##        xtitle = "W Transverse Mass (GeV)," + nJet+"j_"+nTag+"t"
##elif options.var == "hT" :
##        xtitle = "hT, #sum (Jet et + MET + lep pt) (GeV)," + nJet+"j_"+nTag+"t"
##elif options.var == "elEta" :
##        xtitle = "electron #eta," + nJet+"j_"+nTag+"t"
##elif options.var == "jetEt" :
##        xtitle = "#sum (jet et) (GeV)" + nJet+"j_"+nTag+"t"        
##else :
##	xtitle =""

if options.var == "secvtxMass" :
        xtitle = "Secondary Vertex Mass (GeV), #geq 3j #geq 1t"
elif options.var == "MET" :
        xtitle = "Missing Transverse Energy (GeV), #geq 3j #geq 1t"
elif options.var == "wMT" :
        xtitle = "W Transverse Mass (GeV), #geq 3j #geq 1t"
elif options.var == "hT" :
        xtitle = "hT, #sum (Jet et + MET + lep pt) (GeV), #geq 3j #geq 1t"
elif options.var == "lepPt" :
        xtitle = "electron pt, #geq 3j #geq 1t"
elif options.var == "lepEta" :
        xtitle = "electron #eta, #geq 3j #geq 1t"
elif options.var == "jetEt" :
        xtitle = "electron jet Et, #geq 3j #geq 1t"
else :
        xtitle =""

        
if options.nJets >= 0 :
	options.minJets = options.nJets
	options.maxJets = options.nJets
        minJ            = nJet
        maxJ            = nJet
if options.nTags >= 0 :
	options.minTags = options.nTags
	options.maxTags = options.nTags
        minT            = nTag
        maxT            = nTag

# add different jets/tags histograms
def add(EY=0) :
	keys = sorted(hists.keys())
        if options.verbose :
            print "executing add ",EY
            print "Keys: ", keys
        print hists
	sumEY = 0
	if EY != 0 :
		for nJets in range(options.minJets, options.maxJets+1) :
                    for nTags in range(options.minTags, options.maxTags+1):
				sumEY += EY[nTags][nJets-1]
	for ikey in keys[:] :
		weight = hists[ikey]
		if options.simple :
                        ikey_tmp = ikey + options.var
			hists[ikey_tmp] = weight
                        print weight
		else :
                        ikey_tmp = ikey + "_" + options.var
                        #print ikey_tmp
			bins = {}
			for nJets in range(options.minJets, options.maxJets+1) :
				for nTags in range(options.minTags, options.maxTags+1) :
					temp_key = "_" + str(nJets) + "j_" + str(nTags) + "t"
					if EY != 0 :
                                            bins[temp_key] = weight * EY[nTags][nJets-1]/ sumEY
					else :
						bins[temp_key] = weight
                                                #print 'the weight----->', bins[temp_key]
			bin_keys = sorted(bins.keys())
			for ibin in bin_keys[:] :
				ikey_new = ikey_tmp + ibin
				hists[ikey_new] = bins[ibin]
		del hists[ikey]	
	if options.verbose :	
		for ikey in hists.iteritems() :
			print ikey
        #print 'the returned sum', sumEY                
	return sumEY

def init_var(dist) :
	NBINS = dist.hist.GetNbinsX()
	minX = (dist.hist.GetXaxis()).GetXmin()
	maxX = (dist.hist.GetXaxis()).GetXmax()
	var = RooRealVar(options.var,xtitle,minX,maxX)
	var.setBins(NBINS)
	dist.set = RooDataHist(dist.name+"Set",dist.name+"Set",RooArgList(var),dist.hist)
	return var

#================================
#  ======== My Inputs =========
#================================

globalSF       = options.Lumi *1  #Lumi x LepID SF (LepID = 0.9604)

#======= x-sections ============
Top_xs            = 157.5
WJets_xs          = 31314.0
ZJets_xs          = 3048.0
SingleToptW_xs    = 10.6
SingleTopT_xs     = 20.93
SingleTopS_xs     = 4.6/3.0
EMEn2030_xs       = 2454400.0
EMEn3080_xs       = 3866200.0
EMEn80170_xs      = 139500.0
BCtoE2030_xs      = 132160.0
BCtoE3080_xs      = 136804.0 #SHyFT sample
BCtoE80170_xs     = 9360.0 
GJets40100_xs     = 23620.0
GJets100200_xs    = 3476.0
GJets200Inf_xs    = 485.0

#======== Inclusive events ===============
#n_Top             = 1286491  ##Spring 11
#n_WJets           = 14722996 ##Spring 11
#n_ZJets           = 2495072  ##Spring 11
n_Top             = 3688248  ##Summer 11
n_WJets           = 49484941 ##Summer 11
n_ZJets           = 32512091 ##Summer 11
n_SingleToptW     = 489417
n_SingleTopT      = 484060
n_SingleTopS      = 494967
n_EMEn2030        = 36126246
n_EMEn3080        = 70708892 #SHyFT Spring11 sample
n_EMEn80170       = 8069591 
n_BCtoE2030       = 2243439
n_BCtoE3080       = 1995502
n_BCtoE80170      = 1043390
n_GJets40100      = 2196870  
n_GJets100200     = 1065691
n_GJets200Inf     = 1142171

#_____________________________data_________________________________
filenames = [dirMain +"SingleElectron_tlbsm_424_v8"]
if options.subDir=='NULL':
    hists = {tempDir+'/Data': 1}
else:
    hists = {tempDir+'/'+subDir+'/Data': 1}   
add()
data = TDistribution("data", 0, *filenames,**hists)
data.legentry = "Data("+lum+"pb^{-1})"
data.hist.SetMarkerStyle(8)
data.error = "e"
templates = [data]

var = init_var(data)

#____________________________qcd______________________________________
filenames = [dirMain +"QCD_Pt-20to30_BCtoE_TuneZ2_7TeV-pythia6_tlbsm_415_v7",
             dirMain +"GJets_TuneD6T_HT-100To200_7TeV-madgraph_tlbsm_415_v7",
             dirMain +"GJets_TuneD6T_HT-40To100_7TeV-madgraph_tlbsm_415_v7",              
             dirMain +"GJets_TuneD6T_HT-200_7TeV-madgraph_tlbsm_415_v7",
             dirMain +"QCD_Pt-30to80_BCtoE_TuneZ2_7TeV-pythia6_tlbsm_415_v7",             
             dirMain +"QCD_Pt-80to170_BCtoE_TuneZ2_7TeV-pythia6_tlbsm_415_v7",
             dirMain +"QCD_Pt-20to30_EMEnriched_TuneZ2_7TeV-pythia6_tlbsm_415_v7",
             dirMain +"QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6_tlbsm_415_v7",
             dirMain +"QCD_Pt-80to170_EMEnriched_TuneZ2_7TeV-pythia6_tlbsm_415_v7",
             ]
if options.subDir=='NULL':
    hists = {qcdDir+'/PhoJet40100'  : globalSF*GJets40100_xs/n_GJets40100,
             qcdDir+'/PhoJet100200' : globalSF*GJets100200_xs/n_GJets100200,
             qcdDir+'/PhoJet200Inf' : globalSF*GJets200Inf_xs/n_GJets200Inf,
             qcdDir+'/BCtoE2030'    : globalSF*BCtoE2030_xs/n_BCtoE2030,
             qcdDir+'/BCtoE3080'    : globalSF*BCtoE3080_xs/n_BCtoE3080,  # need to be fixed 
             qcdDir+'/BCtoE80170'   : globalSF*BCtoE80170_xs/n_BCtoE80170,
             qcdDir+'/EMEn2030'     : globalSF*EMEn2030_xs/n_EMEn2030,
             qcdDir+'/EMEn3080'     : globalSF*EMEn3080_xs/n_EMEn3080, 
             qcdDir+'/EMEn80170'    : globalSF*EMEn80170_xs/n_EMEn80170, # need to be fixed       
             }
else:    
    hists = {qcdDir+'/'+subDir+'/PhoJet40100'  : globalSF*GJets40100_xs/n_GJets40100,
             qcdDir+'/'+subDir+'/PhoJet100200' : globalSF*GJets100200_xs/n_GJets100200,
             qcdDir+'/'+subDir+'/PhoJet200Inf' : globalSF*GJets200Inf_xs/n_GJets200Inf,
             qcdDir+'/'+subDir+'/BCtoE2030'    : globalSF*BCtoE2030_xs/n_BCtoE2030,
             qcdDir+'/'+subDir+'/BCtoE3080'    : globalSF*BCtoE3080_xs/n_BCtoE3080,
             qcdDir+'/'+subDir+'/BCtoE80170'   : globalSF*BCtoE80170_xs/n_BCtoE80170,
             qcdDir+'/'+subDir+'/EMEn2030'     : globalSF*EMEn2030_xs/n_EMEn2030,
             qcdDir+'/'+subDir+'/EMEn3080'     : globalSF*EMEn3080_xs/n_EMEn3080,
             qcdDir+'/'+subDir+'/EMEn80170'    : globalSF*EMEn80170_xs/n_EMEn80170,
             }
#override to read pretag templates
inputMaxTags=options.maxTags
inputMinTags=options.minTags

#use the pretag shape for QCD fit
if options.fit:
    if options.nJets==1:
        options.maxTags = 1
        options.minTags = 0
    elif options.nJets>1:
        options.maxTags = 2
        options.minTags = 0
print 'maxTags', options.maxTags
print 'minTags', options.minTags
print 'nJets', options.nJets

##    1jet       2jet      3jet     4jet     5jet
EY = [[6807.729, 2408.297, 538.115, 124.712, 56.030,],#0tag
      [255.9,    10.6,     107.,    21.,     11.3,],#1tag 
      [0.0,      0.6,      18.9,    10.3,    2.2,] ]#2tag

if options.fit:
    add()
    qcd = TDistribution("qcd", var, *filenames,**hists)
else:    
    sumEY = add(EY)
    #add(0)
    qcd = TDistribution("qcd", var, *filenames,**hists)
    qcd.hist.Scale(sumEY/qcd.hist.Integral())
    
qcd.legentry = "QCD"
qcd.hist.SetFillColor(220)
templates.append(qcd)


#override once again to the input tags
options.maxTags=inputMaxTags
options.minTags=inputMinTags

#print options.maxTags
#print options.minTags
#print minJ
#print maxJ
    
#_________________________________EWK______________________________________
if options.fit: 
    filenames = [dirMain +"TToBLNu_TuneZ2_t-channel_7TeV-madgraph_tlbsm_415_v7",
                 dirMain +"TToBLNu_TuneZ2_tW-channel_7TeV-madgraph_tlbsm_415_v7",
                 dirMain +"TToBLNu_TuneZ2_s-channel_7TeV-madgraph_tlbsm_415_v7",
                 dirMain +"DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola_tlbsm_424_v8",
                 dirMain +"TTJets_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8",
                 ]
    if options.subDir=='NULL':
        hists = {tempDir+'/SingleTopT' : globalSF*SingleTopT_xs/n_SingleTopT,
                 tempDir+'/SingleToptW': globalSF*SingleToptW_xs/n_SingleToptW,
                 tempDir+'/SingleTops' : globalSF*SingleTopS_xs/n_SingleTopS,
                 tempDir+'/Zjets'      : globalSF*ZJets_xs/n_ZJets,
                 tempDir+'/Top'        : globalSF*Top_xs/n_Top,
                 }
    else:
        hists = {tempDir+'/'+subDir+'/SingleTopT' : globalSF*SingleTopT_xs/n_SingleTopT,
                 tempDir+'/'+subDir+'/SingleToptW': globalSF*SingleToptW_xs/n_SingleToptW,
                 tempDir+'/'+subDir+'/SingleTops' : globalSF*SingleTopS_xs/n_SingleTopS,
                 tempDir+'/'+subDir+'/Zjets'      : globalSF*ZJets_xs/n_ZJets,
                 tempDir+'/'+subDir+'/Top'        : globalSF*Top_xs/n_Top,
                 }
         
    add()
    ewk = TDistribution("ewk",var, *filenames,**hists)
    ewk.legentry = "EWK/TOP"
    ewk.hist.SetFillColor(215)
    templates.append(ewk)
else:
    #_______________________________single Top_____________________________________
    filenames = [dirMain +"TToBLNu_TuneZ2_t-channel_7TeV-madgraph_tlbsm_415_v7",
                 dirMain +"TToBLNu_TuneZ2_tW-channel_7TeV-madgraph_tlbsm_415_v7",
                 dirMain +"TToBLNu_TuneZ2_s-channel_7TeV-madgraph_tlbsm_415_v7",]
    
    if options.subDir=='NULL':
        hists = {tempDir+'/SingleTopT' : globalSF*SingleTopT_xs/n_SingleTopT,
                 tempDir+'/SingleToptW': globalSF*SingleToptW_xs/n_SingleToptW,
                 tempDir+'/SingleTops' : globalSF*SingleTopS_xs/n_SingleTopS}                 
    else:
        hists = {tempDir+'/'+subDir+'/SingleTopT'  : globalSF*SingleTopT_xs/n_SingleTopT,
                 tempDir+'/'+subDir+'/SingleToptW': globalSF*SingleToptW_xs/n_SingleToptW,
                 tempDir+'/'+subDir+'/SingleTops'  : globalSF*SingleTopS_xs/n_SingleTopS}

    ##    1jet       2jet      3jet     4jet     5jet
    EY = [[6807.729, 2408.297, 538.115, 124.712, 56.030,],#0tag ##Dummmyyy
          [323.2,    380.6,    179.7,   55.1,    12.7,],#1tag 
          [0.00,     55.5,     51.9,    25.1,    8.0,  ] ]#2tag
    
    if options.fit:
        add()
        stop = TDistribution("stop", var, *filenames,**hists)
    else:    
        sumEY = add(EY)
        stop = TDistribution("stop", var, *filenames,**hists)
        stop.hist.Scale(sumEY/stop.hist.Integral())
    
    stop.legentry = "SingleTop"
    stop.hist.SetFillColor(95)    
    templates.append(stop)

    #_________________________________DY_________________________________________
    filenames = [dirMain +"DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola_tlbsm_424_v8"]
    
    if options.subDir=='NULL':
        hists = {tempDir+'/Zjets' : globalSF*ZJets_xs/n_ZJets}        
    else:
        hists = {tempDir+'/'+subDir+'/Zjets' : globalSF*ZJets_xs/n_ZJets}
        
    ##    1jet       2jet      3jet     4jet     5jet
    EY = [[6807.729, 2408.297, 538.115, 124.712, 56.030,],#0tag ##Dummmyyy
          [211.1,    151.3,    59.7,    19.1,    6.3,],   #1tag 
          [0.00,     9.7,      5.7,     2.9,     1.3,]  ] #2tag
    
    if options.fit:
        add()
        dy = TDistribution("dy", var, *filenames,**hists)
    else:    
        sumEY = add(EY)
        dy = TDistribution("dy", var, *filenames,**hists)
        dy.hist.Scale(sumEY/dy.hist.Integral())
           
    dy.legentry = "Z+jets"
    dy.hist.SetFillColor(215)
    templates.append(dy)


    #______________________________Top_______________________________________
    filenames = [dirMain +"TTJets_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8"]
    if options.subDir=='NULL':
        hists = {tempDir+'/Top' : globalSF*Top_xs/n_Top}
    else:
        hists = {tempDir+'/'+subDir+'/Top' : globalSF*Top_xs/n_Top}

    ##    1jet       2jet      3jet     4jet     5jet
    EY = [[6807.729, 2408.297, 538.115, 124.712, 56.030, ],#0tag ##Dummmyyy
          [225.4,    789.2,    1107.8,  756.5,   406.2,  ],#1tag 
          [0.00,     223.4,    536.8,   495.8,   314.4,] ] #2tag
    
    if options.fit:
        add()
        top = TDistribution("top", var, *filenames,**hists)
    else:    
        sumEY = add(EY)
        top = TDistribution("top", var, *filenames,**hists)
        top.hist.Scale(sumEY/top.hist.Integral())
        
    top.legentry = "t #bar{t}"
    top.hist.SetFillColor(206)
    templates.append(top)

#______________________________wjets_____________________________________________
filenames = [dirMain +"WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8" ]
#filenames = [dirMain +"WJetsToLNu_TuneD6T_7TeV-madgraph-tauola_tlbsm_415_v7" ]

if options.subDir=='NULL':    
    hists = {tempDir+'/Wjets' : globalSF*WJets_xs/n_WJets}
else:
    hists = {tempDir+'/'+subDir+'/Wjets' : globalSF*WJets_xs/n_WJets}
    
##scale to expected yields
##    1jet       2jet      3jet     4jet     5jet
EY = [[125323.3, 27504.3,  5612.8,  1130.1,  199.5], #0-tag
      [5062.8,   2326.8,   685.3,   134.7,   40],  #1-tag
      [0.00,    80.5,    75.9,    17.2,   6.3] ] #2-tag

if options.fit:
    add()
    wjets = TDistribution("wjets", var, *filenames,**hists)
else:    
    sumEY = add(EY)
    #add(0)
    wjets= TDistribution("wjets", var, *filenames,**hists)
    wjets.hist.Scale(sumEY/wjets.hist.Integral())
    
wjets.legentry = "W+Jets"
wjets.hist.SetFillColor(210)
templates.append(wjets)

# =====================================================
# ================  FIT =======================
# =====================================================

if options.fit :
        var.setRange("fix",0,options.fixBin)
        sum_pdf = RooAddPdf("SumPdf","SumPdf",RooArgList(qcd.pdf,ewk.pdf,wjets.pdf),RooArgList(qcd.N,ewk.N,wjets.N))
	ewk_constr = RooGaussian("ewk_constr","ewk_constr",ewk.SF,RooFit.RooConst(1.),RooFit.RooConst(0.05))
	tot_pdf = RooProdPdf("TotPdf","TotPdf",RooArgList(sum_pdf,ewk_constr))
        
	##sum_pdf = RooAddPdf("SumPdf","SumPdf",RooArgList(qcd.pdf,ewk.pdf,wjets.pdf),RooArgList(qcd.N,ewk.N,wjets.N))
##	ewk_constr = RooGaussian("ewk_constr","ewk_constr",ewk.SF,RooFit.RooConst(1.),RooFit.RooConst(0.05))
##	tot_pdf = RooProdPdf("TotPdf","TotPdf",RooArgList(sum_pdf,ewk_constr))
        
        
        r = tot_pdf.fitTo(data.set,RooFit.Constrain(RooArgSet(ewk.SF)),RooFit.Extended(kTRUE),RooFit.Range("fix"),RooFit.Save())
	params = tot_pdf.getVariables()
	params.Print("v")

      
	for idist in templates[1:] :
                print idist.hist.Print()
                print params.find(idist.name+"SF").getVal()
		idist.hist.Scale(params.find(idist.name+"SF").getVal())
# =====================================================
# ================  PLOT =======================
# =====================================================
for idist in templates:
    print "   ", idist.legentry, "    %5.2f" % idist.hist.Integral()
    NBins = idist.hist.GetNbinsX()
    minB   = idist.hist.GetBinLowEdge(1)
    maxB   = idist.hist.GetBinLowEdge(NBins + 1)
    IMET = int((20 - minB)/(maxB - minB)*float(NBins))
    if idist.hist.GetName() == 'Data_'+options.var+"_"+nJet+"j_"+nTag+"t":
        relErr = 0 
    #elif idist.hist.GetName() != 'Data_'+options.var+"_"+nJet+"j_"+nTag+"t" and options.fit:
        #print  idist.hist.GetName()
    #    relErr = params.find(idist.name+"SF").getError()/params.find(idist.name+"SF").getVal()
    if options.verbose:
        metCalc = minB + (maxB-minB)*float(IMET)/float(NBins);
        print 'MET bin boundary = ', metCalc
    #============== PRINTING ==========
    ##if options.printTable != '' and options.fit and idist.legentry == 'EWK/TOP':
##    #if options.printTable != '' and options.fit and idist.legentry == 'QCD':
##    #if options.printTable != '' and options.fit and idist.legentry == 'Data(194pb^{-1})':    
##        #print params.find(idist.name+"SF").getVal()
##        file=open(options.printTable,'a')
##        #file.write ('\'{0:1}j_{1:1}t\' : {2:1.3f}, \n'.format(
##        #nJet,
##        #nTag,
##        #idist.hist.Integral(IMET+1,NBins),    
##        #params.find(idist.name+"SF").getVal()  
##        #))
##        file.write('{0:<20}{1:1}j{2:1}t  {3:<6.1f}+/- {4:<15.1f}  {5:<6.1f}+/- {6:<15.1f}\n'.format(
##        idist.legentry,
##        nJet,
##        nTag,    
##        idist.hist.Integral(),
##        relErr * idist.hist.Integral(),
##        #idist.hist.Integral(1,IMET),
##        #relErr * idist.hist.Integral(1,IMET),     
##        idist.hist.Integral(IMET+1,NBins),
##        relErr * idist.hist.Integral(IMET+1,NBins)    
##        ))
##        file.close()
        
hs = THStack("nEvents","nEvents")		
for idist in templates[1:] :
	hs.Add(idist.hist)

# draw
if data.hist.GetMaximum() > hs.GetMaximum() :
	hs.SetMaximum(data.hist.GetMaximum())
hs.Draw("HIST")
data.hist.Draw("esame")
	
xs = hs.GetXaxis()
xs.SetTitle(xtitle)
#xs.SetRangeUser(0.,options.nBin)
#xs.SetRangeUser(0.,200)
gPad.RedrawAxis()

#legend		
leg = TLegend(0.65,0.8,0.99,0.99)
leg.AddEntry(data.hist,data.legentry,"pl")
for idist in reversed(templates[1:]) :
	opt = ""
	if idist.hist.GetFillColor() :
		opt += "f"
	elif idist.hist.GetLineColor() != 1 :
		opt += "l"
	if idist.legentry != "" :
		leg.AddEntry(idist.hist,idist.legentry,opt)

Ysize = max(4, len(templates))
leg.SetY1(1-0.05*Ysize)
leg.SetBorderSize(1)
leg.SetFillColor(10)
leg.Draw()



c1.SetLogy(1)
if options.fit == 1:
    c1.SaveAs(options.outputDir+"/"+options.var+"_fit_"+subDir+"_"+nJet+"j_"+nTag+"t_"+lum+"_log.gif")
    c1.SaveAs(options.outputDir+"/"+options.var+"_fit_"+subDir+"_"+nJet+"j_"+nTag+"t_"+lum+"_log.eps")
    gROOT.ProcessLine(".!epstopdf "+options.outputDir+"/"+options.var+"_fit_"+subDir+"_"+nJet+"j_"+nTag+"t_"+lum+"_log.eps")    
elif minJ==maxJ and minT==maxT:
    c1.SaveAs(options.outputDir+"/"+options.var+"_"+subDir+"_"+nJet+"j_"+nTag+"t_"+lum+"_log.gif")
    c1.SaveAs(options.outputDir+"/"+options.var+"_"+subDir+"_"+nJet+"j_"+nTag+"t_"+lum+"_log.eps")
    gROOT.ProcessLine(".!epstopdf "+options.outputDir+"/"+options.var+"_"+subDir+"_"+nJet+"j_"+nTag+"t_"+lum+"_log.eps")
else:
    c1.SaveAs(options.pretagDir+"/"+options.var+"_"+subDir+"_"+minJ+"j_"+minT+"t_"+lum+"_log.gif")
    c1.SaveAs(options.pretagDir+"/"+options.var+"_"+subDir+"_"+minJ+"j_"+minT+"t_"+lum+"_log.eps")
    gROOT.ProcessLine(".!epstopdf "+options.pretagDir+"/"+options.var+"_"+subDir+"_"+minJ+"j_"+minT+"t_"+lum+"_log.eps")
    
c1.SetLogy(0)
if options.fit == 1:
    c1.SaveAs(options.outputDir+"/"+options.var+"_fit_"+subDir+"_"+nJet+"j_"+nTag+"t_"+lum+".gif")
    c1.SaveAs(options.outputDir+"/"+options.var+"_fit_"+subDir+"_"+nJet+"j_"+nTag+"t_"+lum+".eps")
    gROOT.ProcessLine(".!epstopdf "+options.outputDir+"/"+options.var+"_fit_"+subDir+"_"+nJet+"j_"+nTag+"t_"+lum+".eps")
elif minJ==maxJ and minT==maxT:    
    c1.SaveAs(options.outputDir+"/"+options.var+"_"+subDir+"_"+nJet+"j_"+nTag+"t_"+lum+".gif")
    c1.SaveAs(options.outputDir+"/"+options.var+"_"+subDir+"_"+nJet+"j_"+nTag+"t_"+lum+".eps")
    gROOT.ProcessLine(".!epstopdf "+options.outputDir+"/"+options.var+"_"+subDir+"_"+nJet+"j_"+nTag+"t_"+lum+".eps")
else:
    c1.SaveAs(options.pretagDir+"/"+options.var+"_"+subDir+"_"+minJ+"j_"+minT+"t_"+lum+".gif")
    c1.SaveAs(options.pretagDir+"/"+options.var+"_"+subDir+"_"+minJ+"j_"+minT+"t_"+lum+".eps")
    gROOT.ProcessLine(".!epstopdf "+options.pretagDir+"/"+options.var+"_"+subDir+"_"+minJ+"j_"+minT+"t_"+lum+".eps")
    
