# !/bin/python

import subprocess


crabFiles = [
['crab_DYJetsToLL_TuneD6T_M-50_7TeV-madgraph-tauola_shyft_387_v1.cfg', 'DYJetsToLL_TuneD6T_M-50_7TeV-madgraph-tauola_shyft_387_v1'],
['crab_QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_shyft_387_v1.cfg', 'QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_shyft_387_v1'],
['crab_TTJets_TuneD6T_7TeV-madgraph-tauola-tauola_shyft_387_v1.cfg', 'TTJets_TuneD6T_7TeV-madgraph-tauola_shyft_387_v1'],
['crab_TTJets_TuneD6T_largerISRFSR_7TeV-madgraph-tauola-tauola_shyft_387_v1.cfg', 'TTJets_TuneD6T_largerISRFSR_7TeV-madgraph-tauola_shyft_387_v1'],
['crab_TTJets_TuneD6T_matchingdown_7TeV-madgraph-tauola_shyft_387_v1.cfg', 'TTJets_TuneD6T_matchingdown_7TeV-madgraph-tauola_shyft_387_v1'],
['crab_TTJets_TuneD6T_matchingup_7TeV-madgraph-tauola_shyft_387_v1.cfg', 'TTJets_TuneD6T_matchingup_7TeV-madgraph-tauola_shyft_387_v1'],
['crab_TTJets_TuneD6T_scaledown_7TeV-madgraph-tauola_shyft_387_v1.cfg', 'TTJets_TuneD6T_scaledown_7TeV-madgraph-tauola_shyft_387_v1'],
['crab_TTJets_TuneD6T_scaleup_7TeV-madgraph-tauola_shyft_387_v1.cfg', 'TTJets_TuneD6T_scaleup_7TeV-madgraph-tauola_shyft_387_v1'],
['crab_TTJets_TuneD6T_smallerISRFSR_7TeV-madgraph-tauola_shyft_387_v1.cfg', 'TTJets_TuneD6T_smallerISRFSR_7TeV-madgraph-tauola_shyft_387_v1'],
['crab_TTJets_TuneZ2_7TeV-madgraph-tauola_shyft_387_v1.cfg', 'TTJets_TuneZ2_7TeV-madgraph-tauola_shyft_387_v1'],
['crab_TToBLNu_TuneZ2_s-channel_7TeV-madgraph_shyft_387_v1.cfg', 'TToBLNu_TuneZ2_s-channel_7TeV-madgraph_shyft_387_v1'],
['crab_TToBLNu_TuneZ2_t-channel_7TeV-madgraph_shyft_387_v1.cfg', 'TToBLNu_TuneZ2_t-channel_7TeV-madgraph_shyft_387_v1'],
['crab_TToBLNu_TuneZ2_tW-channel_7TeV-madgraph_shyft_387_v1.cfg', 'TToBLNu_TuneZ2_tW-channel_7TeV-madgraph_shyft_387_v1'],
['crab_VQQJetsToLL_TuneD6T_7TeV-madgraph-tauola_shyft_387_v1.cfg', 'VQQJetsToLL_TuneD6T_7TeV-madgraph-tauola_shyft_387_v1'],
['crab_VQQJetsToLL_TuneD6T_scaledown_7TeV-madgraph-tauola_shyft_387_v1.cfg', 'VQQJetsToLL_TuneD6T_scaledown_7TeV-madgraph-tauola_shyft_387_v1'],
['crab_VQQJetsToLL_TuneD6T_scaleup_7TeV-madgraph-tauola_shyft_387_v1.cfg', 'VQQJetsToLL_TuneD6T_scaleup_7TeV-madgraph-tauola_shyft_387_v1'],


    ]



for crabFile in crabFiles :
    s = 'crab -create -cfg ' + crabFile[0]
    print s
    subprocess.call( [s], shell=True )
    s = 'crab -submit -c ' + crabFile[1]
    print s
    subprocess.call( [s], shell=True )
