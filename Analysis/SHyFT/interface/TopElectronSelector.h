/*
Contact:        Sadia Khalil (skhalil@fnal.gov)
*/
#ifndef PhysicsTools_PatUtils_interface_TopElectronSelector_h
#define PhysicsTools_PatUtils_interface_TopElectronSelector_h

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "PhysicsTools/SelectorUtils/interface/Selector.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Common/interface/EventBase.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "EGamma/EGammaAnalysisTools/interface/ElectronEffectiveArea.h"

//Math
#include "CLHEP/Units/GlobalPhysicalConstants.h"
typedef math::XYZPoint Point;

class TopElectronSelector : public Selector<pat::Electron>  {

   public: // interface  

      bool verbose_;
      bool runData_;

      void setUseData(const bool &flag) { runData_ = flag; }
      enum Version_t { VETO, LOOSE, MEDIUM, TIGHT, NONE, N_VERSIONS};
      TopElectronSelector() {}
      

      TopElectronSelector( edm::ParameterSet const & parameters ){

         verbose_ = true;
         
         //runData_= parameters.getParameter<bool>("runData");
         std::string versionStr = parameters.getParameter<std::string>("version");
         Version_t version = N_VERSIONS;
         
         if (versionStr == "VETO"){
            version = VETO;
            if(verbose_) std::cout << "CutBasedElectronSelector: You have choosen version = VETO " <<  std::endl;
         }

         if (versionStr == "LOOSE"){
            version = LOOSE;
            if(verbose_) std::cout << "CutBasedElectronSelector: You have choosen version = LOOSE " <<  std::endl;
         }
         
         if (versionStr == "MEDIUM"){
            version = MEDIUM;
            if(verbose_) std::cout << "CutBasedElectronSelector: You have choosen version = MEDIUM " <<  std::endl;
         }
         
         if (versionStr == "TIGHT"){
            version = TIGHT;
            if(verbose_) std::cout << "CutBasedElectronSelector: You have choosen version = TIGHT " <<  std::endl;
         }

         if ( versionStr == "NONE" ){
            version = NONE;
            if(verbose_){ std::cout << "CutBasedElectronSelector: If you want to use version NONE "
                                    << "then make sure to provide the selection cuts by yourself " << std::endl;}
         }
         initialize( version,
                     parameters.getParameter<Double_t>("deta_EB"), 
                     parameters.getParameter<Double_t>("dphi_EB"),
                     parameters.getParameter<Double_t>("sihih_EB"), 
                     parameters.getParameter<Double_t>("hoe_EB"), 
                     parameters.getParameter<Double_t>("d0_EB"),
                     parameters.getParameter<Double_t>("dZ_EB"),
                     parameters.getParameter<Double_t>("ooemoop_EB"),
                     parameters.getParameter<Double_t>("reliso_EB"),
                     parameters.getParameter<Double_t>("deta_EE"), 
                     parameters.getParameter<Double_t>("dphi_EE"), 
                     parameters.getParameter<Double_t>("sihih_EE"), 
                     parameters.getParameter<Double_t>("hoe_EE"),
                     parameters.getParameter<Double_t>("d0_EE"),
                     parameters.getParameter<Double_t>("dZ_EE"),
                     parameters.getParameter<Double_t>("ooemoop_EE"),
                     parameters.getParameter<Double_t>("reliso_EE"),
                     parameters.getParameter<Int_t>("mHits"),
                     parameters.getParameter<Bool_t>("vtxFitConv")
            );
         
         
          
         if ( parameters.exists("cutsToIgnore") )
            setIgnoredCuts( parameters.getParameter<std::vector<std::string> >("cutsToIgnore") ); 
         
         retInternal_ = getBitTemplate();
         pvSrc_  = parameters.getParameter<edm::InputTag>("pvSrc");
         rhoSrc_ = parameters.getParameter<edm::InputTag>("rhoSrc");
         
      }
      
      void initialize(Version_t version,
                      Double_t sihih_EB, Double_t  dphi_EB, Double_t deta_EB, Double_t hoe_EB, Double_t d0_EB, Double_t dZ_EB, Double_t ooemoop_EB,  
                      Double_t sihih_EE, Double_t  dphi_EE, Double_t deta_EE, Double_t hoe_EE, Double_t d0_EE, Double_t dZ_EE, Double_t ooemoop_EE,
                      Double_t reliso_EB, Double_t reliso_EE, Int_t mHits, Bool_t vtxFitConv)
      {
         version_ = version;

         push_back("deta_EB"    );
         push_back("dphi_EB"    );
         push_back("sihih_EB"   ); 
         push_back("hoe_EB"     );
         push_back("d0_EB"      );
         push_back("dZ_EB"      );         
         push_back("ooemoop_EB" );
         push_back("reliso_EB"  );
         push_back("deta_EE"    );
         push_back("dphi_EE"    );
         push_back("sihih_EE"   );        
         push_back("hoe_EE"     );
         push_back("d0_EE"      );
         push_back("dZ_EE"      ); 
         push_back("ooemoop_EE" );
         push_back("reliso_EE"  );
         push_back("mHits"      );
         push_back("vtxFitConv" );
              
         if (version_ == NONE){
            set("deta_EB",     deta_EB);
            set("dphi_EB",     dphi_EB);
            set("sihih_EB",    sihih_EB);        
            set("hoe_EB",      hoe_EB);
            set("d0_EB",       d0_EB);
            set("dZ_EB",       dZ_EB);
            set("ooemoop_EB",  ooemoop_EB);
            set("reliso_EB",   reliso_EB);
            set("deta_EE",     deta_EE);
            set("dphi_EE",     dphi_EE);
            set("sihih_EE",    sihih_EE);        
            set("hoe_EE",      hoe_EE);
            set("d0_EB",       d0_EE);
            set("dZ_EB",       dZ_EE);
            set("ooemoop_EE",  ooemoop_EE); 
            set("reliso_EE",   reliso_EE);
            set("mHits",       mHits);
            set("vtxFitConv",  vtxFitConv); 
           }
          
          if (version_ == VETO) {
            set("deta_EB",     7.0e-03);
            set("dphi_EB",     8.0e-01);
            set("sihih_EB",    1.0e-02);
            set("hoe_EB",      1.5e-01); 
            set("d0_EB",       4.0e-02);
            set("dZ_EB",       2.0e-01); 
            set("ooemoop_EB",  false);
            set("reliso_EB",   1.5e-01);
            set("deta_EE",     1.0e-02);
            set("dphi_EE",     7.0e-01);
            set("sihih_EE",    3.0e-02);
            set("hoe_EE",      false);//
            set("d0_EE",       4.0e-02);
            set("dZ_EE",       2.0e-01);
            set("ooemoop_EE",  false);
            set("reliso_EE",   1.5e-01);
            set("mHits",       false);
            set("vtxFitConv",  false); 
         }
         
         if (version_ == LOOSE) {
            set("deta_EB",     7.0e-03);
            set("dphi_EB",     1.5e-02);
            set("sihih_EB",    1.0e-02);
            set("hoe_EB",      1.2e-01);
            set("d0_EB",       2.0e-02);
            set("dZ_EB",       2.0e-01); 
            set("ooemoop_EB",  5.0e-02);
            set("reliso_EB",   1.5e-01);
            set("deta_EE",     9.0e-03);
            set("dphi_EE",     1.0e-01);
            set("sihih_EE",    3.0e-02);
            set("hoe_EE",      1.0e-02);
            set("d0_EE",       2.0e-02);
            set("dZ_EE",       2.0e-01);
            set("ooemoop_EE",  5.0e-02);
            set("reliso_EE",   1.5e-01);//
            set("mHits",       1);
            set("vtxFitConv",  1);
         }

          if (version_ == MEDIUM) {
            set("deta_EB",     4.0e-03);
            set("dphi_EB",     6.0e-02);
            set("sihih_EB",    1.0e-02);
            set("hoe_EB",      1.2e-01); 
            set("d0_EB",       2.0e-02);
            set("dZ_EB",       1.0e-01); 
            set("ooemoop_EB",  5.0e-02);
            set("reliso_EB",   1.5e-01);
            set("deta_EE",     7.0e-03);
            set("dphi_EE",     3.0e-02);
            set("sihih_EE",    3.0e-02);
            set("hoe_EE",      1.0e-02);
            set("d0_EE",       2.0e-02);
            set("dZ_EE",       1.0e-01);
            set("ooemoop_EE",  5.0e-02);
            set("reliso_EE",   1.5e-01);//
            set("mHits",       1);
            set("vtxFitConv",  1);
         }

          if (version_ == TIGHT) {
            set("deta_EB",     4.0e-03);
            set("dphi_EB",     3.0e-02);
            set("sihih_EB",    1.0e-02);
            set("hoe_EB",      1.2e-01); 
            set("d0_EB",       2.0e-02);
            set("dZ_EB",       1.0e-01); 
            set("ooemoop_EB",  5.0e-02);
            set("reliso_EB",   1.0e-01);
            set("deta_EE",     5.0e-03);
            set("dphi_EE",     2.0e-02);
            set("sihih_EE",    3.0e-02);
            set("hoe_EE",      1.0e-02);
            set("d0_EE",       2.0e-02);
            set("dZ_EE",       1.0e-01);
            set("ooemoop_EE",  5.0e-02);
            set("reliso_EE",   1.0e-01);//
            set("mHits",       0);
            set("vtxFitConv",  1);
         }

          indexSinhih_EB_     = index_type(&bits_, "sihih_EB"     ); 
          indexDphi_EB_       = index_type(&bits_, "dphi_EB"      );
          indexDeta_EB_       = index_type(&bits_, "deta_EB"      ); 
          indexHoE_EB_        = index_type(&bits_, "hoe_EB"       ); 
          indexD0_EB_         = index_type(&bits_, "d0_EB"        );
          indexDZ_EB_         = index_type(&bits_, "dZ_EB"        );
          indexOoemoop_EB_    = index_type(&bits_, "ooemoop_EB"   );
          indexRelIso_EB_     = index_type(&bits_, "reliso_EB"    );
          indexSinhih_EE_     = index_type(&bits_, "sihih_EE"     ); 
          indexDphi_EE_       = index_type(&bits_, "dphi_EE"      );
          indexDeta_EE_       = index_type(&bits_, "deta_EE"      ); 
          indexHoE_EE_        = index_type(&bits_, "hoe_EE"       ); 
          indexD0_EE_         = index_type(&bits_, "d0_EE"        );
          indexDZ_EE_         = index_type(&bits_, "dZ_EE"        );
          indexOoemoop_EE_    = index_type(&bits_, "ooemoop_EE"   ); 
          indexRelIso_EE_     = index_type(&bits_, "reliso_EE"    );
          indexMHits_         = index_type(&bits_, "mHits"        ); 
          indexVtxFitConv_    = index_type(&bits_, "vtxFitConv"   );   
      }

      using Selector<pat::Electron>::operator();
      

      // Allow for multiple definitions of the cuts. 

      bool operator()( const pat::Electron & electron, edm::EventBase const & event, pat::strbitset & ret)
      {
         edm::Handle<std::vector<reco::Vertex> > pvtxHandle;
         event.getByLabel( pvSrc_, pvtxHandle);
         if ( pvtxHandle->size() > 0 ) {
            PVtx = pvtxHandle->at(0).position();
         } else {
            throw cms::Exception("InvalidInput") << " There needs to be at least one primary vertex in the event." << std::endl;
         }

         edm::Handle<double> rhoHandle;
         event.getByLabel(rhoSrc_, rhoHandle);
         rhoIso = std::max(*(rhoHandle.product()), 0.0);

         return operator()(electron, ret);
      }
      
      //Spring 12 cuts
      bool operator()( const pat::Electron & electron, pat::strbitset & ret) 
      {    
         ret.set(false);
         Double_t scEta   = electron.superCluster()->eta();
         Double_t AEff  = 0;
         if(runData_){
            AEff    = ElectronEffectiveArea::GetElectronEffectiveArea(ElectronEffectiveArea::kEleGammaAndNeutralHadronIso03, scEta, ElectronEffectiveArea::kEleEAData2011);
         }else{
            AEff    = ElectronEffectiveArea::GetElectronEffectiveArea(ElectronEffectiveArea::kEleGammaAndNeutralHadronIso03, scEta, ElectronEffectiveArea::kEleEAFall11MC);
         }
         Double_t chIso = electron.chargedHadronIso();
         Double_t nhIso = electron.neutralHadronIso();
         Double_t phIso = electron.photonIso();
         Double_t Deta  = electron.deltaEtaSuperClusterTrackAtVtx();
         Double_t Dphi  = electron.deltaPhiSuperClusterTrackAtVtx(); 
         Double_t sihih = electron.sigmaIetaIeta();
         Double_t HoE   = electron.hadronicOverEm();  
         Double_t D0    = electron.dB();
         Double_t DZ    = electron.gsfTrack()->dz(PVtx);//
         Double_t Ooemoop = (1.0/electron.ecalEnergy() - electron.eSuperClusterOverP()/electron.ecalEnergy());
         Double_t RelIso  = ( chIso + max(0.0, nhIso + phIso - rhoIso*AEff) )/ electron.ecalDrivenMomentum().pt();
         Int_t mHits   =  electron.gsfTrack()->trackerExpectedHitsInner().numberOfHits();
         Bool_t vtxFitConv = electron.passConversionVeto();

         // now apply the cuts
         if (electron.isEB()) { // BARREL case
            // check the EB cuts
            if ( fabs(Deta)    <  cut(indexDeta_EB_,  double()) || ignoreCut(indexDeta_EB_)  ) passCut(ret, indexDeta_EB_);
            if ( fabs(Dphi)    <  cut(indexDphi_EB_,  double()) || ignoreCut(indexDphi_EB_)  ) passCut(ret, indexDphi_EB_);
            if ( sihih         <  cut(indexSinhih_EB_,double()) || ignoreCut(indexSinhih_EB_)) passCut(ret, indexSinhih_EB_);           
            if ( HoE           <  cut(indexHoE_EB_,   double()) || ignoreCut(indexHoE_EB_)   ) passCut(ret, indexHoE_EB_);
            if ( fabs(D0)      <  cut(indexD0_EB_,    double()) || ignoreCut(indexD0_EB_)    ) passCut(ret, indexD0_EB_);
            if ( fabs(DZ)      <  cut(indexDZ_EB_,    double()) || ignoreCut(indexDZ_EB_)    ) passCut(ret, indexDZ_EB_);
            if ( fabs(Ooemoop) <  cut(indexOoemoop_EB_, double()) || ignoreCut(indexOoemoop_EB_) ) passCut(ret, indexOoemoop_EB_); 
            if ( RelIso        <  cut(indexRelIso_EB_, double()) || ignoreCut(indexRelIso_EB_) ) passCut(ret, indexRelIso_EB_);  
            // pass all the EE cuts
           	passCut(ret, indexDeta_EE_);
            passCut(ret, indexDphi_EE_);
	        passCut(ret, indexSinhih_EE_);
            passCut(ret, indexHoE_EE_);	
            passCut(ret, indexD0_EE_);
            passCut(ret, indexDZ_EE_);
            passCut(ret, indexOoemoop_EE_);
            passCut(ret, indexRelIso_EE_);
         } else if (electron.isEE()) {  // ENDCAPS case
            // check the EE cuts
            if ( fabs(Deta)    <  cut(indexDeta_EE_,  double()) || ignoreCut(indexDeta_EE_)  ) passCut(ret, indexDeta_EE_);
            if ( fabs(Dphi)    <  cut(indexDphi_EE_,  double()) || ignoreCut(indexDphi_EE_)  ) passCut(ret, indexDphi_EE_);
            if ( sihih         <  cut(indexSinhih_EE_,double()) || ignoreCut(indexSinhih_EE_)) passCut(ret, indexSinhih_EE_);
            if ( HoE           <  cut(indexHoE_EE_,   double()) || ignoreCut(indexHoE_EE_)   ) passCut(ret, indexHoE_EE_);
            if ( D0            <  cut(indexD0_EE_,    double()) || ignoreCut(indexD0_EE_)    ) passCut(ret, indexD0_EE_);
            if ( DZ            <  cut(indexDZ_EE_,    double()) || ignoreCut(indexDZ_EE_)    ) passCut(ret, indexDZ_EE_);
            if ( fabs(Ooemoop) <  cut(indexOoemoop_EE_, double()) || ignoreCut(indexOoemoop_EE_) ) passCut(ret, indexOoemoop_EE_); 
            if ( RelIso        <  cut(indexRelIso_EE_, double()) || ignoreCut(indexRelIso_EE_) ) passCut(ret, indexRelIso_EE_); 
            // pass all the EB cuts
            passCut(ret, indexDeta_EB_);
            passCut(ret, indexDphi_EB_);	
            passCut(ret, indexSinhih_EB_);
            passCut(ret, indexHoE_EB_);
            passCut(ret, indexD0_EB_);
            passCut(ret, indexDZ_EB_);
            passCut(ret, indexOoemoop_EB_);
            passCut(ret, indexRelIso_EB_);
           
         }
            if ( mHits         <=  cut(indexMHits_, int()) || ignoreCut(indexMHits_) ) passCut(ret, indexMHits_);
            if (vtxFitConv     ==  cut(indexVtxFitConv_, bool()) || ignoreCut(indexVtxFitConv_) ) passCut(ret, indexVtxFitConv_);
        
         setIgnored(ret);   
         return (bool)ret;
      }
    
   private: // member variables
      Version_t version_;
      edm::InputTag pvSrc_;
      Point PVtx;
      edm::InputTag rhoSrc_;
      Double_t rhoIso;
      index_type indexSinhih_EB_;
      index_type indexDphi_EB_;
      index_type indexDeta_EB_;
      index_type indexHoE_EB_;
      index_type indexD0_EB_;
      index_type indexDZ_EB_; 
      index_type indexOoemoop_EB_;
      index_type indexRelIso_EB_;
      index_type indexSinhih_EE_;
      index_type indexDphi_EE_;
      index_type indexDeta_EE_;
      index_type indexHoE_EE_;
      index_type indexD0_EE_;
      index_type indexDZ_EE_;
      index_type indexOoemoop_EE_;
      index_type indexRelIso_EE_;
      index_type indexMHits_;
      index_type indexVtxFitConv_;
};

#endif
