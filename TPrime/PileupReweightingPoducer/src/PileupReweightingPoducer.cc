
// -*- C++ -*-
//
// Package:    PileupReweightingPoducer
// Class:      PileupReweightingPoducer
// 
/**\class PileupReweightingPoducer PileupReweightingPoducer.cc TPrime/PileupReweightingPoducer/src/PileupReweightingPoducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Ricardo Vasquez Sierra,6 R-025,+41227672274,
//         Created:  Mon Nov 21 15:05:26 CET 2011
// $Id: PileupReweightingPoducer.cc,v 1.5 2012/05/25 13:25:18 vasquez Exp $
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
#include "PhysicsTools/Utilities/interface/Lumi3DReWeighting.h"
#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h" 
#include <vector>

//
// class declaration
//

class PileupReweightingPoducer : public edm::EDProducer {
   public:
      explicit PileupReweightingPoducer(const edm::ParameterSet&);
      ~PileupReweightingPoducer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual void beginRun(edm::Run&, edm::EventSetup const&);
      virtual void endRun(edm::Run&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

      // ----------member data ---------------------------

  bool firsttime_;
  bool oneD_;
  std::string pileupMC_;
  std::string pileupData_;
  edm::Lumi3DReWeighting Lumi3DWeightsNominal_;
  edm::Lumi3DReWeighting Lumi3DWeightsUp_;
  edm::Lumi3DReWeighting Lumi3DWeightsDown_;

  edm::LumiReWeighting LumiWeightsNominal_;
  reweight::PoissonMeanShifter PShiftDown_;
  reweight::PoissonMeanShifter PShiftUp_;

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

PileupReweightingPoducer::PileupReweightingPoducer(const edm::ParameterSet& iConfig)
{
//   firsttime_= iConfig.existsAs<bool>("FirstTime") ? iConfig.getParameter<bool>("FirstTime") : true ;
//   pileupMC_ = iConfig.existsAs<std::string>("PileupMCFile") ? iConfig.getParameter<std::string>("PileupMCFile") : "PUMC_dist.root" ;
//   pileupData_ = iConfig.existsAs<std::string>("PileupDataFile") ? iConfig.getParameter<std::string>("PileupDataFile") : "PUData_dist.root" ;

  firsttime_ =  iConfig.getUntrackedParameter<bool>("FirstTime");
  oneD_  = iConfig.getUntrackedParameter<bool>("oneDReweighting");
  pileupMC_ =  iConfig.getUntrackedParameter<std::string>("PileupMCFile");
  pileupData_ = iConfig.getUntrackedParameter<std::string>("PileupDataFile");

  //register your products
  
  // Distribution used for Fall2011 MC.
  
  std::vector<float> Fall2011MC;
  Double_t Fall2011[50] = {
    0.003388501,
    0.010357558,
    0.024724258,
    0.042348605,
    0.058279812,
    0.068851751,
    0.072914824,
    0.071579609,
    0.066811668,
    0.060672356,
    0.054528356,
    0.04919354,
    0.044886042,
    0.041341896,
    0.0384679,
    0.035871463,
    0.03341952,
    0.030915649,
    0.028395374,
    0.025798107,
    0.023237445,
    0.020602754,
    0.0180688,
    0.015559693,
    0.013211063,
    0.010964293,
    0.008920993,
    0.007080504,
    0.005499239,
    0.004187022,
    0.003096474,
    0.002237361,
    0.001566428,
    0.001074149,
    0.000721755,
    0.000470838,
    0.00030268,
    0.000184665,
    0.000112883,
    6.74043E-05,
    3.82178E-05,
    2.22847E-05,
    1.20933E-05,
    6.96173E-06,
    3.4689E-06,
    1.96172E-06,
    8.49283E-07,
    5.02393E-07,
    2.15311E-07,
    9.56938E-08
  };


  
  std::vector<float> TargetFall2011;
  Double_t TargetFall11[50] = {
    0.00111236, 
    0.000248044, 
    0.00180471, 
    0.0239756, 
    0.0761929, 
    0.10688, 
    0.107854, 
    0.0985592, 
    0.0877882, 
    0.0807251, 
    0.0746043, 
    0.0694981, 
    0.0656867, 
    0.0605124, 
    0.0519228, 
    0.0397695, 
    0.026414, 
    0.0149724, 
    0.00717431, 
    0.00289899, 
    0.000997382, 
    0.000299485, 
    8.14627e-05, 
    2.0927e-05, 
    5.26531e-06, 
    1.32461e-06, 
    3.33011e-07, 
    8.33706e-08, 
    2.20579e-08, 
    8.27493e-09, 
    6.6658e-09, 
    8.80665e-09, 
    1.28408e-08, 
    1.83892e-08, 
    2.53083e-08, 
    3.33488e-08, 
    4.20473e-08, 
    5.07188e-08, 
    5.85266e-08, 
    6.46128e-08, 
    6.82679e-08, 
    6.90279e-08, 
    6.6734e-08, 
    6.17617e-08, 
    5.46921e-08, 
    4.63326e-08, 
    3.75497e-08, 
    2.91145e-08, 
    2.15987e-08, 
    1.53316e-08
  };

  for( int i=0; i < 50; ++i) {
    Fall2011MC.push_back(Fall2011[i]);
    TargetFall2011.push_back(TargetFall11[i]);
  }
  
  produces<std::vector<float> >( "pileupWeights" ).setBranchAlias( "pileupWeights" );

  if ( oneD_ )
    {
      std::cout<< " Doing 1D pileupreweighting " << std::endl;
      LumiWeightsNominal_ = edm::LumiReWeighting( Fall2011MC, TargetFall2011);
      PShiftDown_ = reweight::PoissonMeanShifter(-0.5);
      PShiftUp_ = reweight::PoissonMeanShifter(0.5);

    }
  else
    {
      if ( firsttime_ )
	{

	  std::cout<< " Initializing with the following files MC: " << pileupMC_ << " data: " << pileupData_ << std::endl;
	  Lumi3DWeightsNominal_.weight3D_set( pileupMC_, pileupData_, "pileup", "pileup", "Weight3D.root");
	  Lumi3DWeightsUp_.weight3D_set( pileupMC_, pileupData_, "pileup", "pileup", "Weight3DscaleUp.root");
	  Lumi3DWeightsDown_.weight3D_set( pileupMC_, pileupData_, "pileup", "pileup", "Weight3DscaleDown.root");
	  
	  Lumi3DWeightsNominal_.weight3D_init(1.0);
	  Lumi3DWeightsUp_.weight3D_init(1.08);
	  Lumi3DWeightsDown_.weight3D_init(0.92);
	}
      else 
	{
	  std::cout<< " Initializing with Weight3D.root " << std::endl; 
	  Lumi3DWeightsNominal_.weight3D_init("Weight3D.root");
	  Lumi3DWeightsUp_.weight3D_init("Weight3DscaleUp.root");
	  Lumi3DWeightsDown_.weight3D_init("Weight3DscaleDown.root");
	}
    }
}


PileupReweightingPoducer::~PileupReweightingPoducer()
{
 
   // do anything here that needs to be done at destruction time
   // (e.g. close files, deallocate resources etc.)

}

// ------------ method called to produce the data  ------------
void
PileupReweightingPoducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{


  double nominalWeight = -1.0;
  double weightUp = -1.0;
  double weightDown = -1.0;


  std::auto_ptr<std::vector<float> > pileupWeights( new std::vector<float> );

  if (oneD_)
     {
       //       std::cout << " producing: " << std::endl;
       edm::Handle<std::vector< PileupSummaryInfo > >  PupInfo;
       iEvent.getByLabel(edm::InputTag("addPileupInfo"), PupInfo);
       //       std::cout<< "found product size: " << PupInfo->size() << std::endl;
       std::vector<PileupSummaryInfo>::const_iterator PVI;

       float sum_nvtx = 0;

       for(PVI = PupInfo->begin(); PVI != PupInfo->end(); ++PVI) {

	 int npv = PVI->getPU_NumInteractions();

	 sum_nvtx += float(npv);
       }

       float ave_nvtx = sum_nvtx/3.;

       //       std::cout<< " average: " << ave_nvtx << std::endl; 
       //       std::cout<< " TRUE : " << PupInfo->getTrueNumInteractions() 
       nominalWeight = LumiWeightsNominal_.weight(ave_nvtx);
       weightUp = nominalWeight*PShiftUp_.ShiftWeight(ave_nvtx);
       weightDown = nominalWeight*PShiftDown_.ShiftWeight(ave_nvtx);
       
     }
   else 
     {
       edm::EventBase* iEventB = dynamic_cast<edm::EventBase*>(&iEvent);
       nominalWeight = Lumi3DWeightsNominal_.weight3D( (*iEventB) );
       weightUp = Lumi3DWeightsUp_.weight3D( (*iEventB) );
       weightDown = Lumi3DWeightsDown_.weight3D( (*iEventB) );
     }

   pileupWeights->push_back( nominalWeight );
   pileupWeights->push_back( weightUp );
   pileupWeights->push_back( weightDown );

   iEvent.put(pileupWeights, "pileupWeights");
   
}

// ------------ method called once each job just before starting event loop  ------------
void 
PileupReweightingPoducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
PileupReweightingPoducer::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
PileupReweightingPoducer::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
PileupReweightingPoducer::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
PileupReweightingPoducer::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
PileupReweightingPoducer::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
PileupReweightingPoducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(PileupReweightingPoducer);
