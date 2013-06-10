#ifndef EDWPlusJetsSelector_h
#define EDWPlusJetsSelector_h

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"

//#include "PhysicsTools/UtilAlgos/interface/FWLiteFilterWrapper.h"
#include "PhysicsTools/UtilAlgos/interface/EDFilterWrapper.h"
#include "Analysis/SHyFT/interface/SHyFTSelector.h"

class EDWPlusJetsSelector : public edm::FilterWrapper<SHyFTSelector> {
 public:
 EDWPlusJetsSelector( const edm::ParameterSet & params ) :
  edm::FilterWrapper<SHyFTSelector>( params )
    {
      produces< std::vector<pat::Jet> >      ("jets");
      produces< std::vector<pat::Muon> >     ("muons");
      produces< std::vector<pat::Electron> > ("electrons");
      produces< std::vector<pat::MET > >     ("met");
    };
    
  virtual ~EDWPlusJetsSelector() {}
   
  /// Pass the event to the filter. NOTE! We can't use the eventSetup in FWLite so ignore it.
  virtual bool filter( edm::Event & event, const edm::EventSetup& eventSetup)
  {
    bool passed = edm::FilterWrapper<SHyFTSelector>::filter( event, eventSetup );

    std::vector<reco::ShallowClonePtrCandidate> const & ijets = filter_->cleanedJets();
    std::vector<reco::ShallowClonePtrCandidate> const & imuons = filter_->selectedMuons();
    std::vector<reco::ShallowClonePtrCandidate> const & ielectrons = filter_->selectedElectrons();
    reco::ShallowClonePtrCandidate const &imets = filter_->selectedMET();

    std::auto_ptr< std::vector<pat::Jet> > jets ( new std::vector<pat::Jet> );
    std::auto_ptr< std::vector<pat::Muon> > muons ( new std::vector<pat::Muon> );
    std::auto_ptr< std::vector<pat::Electron> > electrons ( new std::vector<pat::Electron> );
    std::auto_ptr< std::vector<pat::MET > >     met       ( new std::vector<pat::MET> );

    typedef std::vector<reco::ShallowClonePtrCandidate>::const_iterator clone_iter;
    for ( clone_iter ibegin = ijets.begin(), iend = ijets.end(), i = ibegin;
	  i != iend; ++i ) {
      pat::Jet const * ijet = dynamic_cast<pat::Jet const *>( i->masterClonePtr().get() );
      if ( ijet != 0 )
	jets->push_back( *ijet );
	jets->back().setP4( i->p4() );//set back the P4 to the clonned jet
    }


    for ( clone_iter jbegin = imuons.begin(), jend = imuons.end(), j = jbegin;
	  j != jend; ++j ) {
      pat::Muon const * jmuon = dynamic_cast<pat::Muon const *>( j->masterClonePtr().get() );
      if ( jmuon != 0 )
	muons->push_back( *jmuon );
    }


    for ( clone_iter jbegin = ielectrons.begin(), jend = ielectrons.end(), j = jbegin;
	  j != jend; ++j ) {
      pat::Electron const * jelectron = dynamic_cast<pat::Electron const *>( j->masterClonePtr().get() );
      if ( jelectron != 0 )
	electrons->push_back( *jelectron );
    }

    pat::MET const * imet =  dynamic_cast<pat::MET const *>( imets.masterClonePtr().get() ); 
    if ( imet != 0 ){  
      met->push_back( *imet );
      met->back().setP4( imets.p4() );//set back the P4 to the clonned met
    }
    
    event.put( jets, "jets");
    event.put( muons, "muons");
    event.put( electrons, "electrons");
    event.put( met, "met");

    return passed; 
  }

  virtual void endJob() {
    filter_->print(std::cout);
  }
};



typedef edm::FilterWrapper<SHyFTSelector> EDWPlusJetsSelectorBase;
DEFINE_FWK_MODULE(EDWPlusJetsSelectorBase);
DEFINE_FWK_MODULE(EDWPlusJetsSelector);

#endif
