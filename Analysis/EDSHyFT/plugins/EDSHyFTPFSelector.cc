#include "Analysis/EDSHyFT/plugins/EDSHyFTPFSelector.h"
#include "FWCore/Framework/interface/MakerMacros.h"

bool EDSHyFTPFSelector::filter( edm::Event & event, const edm::EventSetup& eventSetup)
{
  bool passed = edm::FilterWrapper<SHyFTPFSelector>::filter( event, eventSetup );

  std::vector<reco::ShallowClonePtrCandidate> const & ijets = filter_->selectedJets();
  reco::ShallowClonePtrCandidate const & imet = filter_->selectedMET();
  std::vector<reco::ShallowClonePtrCandidate> const & imuons = filter_->selectedTightMuons();
  std::vector<reco::ShallowClonePtrCandidate> const & ielectrons = filter_->selectedTightElectrons();

  std::auto_ptr< std::vector<pat::Jet> > jets ( new std::vector<pat::Jet> );
  std::auto_ptr< std::vector<pat::MET> > mets ( new std::vector<pat::MET> );
  std::auto_ptr< std::vector<pat::Muon> > muons ( new std::vector<pat::Muon> );
  std::auto_ptr< std::vector<pat::Electron> > electrons ( new std::vector<pat::Electron> );

  mets->push_back( *(dynamic_cast<pat::MET const *>( imet.masterClonePtr().get() )) );

  typedef std::vector<reco::ShallowClonePtrCandidate>::const_iterator clone_iter;
  for ( clone_iter ibegin = ijets.begin(), iend = ijets.end(), i = ibegin;
	i != iend; ++i ) {
    pat::Jet const * ijet = dynamic_cast<pat::Jet const *>( i->masterClonePtr().get() );
    if ( ijet != 0 )
      jets->push_back( *ijet );
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


  event.put( jets, "jets");
  event.put( mets, "MET");
  event.put( muons, "muons");
  event.put( electrons, "electrons");

  return passed; 
}


typedef edm::FilterWrapper<SHyFTPFSelector> EDSHyFTPFSelectorBase;
DEFINE_FWK_MODULE(EDSHyFTPFSelectorBase);
DEFINE_FWK_MODULE(EDSHyFTPFSelector);
