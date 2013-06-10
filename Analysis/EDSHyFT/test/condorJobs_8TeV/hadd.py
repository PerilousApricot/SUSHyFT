#!/bin/python

import subprocess
import os

path='/uscms_data/d2/skhalil/BPrimeNtuples_8TeV/Nov24/'

ntuples = [
    ['nominal'],
    ['BTagSFdown'],
    ['BTagSFup'],
    ['JERdown'],
    ['JERup'],
    ['JESdown'],
    ['JESup'],
    ]

for ntuple in ntuples :
    sample = ntuple[0]
    s1 = 'hadd TTJets_MassiveBinDECAY_'+sample+'.root '  + path+'TTJets_MassiveBinDECAY_*_'+sample+'.root'
    print s1
    #subprocess.call( [s1], shell=True )
    s2 = 'hadd DYJetsToLL_M-50_'+sample+'.root '  + path+'DYJetsToLL_M-50_*_'+sample+'.root'
    print s2
    #subprocess.call( [s2], shell=True )
    s3 = 'hadd WJetsToLNu_v1_'+sample+'.root '  + path+'WJetsToLNu_v1_*_'+sample+'.root'
    print s3
    #subprocess.call( [s3], shell=True )
    s4 = 'hadd WJetsToLNu_v2_'+sample+'.root '  + path+'WJetsToLNu_v2_*_'+sample+'.root'
    print s4
    #subprocess.call( [s4], shell=True )
