#!/bin/python
from ROOT import *
import math

import sys

def doCutAndCount( lum, Top, SingTop, QCD, Wbx, Wcx, Wqx, Zbx, Zcx, Zqx, Data, ntags=1 ) :
  

    # Get the central value
    bkg = SingTop + QCD + Wbx + Wcx + Wqx + Zbx + Zcx + Zqx
    dbkg = sqrt( 0.30*0.30*SingTop*SingTop
                 + 1.0*1.0*QCD*QCD
                 + 1.0*1.0*(Wbx+Wcx+Wqx+Zbx+Zcx+Zqx)*(Wbx+Wcx+Wqx+Zbx+Zcx+Zqx) )
    print 'Nbkg = {0:6.3f} +- {1:6.3f}'.format(
        bkg, dbkg
        )


    sig = Top

    xs_ttbar = 157.5 # pb-1

    # SF's are NOW SET IN THE TEMPLATES
    sf_btag = 1.0  # 0.914 From AN-2010-162, table 4, per-jet SF = 0.88, from ttbar MC, event SF = 0.914 (see getFbcp.py)
    if ntags is 1 :        
        dsf_btag= 0.099 / 0.9
    elif ntags is 2 :
        dsf_btag= 0.099 / 0.9 * 2.0
    fsf_btag= dsf_btag / sf_btag

    sf_lep  = 1.0   # 0.93 From Jason, trigger SF = 98 +- 1 %, eff SF = 95.0 +- 3.3%
    dsf_lep = 0.03 

    fsf_lep = dsf_lep / sf_lep

    # the JEC is derived directly from this script, using the "up and down" JEC templates

    deff_jec_up = 0.09
    deff_jec_dn = 0.08    


    deff_jec_av = (deff_jec_up + deff_jec_dn) / 2.0

    # the JER is derived directly from this script, using the "up and down" JER templates
    

    eff = sig / (xs_ttbar * lum) * sf_btag * sf_lep

    xs = (Data - bkg) / (eff * lum)
    print 'Data = {0:6.0f}, Bkg = {1:6.3f}, eff={2:6.3f}, lum={3:6.2f}'.format(
        Data, bkg, eff, lum
        )

    # Get the stat uncertainty
    dxs_stat = math.sqrt( Data ) / (Data - bkg)

    # 100% uncertainty on bkg
    dxs_bkg = dbkg / (Data - bkg)

    # Efficiency uncertainty from btag sf, muon sf... will add
    # jec, pdf, i/fsr, q^2, etc
    dEff = sqrt( fsf_btag * fsf_btag + fsf_lep * fsf_lep + deff_jec_av * deff_jec_av )
    dxs_eff = dEff
    print 'Efficiency uncertainties : Btag = {0:6.2f}, Electron Eff = {1:6.2f}, JEC = {2:6.2f}'.format(
        fsf_btag, fsf_lep, deff_jec_av
        )

    BR = 0.11
    print 'BR = ' + str(BR)
    print 'Efficiency*Acc*BR,MC= {0:6.3f}'.format(eff / ( sf_btag * sf_lep ))
    print 'Efficiency*Acc*BR   = {0:6.3f} +- {1:6.3f}'.format(eff,dEff * eff)
    print 'Efficiency*Acc      = {0:6.3f} +- {1:6.3f}'.format(eff/BR,dEff * eff/BR)

    # 10% lumi uncertainty
    dxs_lum = 0.11


    dxs_sys = sqrt( dxs_bkg*dxs_bkg + dxs_eff*dxs_eff + dxs_lum*dxs_lum)


    print ' Cross section = {0:6.1f} +- {1:4.1f} (stat) +- {2:4.1f} (bkg) +- {3:4.1f} (eff) +- {4:4.1f} (lum)'.format(
        xs, dxs_stat * xs, dxs_bkg * xs, dxs_eff * xs, dxs_lum * xs
        )
    print ' Cross section = {0:6.1f} +- {1:4.1f} (stat) +- {2:4.1f} (sys)'.format(
        xs, dxs_stat * xs, dxs_sys * xs
        )
