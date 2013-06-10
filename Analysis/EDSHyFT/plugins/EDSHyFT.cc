#ifndef EDSHyFT_h
#define EDSHyFT_h


#include "Analysis/SHyFT/interface/SHyFT.h"
#include "PhysicsTools/UtilAlgos/interface/EDAnalyzerWrapper.h"
#include "PhysicsTools/UtilAlgos/interface/FWLiteFilterWrapper.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "Analysis/EDSHyFT/plugins/EDMuonInJetSelector.h"
#include "Analysis/EDSHyFT/plugins/EDWPlusJetsSelector.h"

typedef edm::AnalyzerWrapper<SHyFT> EDSHyFT;
//typedef edm::FWLiteFilterWrapper<SHyFTSelector> EDWPlusJets;


DEFINE_FWK_MODULE(EDSHyFT);
//DEFINE_FWK_MODULE(EDWPlusJets);

#endif
