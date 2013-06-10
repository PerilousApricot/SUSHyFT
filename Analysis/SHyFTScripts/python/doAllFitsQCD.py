#!/bin/python

##The fit script, magic_ft.py writes a .txt files
##that one need to propagate to 'getNormalizedQCD.py
##The script 'getNormalizedQCD.py', produces a normalized
##QCD root file to be read by combineBackgrounds_met.py

import subprocess


options = [

###Starting from here: ALL
##########################	
	
        ['1', '0', 'NULL', 'MET', '2', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
	['2', '0', 'NULL', 'MET', '2', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
	['3', '0', 'NULL', 'MET', '2', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
	['4', '0', 'NULL', 'MET', '2', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
	['5', '0', 'NULL', 'MET', '4', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],

	['1', '1', 'NULL', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
	['2', '1', 'NULL', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
	['3', '1', 'NULL', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
	['4', '1', 'NULL', 'MET', '2', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
	['5', '1', 'NULL', 'MET', '4', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
	
	['2', '2', 'NULL', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
	['3', '2', 'NULL', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
	['4', '2', 'NULL', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
	['5', '2', 'NULL', 'MET', '4', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],


#######	#EB_plus------------------------------------------------------------------------------------

##	['1', '0', 'eleEB_plus', 'MET', '2', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['2', '0', 'eleEB_plus', 'MET', '2', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['3', '0', 'eleEB_plus', 'MET', '2', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['4', '0', 'eleEB_plus', 'MET', '3', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['5', '0', 'eleEB_plus', 'MET', '4', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],

##	['1', '1', 'eleEB_plus', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['2', '1', 'eleEB_plus', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['3', '1', 'eleEB_plus', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['4', '1', 'eleEB_plus', 'MET', '2', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['5', '1', 'eleEB_plus', 'MET', '4', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
	
##	['2', '2', 'eleEB_plus', 'MET', '3', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['3', '2', 'eleEB_plus', 'MET', '3', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['4', '2', 'eleEB_plus', 'MET', '3', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['5', '2', 'eleEB_plus', 'MET', '5', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
	
######	#EB_minus------------------------------------------------------------------------------------

##	['1', '0', 'eleEB_minus', 'MET', '2', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['2', '0', 'eleEB_minus', 'MET', '2', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['3', '0', 'eleEB_minus', 'MET', '2', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['4', '0', 'eleEB_minus', 'MET', '2', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['5', '0', 'eleEB_minus', 'MET', '4', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],

##	['1', '1', 'eleEB_minus', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['2', '1', 'eleEB_minus', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['3', '1', 'eleEB_minus', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['4', '1', 'eleEB_minus', 'MET', '2', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['5', '1', 'eleEB_minus', 'MET', '4', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
	
##	['2', '2', 'eleEB_minus', 'MET', '3', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['3', '2', 'eleEB_minus', 'MET', '5', '130', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['4', '2', 'eleEB_minus', 'MET', '3', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['5', '2', 'eleEB_minus', 'MET', '7', '170', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],

######	#EE_plus------------------------------------------------------------------------------------

##	['1', '0', 'eleEE_plus', 'MET', '3', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['2', '0', 'eleEE_plus', 'MET', '2', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['3', '0', 'eleEE_plus', 'MET', '4', '170', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['4', '0', 'eleEE_plus', 'MET', '5', '100', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['5', '0', 'eleEE_plus', 'MET', '5', '120', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],

##	['1', '1', 'eleEE_plus', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['2', '1', 'eleEE_plus', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['3', '1', 'eleEE_plus', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['4', '1', 'eleEE_plus', 'MET', '2', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['5', '1', 'eleEE_plus', 'MET', '4', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
	
##	['2', '2', 'eleEE_plus', 'MET', '4', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['3', '2', 'eleEE_plus', 'MET', '4', '100', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['4', '2', 'eleEE_plus', 'MET', '4', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['5', '2', 'eleEE_plus', 'MET', '10', '80', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],##Giveup and forced to 0 if fit fails
	
########	#EE_minus------------------------------------------------------------------------------------

##	['1', '0', 'eleEE_minus', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['2', '0', 'eleEE_minus', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['3', '0', 'eleEE_minus', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['4', '0', 'eleEE_minus', 'MET', '3', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['5', '0', 'eleEE_minus', 'MET', '4', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],

##	['1', '1', 'eleEE_minus', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['2', '1', 'eleEE_minus', 'MET', '2', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['3', '1', 'eleEE_minus', 'MET', '4', '150', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['4', '1', 'eleEE_minus', 'MET', '4', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['5', '1', 'eleEE_minus', 'MET', '4', '200', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
	
##	['2', '2', 'eleEE_minus', 'MET', '4', '20', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',], ##Giveup and forced to 0 if fit fails
##	['3', '2', 'eleEE_minus', 'MET', '4', '100', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['4', '2', 'eleEE_minus', 'MET', '4', '100', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],
##	['5', '2', 'eleEE_minus', 'MET', '8', '170', 'pfShyftAnaNoMET', 'pfShyftAnaQCDWP95NoMET',],##Giveup and forced to 0 if fit fails

	]

command = 'python magic_fit.py --nJets={0:s} --nTags={1:s} --subDir={2:s} --var={3:s} --rebin={4:s} --fixBin={5:s} --templateDir={6:s} --qcdDir={7:s} --printTable=fitOut.txt --fit'

#command = 'python magic_fit.py --nJets={0:s} --nTags={1:s} --subDir={2:s} --var={3:s} --rebin={4:s} --templateDir={5:s} --qcdDir={6:s} --printTable=fitOut.txt --fit'

for option in options :
        s = command.format(
		option[0], option[1], option[2], option[3], option[4], option[5], option[6], option[7]
		)
	
	print '--------------------------------------------------------------------------'
	print s
	print '--------------------------------------------------------------------------'
	print '--------------------------------------------------------------------------'
	subprocess.call( [s, ""], shell=True )
