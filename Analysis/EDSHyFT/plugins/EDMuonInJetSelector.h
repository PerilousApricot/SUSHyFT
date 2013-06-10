#ifndef EDMuonInJetSelector_h
#define EDMuonInJetSelector_h

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"

#include "PhysicsTools/UtilAlgos/interface/FWLiteFilterWrapper.h"
#include "Analysis/SHyFT/interface/MuonInJetSelector.h"

namespace edm {

  class EDMuonInJetSelectorFunction : public edm::FWLiteFilterWrapper<MuonInJetSelector> {
  public:
  EDMuonInJetSelectorFunction( const edm::ParameterSet & params ) :
    edm::FWLiteFilterWrapper<MuonInJetSelector>( params )
      {
	produces< std::vector<pat::Jet> >  ("jets");
	produces< std::vector<pat::Muon> > ("muons");
      };
    
    virtual ~EDMuonInJetSelectorFunction() {}
   
    /// Pass the event to the filter. NOTE! We can't use the eventSetup in FWLite so ignore it.
    virtual bool filter( edm::Event & event, const edm::EventSetup& eventSetup)
    {
      bool passed = edm::FWLiteFilterWrapper<MuonInJetSelector>::filter( event, eventSetup );

      std::vector<reco::ShallowClonePtrCandidate> const & ijets = filter_->jets();
      std::vector<reco::ShallowClonePtrCandidate> const & imuons = filter_->muons();

      std::auto_ptr< std::vector<pat::Jet> > jets ( new std::vector<pat::Jet> );
      std::auto_ptr< std::vector<pat::Muon> > muons ( new std::vector<pat::Muon> );


      typedef std::vector<reco::ShallowClonePtrCandidate>::const_iterator clone_iter;
      for ( clone_iter ibegin = ijets.begin(), iend = ijets.end(), i = ibegin;
	    i != iend; ++i ) {
	pat::Jet const * ijet = dynamic_cast<pat::Jet const *>( i->masterClonePtr().get() );
	jets->push_back( *ijet );
      }

      for ( clone_iter jbegin = imuons.begin(), jend = imuons.end(), j = jbegin;
	    j != jend; ++j ) {
	pat::Muon const * jmuon = dynamic_cast<pat::Muon const *>( j->masterClonePtr().get() );
	muons->push_back( *jmuon );
      }

      event.put( jets, "jets");
      event.put( muons, "muons");

      return passed; 
    }

    virtual void endJob() {
      filter_->print(std::cout);
    }
  };

}



typedef edm::FWLiteFilterWrapper<MuonInJetSelector> EDMuonInJetSelectorBase;
typedef edm::EDMuonInJetSelectorFunction EDMuonInJetSelector;
DEFINE_FWK_MODULE(EDMuonInJetSelectorBase);
DEFINE_FWK_MODULE(EDMuonInJetSelector);

#endif
