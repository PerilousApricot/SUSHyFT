#ifndef TprimeNtupleDumper_h
#define TprimeNtupleDumper_h

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include <vector>

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Particle.h"

class TprimeNtupleDumper : public edm::EDProducer {
public:
  explicit TprimeNtupleDumper(const edm::ParameterSet& cfg);
  ~TprimeNtupleDumper();
  
private:
  virtual void beginJob(const edm::EventSetup&) ;
  virtual void produce(edm::Event& event, const edm::EventSetup& setup);
  virtual void endJob() ;
  void findTop(edm::Handle<std::vector<reco::GenParticle> > &genParticleCollection, 
	       std::vector<const reco::Candidate*> &ttbarDecay);
  std::string kinFitterLabel_;
  std::string selectorLabel_;
  bool do_MC_;
  int resonanceId_; // 6 means Top, 8 means TPrime
};

#endif

TprimeNtupleDumper::~TprimeNtupleDumper(){
}

void TprimeNtupleDumper::beginJob(const edm::EventSetup&){
}

void TprimeNtupleDumper::endJob(){
}

TprimeNtupleDumper::TprimeNtupleDumper(const edm::ParameterSet& cfg):
  kinFitterLabel_(cfg.getParameter<std::string>("kinFitterLabel")),
  selectorLabel_(cfg.getParameter<std::string>("selectorLabel")),
  do_MC_(cfg.getParameter<bool>("do_MC")),
  resonanceId_(cfg.getParameter<int>("resonanceId"))
{
  produces<double>("fitMass");
  produces<double>("TTMass");
  produces<double>("fitChi2");

  produces<double>("TopLepPt");
  produces<double>("TopHadPt");
  if(do_MC_){
    produces<double>("MCTopLepPt");
    produces<double>("MCTopHadPt");
    produces<double>("MCTopLepMass");
    produces<double>("MCTopHadMass");
    
    produces<double>("MCLeptonPt");
    produces<double>("MCLetonpEta");
    produces<double>("MCLeptonPhi");
    
    produces<double>("MCNuPt");
    produces<double>("MCNuEta");
    produces<double>("MCNuPhi");
    
    produces<double>("MCLepBPt");
    produces<double>("MCLepBEta");
    produces<double>("MCLepBPhi");
    
    produces<double>("MCHadBPt");
    produces<double>("MCHadBEta");
    produces<double>("MCHadBPhi");
    
    produces<double>("MCWPart1Pt");
    produces<double>("MCWPart1Eta");
    produces<double>("MCWPart1Phi");
    
    produces<double>("MCWPart2Pt");
    produces<double>("MCWPart2Eta");
    produces<double>("MCWPart2Phi");
  }
  //produces<int>("nJets");
}

void TprimeNtupleDumper::produce(edm::Event& event, const edm::EventSetup& setup){
  std::auto_ptr<double> pfitMass ( new double(0.0) );
  std::auto_ptr<double> pTTMass  ( new double(0.0) );
  std::auto_ptr<double> pfitChi2 ( new double(-1.0) );
   
  std::auto_ptr<double> pTopLepPt ( new double(-10.0) );
  std::auto_ptr<double> pTopHadPt ( new double(-10.0) );
  std::auto_ptr<double> pMCTopLepPt ( new double(-10.0) );
  std::auto_ptr<double> pMCTopHadPt ( new double(-10.0) );
  std::auto_ptr<double> pMCTopLepMass ( new double(-10.0) );
  std::auto_ptr<double> pMCTopHadMass ( new double(-10.0) );

  std::auto_ptr<double> pMCLeptonPt ( new double(-10.0) );
  std::auto_ptr<double> pMCLetonpEta ( new double(-10.0) );
  std::auto_ptr<double> pMCLeptonPhi ( new double(-10.0) );

  std::auto_ptr<double> pMCNuPt ( new double(-10.0) );
  std::auto_ptr<double> pMCNuEta ( new double(-10.0) );
  std::auto_ptr<double> pMCNuPhi ( new double(-10.0) );

  std::auto_ptr<double> pMCLepBPt ( new double(-10.0) );
  std::auto_ptr<double> pMCLepBEta ( new double(-10.0) );
  std::auto_ptr<double> pMCLepBPhi ( new double(-10.0) );

  std::auto_ptr<double> pMCHadBPt ( new double(-10.0) );
  std::auto_ptr<double> pMCHadBEta ( new double(-10.0) );
  std::auto_ptr<double> pMCHadBPhi ( new double(-10.0) );

  std::auto_ptr<double> pMCWPart1Pt ( new double(-10.0) );
  std::auto_ptr<double> pMCWPart1Eta ( new double(-10.0) );
  std::auto_ptr<double> pMCWPart1Phi ( new double(-10.0) );

  std::auto_ptr<double> pMCWPart2Pt ( new double(-10.0) );
  std::auto_ptr<double> pMCWPart2Eta ( new double(-10.0) );
  std::auto_ptr<double> pMCWPart2Phi ( new double(-10.0) );


  // deal with GenParticles
  std::vector<const reco::Candidate*> ttbarDecay;
  //resonanceId_=6; // comes from cfg
  if(do_MC_){
    edm::Handle<std::vector<reco::GenParticle> > genParticleCollection;
    event.getByLabel(edm::InputTag("prunedGenParticles"), genParticleCollection);  
    findTop(genParticleCollection, ttbarDecay);
    if(ttbarDecay.size()==6){
      // store MC truth information
      *pMCLeptonPt = ttbarDecay[0]->p4().Pt();
      *pMCLetonpEta = ttbarDecay[0]->p4().Eta();
      *pMCLeptonPhi = ttbarDecay[0]->p4().Phi();
      
      *pMCNuPt = ttbarDecay[1]->p4().Pt();
      *pMCNuEta = ttbarDecay[1]->p4().Eta();
      *pMCNuPhi = ttbarDecay[1]->p4().Phi();
      
      *pMCLepBPt = ttbarDecay[2]->p4().Pt();
      *pMCLepBEta = ttbarDecay[2]->p4().Eta();
      *pMCLepBPhi = ttbarDecay[2]->p4().Phi();
      
      *pMCHadBPt = ttbarDecay[3]->p4().Pt();
      *pMCHadBEta = ttbarDecay[3]->p4().Eta();
      *pMCHadBPhi = ttbarDecay[3]->p4().Phi();
      
      *pMCWPart1Pt = ttbarDecay[4]->p4().Pt();
      *pMCWPart1Eta = ttbarDecay[4]->p4().Eta();
      *pMCWPart1Phi = ttbarDecay[4]->p4().Phi();
      
      *pMCWPart2Pt = ttbarDecay[5]->p4().Pt();
      *pMCWPart2Eta = ttbarDecay[5]->p4().Eta();
      *pMCWPart2Phi = ttbarDecay[5]->p4().Phi();
      
      reco::Candidate::LorentzVector MCvect4 = ttbarDecay[0]->p4();
      MCvect4 += ttbarDecay[1]->p4();
      MCvect4 += ttbarDecay[2]->p4();
      *pMCTopLepPt = MCvect4.Pt();
      *pMCTopLepMass = MCvect4.M();
      
      MCvect4 = ttbarDecay[3]->p4();
      MCvect4 += ttbarDecay[4]->p4();
      MCvect4 += ttbarDecay[5]->p4();
      *pMCTopHadPt = MCvect4.Pt();
      *pMCTopHadMass = MCvect4.M();
    }
  } // do_MC_
  //std::auto_ptr<int>    pnJets   ( new int(-1) );
  
  //std::string label="pfShyftSkim";
  //label+=":jets";
  // get the jet collection
  edm::Handle<std::vector<pat::Jet> > jets;
  event.getByLabel(edm::InputTag(selectorLabel_+":jets"), jets);
  // save number of jets is a naive way
  //*pnJets = jets->size();

  // extract and save fit mass and chi^2
  edm::Handle<std::vector<pat::Particle> > fitLeptons;
  event.getByLabel(edm::InputTag(kinFitterLabel_+":Leptons"), fitLeptons);

  edm::Handle<std::vector<pat::Particle> > fitNeutrinos;
  event.getByLabel(edm::InputTag(kinFitterLabel_+":Neutrinos"), fitNeutrinos);

  edm::Handle<std::vector<pat::Particle> > fitPartonsHadB;
  event.getByLabel(edm::InputTag(kinFitterLabel_+":PartonsHadB"), fitPartonsHadB);

  edm::Handle<std::vector<pat::Particle> > fitPartonsHadP;
  event.getByLabel(edm::InputTag(kinFitterLabel_+":PartonsHadP"), fitPartonsHadP);
  
  edm::Handle<std::vector<pat::Particle> > fitPartonsHadQ;
  event.getByLabel(edm::InputTag(kinFitterLabel_+":PartonsHadQ"), fitPartonsHadQ);

  edm::Handle<std::vector<pat::Particle> > fitPartonsLepB;
  event.getByLabel(edm::InputTag(kinFitterLabel_+":PartonsLepB"), fitPartonsLepB);
  
  edm::Handle<std::vector<double> > fitChi2;
  event.getByLabel(edm::InputTag(kinFitterLabel_+":Chi2"), fitChi2);

  // simple solution - take the best Chi2 combination only
  for(size_t i=0; i<(fitChi2->size()); i++){
    //std::cout << "i = " << i << "   Chi2 = " << (fitChi2->at(i)) << "   Neutrino pz = " << fitNeutrinos->at(i).pz() << std::endl;
    if(fitChi2->at(i)>=0){
      *pfitChi2 = fitChi2->at(i);

      reco::Candidate::LorentzVector vect4 = fitPartonsHadP->at(i).p4();
      vect4 += fitPartonsHadQ->at(i).p4();
      vect4 += fitPartonsHadB->at(i).p4();
      
      *pfitMass = vect4.M();
      *pTopHadPt = vect4.Pt();
      reco::Candidate::LorentzVector vect4L = fitLeptons->at(i).p4();
      vect4L += fitNeutrinos->at(i).p4();
      vect4L += fitPartonsLepB->at(i).p4();
      *pTopLepPt = vect4L.Pt();

      vect4 += fitLeptons->at(i).p4();
      vect4 += fitNeutrinos->at(i).p4();
      vect4 += fitPartonsLepB->at(i).p4();

      *pTTMass = vect4.M();
      
      //std::cout << "   fitMass = " << *pfitMass << "   TTmass = " << *pTTMass << std::endl;
      break;    
    }
  }
  
  
  event.put(pfitMass, "fitMass");
  event.put(pTTMass,  "TTMass");
  event.put(pfitChi2, "fitChi2");
  event.put(pTopLepPt, "TopLepPt");
  event.put(pTopHadPt, "TopHadPt");
  if(do_MC_){
    event.put(pMCTopLepPt, "MCTopLepPt");
    event.put(pMCTopHadPt, "MCTopHadPt");
    event.put(pMCTopLepMass, "MCTopLepMass");
    event.put(pMCTopHadMass, "MCTopHadMass");
    
    event.put(pMCLeptonPt, "MCLeptonPt");
    event.put(pMCLetonpEta, "MCLetonpEta");
    event.put(pMCLeptonPhi, "MCLeptonPhi");
    
    event.put(pMCNuPt, "MCNuPt");
    event.put(pMCNuEta, "MCNuEta");
    event.put(pMCNuPhi, "MCNuPhi");
    
    event.put(pMCLepBPt, "MCLepBPt");
    event.put(pMCLepBEta, "MCLepBEta");
    event.put(pMCLepBPhi, "MCLepBPhi");
    
    event.put(pMCHadBPt, "MCHadBPt");
    event.put(pMCHadBEta, "MCHadBEta");
    event.put(pMCHadBPhi, "MCHadBPhi");
    
    event.put(pMCWPart1Pt, "MCWPart1Pt");
    event.put(pMCWPart1Eta, "MCWPart1Eta");
    event.put(pMCWPart1Phi, "MCWPart1Phi");
    
    event.put(pMCWPart2Pt, "MCWPart2Pt");
    event.put(pMCWPart2Eta, "MCWPart2Eta");
    event.put(pMCWPart2Phi, "MCWPart2Phi");
  }
  //event.put(pnJets,   "nJets");
  return;
}


// look for t t-bar like semileptonic decay in GenParticles collection and store 4-vectors of decay products
void TprimeNtupleDumper::findTop(edm::Handle<std::vector<reco::GenParticle> > &genParticleCollection, std::vector<const reco::Candidate*> &ttbarDecay){  
  bool hasLeptW(false), hasHadW(false);
  assert ( genParticleCollection.isValid() );
  ttbarDecay.clear();
  ttbarDecay.resize(6);
  // Iterate over genParticles to find t tbar decay topology
  const std::vector<reco::GenParticle>::const_iterator kGenPartEnd = genParticleCollection->end();
   for(std::vector<reco::GenParticle>::const_iterator gpIter = genParticleCollection->begin(); gpIter != kGenPartEnd; ++gpIter ){
//     std::cout << "GenParticle ID " << gpIter->pdgId();
//     for(size_t di1=0; di1<gpIter->numberOfDaughters(); di1++){
//       std::cout << "  daughter " << gpIter->daughter(di1)->pdgId();
//     }
//     std::cout << std::endl;
    if(gpIter->numberOfDaughters()>=2 && std::abs(gpIter->daughter(0)->pdgId())==resonanceId_ && std::abs(gpIter->daughter(1)->pdgId())==resonanceId_){
      //std::cout <<  "found mother of t tbar" << std::endl;
      const reco::Candidate* tops[2] = { gpIter->daughter(0), gpIter->daughter(1) };
      if(tops[0]->pdgId()*tops[1]->pdgId() > 0) {std::cout << "Weird: same sign tops" << std::endl; break;}
      // check if this ttbar had semileptonic decay
      for(int ti=0; ti<2; ti++){
	//if(tops[ti]->numberOfDaughters()!=2){ std::cout << "top decayed not into 2 particles" << std::endl;}
	for(int di=0; di<2; di++){
	  if(std::abs(tops[ti]->daughter(di)->pdgId())==24){
	    //std::cout << "found W. Check decay mode" << std::endl;
	    if(tops[ti]->daughter(di)->numberOfDaughters()!=2) {std::cout << "W decayed not into 2 particles!" << std::endl; break;}
	    if(std::abs(tops[ti]->daughter(di)->daughter(0)->pdgId())>10){
	      //std::cout << "leptonic W decay" << std::endl;
	      if(std::abs(tops[ti]->daughter(di)->daughter(0)->pdgId())%2==0) {
		ttbarDecay[0]=tops[ti]->daughter(di)->daughter(1); ttbarDecay[1]=tops[ti]->daughter(di)->daughter(0);}
	      else {ttbarDecay[0]=tops[ti]->daughter(di)->daughter(0); ttbarDecay[1]=tops[ti]->daughter(di)->daughter(1);}
	      // now fill the other leg - b quark
	      if(std::abs(tops[ti]->daughter((di+1)%2)->pdgId())!=5){std::cout << "W does not have b quark!" << std::endl; break;}
	      ttbarDecay[2]=tops[ti]->daughter((di+1)%2);
	      hasLeptW=true;
	    }
	    else if(std::abs(tops[ti]->daughter(di)->daughter(0)->pdgId())<5 && std::abs(tops[ti]->daughter(di)->daughter(1)->pdgId())<5){
	      //std::cout << "light quark W decay" << std::endl;
	      if(tops[ti]->daughter(di)->daughter(0)->pt()>tops[ti]->daughter(di)->daughter(1)->pt()){
		ttbarDecay[4]=tops[ti]->daughter(di)->daughter(0); ttbarDecay[5]=tops[ti]->daughter(di)->daughter(1);}
	      else{ttbarDecay[4]=tops[ti]->daughter(di)->daughter(1); ttbarDecay[5]=tops[ti]->daughter(di)->daughter(0);}
	      // fill the b quark for hadronic top
	      if(std::abs(tops[ti]->daughter((di+1)%2)->pdgId())!=5){std::cout << "W does not have b quark!" << std::endl; break;}
	      ttbarDecay[3]=tops[ti]->daughter((di+1)%2);
	      hasHadW=true;
	    }
	  } 
	}
      }
      break; // we don't need to search further if we found ttbar
    } // if
  }
  if(!hasLeptW || !hasHadW) ttbarDecay.clear();
}


#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(TprimeNtupleDumper);
