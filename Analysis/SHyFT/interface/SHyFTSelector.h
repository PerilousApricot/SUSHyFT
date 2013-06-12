#ifndef Analysis_SHyFT_interface_SHyFTSelector_h
#define Analysis_SHyFT_interface_SHyFTSelector_h

#include "PhysicsTools/SelectorUtils/interface/EventSelector.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "PhysicsTools/SelectorUtils/interface/ElectronVPlusJetsIDSelectionFunctor.h"
#include "PhysicsTools/SelectorUtils/interface/MuonVPlusJetsIDSelectionFunctor.h"
#include "PhysicsTools/SelectorUtils/interface/JetIDSelectionFunctor.h"
#include "PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h"
#include "PhysicsTools/SelectorUtils/interface/PVSelector.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Candidate/interface/ShallowClonePtrCandidate.h"
#include "Analysis/SHyFT/interface/TopElectronSelector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "RecoEgamma/EgammaIsolationAlgos/interface/EgammaTowerIsolation.h"
#include "PhysicsTools/SelectorUtils/interface/PFElectronSelector.h"
#include "PhysicsTools/SelectorUtils/interface/PFMuonSelector.h"

class SHyFTSelector : public EventSelector {
   public:
      SHyFTSelector() {}
      SHyFTSelector( edm::ParameterSet const & params );

      virtual void scaleJets(double scale) {jetScale_ = scale;}
  
      virtual bool operator()( edm::EventBase const & t, pat::strbitset & ret);
      using EventSelector::operator();

      std::vector<reco::ShallowClonePtrCandidate> const & allJets           () const { return allJets_;     } 
      //std::vector<reco::ShallowClonePtrCandidate> const & selectedJets      () const { return selectedJets_;     } 
      std::vector<reco::ShallowClonePtrCandidate> const & cleanedJets       () const { return cleanedJets_;      } 
      //std::vector<reco::ShallowClonePtrCandidate> const & oldElectrons      () const { return oldElectrons_;}
      std::vector<reco::ShallowClonePtrCandidate> const & selectedMuons     () const { return selectedMuons_;    }       
      reco::ShallowClonePtrCandidate const &              selectedMET       () const { return met_; }
      std::vector<reco::ShallowClonePtrCandidate> const & selectedElectrons () const { return selectedElectrons_; }
      std::vector<reco::ShallowClonePtrCandidate> const & selectedTaus () const { return selectedTaus_; }

      //std::vector<reco::ShallowClonePtrCandidate> const & selectedLooseElectrons() const { return selectedLooseElectrons_; }
      
      void printSelectors(std::ostream & out) const {
         out << "PV Selector: " << std::endl;
         pvSelector_.print(out);
         // out << "Muon ID Tight Selector: " << std::endl;
         //muonIdTight_.print(out);
         //out << "Muon ID Loose Selector: " << std::endl;
         //muonIdLoose_.print(out);
         out << "Electron ID Veto Selector: " << std::endl;
         electronIdVeto_.print(out);
         
      }
 
   protected: 

      edm::InputTag               muonTag_;
      edm::InputTag               electronTag_;
      edm::InputTag               jetTag_;
      edm::InputTag               metTag_;
      edm::InputTag               rhoTag_;
      edm::InputTag               rhoIsoTag_;
      edm::InputTag               trigTag_;
      edm::InputTag               tauTag_;

      std::string                 muTrig_;
      std::string                 eleTrig_;
      std::vector<std::string>    muTriggerList_;
      std::vector<std::string>    eleTriggerList_;
      std::vector<reco::ShallowClonePtrCandidate> allJets_;
      //std::vector<reco::ShallowClonePtrCandidate> selectedJets_;
      std::vector<reco::ShallowClonePtrCandidate> selectedElectrons_;
      std::vector<reco::ShallowClonePtrCandidate> allMuons_;
      std::vector<reco::ShallowClonePtrCandidate> selectedMuons_;
      //std::vector<reco::ShallowClonePtrCandidate> oldElectrons_;
      std::vector<reco::ShallowClonePtrCandidate> looseMuons_;
      std::vector<reco::ShallowClonePtrCandidate> allElectrons_;
      std::vector<reco::ShallowClonePtrCandidate> looseElectrons_;
      std::vector<reco::ShallowClonePtrCandidate> selectedMETs_;
      std::vector<reco::ShallowClonePtrCandidate> cleanedJets_;
      reco::ShallowClonePtrCandidate              met_;
      std::vector<reco::ShallowClonePtrCandidate> selectedLooseElectrons_;
      std::vector<reco::ShallowClonePtrCandidate> selectedLooseMuons_;
      std::vector<reco::ShallowClonePtrCandidate> allTaus_;
      std::vector<reco::ShallowClonePtrCandidate> selectedTaus_;

      PVSelector                           pvSelector_;
      PFMuonSelector                       muonIdTight_;
      PFMuonSelector                       muonIdLoose_;
      TopElectronSelector                  electronIdVeto_;
      TopElectronSelector                  electronIdTight_;
      
      int minJets_;
      double muJetDR_;
      double eleJetDR_;
      bool muPlusJets_;
      bool ePlusJets_;
      double muPtMin_  ;
      double muEtaMax_ ;
      double eleEtMin_ ;
      double eleEtaMax_;

      double tauPtMin_;
      double tauPtMax_;
      double tauEtaMax_;

      bool firstTime_;

      double muPtMinLoose_  ;
      double muEtaMaxLoose_ ;
      double eleEtMinLoose_ ;
      double eleEtaMaxLoose_;

      double jetPtMin_ ;
      double jetEtaMax_;

      double jetScale_;
      double jetUncertainty_; // "flat" uncertainty after the L2L3 uncertainty
      double jetSmear_;
      double unclMetScale_; 
      double ePtScale_;        
      double ePtUncertaintyEE_;

      index_type   inclusiveIndex_; 
      index_type   triggerIndex_;   
      index_type   pvIndex_;        
      index_type   lep1Index_;      
      index_type   lep2Index_;      
      index_type   lep3Index_;      
      index_type   lep4Index_;  
      index_type   conversionIndex_;
      index_type   dlepvetoIndex_;      
      index_type   zvetoIndex_;         
      index_type   metLowIndex_;  
      index_type   metHighIndex_;  
      index_type   wmtIndex_;
      index_type   cosmicIndex_;    
      index_type   jet1Index_;      
      index_type   jet2Index_;      
      index_type   jet3Index_;      
      index_type   jet4Index_;      
      index_type   jet5Index_;      
      index_type   jet6Index_;
      index_type   jet7Index_;
      index_type   jet8Index_;
      index_type   jet9Index_;

      double         eRelIso_;
      double         muRelIso_;
      double         eEt_;
      double         dxy_;
      edm::InputTag  pvTag_;
      bool           useData_;    
      bool           useNoPFIso_;      
      bool           useNoID_;   
     
      edm::InputTag pfEleSrc_;

      // Jet energy corrections object
      std::vector<std::string> jecPayloads_;
      boost::shared_ptr<JetCorrectionUncertainty> jecUnc_;
      boost::shared_ptr<FactorizedJetCorrector> jec_;
};


#endif
