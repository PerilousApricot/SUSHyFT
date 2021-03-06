//--------------------------------------------------------------------------------------------------
// $Id $
//
// PFIsolationEstimator 
//
// Helper Class for calculating PFIsolation for Photons & Electron onthe fly. This class takes 
//        PF Particle collection and the reconstructed vertex collection as input.
//
// Authors: Vasundhara Chetluru
//--------------------------------------------------------------------------------------------------


/// --> NOTE if you want to use this class as standalone without the CMSSW part 
///  you need to uncomment the below line and compile normally with scramv1 b 
///  Then you need just to load it in your root macro the lib with the correct path, eg:
///  gSystem->Load("/data/benedet/CMSSW_5_2_2/lib/slc5_amd64_gcc462/pluginEGammaEGammaAnalysisTools.so");

//#define STANDALONE   // <---- this line

#ifndef PFIsolationEstimator_H
#define PFIsolationEstimator_H

#ifndef STANDALONE
#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalClusterLazyTools.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#endif
#include <TROOT.h>
#include "TMVA/Factory.h"
#include "TMVA/Tools.h"
#include "TMVA/Reader.h"
#include "TH1.h"
#include "TH2.h"


#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/ParticleFlowCandidate/interface/PileUpPFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PileUpPFCandidateFwd.h"

#include "DataFormats/EgammaCandidates/interface/Photon.h"
#include "DataFormats/EgammaCandidates/interface/PhotonFwd.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

using namespace std;
using namespace edm;
using namespace reco;


class PFIsolationEstimator{
 public:
  PFIsolationEstimator();
  ~PFIsolationEstimator(); 
  
  enum VetoType {
    kElectron = -1,      // MVA for non-triggering electrons          
    kPhoton  =  1            // MVA for triggering electrons
  };
  

  void     initializeElectronIsolation( Bool_t  bApplyVeto, float  fConeSize = 0.3 );
  void     initializePhotonIsolation( Bool_t  bApplyVeto, float  fConeSize = 0.4  );
  void     initializeElectronIsolationInRings( Bool_t  bApplyVeto, int iNumberOfRings, float fRingSize );
  void     initializePhotonIsolationInRings( Bool_t  bApplyVeto, int iNumberOfRings, float fRingSize  );
  void     initializeRings(int iNumberOfRings, float fRingSize);
  Bool_t   isInitialized() const { return fisInitialized; }
  

  float fGetIsolation(const reco::PFCandidate * pfCandidate,const reco::PFCandidateCollection* pfParticlesColl, reco::Vertex& vtx, edm::Handle< reco::VertexCollection >  vertices );
  vector<float >  fGetIsolationInRings(const reco::PFCandidate * pfCandidate,const reco::PFCandidateCollection* pfParticlesColl,reco::Vertex& vtx, edm::Handle< reco::VertexCollection > vertices);
  
   float fGetIsolation(const reco::Photon* photon,const reco::PFCandidateCollection* pfParticlesColl, reco::Vertex& vtx, edm::Handle< reco::VertexCollection >  vertices );
  vector<float >  fGetIsolationInRings(const reco::Photon* photon,const reco::PFCandidateCollection* pfParticlesColl,reco::Vertex& vtx, edm::Handle< reco::VertexCollection > vertices);

  VertexRef chargedHadronVertex(edm::Handle< reco::VertexCollection > verticies, const reco::PFCandidate& pfcand );

  void setConeSize(float fValue = 0.4){ fConeSize = fValue;};

  void setParticleType(int iValue){iParticleType = iValue;};

  //Veto booleans
  void setApplyVeto(Bool_t bValue = kTRUE){  bApplyVeto = bValue;};
  void setDeltaRVetoBarrel(Bool_t bValue = kTRUE){  bDeltaRVetoBarrel = bValue;};
  void setDeltaRVetoEndcap(Bool_t bValue = kTRUE){  bDeltaRVetoEndcap = bValue;};
  void setRectangleVetoBarrel(Bool_t bValue = kTRUE){  bRectangleVetoBarrel = bValue;};
  void setRectangleVetoEndcap(Bool_t bValue = kTRUE){  bRectangleVetoEndcap = bValue;};

  //Veto Values
  void setDeltaRVetoBarrelPhotons(float fValue = -1.0){fDeltaRVetoBarrelPhotons=fValue;};
  void setDeltaRVetoBarrelNeutrals(float fValue = -1.0){fDeltaRVetoBarrelNeutrals=fValue;};
  void setDeltaRVetoBarrelCharged(float fValue = -1.0){fDeltaRVetoBarrelPhotons=fValue;};
  void setDeltaRVetoEndcapPhotons(float fValue = -1.0){fDeltaRVetoEndcapPhotons=fValue;};
  void setDeltaRVetoEndcapNeutrals(float fValue = -1.0){fDeltaRVetoEndcapNeutrals=fValue;};
  void setDeltaRVetoEndcapCharged(float fValue = -1.0){fDeltaRVetoEndcapPhotons=fValue;};

  
  void setRectangleDeltaPhiVetoBarrelPhotons(float fValue = -1.0){fRectangleDeltaPhiVetoBarrelPhotons=fValue;};
  void setRectangleDeltaPhiVetoBarrelNeutrals(float fValue = -1.0){fRectangleDeltaPhiVetoBarrelNeutrals=fValue;};
  void setRectangleDeltaPhiVetoBarrelCharged(float fValue = -1.0){fRectangleDeltaPhiVetoBarrelPhotons=fValue;};
  void setRectangleDeltaPhiVetoEndcapPhotons(float fValue = -1.0){fRectangleDeltaPhiVetoEndcapPhotons=fValue;};
  void setRectangleDeltaPhiVetoEndcapNeutrals(float fValue = -1.0){fRectangleDeltaPhiVetoEndcapNeutrals=fValue;};
  void setRectangleDeltaPhiVetoEndcapCharged(float fValue = -1.0){fRectangleDeltaPhiVetoEndcapPhotons=fValue;};
  

  void setRectangleDeltaEtaVetoBarrelPhotons(float fValue = -1.0){fRectangleDeltaEtaVetoBarrelPhotons=fValue;};
  void setRectangleDeltaEtaVetoBarrelNeutrals(float fValue = -1.0){fRectangleDeltaEtaVetoBarrelNeutrals=fValue;};
  void setRectangleDeltaEtaVetoBarrelCharged(float fValue = -1.0){fRectangleDeltaEtaVetoBarrelPhotons=fValue;};
  void setRectangleDeltaEtaVetoEndcapPhotons(float fValue = -1.0){fRectangleDeltaEtaVetoEndcapPhotons=fValue;};
  void setRectangleDeltaEtaVetoEndcapNeutrals(float fValue = -1.0){fRectangleDeltaEtaVetoEndcapNeutrals=fValue;};
  void setRectangleDeltaEtaVetoEndcapCharged(float fValue = -1.0){fRectangleDeltaEtaVetoEndcapPhotons=fValue;};

  //Veto implementation
  float  isPhotonParticleVetoed( const reco::PFCandidate* pfIsoCand );
  float  isNeutralParticleVetoed( const reco::PFCandidate* pfIsoCand );
  float  isChargedParticleVetoed(const reco::PFCandidate* pfIsoCand, edm::Handle< reco::VertexCollection > vertices);  
  float  isChargedParticleVetoed( const reco::PFCandidate* pfIsoCand, reco::Vertex& vtx, edm::Handle< reco::VertexCollection >  vertices  );
 
  
  float getIsolationPhoton(){   fIsolationPhoton = 	fIsolationInRingsPhoton[0]; return fIsolationPhoton; };
  float getIsolationNeutral(){ fIsolationNeutral = 	fIsolationInRingsNeutral[0]; return fIsolationNeutral; };
  float getIsolationCharged(){  fIsolationCharged =   fIsolationInRingsCharged[0]; return fIsolationCharged; };
  float getIsolationChargedAll(){ return fIsolationChargedAll; };

  vector<float >  getIsolationInRingsPhoton(){ return fIsolationInRingsPhoton; };
  vector<float >  getIsolationInRingsNeutral(){ return fIsolationInRingsNeutral; };
  vector<float >  getIsolationInRingsCharged(){ return fIsolationInRingsCharged; };
  vector<float >  getIsolationInRingsChargedAll(){ return fIsolationInRingsChargedAll; };


  void setNumbersOfRings(int iValue = 1){iNumberOfRings = iValue;};
  void setRingSize(float fValue = 0.4){fRingSize = fValue;};

  int getNumbersOfRings(){return iNumberOfRings;};
  float getRingSize(){return fRingSize; };
  
  int matchPFObject(const reco::Photon* photon, const reco::PFCandidateCollection* pfParticlesColl );
  
 
 private:
 

  int                     iParticleType;

  Bool_t                    fisInitialized;
  float                   fIsolation;
  float                   fIsolationPhoton;
  float                   fIsolationNeutral;
  float                   fIsolationCharged;
  float                   fIsolationChargedAll;
  
  vector<float >          fIsolationInRings;
  vector<float >          fIsolationInRingsPhoton;
  vector<float >          fIsolationInRingsNeutral;
  vector<float >          fIsolationInRingsCharged;  
  vector<float >          fIsolationInRingsChargedAll;

  Bool_t                    checkClosestZVertex;
  float                     fConeSize;
  Bool_t                    bApplyVeto;
  
  Bool_t                    bDeltaRVetoBarrel; 
  Bool_t                    bDeltaRVetoEndcap; 
  
  Bool_t                    bRectangleVetoBarrel; 
  Bool_t                    bRectangleVetoEndcap; 
  
  float                   fDeltaRVetoBarrelPhotons; 
  float                   fDeltaRVetoBarrelNeutrals;
  float                   fDeltaRVetoBarrelCharged;

  float                   fDeltaRVetoEndcapPhotons; 
  float                   fDeltaRVetoEndcapNeutrals;
  float                   fDeltaRVetoEndcapCharged;  

  float                   fRectangleDeltaPhiVetoBarrelPhotons; 
  float                   fRectangleDeltaPhiVetoBarrelNeutrals;
  float                   fRectangleDeltaPhiVetoBarrelCharged;

  float                   fRectangleDeltaPhiVetoEndcapPhotons; 
  float                   fRectangleDeltaPhiVetoEndcapNeutrals;
  float                   fRectangleDeltaPhiVetoEndcapCharged;
  
  float                   fRectangleDeltaEtaVetoBarrelPhotons; 
  float                   fRectangleDeltaEtaVetoBarrelNeutrals;
  float                   fRectangleDeltaEtaVetoBarrelCharged;

  float                   fRectangleDeltaEtaVetoEndcapPhotons; 
  float                   fRectangleDeltaEtaVetoEndcapNeutrals;
  float                   fRectangleDeltaEtaVetoEndcapCharged;

  int                     iNumberOfRings;
  float                   fRingSize;

  float                   fDeltaR;
  float                   fDeltaEta;
  float                   fDeltaPhi;

  float                   fEta;
  float                   fPhi;
  float                   fPt;
  float                   fVx;
  float                   fVy;
  float                   fVz;


  math::XYZVector         vtxWRTCandidate;
   
  void     initialize( Bool_t  bApplyVeto, int iParticleType);
};

#endif
