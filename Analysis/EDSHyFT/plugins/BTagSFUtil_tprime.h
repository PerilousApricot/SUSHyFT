/*************************************************************

Class Usage:

This class should only be used for upgrading and downgrading
if a single operating point is used in an analysis.

bool isBTagged = b-tag flag for jet
float Btag_SF = data/MC scale factor for b-tagging efficiency
float Btag_eff = b-tagging efficiency in MC

Author: Michael Segala
Contact: michael.segala@gmail.com
Updated: Ulrich Heintz 12/23/2011
Modified: Dinko Ferencek 10/01/2012

*************************************************************/


#ifndef BTagSFUtil_tprime_h
#define BTagSFUtil_tprime_h

#include <Riostream.h>
#include "TRandom3.h"
#include "TMath.h"


class BTagSFUtil{

 public:

  BTagSFUtil( int seed=0 );
  ~BTagSFUtil();

  bool applySF(bool isBTagged, float Btag_SF = 0.98, float Btag_eff = 1.0);

 private:

  TRandom3* rand_;

};


BTagSFUtil::BTagSFUtil( int seed ) {

  rand_ = new TRandom3(seed);

}

BTagSFUtil::~BTagSFUtil() {

  delete rand_;

}

bool BTagSFUtil::applySF(bool isBTagged, float Btag_SF, float Btag_eff){

  bool newBTag = isBTagged;

  if (Btag_SF == 1) return newBTag; //no correction needed

  //throw die
  float coin = rand_->Uniform(1.);

  if(Btag_SF > 1){  // use this if SF>1

    if( !isBTagged ) {

      //fraction of jets that need to be upgraded
      float mistagPercent = (1.0 - Btag_SF) / (1.0 - (1.0/Btag_eff) );

      //upgrade to tagged
      if( coin < mistagPercent ) {newBTag = true;}
    }

  }else{  // use this if SF<1

    //downgrade tagged to untagged
    if( isBTagged && coin > Btag_SF ) {newBTag = false;}

  }

  return newBTag;
}


#endif

