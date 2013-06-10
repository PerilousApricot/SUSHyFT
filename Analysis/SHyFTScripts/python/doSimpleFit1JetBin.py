#!/bin/python


# ===================================================
#             make_plots.py
#
#  Simple script to plot a stitched distribution
# ===================================================
# ===================================================



from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputFile', metavar='F', type='string', action='store',
                  default='shyftPlots_stitched_pfShyftAna_35pb_387v1data_387v1mc.root',
                  dest='inputFile',
                  help='input file tag to be used')

parser.add_option('--wqqQ2Variation', metavar='S', type='string', action='store',
                  default='nominal',
                  dest='wqqQ2Variation',
                  help='very simple W+QQ Q^2 variation, taken from 3-jet, 1-tag sample')

parser.add_option('--wcxQ2Variation', metavar='S', type='string', action='store',
                  default='nominal',
                  dest='wcxQ2Variation',
                  help='very simple W+c+X Q^2 variation, taken from 3-jet, 1-tag sample')

parser.add_option('--wbxQ2Variation', metavar='S', type='string', action='store',
                  default='nominal',
                  dest='wbxQ2Variation',
                  help='very simple W+b+X Q^2 variation, taken from 3-jet, 1-tag sample')



parser.add_option('--noFit', action='store_true',
                  default=False,
                  dest='noFit',
                  help='ignore the fit')


parser.add_option('--outLabel', metavar='L', type='string', action='store',
                  default='simpleFit',
                  dest='outLabel',
                  help='output label')

(options, args) = parser.parse_args()

argv = []



from ROOT import *
from array import *

gROOT.Macro("rootlogon.C")

f = TFile(options.inputFile)

species = [
    'QCD_B',
    'Zbx',  
    'Zcx',  
    'Zqq',  
    'Wbx',  
    'Wcx',  
    'Wqq',   
    'SingleTop',
    'Top',
    'Data'
    ]

hists = []

for ispecies in species :
#    print 'processing species ' + ispecies
    jetbinhists = []
    ijet = 1
    itag = 1
    h = f.Get( ispecies + '_secvtxMass_' + str(ijet) + 'j_' + str(itag) + 't').Clone()
    tagbinhist = h
    jetbinhist = tagbinhist
    hists.append(jetbinhist)


plothists = [hists[0].Clone(),
             hists[1].Clone(),
             hists[4].Clone(),
             hists[5].Clone(),
             hists[6].Clone(),
             hists[7].Clone(),
             hists[8].Clone(),
             hists[9].Clone()]

# Add Z+Jets together
plothists[1].Add( hists[2] )
plothists[1].Add( hists[3] )

# Do a simple Q^2 variation

wbxDict = dict ( {'down':0.28, 'nominal':1.0, 'up':1.24 } )
wcxDict = dict ( {'down':0.46, 'nominal':1.0, 'up':2.00 } )
wqqDict = dict ( {'down':0.80, 'nominal':1.0, 'up':1.82 } )

bscale = wbxDict[options.wbxQ2Variation]
cscale = wcxDict[options.wcxQ2Variation]
lfscale = wqqDict[options.wqqQ2Variation]

# Add W+jets together
#plothists[2].Scale( bscale )
#plothists[2].Add( hists[5], cscale )
#plothists[2].Add( hists[6], lfscale )


print '--------------------------------------------------------------'
print 'NHF              : Wbx = {0:6.2f}, Wcx = {1:6.2f}, Wqq = {2:6.2f}'.format(
#    bscale * hists[4].Integral(), cscale * hists[5].Integral(), lfscale * hists[6].Integral()
    hists[4].Integral(), hists[5].Integral(), hists[6].Integral()
    )
print 'Number of events : Top = {0:6.2f}, Single Top = {1:6.2f}, W+LF = {2:6.2f}, W+C = {3:6.2f}, W+B = {4:6.2f}, Zjets = {5:6.2f}, QCD = {6:6.2f}'.format(
    plothists[6].Integral(),
    plothists[5].Integral(),
    plothists[4].Integral(),
    plothists[3].Integral(),
    plothists[2].Integral(),
    plothists[1].Integral(),
    plothists[0].Integral(),
    )
print 'RMS              : Top = {0:6.2f}, Single Top = {1:6.2f}, W+LF = {2:6.2f}, W+C = {3:6.2f}, W+B = {4:6.2f}, Zjets = {3:6.2f}, QCD = {4:6.2f}'.format(
    plothists[6].GetRMS(),
    plothists[5].GetRMS(),
    plothists[4].GetRMS(),
    plothists[3].GetRMS(),    plothists[2].GetRMS(),
    plothists[1].GetRMS(),
    plothists[0].GetRMS(),    
    )
print '--------------------------------------------------------------'

colors = [
    TColor.kYellow,
    TColor.kAzure-2,
    TColor.kGreen-3,
    TColor.kGreen-2,
    TColor.kGreen-1,
    TColor.kMagenta,
    TColor.kRed+1,
    TColor.kBlack
    ]
names = [
    'QCD',
    'Z/#gamma*#rightarrowl^{+}l^{-}',
    'W#rightarrowl#nu+b',
    'W#rightarrowl#nu+c',
    'W#rightarrowl#nu+q',    
    'Single Top',
    't#bar{t}'
    ]

leg = TLegend(0.5, 0.5, 0.8, 0.8)
leg.SetFillColor(0)
leg.SetBorderSize(0)
stack = THStack('hs','hs')
for hist in range(0, len(plothists)-1):
    plothists[hist].SetFillStyle(1001)
    plothists[hist].SetFillColor(colors[hist])
    stack.Add( plothists[hist] )
    leg.AddEntry( plothists[hist], names[hist], 'f')

plothists[len(plothists)-1].SetMarkerStyle(20)
plothists[len(plothists)-1].Draw('e')
plothists[len(plothists)-1].SetName('data_1jets_1tags')
plothists[len(plothists)-1].SetTitle('Secondary Vertex Mass, >=3 Jets, >=1 Tags;Vertex Mass (GeV/c^{2});Number of events')
stack.Draw('hist same')
plothists[len(plothists)-1].Draw('e same')
leg.Draw()

c2 = TCanvas('c2', 'c2')
stack2 = THStack('hs','hs')
for hist in range(0, len(hists)-1):    
    stack2.Add( hists[hist] )

hists[len(hists)-1].SetMarkerStyle(20)
hists[len(hists)-1].Draw('e')
hists[len(hists)-1].SetName('data_1jets_1tags')
hists[len(hists)-1].SetTitle('Secondary Vertex Mass, >=3 Jets, >=1 Tags;Vertex Mass (GeV/c^{2});Number of events')
stack2.Draw('hist same')
hists[len(hists)-1].Draw('e same')

c1.Print( options.outLabel + 'mcExp1jet.png', 'png')
c1.Print( options.outLabel + 'mcExp1jet.pdf', 'pdf')

if options.noFit is False:

    x = RooRealVar('x', 'x', 0., 10.0)


    h_rf_data = RooDataHist("dR0", "dR0", RooArgList(x), plothists[len(plothists)-1] )

    h_rf_qcd   =RooDataHist ("h_rf_qcd",   "h_rf_qcd",   RooArgList(x), plothists[0] )
    pdf_qcd_bare =RooHistPdf  ("pdf_qcd",    "pdf_qcd",    RooArgSet(x), h_rf_qcd)
    qcdfrac = RooRealVar('qcdfrac','QCD Fraction', plothists[0].Integral(), 0.0, 10000.0)
    constraint_qcd = RooGaussian("constraint_qcd","constraint_qcd",qcdfrac,
                                 RooFit.RooConst(plothists[0].Integral()),
                                 RooFit.RooConst(plothists[0].Integral() * 1.0)
                                 )
    pdf_qcd = RooProdPdf("sumc","sum with constraint",RooArgList(pdf_qcd_bare, constraint_qcd), 0.) ;

    h_rf_zjets   =RooDataHist ("h_rf_zjets",   "h_rf_zjets",   RooArgList(x), plothists[1] )
    pdf_zjets    =RooHistPdf  ("pdf_zjets",    "pdf_zjets",    RooArgSet(x), h_rf_zjets)

    h_rf_wb   =RooDataHist ("h_rf_wb",   "h_rf_wb",   RooArgList(x), plothists[2] )
    pdf_wb    =RooHistPdf  ("pdf_wb",    "pdf_wb",    RooArgSet(x), h_rf_wb)

    h_rf_wc   =RooDataHist ("h_rf_wc",   "h_rf_wc",   RooArgList(x), plothists[3] )
    pdf_wc    =RooHistPdf  ("pdf_wc",    "pdf_wc",    RooArgSet(x), h_rf_wc)

    h_rf_wq   =RooDataHist ("h_rf_wq",   "h_rf_wq",   RooArgList(x), plothists[4] )
    pdf_wq    =RooHistPdf  ("pdf_wq",    "pdf_wq",    RooArgSet(x), h_rf_wq)

    
    h_rf_singletop   =RooDataHist ("h_rf_singletop",   "h_rf_singletop",   RooArgList(x), plothists[5] )
    pdf_singletop    =RooHistPdf  ("pdf_singletop",    "pdf_singletop",    RooArgSet(x), h_rf_singletop)

    h_rf_top   =RooDataHist ("h_rf_top",   "h_rf_top",   RooArgList(x), plothists[6] )
    pdf_top    =RooHistPdf  ("pdf_top",    "pdf_top",    RooArgSet(x), h_rf_top)




    zjetsfrac = RooRealVar('zjetsfrac','Z+jets Fraction',plothists[1].Integral(), 0.0, 10000.0)
    wbfrac = RooRealVar('wbfrac','W+jets Fraction',plothists[2].Integral(), 0.0, 10000.0)    
    wcfrac = RooRealVar('wcfrac','W+jets Fraction',plothists[3].Integral(), 0.0, 10000.0)
    wqfrac = RooRealVar('wqfrac','W+jets Fraction',plothists[4].Integral(), 0.0, 10000.0)
    singletopfrac = RooRealVar('stopfrac','Single Top Fraction',plothists[5].Integral(), 0.0, 10000.0)
    topfrac = RooRealVar('topfrac','TTbar Fraction',plothists[6].Integral(), 0.0, 10000.0)

    #pdf_mass = RooAddPdf("pdf_mass", "pdf_mass",
    #                     RooArgList(pdf_qcd, pdf_zjets, pdf_wjets, pdf_singletop, pdf_top),
    #                     RooArgList(qcdfrac,zjetsfrac,wjetsfrac,singletopfrac,topfrac) )
    pdf_mass = RooAddPdf("pdf_mass", "pdf_mass",
                         RooArgList(pdf_qcd,pdf_wq,pdf_wc,pdf_wb,pdf_singletop,pdf_top),
                         RooArgList(qcdfrac,wqfrac,wcfrac,wbfrac,singletopfrac,topfrac) )



    r = pdf_mass.fitTo( h_rf_data, RooFit.Save(), RooFit.Extended(), RooFit.Constrain(RooArgSet(qcdfrac)) )
    r.Print()

    xframe = x.frame(RooFit.Title("Secondary Vertex Mass, 1 jet, 1 tag;SecVtx Mass (GeV/c^2);Events")) ;

    RooAbsData.plotOn(h_rf_data, xframe, )
    #RooAddPdf.plotOn(pdf_mass, xframe, RooFit.LineColor(kBlack))
    argset1 = RooArgSet(pdf_top,pdf_singletop,pdf_wq,pdf_wc,pdf_wb,pdf_qcd)
    pdf_mass.plotOn(xframe, RooFit.Components(argset1), RooFit.FillColor(2), RooFit.LineColor(1), RooFit.DrawOption("F"))

    argset1a = RooArgSet(pdf_singletop,pdf_wq,pdf_wc,pdf_wb,pdf_qcd)
    pdf_mass.plotOn(xframe, RooFit.Components(argset1a), RooFit.FillColor(kMagenta), RooFit.LineColor(1), RooFit.DrawOption("F"))
    
    argset2 = RooArgSet(pdf_wq,pdf_wc,pdf_wb,pdf_qcd)
    pdf_mass.plotOn(xframe, RooFit.Components(argset2), RooFit.FillColor(kGreen-1), RooFit.LineColor(1), RooFit.DrawOption("F")) 

    argset3 = RooArgSet(pdf_wc,pdf_wb,pdf_qcd)
    pdf_mass.plotOn(xframe, RooFit.Components(argset3), RooFit.FillColor(kGreen-2), RooFit.LineColor(1), RooFit.DrawOption("F")) 

    argset4 = RooArgSet(pdf_wb,pdf_qcd)
    pdf_mass.plotOn(xframe, RooFit.Components(argset4), RooFit.FillColor(kGreen-3), RooFit.LineColor(1), RooFit.DrawOption("F")) 

    argset5 = RooArgSet(pdf_qcd)
    pdf_mass.plotOn(xframe, RooFit.Components(argset5), RooFit.FillColor(kYellow), RooFit.LineColor(1), RooFit.DrawOption("F"))
    RooAbsData.plotOn(h_rf_data, xframe)
    #RooAbsPdf.plotOn(pdf_wjets, xframe, RooFit.LineColor(kGreen))
    #RooAbsPdf.plotOn(pdf_qcd, xframe, RooFit.LineColor(kYellow))

    #pdf_mass.plotOn(xframe, RooFit.Components(RooArgSet(pdf_top, pdf_wjets)), RooFit.LineColor(kMagenta) )
    #pdf_mass.plotOn(xframe, RooFit.Components(RooArgSet(pdf_wjets)), RooFit.LineColor(kRed) )



    c3 = TCanvas('c3', 'c3')
    xframe.Draw()

    c3.Print( options.outLabel + 'simplefit1jet.png','png')
    c3.Print( options.outLabel + 'simplefit1jet.pdf','pdf')

