#!/bin/python

from ROOT import *
from array import *

gROOT.Macro("~/rootlogon.C")
gStyle.SetOptStat(000000)

f_nominal = TFile('../RootFiles_v5b/TTJets_TuneZ2_7TeV-madgraph-tauola_tlbsm_424_v8.root')
n_ttbar_central =  3688248

##Due to JES
##==========

hist_nom = 'pfShyftAna/Top_secvtxMass_'
hist_jesup = 'pfShyftAnaJES105/Top_secvtxMass_'
hist_jesdn = 'pfShyftAnaJES095/Top_secvtxMass_'

hists_tag_nominal = []
hists_tag_jesup = []
hists_tag_jesdn = []

# >= 3jets, >=1 tags
for ijet in range(3,6) :
    #print 'working tags : ijet = ' + str(ijet)
    for itag in range(1, min(ijet,2) + 1) :
        #print 'working tags : itag = ' + str(itag)
        #print 'Getting ' + hist_tag + str(ijet) + 'j_' + str(itag) + 't'
        hist_tag_nominal = f_nominal.Get( hist_nom + str(ijet) + 'j_' + str(itag) + 't' ).Clone()
        hist_tag_jesup   = f_nominal.Get( hist_jesup + str(ijet) + 'j_' + str(itag) + 't' ).Clone()
        hist_tag_jesdn   = f_nominal.Get( hist_jesdn + str(ijet) + 'j_' + str(itag) + 't' ).Clone()
        hists_tag_nominal.append( hist_tag_nominal )
        hists_tag_jesup.append( hist_tag_jesup )
        hists_tag_jesdn.append( hist_tag_jesdn )
        
hist_tag_nominal_sum = hists_tag_nominal[0]
for hist in range(1,len(hists_tag_nominal)):
    hist_tag_nominal_sum.Add( hists_tag_nominal[hist] )
    
accept =  hist_tag_nominal_sum.Integral()/n_ttbar_central
print '>=3jets,>=1tag nominal events = {0:6.1f}, Acceptance = {1:6.3f} '.format(
        hist_tag_nominal_sum.Integral(), accept
        )

hist_tag_jesup_sum = hists_tag_jesup[0]
for hist in range(1,len(hists_tag_jesup)):
    hist_tag_jesup_sum.Add( hists_tag_jesup[hist] )

accept_jesup =  hist_tag_jesup_sum.Integral()/n_ttbar_central
print '>=3jets,>=1tag JES up events = {0:6.1f}, Acceptance = {1:6.3f} '.format(
        hist_tag_jesup_sum.Integral(), accept_jesup
        )

hist_tag_jesdn_sum = hists_tag_jesdn[0]
for hist in range(1,len(hists_tag_jesdn)):
    hist_tag_jesdn_sum.Add( hists_tag_jesdn[hist] )

accept_jesdn =  hist_tag_jesdn_sum.Integral()/n_ttbar_central
print '>=3jets,>=1tag JES dn events = {0:6.1f}, Acceptance = {1:6.3f} '.format(
        hist_tag_jesdn_sum.Integral(), accept_jesdn
        )

delta_accp_jesup  = ((accept - accept_jesup)/accept)*100
delta_accp_jesdn  = ((accept - accept_jesdn)/accept)*100
print '_____Delta Acceptance for JES for >=3jets,>=1 tag_____'
print 'Delta_A_jesup = {0:3.1f} %, Delta_A_jesdn = {1:3.1f} %, Ave = {2:3.1f}%'.format(
       delta_accp_jesup, delta_accp_jesdn, (fabs(delta_accp_jesup)+fabs(delta_accp_jesdn))/2)


##Due to JER
##==========

hist_jerup = 'pfShyftAnaJER020/Top_secvtxMass_'
hist_jerdn = 'pfShyftAnaJER000/Top_secvtxMass_'

hists_tag_jerup = []
hists_tag_jerdn = []

# >= 3jets, >=1 tags
for ijet in range(3,6) :
    for itag in range(1, min(ijet,2) + 1) :
        hist_tag_jerup   = f_nominal.Get( hist_jerup + str(ijet) + 'j_' + str(itag) + 't' ).Clone()
        hist_tag_jerdn   = f_nominal.Get( hist_jerdn + str(ijet) + 'j_' + str(itag) + 't' ).Clone()
        hists_tag_jerup.append( hist_tag_jerup )
        hists_tag_jerdn.append( hist_tag_jerdn )
        

hist_tag_jerup_sum = hists_tag_jerup[0]
for hist in range(1,len(hists_tag_jerup)):
    hist_tag_jerup_sum.Add( hists_tag_jerup[hist] )

accept_jerup =  hist_tag_jerup_sum.Integral()/n_ttbar_central
print '>=3jets,>=1tag JER up events = {0:6.1f}, Acceptance = {1:6.3f} '.format(
        hist_tag_jerup_sum.Integral(), accept_jerup
        )

hist_tag_jerdn_sum = hists_tag_jerdn[0]
for hist in range(1,len(hists_tag_jerdn)):
    hist_tag_jerdn_sum.Add( hists_tag_jerdn[hist] )

accept_jerdn =  hist_tag_jerdn_sum.Integral()/n_ttbar_central
print '>=3jets,>=1tag JER dn events = {0:6.1f}, Acceptance = {1:6.3f} '.format(
        hist_tag_jerdn_sum.Integral(), accept_jerdn
        )

delta_accp_jerup  = ((accept - accept_jerup)/accept)*100
delta_accp_jerdn  = ((accept - accept_jerdn)/accept)*100
print '_____Delta Acceptance for JER for >=3jets,>=1 tag_____'
print 'Delta_A_jerup = {0:3.1f} %, Delta_A_jerdn = {1:3.1f} %, Ave = {2:3.1f}%'.format(
       delta_accp_jerup, delta_accp_jerdn, (fabs(delta_accp_jerup)+fabs(delta_accp_jerdn))/2)


##Due to MET UnClustered Energy
##=============================

hist_metResup = 'pfShyftAnaMETRES090/Top_secvtxMass_'
hist_metResdn = 'pfShyftAnaMETRES110/Top_secvtxMass_'

hists_tag_metResup = []
hists_tag_metResdn = []

# >= 3jets, >=1 tags
for ijet in range(3,6) :
    for itag in range(1, min(ijet,2) + 1) :
        hist_tag_metResup   = f_nominal.Get( hist_metResup + str(ijet) + 'j_' + str(itag) + 't' ).Clone()
        hist_tag_metResdn   = f_nominal.Get( hist_metResdn + str(ijet) + 'j_' + str(itag) + 't' ).Clone()
        hists_tag_metResup.append( hist_tag_metResup )
        hists_tag_metResdn.append( hist_tag_metResdn )
        

hist_tag_metResup_sum = hists_tag_metResup[0]
for hist in range(1,len(hists_tag_metResup)):
    hist_tag_metResup_sum.Add( hists_tag_metResup[hist] )

accept_metResup =  hist_tag_metResup_sum.Integral()/n_ttbar_central
print '>=3jets,>=1tag METRES up events = {0:6.1f}, Acceptance = {1:6.3f} '.format(
        hist_tag_metResup_sum.Integral(), accept_metResup
        )

hist_tag_metResdn_sum = hists_tag_metResdn[0]
for hist in range(1,len(hists_tag_metResdn)):
    hist_tag_metResdn_sum.Add( hists_tag_metResdn[hist] )

accept_metResdn =  hist_tag_metResdn_sum.Integral()/n_ttbar_central
print '>=3jets,>=1tag METRES dn events = {0:6.1f}, Acceptance = {1:6.3f} '.format(
        hist_tag_metResdn_sum.Integral(), accept_metResdn
        )

delta_accp_metResup  = ((accept - accept_metResup)/accept)*100
delta_accp_metResdn  = ((accept - accept_metResdn)/accept)*100
print '_____Delta Acceptance for MET Resolution for >=3jets,>=1 tag_____'
print 'Delta_A_metResup = {0:3.1f} %, Delta_A_metResdn = {1:3.1f} %, Ave = {2:3.1f}%'.format(
       delta_accp_metResup, delta_accp_metResdn, (fabs(delta_accp_metResup)+fabs(delta_accp_metResdn))/2)

##Due to PileUp
##=============================
hist_PUup = 'pfShyftAnaPUup/Top_secvtxMass_'
hist_PUdn = 'pfShyftAnaPUdown/Top_secvtxMass_'

hists_tag_PUup = []
hists_tag_PUdn = []

# >= 3jets, >=1 tags
for ijet in range(3,6) :
    for itag in range(1, min(ijet,2) + 1) :
        hist_tag_PUup   = f_nominal.Get( hist_PUup + str(ijet) + 'j_' + str(itag) + 't' ).Clone()
        hist_tag_PUdn   = f_nominal.Get( hist_PUdn + str(ijet) + 'j_' + str(itag) + 't' ).Clone()
        hists_tag_PUup.append( hist_tag_PUup )
        hists_tag_PUdn.append( hist_tag_PUdn )
        

hist_tag_PUup_sum = hists_tag_PUup[0]
for hist in range(1,len(hists_tag_PUup)):
    hist_tag_PUup_sum.Add( hists_tag_PUup[hist] )

accept_PUup =  hist_tag_PUup_sum.Integral()/n_ttbar_central
print '>=3jets,>=1tag PU up events = {0:6.1f}, Acceptance = {1:6.3f} '.format(
        hist_tag_PUup_sum.Integral(), accept_PUup
        )

hist_tag_PUdn_sum = hists_tag_PUdn[0]
for hist in range(1,len(hists_tag_PUdn)):
    hist_tag_PUdn_sum.Add( hists_tag_PUdn[hist] )

accept_PUdn =  hist_tag_PUdn_sum.Integral()/n_ttbar_central
print '>=3jets,>=1tag PU dn events = {0:6.1f}, Acceptance = {1:6.3f} '.format(
        hist_tag_PUdn_sum.Integral(), accept_PUdn
        )

delta_accp_PUup  = ((accept - accept_PUup)/accept)*100
delta_accp_PUdn  = ((accept - accept_PUdn)/accept)*100
print '_____Delta Acceptance for PileUp for >=3jets,>=1 tag_____'
print 'Delta_A_PUup = {0:3.1f} %, Delta_A_PUdn = {1:3.1f} %, Ave = {2:3.1f}%'.format(
       delta_accp_PUup, delta_accp_PUdn, (fabs(delta_accp_PUup)+fabs(delta_accp_PUdn))/2)


##Due to B-Tagging
##=============================
## b-tag SF
hist_btag080 = 'pfShyftAnaReweightedBTag080/Top_secvtxMass_'
hist_btag090 = 'pfShyftAnaReweightedBTag090/Top_secvtxMass_'
hist_btag110 = 'pfShyftAnaReweightedBTag110/Top_secvtxMass_'
hist_btag120 = 'pfShyftAnaReweightedBTag120/Top_secvtxMass_'
## lf-tag SF
hist_LFtag080 = 'pfShyftAnaReweightedLFTag080/Top_secvtxMass_'
hist_LFtag090 = 'pfShyftAnaReweightedLFTag090/Top_secvtxMass_'
hist_LFtag110 = 'pfShyftAnaReweightedLFTag110/Top_secvtxMass_'
hist_LFtag120 = 'pfShyftAnaReweightedLFTag120/Top_secvtxMass_'
