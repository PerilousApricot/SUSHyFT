#!/bin/python

import subprocess

options = [

###_________________________________________
##                Using JetEt as 0-tag    
###________________________________________
    

    
#########___________________________________All___________________________________________________________

##    ['pfShyftAna',        'pfShyftAna',     'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'jetEt'],
    
##    ####JES
##    ['pfShyftAnaJES095',  'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'jetEt'],
##    ['pfShyftAnaJES105',  'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'jetEt'],
    
##    ##BTagging
##    ['pfShyftAnaReweightedBTag080', 'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'jetEt'],
##    ['pfShyftAnaReweightedBTag090', 'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'jetEt'],
##    ['pfShyftAnaReweightedBTag110', 'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'jetEt'],
##    ['pfShyftAnaReweightedBTag120', 'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag080','pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag090','pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag110','pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag120','pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'jetEt'],
    
##    ## systematics (JER, jetEt resolution, elePt in EE on resolution)
##    ['pfShyftAnaJER000',          'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'jetEt'],
##    ['pfShyftAnaJER020',          'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'jetEt'],
##    ['pfShyftAnaMETRES090',     'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'jetEt'],
##    ['pfShyftAnaMETRES110',     'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'jetEt'],
    
###___________________________________EB plus___________________________________________________________

##      ['pfShyftAna/eleEB_plus',        'pfShyftAna/eleEB_plus',     'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'jetEt'],
    
##    ##JES
##    ['pfShyftAnaJES095/eleEB_plus',  'pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'jetEt'],
##    ['pfShyftAnaJES105/eleEB_plus',  'pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'jetEt'],
    
##    ##BTagging
##    ['pfShyftAnaReweightedBTag080/eleEB_plus', 'pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'jetEt'],
##    ['pfShyftAnaReweightedBTag090/eleEB_plus', 'pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'jetEt'],
##    ['pfShyftAnaReweightedBTag110/eleEB_plus', 'pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'jetEt'],
##    ['pfShyftAnaReweightedBTag120/eleEB_plus', 'pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag080/eleEB_plus','pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag090/eleEB_plus','pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag110/eleEB_plus','pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag120/eleEB_plus','pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'jetEt'],
    
##    ## systematics (JER, jetEt resolution, elePt in EE on resolution)
##    ['pfShyftAnaJER000/eleEB_plus',           'pfShyftAna/eleEB_plus',  'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'jetEt'],
##    ['pfShyftAnaJER020/eleEB_plus',           'pfShyftAna/eleEB_plus',  'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'jetEt'],
##    ['pfShyftAnaMETRES090/eleEB_plus',        'pfShyftAna/eleEB_plus',  'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'jetEt'],
##    ['pfShyftAnaMETRES110/eleEB_plus',        'pfShyftAna/eleEB_plus',  'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'jetEt'],


###___________________________________EB minus___________________________________________________________

##    ['pfShyftAna/eleEB_minus',        'pfShyftAna/eleEB_minus',  'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'jetEt'],
    
##    ##JES
##    ['pfShyftAnaJES095/eleEB_minus',  'pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'jetEt'],
##    ['pfShyftAnaJES105/eleEB_minus',  'pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'jetEt'],
    
##    ##BTagging
##    ['pfShyftAnaReweightedBTag080/eleEB_minus', 'pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'jetEt'],
##    ['pfShyftAnaReweightedBTag090/eleEB_minus', 'pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'jetEt'],
##    ['pfShyftAnaReweightedBTag110/eleEB_minus', 'pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'jetEt'],
##    ['pfShyftAnaReweightedBTag120/eleEB_minus', 'pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag080/eleEB_minus','pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag090/eleEB_minus','pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag110/eleEB_minus','pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag120/eleEB_minus','pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'jetEt'],
    
##    ## systematics (JER, jetEt resolution, elePt in EE on resolution)
##    ['pfShyftAnaJER000/eleEB_minus',           'pfShyftAna/eleEB_minus',  'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'jetEt'],
##    ['pfShyftAnaJER020/eleEB_minus',           'pfShyftAna/eleEB_minus',  'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'jetEt'],
##    ['pfShyftAnaMETRES090/eleEB_minus',        'pfShyftAna/eleEB_minus',  'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'jetEt'],
##    ['pfShyftAnaMETRES110/eleEB_minus',        'pfShyftAna/eleEB_minus',  'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'jetEt'],
        
###___________________________________EE plus___________________________________________________________

##    ['pfShyftAna/eleEE_plus',        'pfShyftAna/eleEE_plus',     'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'jetEt'],
    
##    ##JES
##    ['pfShyftAnaJES095/eleEE_plus',  'pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'jetEt'],
##    ['pfShyftAnaJES105/eleEE_plus',  'pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'jetEt'],
    
##    ##BTagging
##    ['pfShyftAnaReweightedBTag080/eleEE_plus', 'pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'jetEt'],
##    ['pfShyftAnaReweightedBTag090/eleEE_plus', 'pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'jetEt'],
##    ['pfShyftAnaReweightedBTag110/eleEE_plus', 'pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'jetEt'],
##    ['pfShyftAnaReweightedBTag120/eleEE_plus', 'pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag080/eleEE_plus','pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag090/eleEE_plus','pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag110/eleEE_plus','pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag120/eleEE_plus','pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'jetEt'],
    
##    ## systematics (JER, jetEt resolution, elePt in EE on resolution)
##    ['pfShyftAnaJER000/eleEE_plus',           'pfShyftAna/eleEE_plus',  'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'jetEt'],
##    ['pfShyftAnaJER020/eleEE_plus',           'pfShyftAna/eleEE_plus',  'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'jetEt'],
##    ['pfShyftAnaMETRES090/eleEE_plus',        'pfShyftAna/eleEE_plus',  'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'jetEt'],
##    ['pfShyftAnaMETRES110/eleEE_plus',        'pfShyftAna/eleEE_plus',  'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'jetEt'],


#####___________________________________EE minus___________________________________________________________

##    ['pfShyftAna/eleEE_minus',        'pfShyftAna/eleEE_minus',  'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'jetEt'],
    
##    ##JES
##    ['pfShyftAnaJES095/eleEE_minus',  'pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'jetEt'],
##    ['pfShyftAnaJES105/eleEE_minus',  'pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'jetEt'],
    
##    ##BTagging
##    ['pfShyftAnaReweightedBTag080/eleEE_minus', 'pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'jetEt'],
##    ['pfShyftAnaReweightedBTag090/eleEE_minus', 'pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'jetEt'],
##    ['pfShyftAnaReweightedBTag110/eleEE_minus', 'pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'jetEt'],
##    ['pfShyftAnaReweightedBTag120/eleEE_minus', 'pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag080/eleEE_minus','pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag090/eleEE_minus','pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag110/eleEE_minus','pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'jetEt'],
##    ['pfShyftAnaReweightedLFTag120/eleEE_minus','pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'jetEt'],
    
##    ## systematics (JER, jetEt resolution, elePt in EE on resolution)
##    ['pfShyftAnaJER000/eleEE_minus',           'pfShyftAna/eleEE_minus',  'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'jetEt'],
##    ['pfShyftAnaJER020/eleEE_minus',           'pfShyftAna/eleEE_minus',  'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'jetEt'],
##    ['pfShyftAnaMETRES090/eleEE_minus',        'pfShyftAna/eleEE_minus',  'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'jetEt'],
##    ['pfShyftAnaMETRES110/eleEE_minus',        'pfShyftAna/eleEE_minus',  'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'jetEt'],


###_________________________________________
##                Using Centrality as 0-tag    
###________________________________________
    

    
######___________________________________NULL(All regions combined)___________________________________________________________

    ['pfShyftAna',        'pfShyftAna',     'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'Central'],
    
    ##JES
    ['pfShyftAnaJES095',  'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'Central'],
    ['pfShyftAnaJES105',  'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'Central'],
    
    ##BTagging
    ['pfShyftAnaReweightedBTag080', 'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'Central'],
    ['pfShyftAnaReweightedBTag090', 'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'Central'],
    ['pfShyftAnaReweightedBTag110', 'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'Central'],
    ['pfShyftAnaReweightedBTag120', 'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'Central'],
    ['pfShyftAnaReweightedLFTag080','pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'Central'],
    ['pfShyftAnaReweightedLFTag090','pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'Central'],
    ['pfShyftAnaReweightedLFTag110','pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'Central'],
    ['pfShyftAnaReweightedLFTag120','pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'Central'],
    
    ## systematics (JER, JES resolution, elePt in EE on resolution)
    ['pfShyftAnaJER000',          'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'Central'],
    ['pfShyftAnaJER020',          'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'Central'],
    ['pfShyftAnaMETRES090',     'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'Central'],
    ['pfShyftAnaMETRES110',     'pfShyftAna', 'All', 'qcd_NULL_772.root', 'pfShyftAnaMC', 'Central'],
    
######___________________________________EB plus___________________________________________________________

      ['pfShyftAna/eleEB_plus',        'pfShyftAna/eleEB_plus',     'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'Central'],
    
    ##JES
    ['pfShyftAnaJES095/eleEB_plus',  'pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'Central'],
    ['pfShyftAnaJES105/eleEB_plus',  'pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'Central'],
    
    ##BTagging
    ['pfShyftAnaReweightedBTag080/eleEB_plus', 'pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'Central'],
    ['pfShyftAnaReweightedBTag090/eleEB_plus', 'pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'Central'],
    ['pfShyftAnaReweightedBTag110/eleEB_plus', 'pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'Central'],
    ['pfShyftAnaReweightedBTag120/eleEB_plus', 'pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'Central'],
    ['pfShyftAnaReweightedLFTag080/eleEB_plus','pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'Central'],
    ['pfShyftAnaReweightedLFTag090/eleEB_plus','pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'Central'],
    ['pfShyftAnaReweightedLFTag110/eleEB_plus','pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'Central'],
    ['pfShyftAnaReweightedLFTag120/eleEB_plus','pfShyftAna/eleEB_plus', 'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'Central'],
    
    ## systematics (JER, JES resolution, elePt in EE on resolution)
    ['pfShyftAnaJER000/eleEB_plus',           'pfShyftAna/eleEB_plus',  'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'Central'],
    ['pfShyftAnaJER020/eleEB_plus',           'pfShyftAna/eleEB_plus',  'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'Central'],
    ['pfShyftAnaMETRES090/eleEB_plus',        'pfShyftAna/eleEB_plus',  'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'Central'],
    ['pfShyftAnaMETRES110/eleEB_plus',        'pfShyftAna/eleEB_plus',  'EB', 'qcd_eleEB_plus_772.root', 'pfShyftAnaMC/eleEB_plus', 'Central'],


#########___________________________________EB minus___________________________________________________________

    ['pfShyftAna/eleEB_minus',        'pfShyftAna/eleEB_minus',  'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'Central'],
    
    ##JES
    ['pfShyftAnaJES095/eleEB_minus',  'pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'Central'],
    ['pfShyftAnaJES105/eleEB_minus',  'pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'Central'],
    
    ##BTagging
    ['pfShyftAnaReweightedBTag080/eleEB_minus', 'pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'Central'],
    ['pfShyftAnaReweightedBTag090/eleEB_minus', 'pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'Central'],
    ['pfShyftAnaReweightedBTag110/eleEB_minus', 'pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'Central'],
    ['pfShyftAnaReweightedBTag120/eleEB_minus', 'pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'Central'],
    ['pfShyftAnaReweightedLFTag080/eleEB_minus','pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'Central'],
    ['pfShyftAnaReweightedLFTag090/eleEB_minus','pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'Central'],
    ['pfShyftAnaReweightedLFTag110/eleEB_minus','pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'Central'],
    ['pfShyftAnaReweightedLFTag120/eleEB_minus','pfShyftAna/eleEB_minus', 'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'Central'],
    
    ## systematics (JER, JES resolution, elePt in EE on resolution)
    ['pfShyftAnaJER000/eleEB_minus',           'pfShyftAna/eleEB_minus',  'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'Central'],
    ['pfShyftAnaJER020/eleEB_minus',           'pfShyftAna/eleEB_minus',  'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'Central'],
    ['pfShyftAnaMETRES090/eleEB_minus',        'pfShyftAna/eleEB_minus',  'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'Central'],
    ['pfShyftAnaMETRES110/eleEB_minus',        'pfShyftAna/eleEB_minus',  'EB', 'qcd_eleEB_minus_772.root', 'pfShyftAnaMC/eleEB_minus', 'Central'],
        
######___________________________________EE plus___________________________________________________________

    ['pfShyftAna/eleEE_plus',        'pfShyftAna/eleEE_plus',     'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'Central'],
    
    ##JES
    ['pfShyftAnaJES095/eleEE_plus',  'pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'Central'],
    ['pfShyftAnaJES105/eleEE_plus',  'pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'Central'],
    
    ##BTagging
    ['pfShyftAnaReweightedBTag080/eleEE_plus', 'pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'Central'],
    ['pfShyftAnaReweightedBTag090/eleEE_plus', 'pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'Central'],
    ['pfShyftAnaReweightedBTag110/eleEE_plus', 'pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'Central'],
    ['pfShyftAnaReweightedBTag120/eleEE_plus', 'pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'Central'],
    ['pfShyftAnaReweightedLFTag080/eleEE_plus','pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'Central'],
    ['pfShyftAnaReweightedLFTag090/eleEE_plus','pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'Central'],
    ['pfShyftAnaReweightedLFTag110/eleEE_plus','pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'Central'],
    ['pfShyftAnaReweightedLFTag120/eleEE_plus','pfShyftAna/eleEE_plus', 'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'Central'],
    
    ## systematics (JER, JES resolution, elePt in EE on resolution)
    ['pfShyftAnaJER000/eleEE_plus',           'pfShyftAna/eleEE_plus',  'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'Central'],
    ['pfShyftAnaJER020/eleEE_plus',           'pfShyftAna/eleEE_plus',  'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'Central'],
    ['pfShyftAnaMETRES090/eleEE_plus',        'pfShyftAna/eleEE_plus',  'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'Central'],
    ['pfShyftAnaMETRES110/eleEE_plus',        'pfShyftAna/eleEE_plus',  'EE', 'qcd_eleEE_plus_772.root', 'pfShyftAnaMC/eleEE_plus', 'Central'],


#####___________________________________EE minus___________________________________________________________

    ['pfShyftAna/eleEE_minus',        'pfShyftAna/eleEE_minus',  'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'Central'],
    
    ##JES
    ['pfShyftAnaJES095/eleEE_minus',  'pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'Central'],
    ['pfShyftAnaJES105/eleEE_minus',  'pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'Central'],
    
    ##BTagging
    ['pfShyftAnaReweightedBTag080/eleEE_minus', 'pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'Central'],
    ['pfShyftAnaReweightedBTag090/eleEE_minus', 'pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'Central'],
    ['pfShyftAnaReweightedBTag110/eleEE_minus', 'pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'Central'],
    ['pfShyftAnaReweightedBTag120/eleEE_minus', 'pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'Central'],
    ['pfShyftAnaReweightedLFTag080/eleEE_minus','pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'Central'],
    ['pfShyftAnaReweightedLFTag090/eleEE_minus','pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'Central'],
    ['pfShyftAnaReweightedLFTag110/eleEE_minus','pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'Central'],
    ['pfShyftAnaReweightedLFTag120/eleEE_minus','pfShyftAna/eleEE_minus', 'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'Central'],
    
    ## systematics (JER, JES resolution, elePt in EE on resolution)
    ['pfShyftAnaJER000/eleEE_minus',           'pfShyftAna/eleEE_minus',  'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'Central'],
    ['pfShyftAnaJER020/eleEE_minus',           'pfShyftAna/eleEE_minus',  'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'Central'],
    ['pfShyftAnaMETRES090/eleEE_minus',        'pfShyftAna/eleEE_minus',  'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'Central'],
    ['pfShyftAnaMETRES110/eleEE_minus',        'pfShyftAna/eleEE_minus',  'EE', 'qcd_eleEE_minus_772.root', 'pfShyftAnaMC/eleEE_minus', 'Central'],
          
     ]
command = 'python combineBackgroundPlots_met.py --input=415_v7 --mcDir={0:s} --dataDir={1:s} --outputLabel={2:s} --dataQCDFile={3:s} --templateDir={4:s} --var0tag={5:s} '

    
for option in options :
    
    s = command.format(
        option[0], option[1], option[2], option[3], option[4], option[5]
        )
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo %s"%s,""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)

    subprocess.call( [s, ""], shell=True )    
