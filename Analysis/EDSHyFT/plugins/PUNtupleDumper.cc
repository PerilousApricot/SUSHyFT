#ifndef PUNtupleDumper_h
#define PUNtupleDumper_h

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include <vector>

#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

class PUNtupleDumper : public edm::EDProducer {
public:
  explicit PUNtupleDumper(const edm::ParameterSet& cfg);
  ~PUNtupleDumper();
  
private:
  virtual void beginJob(const edm::EventSetup&) ;
  virtual void produce(edm::Event& event, const edm::EventSetup& setup);
  virtual void endJob() ;

  std::string PUscenario_;
  bool use42X_;

  // used for reweighting
  edm::LumiReWeighting lumiWeights_;
  reweight::PoissonMeanShifter PShiftDown_;
  reweight::PoissonMeanShifter PShiftUp_;
};

#endif

PUNtupleDumper::~PUNtupleDumper(){
}

void PUNtupleDumper::beginJob(const edm::EventSetup&){
}

void PUNtupleDumper::endJob(){
}

PUNtupleDumper::PUNtupleDumper(const edm::ParameterSet& cfg):
  PUscenario_(cfg.getParameter<std::string>("PUscenario"))
{
  produces<std::vector<float> >("PUweightNominalUpDown");
  
  // will need more intelligence here
  if(PUscenario_=="42X") use42X_=true;
  else use42X_=false;

  // copied from   SHyFT::initializeMCPUWeight
  // =========================================
  // should probably add a parameter to configure the era of MC we want to use
  // so the weight can be included - melo 7/2011
  std::vector< float > TrueDist2011;
  float TrueDist2011_f[25] = {
    0.013256,
    0.031699,
    0.071946,
    0.115284,
    0.145239,
    0.152783,
    0.139182,
    0.112847,
    0.082904,
    0.055968,
    0.035100,
    0.020627,
    0.011441,
    0.006026,
    0.003030,
    0.001461,
    0.000678,
    0.000304,
    0.000132,
    0.000056,
    0.000023,
    0.000009,
    0.000004,
    0.000001,
    0.000001
  };
  
  std::vector< float > probdistFlat10;
  float probdistFlat10_d[25] = {
    0.0698146584,
    0.0698146584,
    0.0698146584,
    0.0698146584,
    0.0698146584,
    0.0698146584,
    0.0698146584,
    0.0698146584,
    0.0698146584,
    0.0698146584,
    0.0698146584,
    0.0630151648,
    0.0526654164,
    0.0402754482,
    0.0292988928,
    0.0194384503,
    0.0122016783,
    0.007207042,
    0.004003637,
    0.0020278322,
    0.0010739954,
    0.0004595759,
    0.0002229748,
    0.0001028162,
    4.58337152809607E-05
  };
  
  // Summer11 PU_S4, distribution obtained by averaging the number of interactions
  // in each beam crossing to estimate the true mean.  THIS IS THE RECOMMENDED ONE for reweighting.
  
  std::vector< float > poissonIntDist;
  float poissonIntDist_d[25] = {
    0.104109,
    0.0703573,
    0.0698445,
    0.0698254,
    0.0697054,
    0.0697907,
    0.0696751,
    0.0694486,
    0.0680332,
    0.0651044,
    0.0598036,
    0.0527395,
    0.0439513,
    0.0352202,
    0.0266714,
    0.019411,
    0.0133974,
    0.00898536,
    0.0057516,
    0.00351493,
    0.00212087,
    0.00122891,
    0.00070592,
    0.000384744,
    0.000219377
  };
  
  
  for( int i=0; i<25; ++i) {
    TrueDist2011.push_back(TrueDist2011_f[i]);
    probdistFlat10.push_back(probdistFlat10_d[i]);
    poissonIntDist.push_back(poissonIntDist_d[i]);
  }
  //now do what ever initialization is needed
  if(use42X_){
    lumiWeights_ = edm::LumiReWeighting( poissonIntDist, TrueDist2011);
  }
  else
    lumiWeights_ = edm::LumiReWeighting( probdistFlat10, TrueDist2011);
  
  // will need it for systematics
  PShiftDown_ = reweight::PoissonMeanShifter(-0.5);
  PShiftUp_ = reweight::PoissonMeanShifter(0.5);
 
}


void PUNtupleDumper::produce(edm::Event& event, const edm::EventSetup& setup){
  std::auto_ptr<std::vector<float> > pPUweight ( new std::vector<float> );
  
  //copied from    SHyFT::weightPU
  //==============================
  
  // get weights from MC PU
  edm::Handle<std::vector< PileupSummaryInfo > >  PupInfo;
  event.getByLabel(edm::InputTag("addPileupInfo"), PupInfo);
  std::vector<PileupSummaryInfo>::const_iterator PVI;

  int npv = -1; float sum_nvtx = 0.0; double puweight = -1000.0; 
  double puweightShiftUp = -1000.0; double puweightShiftDown = -1000.0;
  for(PVI = PupInfo->begin(); PVI != PupInfo->end(); ++PVI) {
    
    int BX = PVI->getBunchCrossing();
    
    if(BX == 0 && !use42X_) { //skip the OOT PU for Spring11
      npv = PVI->getPU_NumInteractions();
      continue;
    }
    else {
      npv = PVI->getPU_NumInteractions();
      //cout << npv << endl;
      sum_nvtx += float(npv);
    }
    
  }
  float ave_nvtx = sum_nvtx/3.;
  //std::cout << "sum_nvtx = " << sum_nvtx << "ave_nvtx = "<< ave_nvtx << std::endl;
  //theDir.getObject<TH1>("npuTruth")->Fill(npv, 1.0);
  if(use42X_){
    puweight = lumiWeights_.weight( ave_nvtx);//default for 42X
    puweightShiftUp = puweight * PShiftUp_.ShiftWeight( ave_nvtx );  
    puweightShiftDown = puweight * PShiftDown_.ShiftWeight( ave_nvtx );
  }  
  else{  
    puweight = lumiWeights_.weight( npv ); 
    puweightShiftUp = puweight * PShiftUp_.ShiftWeight( npv );
    puweightShiftDown = puweight * PShiftDown_.ShiftWeight( npv );
  }
  
  //if( puUp_ || puDn_ ) globalWeight_ *= puweightShift; 
  //else               globalWeight_ *= puweight;
  
  pPUweight->push_back(puweight);
  pPUweight->push_back(puweightShiftUp);
  pPUweight->push_back(puweightShiftDown);
  
  event.put(pPUweight, "PUweightNominalUpDown");
  return;
}



#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PUNtupleDumper);
