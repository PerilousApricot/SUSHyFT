#include "Analysis/SHyFT/interface/SHyFTSelector.h"
#include "DataFormats/Candidate/interface/ShallowCloneCandidate.h"
#include "DataFormats/RecoCandidate/interface/IsoDepositDirection.h"
#include "DataFormats/RecoCandidate/interface/IsoDeposit.h"
#include "DataFormats/RecoCandidate/interface/IsoDepositVetos.h"
#include "DataFormats/PatCandidates/interface/Isolation.h"
#include "EGamma/EGammaAnalysisTools/interface/ElectronEffectiveArea.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"

#include <iostream>
#include <boost/algorithm/string.hpp>

using namespace std;
using namespace reco;
using namespace isodeposit;
typedef math::XYZPoint Point;

SHyFTSelector::SHyFTSelector( edm::ParameterSet const & params ) :
    EventSelector(),
    muonTag_         (params.getParameter<edm::InputTag>("muonSrc") ),
    electronTag_     (params.getParameter<edm::InputTag>("electronSrc") ),
    jetTag_          (params.getParameter<edm::InputTag>("jetSrc") ),
    metTag_          (params.getParameter<edm::InputTag>("metSrc") ), 
    rhoTag_          (params.getParameter<edm::InputTag>("rhoSrc") ), 
    rhoIsoTag_       (params.getParameter<edm::InputTag>("rhoIsoSrc") ), 
    trigTag_         (params.getParameter<edm::InputTag>("trigSrc") ),
    tauTag_          (params.getParameter<edm::InputTag>("tauSrc") ),
    muTrig_          (params.getParameter<std::string>("muTrig")),
    eleTrig_         (params.getParameter<std::string>("eleTrig")),
    pvSelector_      (params.getParameter<edm::ParameterSet>("pvSelector") ),
    //muonIdTight_     (params.getParameter<edm::ParameterSet>("muonIdTight") ),
    //muonIdLoose_     (params.getParameter<edm::ParameterSet>("muonIdLoose") ),
    electronIdVeto_  (params.getParameter<edm::ParameterSet>("electronIdVeto") ),
    //electronIdTight_ (params.getParameter<edm::ParameterSet>("electronIdTight") ),
    minJets_         (params.getParameter<int> ("minJets") ),
    muJetDR_         (params.getParameter<double>("muJetDR")),
    eleJetDR_        (params.getParameter<double>("eleJetDR")),
    muPlusJets_      (params.getParameter<bool>("muPlusJets") ),
    ePlusJets_       (params.getParameter<bool>("ePlusJets") ),
    muPtMin_         (params.getParameter<double>("muPtMin")), 
    muEtaMax_        (params.getParameter<double>("muEtaMax")), 
    eleEtMin_        (params.getParameter<double>("eleEtMin")), 
    eleEtaMax_       (params.getParameter<double>("eleEtaMax")), 
    muPtMinLoose_    (params.getParameter<double>("muPtMinLoose")), 
    muEtaMaxLoose_   (params.getParameter<double>("muEtaMaxLoose")), 
    eleEtMinLoose_   (params.getParameter<double>("eleEtMinLoose")), 
    eleEtaMaxLoose_  (params.getParameter<double>("eleEtaMaxLoose")), 
    jetPtMin_        (params.getParameter<double>("jetPtMin")), 
    jetEtaMax_       (params.getParameter<double>("jetEtaMax")),
    jetScale_        (params.getParameter<double>("jetScale")),
    tauPtMin_        (params.getParameter<double>("tauPtMin")),
    tauEtaMax_       (params.getParameter<double>("tauEtaMax")),
    jetSmear_        (params.getParameter<double>("jetSmear")),
    unclMetScale_    (params.getParameter<double>("unclMetScale")),
    ePtScale_        (params.getParameter<double>("ePtScale")),
    ePtUncertaintyEE_(params.getParameter<double>("ePtUncertaintyEE")),
    eRelIso_         (params.getParameter<double>("eRelIso")),
    muRelIso_        (params.getParameter<double>("muRelIso")),
    eEt_             (params.getParameter<double>("eEt")),
    dxy_             (params.getParameter<double>("dxy")),
    pvTag_           (params.getParameter<edm::InputTag>("pvSrc")),
    useData_         (params.getParameter<bool>("useData")),
    useNoPFIso_      (params.getParameter<bool>("useNoPFIso")),
    useNoID_         (params.getParameter<bool>("useNoID")),
    pfEleSrc_       (params.getParameter<edm::InputTag>( "pfEleSrc" )),
    jecPayloads_     (params.getParameter<std::vector<std::string> >("jecPayloads"))
{
   electronIdVeto_.setUseData(useData_);
   
    // make the bitset
    push_back( "Inclusive"      );
    push_back( "Trigger"        );
    push_back( "PV"             );
    push_back( ">= 1 Lepton"    );
    push_back( "== 1 Tight Lepton"    );
    push_back( "== 1 Tight Lepton, Mu Veto");
    push_back( "== 1 Lepton"    );
    push_back( "Dilepton Veto"  );
    push_back( "Cosmic Veto"    );
    push_back( ">=1 Jets"       );
    push_back( ">=2 Jets"       );
    push_back( ">=3 Jets"       );
    push_back( ">=4 Jets"       );
    push_back( ">=5 Jets"       );
    push_back( ">=6 Jets"       );
    push_back( ">=7 Jets"       );
    push_back( ">=8 Jets"       );
    push_back( ">=9 Jets"       );







    // turn (almost) everything on by default
    set( "Inclusive"      );
    set( "Trigger"        );
    set( "PV"             );
    set( ">= 1 Lepton"    );
    set( "== 1 Tight Lepton"    );
    set( "== 1 Tight Lepton, Mu Veto");
    set( "== 1 Lepton"    );
    set( "Dilepton Veto"  );
    set( "Cosmic Veto"    );
    set( ">=1 Jets", minJets_ >= 1);
    set( ">=2 Jets", minJets_ >= 2);
    set( ">=3 Jets", minJets_ >= 3);
    set( ">=4 Jets", minJets_ >= 4);
    set( ">=5 Jets", minJets_ >= 5); 
    set( ">=6 Jets", minJets_ >= 6); 
    set( ">=7 Jets", minJets_ >= 7); 
    set( ">=8 Jets", minJets_ >= 8); 
    set( ">=9 Jets", minJets_ >= 9); 

    inclusiveIndex_ = index_type(&bits_, std::string("Inclusive"      ));
    triggerIndex_ = index_type(&bits_, std::string("Trigger"        ));
    pvIndex_ = index_type(&bits_, std::string("PV"             ));
    lep1Index_ = index_type(&bits_, std::string(">= 1 Lepton"    ));
    lep2Index_ = index_type(&bits_, std::string("== 1 Tight Lepton"    ));
    lep3Index_ = index_type(&bits_, std::string("== 1 Tight Lepton, Mu Veto"));
    lep4Index_ = index_type(&bits_, std::string("== 1 Lepton"    ));
    dlepvetoIndex_ = index_type(&bits_, std::string("Dilepton Veto"));
    cosmicIndex_ = index_type(&bits_, std::string("Cosmic Veto"));
    jet1Index_ = index_type(&bits_, std::string(">=1 Jets"));
    jet2Index_ = index_type(&bits_, std::string(">=2 Jets"));
    jet3Index_ = index_type(&bits_, std::string(">=3 Jets"));
    jet4Index_ = index_type(&bits_, std::string(">=4 Jets"));
    jet5Index_ = index_type(&bits_, std::string(">=5 Jets")); 
    jet6Index_ = index_type(&bits_, std::string(">=6 Jets")); 
    jet7Index_ = index_type(&bits_, std::string(">=7 Jets")); 
    jet8Index_ = index_type(&bits_, std::string(">=8 Jets")); 
    jet9Index_ = index_type(&bits_, std::string(">=9 Jets")); 
    cout << "calling shyftselector\n";
    if ( params.exists("cutsToIgnore") )
        setIgnoredCuts( params.getParameter<std::vector<std::string> >("cutsToIgnore") );

    retInternal_ = getBitTemplate();

    //Get the factorized jet corrector. 
    // The payloads contain N elements, the Nth is the uncertainty, and the first N-1 elements are the
    // actual correction levels.The N-2 element is only used for data 
    vector<JetCorrectorParameters> vPar;
    for ( std::vector<std::string>::const_iterator payloadBegin = jecPayloads_.begin(),
            payloadEnd = jecPayloads_.end(), ipayload = payloadBegin; ipayload != payloadEnd - 1; ++ipayload ) {
        std::cout << "Attempting to load payload " << *ipayload << std::endl;
        JetCorrectorParameters pars(*ipayload);

        if(ipayload != payloadEnd - 2){
            std::cout << "Adding payload for mc: " << *ipayload  << std::endl;
            vPar.push_back(pars);}  
        else if (( ipayload == payloadEnd - 2) && ( useData_)){
            std::cout << "Adding payload for data: " << *ipayload << std::endl;
            vPar.push_back(pars);}   
    }

    jec_ = boost::shared_ptr<FactorizedJetCorrector> ( new FactorizedJetCorrector(vPar) );
    jecUnc_ = boost::shared_ptr<JetCorrectionUncertainty>( new JetCorrectionUncertainty(jecPayloads_.back()));
    firstTime_ = true;

    // Attempt to split the trigger into a list of triggers
    boost::algorithm::split(eleTriggerList_, eleTrig_, boost::algorithm::is_any_of(","));
    boost::algorithm::split(muTriggerList_, muTrig_, boost::algorithm::is_any_of(","));
}

bool SHyFTSelector::operator() ( edm::EventBase const & event, pat::strbitset & ret)
{
    ret.set(false);

    allJets_.clear();
    //selectedJets_.clear();
    cleanedJets_.clear();
    allMuons_.clear();
    selectedMuons_.clear();
    //oldElectrons_.clear();
    looseMuons_.clear();
    looseElectrons_.clear();
    selectedMETs_.clear();
    met_=reco::ShallowClonePtrCandidate();
    allElectrons_.clear();
    selectedElectrons_.clear();//to select ==1 tight electron
    selectedLooseElectrons_.clear();//to apply Dilepton Veto 
    selectedLooseMuons_.clear();
    allTaus_.clear();
    selectedTaus_.clear();
    passCut( ret, inclusiveIndex_);


    bool passTrig = false;
    if (!ignoreCut(triggerIndex_) ) {

        edm::Handle<pat::TriggerEvent> triggerEvent;
        event.getByLabel(trigTag_, triggerEvent);
        pat::TriggerEvent const * trig =  &*triggerEvent;

        if ( trig->wasRun() && trig->wasAccept() ) { 

            const pat::TriggerPathCollection *paths = trig->paths();
            //if ( firstTime_ == true ) {
            //    for (unsigned int i = 0; i != paths->size(); ++i) {
            //        std::cout << (*paths)[i].name() << std::endl;
            //    }
            //    firstTime_ = false;
            //}
            pat::TriggerPath const * lepPath;
            std::vector<std::string> * triggerList;
            if (muPlusJets_) {
                triggerList = &muTriggerList_;
            } else if (ePlusJets_) {
                triggerList = &eleTriggerList_;
            }
            for (unsigned int i = 0; i != triggerList->size(); ++i) {
                lepPath = trig->path((*triggerList)[i]);
                if ( lepPath != 0 && lepPath->wasAccept() ) {
                    passTrig = true;    
                }
            }
        }
    }

    if ( ignoreCut(triggerIndex_) || 
            passTrig ) {
        passCut(ret, triggerIndex_);

        bool passPV = false;

        passPV = pvSelector_( event );
        if ( ignoreCut(pvIndex_) || passPV ) {
            passCut(ret, pvIndex_);

            edm::Handle<std::vector<reco::Vertex> > primVtxHandle;
            event.getByLabel(pvTag_, primVtxHandle);

            double PVz = -999; Point PV(0,0,0);
            if ( primVtxHandle->size() > 0 ) {
                PVz = primVtxHandle->at(0).z();
                PV  = primVtxHandle->at(0).position();
            } else {
                throw cms::Exception("InvalidInput") << " There needs to be at least one primary vertex in the event." << std::endl;
            }

            edm::Handle< vector< pat::Electron > > electronHandle;
            event.getByLabel (electronTag_, electronHandle);

            edm::Handle< vector< pat::Muon > > muonHandle;
            event.getByLabel (muonTag_, muonHandle);

            edm::Handle< vector< pat::Jet > > jetHandle;
            event.getByLabel (jetTag_, jetHandle);

            edm::Handle< vector< pat::Tau > > tauHandle;
            event.getByLabel (tauTag_, tauHandle);

            edm::Handle< edm::OwnVector<reco::Candidate> > jetClonesHandle ;

            edm::Handle< vector< pat::MET > > metHandle;
            event.getByLabel (metTag_, metHandle);

            reco::Candidate::LorentzVector metP4 = metHandle->at(0).p4();

            edm::Handle<double> rhoHandle;
            event.getByLabel(rhoTag_, rhoHandle);

            edm::Handle<double> rhoHandleIso;
            event.getByLabel(rhoIsoTag_, rhoHandleIso);     
            double rhoIso = std::max(*(rhoHandleIso.product()), 0.0);

            int nElectrons = 0;

            //Electron selections:
            //-------------------
            for ( std::vector<pat::Electron>::const_iterator electronBegin = electronHandle->begin(),
                    electronEnd = electronHandle->end(), ielectron = electronBegin;
                    ielectron != electronEnd; ++ielectron ) {
                allElectrons_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Electron>( electronHandle, ielectron - electronBegin ) ) );
                ++nElectrons;
                double AEff    = 0.0;
                double scEta   = ielectron->superCluster()->eta();
                double eta     = ielectron->eta();
                double et      = ielectron->et();
                double dB      = ielectron->dB();
                if(useData_){
                    AEff    = ElectronEffectiveArea::GetElectronEffectiveArea(ElectronEffectiveArea::kEleGammaAndNeutralHadronIso03, scEta, ElectronEffectiveArea::kEleEAData2011);
                }else{
                    AEff    = ElectronEffectiveArea::GetElectronEffectiveArea(ElectronEffectiveArea::kEleGammaAndNeutralHadronIso03, scEta, ElectronEffectiveArea::kEleEAFall11MC);
                }
                double chIso = ielectron->userIsolation(pat::PfChargedHadronIso);
                double nhIso = ielectron->userIsolation(pat::PfNeutralHadronIso);
                double phIso  = ielectron->userIsolation(pat::PfGammaIso);
                double relIso = ( chIso + max(0.0, nhIso + phIso - rhoIso*AEff) )/ ielectron->ecalDrivenMomentum().pt();           
                int mHits  =  ielectron->gsfTrack()->trackerExpectedHitsInner().numberOfHits();   

                //Electron Selection for e+jets
                //-----------------------------  
                if (fabs(scEta) > 1.4442 &&  fabs(scEta) < 1.5660 ) continue;  //Fiducial cuts 

                bool passTopCuts(0), passIso(0), passMVAID(0), passVetoID(0);

                passTopCuts = (fabs(eta)< 2.5 && 
                        fabs(dB) < dxy_ &&
                        et       > eEt_ &&
                        mHits    <= 0 &&
                        (ielectron->passConversionVeto()) 
                        );

                if(useNoPFIso_) passIso = 1;
                else passIso = relIso < eRelIso_;  

                if(useNoID_) passMVAID = 1;
                else passMVAID = ielectron->electronID("mvaTrigV0") > 0;

                passVetoID = electronIdVeto_(*ielectron,event);//WP:"Veto" from cut based ID
               
                if(passTopCuts && passIso && passMVAID){

                    selectedElectrons_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Electron>( electronHandle, ielectron - electronBegin ) ) );
                }
                else if(passVetoID && et > 20.0){
                    selectedLooseElectrons_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Electron>( electronHandle, ielectron - electronBegin ) ) );
                }   

                //Loose Electron Selection to be vetoed for mu+jets
                //-------------------------------------------------
                if ( et > eleEtMinLoose_ && eta < eleEtaMaxLoose_ && relIso < 0.2 ){
                    looseElectrons_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Electron>( electronHandle, ielectron - electronBegin ) ) );
                }
            }


            //Muons Selection:
            //---------------
            for ( std::vector<pat::Muon>::const_iterator muonBegin = muonHandle->begin(),
                    muonEnd = muonHandle->end(), imuon = muonBegin;
                    imuon != muonEnd; ++imuon ) { 

                bool passIso(0);
                double chIso   = imuon->userIsolation(pat::PfChargedHadronIso);
                double nhIso   = imuon->userIsolation(pat::PfNeutralHadronIso);
                double phIso   = imuon->userIsolation(pat::PfGammaIso);
                double puIso   = imuon->userIsolation(pat::PfPUChargedHadronIso);
                double relIso  = (chIso+ max(0.,nhIso+phIso - 0.5*puIso)) /imuon->pt();
                
                //if ( !imuon->isGlobalMuon() ) continue;
                              
                //Muon Selection for mu+jets
                //-------------------------- 
                if(useNoPFIso_) passIso = 1; //no isolation by default
                else passIso = relIso < muRelIso_; 
                
                // Loose cuts: in the vector-like quark analysis, we will use the loose muon selection from muon POG without isolation cut.
                bool passLoose = imuon->isPFMuon() && ( imuon->isGlobalMuon() || imuon->isTrackerMuon() );
               
                if ( imuon->pt() > muPtMin_ && fabs(imuon->eta()) < muEtaMax_ && passLoose && passIso ) {                   
                   selectedMuons_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Muon>( muonHandle, imuon - muonBegin ) ) );
                } else {
                    // Loose cuts : currently the same passLoose is applied but pt and iso can be different.
                   if ( imuon->pt() > muPtMinLoose_ && fabs(imuon->eta()) < muEtaMaxLoose_ && passLoose && relIso < 0.2) {
                      looseMuons_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Muon>( muonHandle, imuon - muonBegin ) ) );
                   }
                }

                //Loose Muon Selection to be vetoed for e+jets 
                //--------------------------------------------
                if ( imuon->pt() > muPtMinLoose_ && fabs(imuon->eta()) < muEtaMaxLoose_ &&  relIso < 0.2 ) {
                    selectedLooseMuons_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Muon>( muonHandle, imuon - muonBegin ) ) );
                }
                
            }

            //Tau selection
            //-------------	            

            for ( std::vector<pat::Tau>::const_iterator tauBegin = tauHandle->begin(),
                    tauEnd = tauHandle->end(), itau = tauBegin;
                    itau != tauEnd; ++itau ) {
                if ( (itau->pt() > tauPtMin_) && (fabs(itau->eta()) < tauEtaMax_) ){
                    allTaus_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Tau>( tauHandle, itau - tauBegin ) ) );
                    selectedTaus_.push_back( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Tau>( tauHandle, itau - tauBegin ) ) );
                }
            }

            //Jet selection
            //-------------	            

            for ( std::vector<pat::Jet>::const_iterator jetBegin = jetHandle->begin(),
                    jetEnd = jetHandle->end(), ijet = jetBegin;
                    ijet != jetEnd; ++ijet ) {

                // get a copy of the uncorrected p4
                reco::Candidate::LorentzVector uncorrJet = ijet->correctedP4(0);

                // Then get the correction (L1+L2+L3 [+L2L3 for data])
                jec_->setJetEta( uncorrJet.eta() );
                jec_->setJetPt ( uncorrJet.pt() );
                jec_->setJetE  ( uncorrJet.energy() );
                jec_->setJetA  ( ijet->jetArea() );
                jec_->setRho   ( *(rhoHandle.product()) );
                jec_->setNPV   ( primVtxHandle->size() );
                double corr = jec_->getCorrection();


                // Here will be the working variable for all the jet energy effects
                reco::Candidate::LorentzVector scaledJetP4 = uncorrJet * corr;

                // -------
                // Jet energy scale variation
                //    - Also computes a piece of MET uncertainty due to this effect
                // -------
                if ( fabs(jetScale_) > 0.0 ) {	     
                    // First subtract the uncorrected px and py from MET
                    metP4.SetPx( metP4.Px() + uncorrJet.px() );
                    metP4.SetPy( metP4.Py() + uncorrJet.py() );


                    // Now get the uncertainties
                    jecUnc_->setJetEta( scaledJetP4.eta() );
                    jecUnc_->setJetPt( scaledJetP4.pt() );
                    double unc = fabs(jecUnc_->getUncertainty( bool(jetScale_ > 0) ));

                    // Scale up or down by jetScale_
                    double ijetscale = (1 + jetScale_ * unc);
                    scaledJetP4 *= ijetscale;

                    // Correct the MET back again for this effect
                    metP4.SetPx( metP4.Px() - uncorrJet.px() * ijetscale);
                    metP4.SetPy( metP4.Py() - uncorrJet.py() * ijetscale);	     
                }

                // -------
                // Jet energy resolution variation
                //    - Also computes a piece of MET uncertainty due to this effect
                // -------
                if ( fabs(jetSmear_) > 0.0 && ijet->genJet() != 0 && ijet->genJet()->pt() > 15.0 ) {
                    // First subtract the uncorrected px and py from MET
                    metP4.SetPx( metP4.Px() + uncorrJet.px() );
                    metP4.SetPy( metP4.Py() + uncorrJet.py() );
                    // Next smear the jets
                    double scale = jetSmear_;
                    double recopt = ijet->pt();
                    double genpt = ijet->genJet()->pt();
                    double deltapt = (recopt-genpt)*scale;
                    double ptscale = std::max((double)0.0,(recopt+deltapt)/recopt);
                    scaledJetP4 *= ptscale;
                    // Correct the MET back again for this effect
                    metP4.SetPx( metP4.Px() - uncorrJet.px() * ptscale);
                    metP4.SetPy( metP4.Py() - uncorrJet.py() * ptscale);
                }            

                reco::ShallowClonePtrCandidate scaledJet ( reco::ShallowClonePtrCandidate( edm::Ptr<pat::Jet>( jetHandle, ijet - jetBegin ),
                            ijet->charge(),
                            scaledJetP4 ) );
                allJets_.push_back( scaledJet );

                if ( scaledJet.pt() > jetPtMin_ && fabs(scaledJet.eta()) < jetEtaMax_ ) {  
                   //selectedJets_.push_back( scaledJet );
                    cleanedJets_.push_back( scaledJet );

/*
                    if ( muPlusJets_ ) {
                        //Remove some jets
                        bool indeltaR = false;
                        for( std::vector<reco::ShallowClonePtrCandidate>::const_iterator muonBegin = selectedMuons_.begin(),
                                muonEnd = selectedMuons_.end(), imuon = muonBegin;
                                imuon != muonEnd; ++imuon ) {
                            if( reco::deltaR( imuon->eta(), imuon->phi(), scaledJet.eta(), scaledJet.phi() ) < muJetDR_ )
                            {  indeltaR = true; }
                        }
                        if( !indeltaR ) {
                            cleanedJets_.push_back( scaledJet );
                        }// end if jet is not within dR of a muon
                    }// end if mu+jets
                    else {

                        //Remove some jets
                        bool indeltaR = false;
                        for( std::vector<reco::ShallowClonePtrCandidate>::const_iterator electronBegin = selectedElectrons_.begin(),
                                electronEnd = selectedElectrons_.end(), ielectron = electronBegin;
                                ielectron != electronEnd; ++ielectron ) {

                            const pat::Electron * electron_ = dynamic_cast<const pat::Electron *>(ielectron->masterClonePtr().get());

                            if( reco::deltaR( ielectron->eta(), ielectron->phi(), scaledJet.eta(), scaledJet.phi() ) < eleJetDR_ ){
                                indeltaR = true; }                     
                        }
                        if( !indeltaR ) {
                            cleanedJets_.push_back( scaledJet );
                        }// end if jet is not within dR of an electron
                    }// end if e+jets
*/
                }// end if pass id and kin cuts
            }// end loop over jets




            // -------
            // Unclustered MET resolution
            // -------
            if ( unclMetScale_ > 0.0 ) {

                // Subtract off the (uncorrected) jets
                for ( std::vector<reco::ShallowClonePtrCandidate>::const_iterator jetBegin = allJets_.begin(),
                        jetEnd = allJets_.end(), ijet = jetBegin;
                        ijet != jetEnd; ++ijet ) {
                    pat::Jet const & jet = dynamic_cast<pat::Jet const &>( *(ijet->masterClonePtr().get() ));
                    metP4.SetPx( metP4.px() + jet.correctedP4(0).px() );
                    metP4.SetPy( metP4.py() + jet.correctedP4(0).py() );
                }

                // Subtract off muons
                for ( std::vector<reco::ShallowClonePtrCandidate>::const_iterator muBegin = allMuons_.begin(),
                        muEnd = allMuons_.end(), imu = muBegin;
                        imu != muEnd; ++imu ) {
                    metP4.SetPx( metP4.px() + imu->px() );
                    metP4.SetPy( metP4.py() + imu->py() );	       
                }

                // Subtract off electrons
                for ( std::vector<reco::ShallowClonePtrCandidate>::const_iterator eleBegin = allElectrons_.begin(),
                        eleEnd = allElectrons_.end(), iele = eleBegin;
                        iele != eleEnd; ++iele ) {
                    metP4.SetPx( metP4.px() + iele->px() );
                    metP4.SetPy( metP4.py() + iele->py() );	       
                }

                // met_x and met_y are now unclustered energy
                // apply the 10% on the unclustered energy. "factor" is either 0.9 or 1.1, for MET_minus or MET_plus, resp.
                metP4.SetPx( metP4.px() * unclMetScale_ );
                metP4.SetPy( metP4.py() * unclMetScale_ );


                // Add back the jets
                for ( std::vector<reco::ShallowClonePtrCandidate>::const_iterator jetBegin = allJets_.begin(),
                        jetEnd = allJets_.end(), ijet = jetBegin;
                        ijet != jetEnd; ++ijet ) {
                    pat::Jet const & jet = dynamic_cast<pat::Jet const &>( *(ijet->masterClonePtr().get() ));
                    metP4.SetPx( metP4.px() - jet.correctedP4(0).px() );
                    metP4.SetPy( metP4.py() - jet.correctedP4(0).py() );
                }

                // Add back the muons
                for ( std::vector<reco::ShallowClonePtrCandidate>::const_iterator muBegin = allMuons_.begin(),
                        muEnd = allMuons_.end(), imu = muBegin;
                        imu != muEnd; ++imu ) {
                    metP4.SetPx( metP4.px() - imu->px() );
                    metP4.SetPy( metP4.py() - imu->py() );	       
                }


                // Add back the electrons
                for ( std::vector<reco::ShallowClonePtrCandidate>::const_iterator eleBegin = allElectrons_.begin(),
                        eleEnd = allElectrons_.end(), iele = eleBegin;
                        iele != eleEnd; ++iele ) {
                    metP4.SetPx( metP4.px() - iele->px() );
                    metP4.SetPy( metP4.py() - iele->py() );	       
                }


            }


            // -------
            // Endcap Electron Momentum uncertainity on MET resolution
            // -------
            if ( fabs(ePtScale_) > 0.0 && ePlusJets_) {                
                for ( std::vector<reco::ShallowClonePtrCandidate>::const_iterator eleBegin = allElectrons_.begin(),
                        eleEnd = allElectrons_.end(), iele = eleBegin;
                        iele != eleEnd; ++iele ) {
                    pat::Electron const & e = dynamic_cast<pat::Electron const &>( *(iele->masterClonePtr().get() ));
                    if(e.isEE()){  // Subtract off pt of endcap electrons
                        metP4.SetPx( metP4.px() + e.px() );
                        metP4.SetPy( metP4.py() + e.py() );

                        // Scale up or down by ptScale_ by 0.025 as ePUncertaintyEE_
                        double iptscaleunc = (1 + ePtScale_ * ePtUncertaintyEE_ ); 
                        //cout<< iptscaleunc << endl;
                        // Correct the MET back again for this effect
                        metP4.SetPx( metP4.px() - e.px() * iptscaleunc );
                        metP4.SetPy( metP4.py() - e.px() * iptscaleunc );
                    }
                    else continue;   
                }
            }


            // Set the MET
            met_ = reco::ShallowClonePtrCandidate( edm::Ptr<pat::MET>( metHandle, 0),
                    metHandle->at(0).charge(),
                    metP4 );

            int nleptons = 0;
            if ( muPlusJets_ )
                nleptons += selectedMuons_.size();

            if ( ePlusJets_ ) 
                nleptons += selectedElectrons_.size();

            if ( ignoreCut(lep1Index_) || 
                    ( nleptons > 0 ) ){
                passCut( ret, lep1Index_);


                if ( ignoreCut(lep2Index_) || 
                        ( nleptons == 1 ) ){
                    passCut( ret, lep2Index_);


                    bool oneMuon = 
                        ( selectedMuons_.size() == 1 && 
                          looseMuons_.size() + looseElectrons_.size() == 0 
                        );
                    bool oneElectron =
                        (selectedElectrons_.size() == 1 && 
                         selectedLooseMuons_.size() + selectedLooseElectrons_.size() == 0 
                        );

                    bool oneMuonMuVeto = 
                        ( selectedMuons_.size() == 1 && 
                          looseMuons_.size() == 0 
                        );
                    bool oneElectronMuVeto = 
                        ( selectedElectrons_.size() == 1 && 
                          selectedLooseMuons_.size() == 0 
                        );

                    if ( ignoreCut(lep3Index_) || 
                            (ePlusJets_ &&  oneElectronMuVeto)||
                            (muPlusJets_ && oneMuonMuVeto)
                       ) {
                        passCut(ret, lep3Index_);

                        if ( ignoreCut(lep4Index_) || 
                                ((muPlusJets_ && oneMuonMuVeto) ^ (ePlusJets_ && oneElectronMuVeto )  )
                           ) {
                            passCut(ret, lep4Index_);	  


                            //Dilepton veto
                            if ( ignoreCut(dlepvetoIndex_) ||
                                    (ePlusJets_ && oneElectron) ||
                                    (muPlusJets_ && oneMuon)
                               ){
                                passCut(ret, dlepvetoIndex_);

                                bool cosmicVeto = true;
                                if ( ignoreCut(cosmicIndex_) ||
                                        cosmicVeto ) {
                                    passCut(ret,cosmicIndex_);

                                    if ( ignoreCut(jet1Index_) ||
                                            static_cast<int>(cleanedJets_.size()) >=  1 ){
                                        passCut(ret,jet1Index_);  
                                    } // end if >=1 tight jets

                                    if ( ignoreCut(jet2Index_) ||
                                            static_cast<int>(cleanedJets_.size()) >=  2 ){
                                        passCut(ret,jet2Index_);  
                                    } // end if >=2 tight jets

                                    if ( ignoreCut(jet3Index_) ||
                                            static_cast<int>(cleanedJets_.size()) >=  3 ){
                                        passCut(ret,jet3Index_);  
                                    } // end if >=3 tight jets

                                    if ( ignoreCut(jet4Index_) ||
                                            static_cast<int>(cleanedJets_.size()) >=  4 ){
                                        passCut(ret,jet4Index_);  
                                    } // end if >=4 tight jets

                                    if ( ignoreCut(jet5Index_) ||
                                            static_cast<int>(cleanedJets_.size()) >=  5 ){
                                        passCut(ret,jet5Index_);  
                                    } // end if >=5 tight jets

                                    if ( ignoreCut(jet6Index_) ||
                                            static_cast<int>(cleanedJets_.size()) >=  6 ){
                                        passCut(ret,jet6Index_);  
                                    } // end if >=6 tight jets

                                    if ( ignoreCut(jet7Index_) ||
                                            static_cast<int>(cleanedJets_.size()) >=  7 ){
                                        passCut(ret,jet7Index_);  
                                    } // end if >=7 tight jets

                                    if ( ignoreCut(jet8Index_) ||
                                            static_cast<int>(cleanedJets_.size()) >=  8 ){
                                        passCut(ret,jet8Index_);  
                                    } // end if >=8 tight jets

                                    if ( ignoreCut(jet9Index_) ||
                                            static_cast<int>(cleanedJets_.size()) >=  9 ){
                                        passCut(ret,jet9Index_);  
                                    } // end if >=9 tight jets

                                } // end if cosmic veto	

                            } //end if dilepton veto

                        } // end if == 1 lepton

                    } // end if == 1 tight lepton with a muon veto separately

                } // end if == 1 tight lepton

            } // end if >= 1 lepton

        }// end if PV

    } // end if trigger


    setIgnored(ret);
    return (bool)ret;
}
