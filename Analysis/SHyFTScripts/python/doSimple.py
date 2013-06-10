#!/bin/python

import subprocess

options = [
       #['nPrimVertices', '1', '20']	
       ['nJets',   '1', '6'],
##     ['nTags',   '1', '3'],		
##     ['m3',      '2', '600'],	
##     ['m3_2t',   '2', '600'],
##     ['m3_1t',   '2', '600'],
##     ['m3_0t',   '2', '600'],
##     ['jet1Pt',  '4', '300'],	
##     ['jet2Pt',  '3', '300'],
##     ['jet3Pt',  '3', '300'],	
##     ['jet4Pt',  '3', '300'],
##     ['discriminator', '1', '8'],
##     ['jet4Mass',  '1', '40'],
##	['jet4Phi',  '2', '40'],	
##     ['lepRelIso','1', '1'],#useless idiot plot because of stupid binning :(
	#['lepEta', '1', '1']
#	['lepPhi', '1', '1']
	#['lepJetdR', '1', '1']
    ]

command = 'python simple.py --var={0:s} --rebin={1:s} --nBin={2:s} --verbose'

for option in options :
        s = command.format(
		option[0], option[1], option[2]
		)
		
	print '--------------------------------------------------------------------------'
	print s
	print '--------------------------------------------------------------------------'
	subprocess.call( [s, ""], shell=True )
	
##options = [
##     ['3', '1', '3', '2', 'NULL', 'm3_2t', '2', 'pfShyftAna', 'pfShyftAnaQCDWP95', 'plots'],
##    ]

##command = 'python magic_fit.py --minJets={0:s} --minTags={1:s} --maxJet={2:s} --maxTag={3:s} --subDir={4:s} --var={5:s} --rebin={6:s} --templateDir={7:s} --qcdDir={8:s} --outputDir={9:s} --simple'

##for option in options :
##        s = command.format(
##		option[0], option[1], option[2], option[3], option[4], option[5],
##                option[6], option[7], option[8], option[9]
##		)

