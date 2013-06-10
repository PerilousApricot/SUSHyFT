#! /usr/bin/env python


from optparse import OptionParser

# Create a command line option parser
parser = OptionParser()


# Option to use MC
parser.add_option('--doMC', action='store_true',
                  default=False,
                  dest='doMC',
                  help='use MC')

parser.add_option("--inputDir", action='store',
                  default=None,
                  dest='inputDir',
                  help='Input directory to find files')

parser.add_option("--inputFiles", action='store',
                  default="input_files.txt",
                  dest="inputFiles",
                  help="Text file containing list of files you want to process")

parser.add_option("--outputFile", action='store',
                  default="plots.root",
                  dest="outputFile",
                  help="Output file name")

# Parse and get arguments
(options, args) = parser.parse_args()

# This is needed so that ROOT is happy after we played with the
# command line arguments
argv = []

# Import everything from ROOT
import ROOT
import sys

# Import what we need from FWLite
from DataFormats.FWLite import Events, Handle

# Read the input file
# Add the files in the input file
infile = open( options.inputFiles )
allInputFiles = infile.readlines()
files = []
for ifile in allInputFiles :
    if options.inputDir is not None:
        s = options.inputDir + '/' + ifile 
    else :
        s = ifile    
    files.append(s.rstrip() ) # make sure to remove trailing whitespace

# Print it out
print 'Processing files '
for ifile in files :
    print ifile

# Get the FWLite "Events"
events = Events (files)

# Get a "handle" (i.e. a smart pointer) to the vector of jets
jetsH  = Handle ("std::vector<pat::Jet>")

# Get the label we assigned to our vector of jets
jetsLabel = ("pfShyftSkim", "jets")


# Create an output file and a histogram 
f = ROOT.TFile(options.outputFile, "RECREATE")
f.cd()
secvtxMass = ROOT.TH1F("secvtxMass","secvtxMass",   100, 0.0,  10.0 )



# Keep some timing information
nEventsAnalyzed = 0
timer = ROOT.TStopwatch()
timer.Start()


# loop over events
i = 0
for event in events:
    i = i + 1
    if i % 1000 == 0 :
        print i
    nEventsAnalyzed = nEventsAnalyzed + 1

    # Get the jets "by label" from label "jetsLabel", and put them into "jetsH"
    event.getByLabel (jetsLabel,  jetsH)
    # Get the "product" of the handle (i.e. what it's "pointing to" in C++)
    jets = jetsH.product()
    
    # Now loop over the jets, and store the secondary vertex mass.
    # Here, we've pre-stored the mass with a "user-defined" variable in the pat::Jet, called "secvtxMass"
    for jet in jets :
        mass =jet.userFloat('secvtxMass')
        secvtxMass.Fill( mass )

# Done processing the events!


# Stop our timer
timer.Stop()

# Print out our timing information
rtime = timer.RealTime(); # Real time (or "wall time")
ctime = timer.CpuTime(); # CPU time
print("Analyzed events: {0:6d}").format(nEventsAnalyzed);
print("RealTime={0:6.2f} seconds, CpuTime={1:6.2f} seconds").format(rtime,ctime)
print("{0:4.2f} events / RealTime second .").format( nEventsAnalyzed/rtime)
print("{0:4.2f} events / CpuTime second .").format( nEventsAnalyzed/ctime)

# "cd" to our output file
f.cd()

# Write our histogram
secvtxMass.Write()

# Close it
f.Close()
