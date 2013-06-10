#!/bin/python

import subprocess


options = [
       #['3', '1', '5', '2', 'NULL', 'MET', '5', 'pfShyftAna', 'pfShyftAnaQCDWP95', 'plots'],
       #['3', '1', '5', '2', 'NULL', 'wMT', '5', 'pfShyftAna', 'pfShyftAnaQCDWP95', 'plots'],
       #['3', '1', '5', '2', 'NULL', 'secvtxMass', '5', 'pfShyftAna', 'pfShyftAnaQCDWP95', 'plots'],
       #['3', '1', '5', '2', 'NULL', 'hT', '5', 'pfShyftAna', 'pfShyftAnaQCDWP95', 'plots'],
       #['3', '1', '5', '2', 'NULL', 'lepPt', '5', 'pfShyftAna', 'pfShyftAnaQCDWP95', 'plots'],
       ['3', '1', '5', '2', 'NULL', 'lepEta', '1', 'pfShyftAna', 'pfShyftAnaQCDWP95', 'plots'],
       #['3', '1', '5', '2', 'NULL', 'jetEt', '5', 'pfShyftAna', 'pfShyftAnaQCDWP95', 'plots'],
       #['3', '1', '5', '2', 'NULL', 'Central', '5', 'pfShyftAna', 'pfShyftAnaQCDWP95', 'plots'],	
    ]

command = 'python magic_fit.py --minJets={0:s} --minTags={1:s} --maxJet={2:s} --maxTag={3:s} --subDir={4:s} --var={5:s} --rebin={6:s} --templateDir={7:s} --qcdDir={8:s} --outputDir={9:s} '


for option in options :
        s = command.format(
		option[0], option[1], option[2], option[3], option[4],
		option[5], option[6], option[7], option[8], option[9]
		)
	
	print '--------------------------------------------------------------------------'
	print s
	print '--------------------------------------------------------------------------'
	print '--------------------------------------------------------------------------'
	subprocess.call( [s, ""], shell=True )
