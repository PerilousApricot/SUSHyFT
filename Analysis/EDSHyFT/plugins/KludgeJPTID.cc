// -*- C++ -*-
//
// Package:    KludgeJPTID
// Class:      KludgeJPTID
// 
/**\class KludgeJPTID KludgeJPTID.cc Analysis/KludgeJPTID/src/KludgeJPTID.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  "Salvatore Rappoccio"
//         Created:  Mon Aug 30 12:06:21 CDT 2010
// $Id: KludgeJPTID.cc,v 1.1 2010/08/30 19:43:00 srappocc Exp $
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

//
// class declaration
//

class KludgeJPTID : public edm::EDProducer {
   public:
      explicit KludgeJPTID(const edm::ParameterSet&);
      ~KludgeJPTID();

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      // ----------member data ---------------------------
  edm::InputTag jetSrc_;
};

//
// constants, enums and typedefs
//


//
// static data member definitions
//

//
// constructors and destructor
//
KludgeJPTID::KludgeJPTID(const edm::ParameterSet& iConfig) :
  jetSrc_( iConfig.getParameter<edm::InputTag>("jetSrc"))
{
   //register your products


  produces<std::vector<pat::Jet> > ();
  
}


KludgeJPTID::~KludgeJPTID()
{
}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
KludgeJPTID::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  std::auto_ptr< std::vector<pat::Jet> > jetsOut ( new std::vector<pat::Jet> () );

  edm::Handle< std::vector<pat::Jet> > h_jets;
  iEvent.getByLabel( jetSrc_, h_jets );

  for ( std::vector<pat::Jet>::const_iterator jetBegin = h_jets->begin(),
	  jetEnd = h_jets->end(), ijet = jetBegin;
	ijet != jetEnd; ++ijet ) {
    jetsOut->push_back( *ijet );


    reco::JPTJet const * jptjet = dynamic_cast<reco::JPTJet const *> (&*ijet);

    if ( jptjet == 0 ) throw cms::Exception("InvalidInput") << " Jet is not a JPT Jet" << std::endl;
    edm::RefToBase<reco::Jet>  jetRef = jptjet->getCaloJetRef();
    reco::CaloJet const * rawcalojet = dynamic_cast<reco::CaloJet const *>( &* jetRef);
    if ( rawcalojet == 0 ) throw cms::Exception("InvalidInput") << " Original jet from JPT jet is not a Calo Jet" << std::endl;
    jetsOut->back().addUserFloat("caloEMF", rawcalojet->emEnergyFraction() );
    jetsOut->back().addUserFloat("caloE", rawcalojet->energy() );
  }

  iEvent.put( jetsOut );
 
}

// ------------ method called once each job just before starting event loop  ------------
void 
KludgeJPTID::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
KludgeJPTID::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(KludgeJPTID);
