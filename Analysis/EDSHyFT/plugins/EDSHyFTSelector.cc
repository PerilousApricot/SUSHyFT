#include "Analysis/EDSHyFT/plugins/EDSHyFTSelector.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include <iostream>
#include <algorithm>
#include <cxxabi.h>
using namespace std;

bool EDSHyFTSelector::filter( edm::Event & event, const edm::EventSetup& eventSetup )
{
    bool passed = edm::FilterWrapper<SHyFTSelector>::filter( event, eventSetup );

    std::vector<reco::ShallowClonePtrCandidate> const & ijets = filter_->cleanedJets();
    reco::ShallowClonePtrCandidate const & imet = filter_->selectedMET();
    std::vector<reco::ShallowClonePtrCandidate> const & imuons = filter_->selectedMuons();
    std::vector<reco::ShallowClonePtrCandidate> const & ielectrons = filter_->selectedElectrons();
    std::vector<reco::ShallowClonePtrCandidate> const & itaus = filter_->selectedTaus();

    std::auto_ptr< std::vector<pat::Jet> > jets ( new std::vector<pat::Jet> );
    std::auto_ptr< std::vector<pat::MET> > mets ( new std::vector<pat::MET> );
    std::auto_ptr< std::vector<pat::Muon> > muons ( new std::vector<pat::Muon> );
    std::auto_ptr< std::vector<pat::Electron> > electrons ( new std::vector<pat::Electron> );
    std::auto_ptr< std::vector<pat::Tau> > taus ( new std::vector<pat::Tau> );

    pat::MET const * patmet = dynamic_cast<pat::MET const *>( imet.masterClonePtr().get() ); 
    if ( patmet != 0 ){  
        mets->push_back( *patmet );
        mets->back().setP4( imet.p4() );//set back the P4 to the clonned met
    }

    typedef std::vector<reco::ShallowClonePtrCandidate>::const_iterator clone_iter;
    edm::Handle<std::vector<reco::GenJet> > h_genJets;
    bool isRealData = ( ! ( !event.isRealData()) );
    if ( matchByHand_ && !isRealData ) {
        event.getByLabel("ca8GenJetsNoNu", h_genJets);
    }

    for ( clone_iter ibegin = ijets.begin(), iend = ijets.end(), i = ibegin;i != iend; ++i ) {
        pat::Jet const * ijet = dynamic_cast<pat::Jet const *>( i->masterClonePtr().get() );
        if ( matchByHand_ && !isRealData ) {
            if ( ijet != 0 ) {
                int matched = 0;
                jets->push_back( *ijet );
                jets->back().setP4( i->p4() );//set back the P4 to the clonned jet
                jets->back().addUserInt("matched",matched);

                //Find mathcing genJet for systematic smearing
                float minDR = 9.9;
                float dR = 10.;
                reco::GenJet theMatchingGenJet; 
                for ( std::vector<reco::GenJet>::const_iterator genJBegin = h_genJets->begin(), genJEnd = h_genJets->end(), igenjet = genJBegin; igenjet != genJEnd; ++igenjet ) {
                    dR = reco::deltaR<double>( ijet->eta(), ijet->phi(), igenjet->eta(), igenjet->phi() );
                    if ( dR < minDR ) {
                        theMatchingGenJet = (*igenjet);
                        minDR = dR;
                        matched = 1;
                    }       
                }
                if ( matched == 1 ) {
                    jets->back().addUserFloat("genJetPt",theMatchingGenJet.pt());
                    jets->back().addUserFloat("genJetPhi", theMatchingGenJet.phi());
                    jets->back().addUserFloat("genJetEta", theMatchingGenJet.eta());
                    jets->back().addUserFloat("genJetMass", theMatchingGenJet.mass());
                } else {
                    jets->back().addUserFloat("genJetPt", -10);
                    jets->back().addUserFloat("genJetPhi", -10);
                    jets->back().addUserFloat("genJetEta", -10);
                    jets->back().addUserFloat("genJetMass", -10);
                }
            }   
        } else {
            if ( ijet != 0 ){
                int matched = 0; 
                if ( ijet->genJet() ) matched=1;
                jets->push_back( *ijet );
                jets->back().setP4( i->p4() );//set back the P4 to the clonned jet
                jets->back().addUserInt("matched",matched);
                if ( matched == 1 ) { 
                    jets->back().addUserFloat("genJetPt",ijet->genJet()->pt());
                    jets->back().addUserFloat("genJetPhi", ijet->genJet()->phi());
                    jets->back().addUserFloat("genJetEta", ijet->genJet()->eta());
                    jets->back().addUserFloat("genJetMass", ijet->genJet()->mass());
                }else{
                    jets->back().addUserFloat("genJetPt", -10);
                    jets->back().addUserFloat("genJetPhi", -10);
                    jets->back().addUserFloat("genJetEta", -10);
                    jets->back().addUserFloat("genJetMass", -10);
                }
            }
        }
        if ( ijet != 0 ) {
            // match jet object with a (potential) Tau matching it
            for ( clone_iter jbegin = itaus.begin(), jend = itaus.end(), j = jbegin; j != jend; ++j ) {
                pat::Tau const * jtau = dynamic_cast<pat::Tau const *>( j->masterClonePtr().get() );
                if ( jtau == 0) {
                    continue;
                }
                if (reco::deltaR( jtau->eta(), jtau->phi(),
                                  ijet->eta(), ijet->phi() ) < 0.3) {
                    jets->back().addUserFloat("tauJetPt", jtau->pt());
                    jets->back().addUserFloat("tauJetPhi", jtau->phi());
                    jets->back().addUserFloat("tauJetEta", jtau->eta());
                    jets->back().addUserFloat("tauJetMass", jtau->mass());
                    //jets->back().addUserFloat("hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr3Hits", jtau->tauID("hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr3Hits"));
                    //jets->back().addUserFloat("hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr", jtau->tauID("hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr"));
                    //jets->back().addUserFloat("hpsPFTauDiscriminationByIsolationMVAraw", jtau->tauID("hpsPFTauDiscriminationByIsolationMVAraw"));
                    //jets->back().addUserFloat("hpsPFTauDiscriminationByIsolationMVA2raw", jtau->tauID("hpsPFTauDiscriminationByIsolationMVA2raw"));
                    jets->back().addUserFloat("byLooseCombinedIsolationDeltaBetaCorr3Hits", jtau->tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits") );
                    jets->back().addUserInt("byMediumCombinedIsolationDeltaBetaCorr3Hits", jtau->tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits"));
                    jets->back().addUserInt("byTightCombinedIsolationDeltaBetaCorr3Hits", jtau->tauID("byTightCombinedIsolationDeltaBetaCorr3Hits"));
                    jets->back().addUserInt("byLooseIsolationMVA2", jtau->tauID("byLooseIsolationMVA2"));
                    jets->back().addUserInt("byMediumIsolationMVA2", jtau->tauID("byMediumIsolationMVA2"));
                    jets->back().addUserInt("byTightIsolationMVA2", jtau->tauID("byTightIsolationMVA2"));
                    
                }
                    //int status = 0;
                //std::cout << abi::__cxa_demangle(typeid(jtau->pfJetRef()).name(),0,0,&status) << std::endl;
                //std::cout << abi::__cxa_demangle(typeid(ijet->originalObject()).name(),0,0,&status) << std::endl;
                //if ( (jtau->pfJetRef()) == *(ijet->originalObject()) ) {
                //    cout << "found a match";
                //}
                //jtau->pfJetRef();
                //size_t jetNum = jtau->pfJetRef()->size();
                //for (size_t n = 0; n < jetNum; ++n) {
                //    reco::PFJetRef aJet(jtau->pfJetRef(), n);
                //    //if ( *ijet == aJet ) {
                //    //    cout << "found a match" << endl;
                    //}
                //}
            }
        }
    }

    for ( clone_iter jbegin = imuons.begin(), jend = imuons.end(), j = jbegin; j != jend; ++j ) {
        pat::Muon const * jmuon = dynamic_cast<pat::Muon const *>( j->masterClonePtr().get() );
        if ( jmuon != 0 )
            muons->push_back( *jmuon );
    }

    for ( clone_iter jbegin = ielectrons.begin(), jend = ielectrons.end(), j = jbegin; j != jend; ++j ) {
        pat::Electron const * jelectron = dynamic_cast<pat::Electron const *>( j->masterClonePtr().get() );
        if ( jelectron != 0 )
            electrons->push_back( *jelectron );
    }

    for ( clone_iter jbegin = itaus.begin(), jend = itaus.end(), j = jbegin; j != jend; ++j ) {
        pat::Tau const * jtau = dynamic_cast<pat::Tau const *>( j->masterClonePtr().get() );
        if ( jtau != 0)
            taus->push_back( *jtau );
    }

    event.put( jets, "jets");
    event.put( mets, "MET");
    event.put( muons, "muons");
    event.put( electrons, "electrons");
    event.put( taus, "taus" );
    return passed; 
}


typedef edm::FilterWrapper<SHyFTSelector> EDSHyFTSelectorBase;
DEFINE_FWK_MODULE(EDSHyFTSelectorBase);
DEFINE_FWK_MODULE(EDSHyFTSelector);
