#ifndef BoostedParticles_h
#define BoostedParticles_h

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include <vector>

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Particle.h"

typedef reco::Candidate::PolarLorentzVector LorentzV;
typedef std::vector< LorentzV > p4_vector;

class BoostedParticles : public edm::EDProducer {
   public:
      explicit BoostedParticles(const edm::ParameterSet& cfg);
      ~BoostedParticles();
   private:
      virtual void beginJob(const edm::EventSetup&) ;
      virtual void produce(edm::Event& event, const edm::EventSetup& setup);
      virtual void endJob() ;
      void  topDecay(const reco::Candidate* bprimes, int numTopDau, int di,  
                     const reco::Candidate* &TtoWtoLep, const reco::Candidate* &TtoWtoHad, 
                     const reco::Candidate* &Ttob);
      void setPointers(std::vector<const reco::Candidate *> decayList);
      //bool pick_bZtW_;
      // ----------member data ---------------------------
   protected:
      
};

#endif

BoostedParticles::BoostedParticles(const edm::ParameterSet& cfg)//:
   //pick_bZtW_(cfg.getParameter<bool>("pick_bZtW"))
{  
   //register the products
    
   //leptonic side of b'->tW->tlnu
   produces< LorentzV > ("Lep1");
   produces< LorentzV > ("Nu1");
   produces< LorentzV > ("LepT1");
   produces< LorentzV > ("Lep2");
   produces< LorentzV > ("Nu2");
   produces< LorentzV > ("LepT2");
   //P4 of W and b from a t decay: t->Wb->(lnub, qqb)
   produces< LorentzV > ("LepT1toWtoLep");
   produces< LorentzV > ("LepT1toWtoHad");
   produces< LorentzV > ("LepT1tob");
   produces< LorentzV > ("LepT2toWtoLep");
   produces< LorentzV > ("LepT2toWtoHad");
   produces< LorentzV > ("LepT2tob");
   //hadronic side of b'->tW->tqq
   produces< LorentzV > ("WPart1");
   produces< LorentzV > ("WPart2");
   produces< LorentzV > ("HadT1");
   produces< LorentzV > ("WPart3");
   produces< LorentzV > ("WPart4");
   produces< LorentzV > ("HadT2");
   //P4 of W and b from a t decay: t->Wb->(lnub, qqb)
   produces< LorentzV > ("HadT1toWtoLep");
   produces< LorentzV > ("HadT1toWtoHad");
   produces< LorentzV > ("HadT1tob");
   produces< LorentzV > ("HadT2toWtoLep");
   produces< LorentzV > ("HadT2toWtoHad");
   produces< LorentzV > ("HadT2tob");
   //leptonic side of b'->bZ->bll
   produces< LorentzV > ("ZLep1");
   produces< LorentzV > ("ZLep2");
   produces< LorentzV > ("LepB1");
   produces< LorentzV > ("ZLep3");
   produces< LorentzV > ("ZLep4");
   produces< LorentzV > ("LepB2");
   //hadronic side of b'->bZ->bqq
   produces< LorentzV > ("ZPart1");
   produces< LorentzV > ("ZPart2");
   produces< LorentzV > ("HadB1");
   produces< LorentzV > ("ZPart3");
   produces< LorentzV > ("ZPart4");
   produces< LorentzV > ("HadB2");
   //event configuration of b'b'->tWtW
   produces<int> ("WtWtTolnutlnut"); 
   produces<int> ("WtWtToqqtqqt");
   produces<int> ("WtWtToluntqqt"); 
   produces<int> ("BBtoWtWt"); 
   //event configuration of b'b'->bZbZ
   produces<int> ("ZbZbTollbllb"); 
   produces<int> ("ZbZbToqqbqqb");
   produces<int> ("ZbZbTollbqqb"); 
   produces<int> ("BBtoZbZb");
   //event configuration of b'b'->bZtW
   produces<int> ("WtZbTolnutllb"); 
   produces<int> ("WtZbTolnutqqb");
   produces<int> ("WtZbToqqtllb"); 
   produces<int> ("WtZbToqqtqqb");
   produces<int> ("BBtoWtZb");
}


BoostedParticles::~BoostedParticles()
{
}

// ------------ method called once each job just before starting event loop  ------------
void BoostedParticles::beginJob(const edm::EventSetup&)
{
}

// ------------ method called once each job just after ending the event loop  ------------
void BoostedParticles::endJob() {
 std::cout << "----------------------------------------------------------------------------------------" << std::endl;
 std::cout << "So long, and thanks for all the fish..." << std::endl;
 std::cout << "----------------------------------------------------------------------------------------" << std::endl;
}
