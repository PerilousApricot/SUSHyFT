// -*- C++ -*-
//
// Package:    PATElectronUserData
// Class:      PATElectronUserData
// 
/**\class PATElectronUserData PATElectronUserData.cc User/PATElectronUserData/src/PATElectronUserData.cc

 Description: <one line class summary>

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  Malina Kirn
//         Created:  Tue Mar 17 15:19:19 EDT 2009
// $Id: PATElectronUserData.cc,v 1.1 2010/10/24 04:17:08 srappocc Exp $
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
//#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
//#include "RecoLocalCalo/EcalRecAlgos/interface/EcalSeverityLevelAlgo.h"

#include "RecoEgamma/EgammaTools/interface/ConversionFinder.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackExtra.h"
#include "DataFormats/Scalers/interface/DcsStatus.h"

//
// class decleration
//

class PATElectronUserData : public edm::EDProducer {
   public:
      explicit PATElectronUserData(const edm::ParameterSet&);
      ~PATElectronUserData();

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      // ----------member data ---------------------------
      edm::InputTag src_;
      //edm::InputTag ecalRecHitsEBsrc_;
      bool isDataInput_;

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
PATElectronUserData::PATElectronUserData(const edm::ParameterSet& iConfig):  
  src_(iConfig.getParameter<edm::InputTag>("src")),
  //ecalRecHitsEBsrc_(iConfig.getParameter<edm::InputTag>("ecalRecHitsEBsrc")),
  isDataInput_ (iConfig.getParameter<bool>("useData"))
{
  produces<std::vector<pat::Electron> >();
}


PATElectronUserData::~PATElectronUserData()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
PATElectronUserData::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  
    // collection needed for conversions
    double bField = 3.801;
    //Get gTracks and  magneticField to get conversion info
    edm::Handle<reco::TrackCollection> gTracks;
    iEvent.getByLabel("generalTracks", gTracks);
    if (!gTracks.isValid()) {
      edm::LogError ("reading gTracks not found");
      return;
    }
    edm::Handle<DcsStatusCollection> dcsStatus;
    iEvent.getByLabel("scalersRawToDigi", dcsStatus);
    if (!dcsStatus.isValid()) {
      edm::LogError ("reading dcsStatus not found");
      return;
    }
    if(!isDataInput_){
       //std::cout<<"using MC -->" << std::endl;
      edm::ESHandle<MagneticField> magneticField;
      iSetup.get<IdealMagneticFieldRecord>().get(magneticField);
      bField = magneticField->inTesla(GlobalPoint(0.,0.,0.)).z();
    }
    else{
       //std::cout<<"using Data -->" << std::endl;
      float currentToBFieldScaleFactor = 2.09237036221512717e-04;
      float current = -10.;
      if( (*dcsStatus).size() != 0 ) {
        current = (*dcsStatus)[0].magnetCurrent();
        bField = current*currentToBFieldScaleFactor;
      }
      else bField  = 3.801;
    }
  
  edm::Handle<edm::View<pat::Electron> > electrons;
  iEvent.getByLabel(src_,electrons);
/*
  // For 'swiss cross' spike cleaning in 36x data
  edm::Handle<EcalRecHitCollection> recHits;
  iEvent.getByLabel(ecalRecHitsEBsrc_, recHits);
  const EcalRecHitCollection *myRecHits = recHits.product();
*/
  std::auto_ptr<std::vector<pat::Electron> > output(new std::vector<pat::Electron>());
  for (edm::View<pat::Electron>::const_iterator electron = electrons->begin(), end = electrons->end(); electron != end; ++electron) {
    pat::Electron myElectron = *electron; // copy
    

    ConversionFinder convFinder;
    ConversionInfo convInfo = convFinder.getConversionInfo(*electron, gTracks, bField);
    float el_dist = convInfo.dist();
    float el_dcot = convInfo.dcot();
    //if(el_dist!=0 && el_dcot!=0){
    // std::cout << "dist = " <<el_dist <<",dcot= " << el_dcot<<std::endl; 
    //}
    myElectron.addUserFloat("el_dist", el_dist);
    myElectron.addUserFloat("el_dcot", el_dcot);

    float combRelIso = (electron->dr03TkSumPt()+electron->dr03EcalRecHitSumEt()+electron->dr03HcalTowerSumEt())/electron->et();
    myElectron.addUserFloat("CombRelIso", combRelIso);
/*
    const reco::CaloClusterPtr seed = electron->superCluster()->seed(); // seed cluster                                 
    DetId seedId = seed->seed();
    EcalSeverityLevelAlgo severity;
    float mySwissCross = severity.swissCross(seedId, *myRecHits);
    myElectron.addUserFloat("SwissCross", mySwissCross);
*/
    output->push_back(myElectron);
  }
  //std::cout << "writting the good electrons" << std::endl;
  iEvent.put(output); 
}

// ------------ method called once each job just before starting event loop  ------------
void 
PATElectronUserData::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
PATElectronUserData::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(PATElectronUserData);
