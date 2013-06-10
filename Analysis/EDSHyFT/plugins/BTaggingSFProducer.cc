// system include files
#include <memory>
#include <iostream>
#include <string>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "Analysis/EDSHyFT/plugins/BTagSFUtil_tprime.h"
#include "TFile.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TF1.h"

class BTaggingSFProducer : public edm::EDProducer {
public:
  explicit BTaggingSFProducer(const edm::ParameterSet&);
  ~BTaggingSFProducer();
  
private:
  virtual void beginJob() ;
  virtual void produce(edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
  
  // ----------member data --------------------------
  edm::InputTag jetSource_;
  std::string discriminatorTag_;
  double discriminatorValue_;
  std::string effMapFile_;

  TF1  *CSVM_SFb_0to2p4;
  TH1D *CSVM_SFb_errors;

  TF1 *CSVM_SFl_0to2p4;
  TF1 *CSVM_SFl_0to0p8;
  TF1 *CSVM_SFl_0p8to1p6;
  TF1 *CSVM_SFl_1p6to2p4;

  TF1 *CSVM_SFl_0to2p4_min;
  TF1 *CSVM_SFl_0to0p8_min;
  TF1 *CSVM_SFl_0p8to1p6_min;
  TF1 *CSVM_SFl_1p6to2p4_min;

  TF1 *CSVM_SFl_0to2p4_max;
  TF1 *CSVM_SFl_0to0p8_max;
  TF1 *CSVM_SFl_0p8to1p6_max;
  TF1 *CSVM_SFl_1p6to2p4_max;

  double SFb_Unc_MultFactor;
  TF1 *CSVM_SFl_Corr;

  TFile *f_EffMap;

  TH2D *h2_EffMapB;
  TH2D *h2_EffMapC;
  TH2D *h2_EffMapUDSG;
};

BTaggingSFProducer::BTaggingSFProducer(const edm::ParameterSet& iConfig)
{
  jetSource_= iConfig.getParameter<edm::InputTag>("JetSource");
  discriminatorTag_ = iConfig.getParameter<std::string>("DiscriminatorTag");
  discriminatorValue_ = iConfig.getParameter<double>("DiscriminatorValue");
  effMapFile_ = iConfig.getParameter<std::string>("EffMapFile");

  double PtBins[] = {30, 40, 50, 60, 70, 80, 100, 120, 160, 210, 260, 320, 400, 500, 670};

  CSVM_SFb_0to2p4 = new TF1("CSVM_SFb_0to2p4","0.6981*((1.+(0.414063*x))/(1.+(0.300155*x)))", 30.,670.);

  CSVM_SFb_errors = new TH1D("CSVM_SFb_errors", "CSVM_SFb_errors", 14, PtBins);
  CSVM_SFb_errors->SetBinContent( 0,0.12);
  CSVM_SFb_errors->SetBinContent( 1,0.0295675);
  CSVM_SFb_errors->SetBinContent( 2,0.0295095);
  CSVM_SFb_errors->SetBinContent( 3,0.0210867);
  CSVM_SFb_errors->SetBinContent( 4,0.0219349);
  CSVM_SFb_errors->SetBinContent( 5,0.0227033);
  CSVM_SFb_errors->SetBinContent( 6,0.0204062);
  CSVM_SFb_errors->SetBinContent( 7,0.0185857);
  CSVM_SFb_errors->SetBinContent( 8,0.0256242);
  CSVM_SFb_errors->SetBinContent( 9,0.0383341);
  CSVM_SFb_errors->SetBinContent(10,0.0409675);
  CSVM_SFb_errors->SetBinContent(11,0.0420284);
  CSVM_SFb_errors->SetBinContent(12,0.0541299);
  CSVM_SFb_errors->SetBinContent(13,0.0578761);
  CSVM_SFb_errors->SetBinContent(14,0.0655432);
  CSVM_SFb_errors->SetBinContent(15,(2*0.0655432));

  CSVM_SFl_0to2p4 =   new TF1("CSVM_SFl_0to2p4","((1.04318+(0.000848162*x))+(-2.5795e-06*(x*x)))+(1.64156e-09*(x*(x*x)))", 20.,670.);
  CSVM_SFl_0to0p8 =   new TF1("CSVM_SFl_0to0p8","((1.06182+(0.000617034*x))+(-1.5732e-06*(x*x)))+(3.02909e-10*(x*(x*x)))", 20.,670.);
  CSVM_SFl_0p8to1p6 = new TF1("CSVM_SFl_0p8to1p6","((1.111+(-9.64191e-06*x))+(1.80811e-07*(x*x)))+(-5.44868e-10*(x*(x*x)))", 20.,670.);
  CSVM_SFl_1p6to2p4 = new TF1("CSVM_SFl_1p6to2p4","((1.08498+(-0.000701422*x))+(3.43612e-06*(x*x)))+(-4.11794e-09*(x*(x*x)))", 20.,670.);

  CSVM_SFl_0to2p4_min =   new TF1("CSVM_SFl_0to2p4_min","((0.962627+(0.000448344*x))+(-1.25579e-06*(x*x)))+(4.82283e-10*(x*(x*x)))", 20.,670.);
  CSVM_SFl_0to0p8_min =   new TF1("CSVM_SFl_0to0p8_min","((0.972455+(7.51396e-06*x))+(4.91857e-07*(x*x)))+(-1.47661e-09*(x*(x*x)))", 20.,670.);
  CSVM_SFl_0p8to1p6_min = new TF1("CSVM_SFl_0p8to1p6_min","((1.02055+(-0.000378856*x))+(1.49029e-06*(x*x)))+(-1.74966e-09*(x*(x*x)))", 20.,670.);
  CSVM_SFl_1p6to2p4_min = new TF1("CSVM_SFl_1p6to2p4_min","((0.983476+(-0.000607242*x))+(3.17997e-06*(x*x)))+(-4.01242e-09*(x*(x*x)))", 20.,670.);

  CSVM_SFl_0to2p4_max =   new TF1("CSVM_SFl_0to2p4_max","((1.12368+(0.00124806*x))+(-3.9032e-06*(x*x)))+(2.80083e-09*(x*(x*x)))", 20.,670.);
  CSVM_SFl_0to0p8_max =   new TF1("CSVM_SFl_0to0p8_max","((1.15116+(0.00122657*x))+(-3.63826e-06*(x*x)))+(2.08242e-09*(x*(x*x)))", 20.,670.);
  CSVM_SFl_0p8to1p6_max = new TF1("CSVM_SFl_0p8to1p6_max","((1.20146+(0.000359543*x))+(-1.12866e-06*(x*x)))+(6.59918e-10*(x*(x*x)))", 20.,670.);
  CSVM_SFl_1p6to2p4_max = new TF1("CSVM_SFl_1p6to2p4_max","((1.18654+(-0.000795808*x))+(3.69226e-06*(x*x)))+(-4.22347e-09*(x*(x*x)))", 20.,670.);

  SFb_Unc_MultFactor = 1.5;
  CSVM_SFl_Corr = new TF1("CSVM_SFl_Corr","(1.10422 + (-0.000523856*x) + (1.14251e-06*(x*x)))", 0.,670.);

  edm::FileInPath fipEffMap(effMapFile_);

  f_EffMap = new TFile(fipEffMap.fullPath().c_str());

  h2_EffMapB    = (TH2D*)f_EffMap->Get("efficiency_b");
  h2_EffMapC    = (TH2D*)f_EffMap->Get("efficiency_c");
  h2_EffMapUDSG = (TH2D*)f_EffMap->Get("efficiency_udsg");

  produces< std::vector< pat::Jet > >();
}

BTaggingSFProducer::~BTaggingSFProducer()
{
}

// ------------ method called to produce the data  ------------
void
BTaggingSFProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  using namespace reco;

  edm::Handle<std::vector<pat::Jet > > jetsH;
  iEvent.getByLabel(jetSource_, jetsH);

  std::auto_ptr< std::vector<pat::Jet> > jetsBtags( new std::vector<pat::Jet> (*jetsH) );

  int runNumber = iEvent.id().run();
  int eventNumber = iEvent.id().event();

  BTagSFUtil btaggingUtility( runNumber+eventNumber );

  for ( std::vector<pat::Jet>::iterator jetIt = jetsBtags->begin(); jetIt != jetsBtags->end(); ++jetIt )
  {
    // Get the mistag efficiency and the light and heavy flavour tagging scale factors
    double ScaleFactor;
    double ScaleFactor_up;
    double ScaleFactor_down;
    double ScaleFactor_unc;
    double tagEfficiency;

    int parton = jetIt->partonFlavour();

    bool btag = false;
    bool btagNominal = false;
    bool btagUp = false;
    bool btagDown = false;

    if ( jetIt->bDiscriminator(discriminatorTag_.c_str()) >= discriminatorValue_ ) btag = true;

    // if b jet
    if ( abs(parton) == 5 )
    {
      double jetPt = jetIt->pt();
      if ( jetPt>670. ) jetPt = 670.;
      else if ( jetPt<30. ) jetPt = 30.;

      ScaleFactor     = CSVM_SFb_0to2p4->Eval(jetPt);
      ScaleFactor_unc = CSVM_SFb_errors->GetBinContent(CSVM_SFb_errors->GetXaxis()->FindBin(jetIt->pt()));

      ScaleFactor_up   = ScaleFactor + SFb_Unc_MultFactor*ScaleFactor_unc;
      ScaleFactor_down = ScaleFactor - SFb_Unc_MultFactor*ScaleFactor_unc;

      tagEfficiency = h2_EffMapB->GetBinContent( h2_EffMapB->GetXaxis()->FindBin(jetIt->pt()), h2_EffMapB->GetYaxis()->FindBin(fabs(jetIt->eta())) );
    }
    // if c jet
    else if ( abs(parton) == 4 )
    {
      double jetPt = jetIt->pt();
      if ( jetPt>670. ) jetPt = 670.;
      else if ( jetPt<30. ) jetPt = 30.;

      ScaleFactor     = CSVM_SFb_0to2p4->Eval(jetPt);
      ScaleFactor_unc = CSVM_SFb_errors->GetBinContent(CSVM_SFb_errors->GetXaxis()->FindBin(jetIt->pt()));

      ScaleFactor_up   = ScaleFactor + 2*SFb_Unc_MultFactor*ScaleFactor_unc;
      ScaleFactor_down = ScaleFactor - 2*SFb_Unc_MultFactor*ScaleFactor_unc;

      tagEfficiency = h2_EffMapC->GetBinContent( h2_EffMapC->GetXaxis()->FindBin(jetIt->pt()), h2_EffMapC->GetYaxis()->FindBin(fabs(jetIt->eta())) );
    }
    else
    {
      double jetPt = jetIt->pt();
      if ( jetPt>670. ) jetPt = 670.;
      else if ( jetPt<20. ) jetPt = 20.;
      double jetAbsEta = fabs(jetIt->eta());

      // here, we need to keep the relative uncertainties unchanged
      if( jetIt->pt()>670 )
      {
	ScaleFactor      = CSVM_SFl_Corr->Eval(670)*CSVM_SFl_0to2p4->Eval(670);
	ScaleFactor_up   = ScaleFactor + 2*( (CSVM_SFl_0to2p4_max->Eval(670) - CSVM_SFl_0to2p4->Eval(670))/CSVM_SFl_0to2p4->Eval(670) )*ScaleFactor;
        ScaleFactor_down = ScaleFactor + 2*( (CSVM_SFl_0to2p4_min->Eval(670) - CSVM_SFl_0to2p4->Eval(670))/CSVM_SFl_0to2p4->Eval(670) )*ScaleFactor;
      }
      else
      {
	if(jetAbsEta<0.8)
	{
	  ScaleFactor      = CSVM_SFl_Corr->Eval(jetPt)*CSVM_SFl_0to0p8->Eval(jetPt);
	  ScaleFactor_up   = ScaleFactor + ( (CSVM_SFl_0to0p8_max->Eval(jetPt) - CSVM_SFl_0to0p8->Eval(jetPt))/CSVM_SFl_0to0p8->Eval(jetPt) )*ScaleFactor;
	  ScaleFactor_down = ScaleFactor + ( (CSVM_SFl_0to0p8_min->Eval(jetPt) - CSVM_SFl_0to0p8->Eval(jetPt))/CSVM_SFl_0to0p8->Eval(jetPt) )*ScaleFactor;
	}
	else if(jetAbsEta>=0.8 && jetAbsEta<1.6)
	{
	  ScaleFactor      = CSVM_SFl_Corr->Eval(jetPt)*CSVM_SFl_0p8to1p6->Eval(jetPt);
	  ScaleFactor_up   = ScaleFactor + ( (CSVM_SFl_0p8to1p6_max->Eval(jetPt) - CSVM_SFl_0p8to1p6->Eval(jetPt))/CSVM_SFl_0p8to1p6->Eval(jetPt) )*ScaleFactor;
	  ScaleFactor_down = ScaleFactor + ( (CSVM_SFl_0p8to1p6_min->Eval(jetPt) - CSVM_SFl_0p8to1p6->Eval(jetPt))/CSVM_SFl_0p8to1p6->Eval(jetPt) )*ScaleFactor;
	}
	else
	{
	  ScaleFactor      = CSVM_SFl_Corr->Eval(jetPt)*CSVM_SFl_1p6to2p4->Eval(jetPt);
	  ScaleFactor_up   = ScaleFactor + ( (CSVM_SFl_1p6to2p4_max->Eval(jetPt) - CSVM_SFl_1p6to2p4->Eval(jetPt))/CSVM_SFl_1p6to2p4->Eval(jetPt) )*ScaleFactor;
	  ScaleFactor_down = ScaleFactor + ( (CSVM_SFl_1p6to2p4_min->Eval(jetPt) - CSVM_SFl_1p6to2p4->Eval(jetPt))/CSVM_SFl_1p6to2p4->Eval(jetPt) )*ScaleFactor;
	}
      }

      tagEfficiency = h2_EffMapUDSG->GetBinContent( h2_EffMapUDSG->GetXaxis()->FindBin(jetIt->pt()), h2_EffMapUDSG->GetYaxis()->FindBin(fabs(jetIt->eta())) );
    }

    btagNominal = btaggingUtility.applySF( btag, ScaleFactor, tagEfficiency);
    btagUp = btaggingUtility.applySF( btag, ScaleFactor_up, tagEfficiency);
    btagDown = btaggingUtility.applySF( btag, ScaleFactor_down, tagEfficiency);

    int btaggingSummary = 1*btag + 2*btagNominal + 4*btagUp + 8*btagDown;

    jetIt->addUserInt("btagRegular", btaggingSummary);
  }

  // put jets into event
  iEvent.put(jetsBtags);
}

// ------------ method called once each job just before starting event loop  ------------
void
BTaggingSFProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void
BTaggingSFProducer::endJob()
{
}

//define this as a plug-in
DEFINE_FWK_MODULE(BTaggingSFProducer);
