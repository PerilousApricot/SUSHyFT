import FWCore.ParameterSet.Config as cms

process = cms.Process("btagProducer")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.load("CondCore.DBCommon.CondDBCommon_cfi")

#Data measurements from Summer11
process.load ("RecoBTag.PerformanceDB.BTagPerformanceDB1107")
process.load ("RecoBTag.PerformanceDB.PoolBTagPerformanceDB1107")

process.source = cms.Source("PoolSource",
                                # replace 'myfile.root' with the source file you want to use
                                fileNames = cms.untracked.vstring(
     '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_100_1_kxn.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_101_1_Xcl.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_102_1_H7P.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_103_1_cVw.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_104_1_u9i.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_105_1_YLK.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_106_1_fQl.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_107_1_Wlw.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_108_2_hXU.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_109_1_7Fe.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_10_1_UOP.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_110_1_x9a.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_111_1_1HD.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_112_1_r8f.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_113_1_G8W.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_114_1_hkM.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_115_1_U9X.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_116_2_2Tf.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_117_1_B7z.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_118_1_pck.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_119_1_IDM.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_11_1_6qN.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_120_1_D2e.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_121_1_rOq.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_122_1_ib5.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_123_1_f0c.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_124_2_e3a.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_125_1_WOr.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_126_2_dUB.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_127_1_l5F.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_128_1_L1a.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_129_1_joe.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_12_1_Rud.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_130_1_SC6.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_131_2_u82.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_132_1_uKN.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_133_1_f2m.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_134_2_WNH.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_135_1_tWs.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_136_1_n4N.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_137_2_0Hh.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_138_2_YDR.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_139_2_FDx.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_13_1_Gqq.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_140_1_Yj6.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_141_1_vQN.root',
           '/store/user/lpctlbsm/skhalil/GJets_TuneZ2_200_HT_inf_7TeV-madgraph/ttbsm_v9_Summer11-PU_S4_START42_V11-v1/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_142_1_zh3.root'
#    '/store/user/lpctlbsm/samvel/T_TuneZ2_s-channel_7TeV-powheg-tauola/prod_2011_10_03_17_19_46/bf57a985b107a689982b667a3f2f23c7/ttbsm_42x_mc_9_1_3hF.root'
    )
   )

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.btaggingProducer = cms.EDProducer("BTaggingSFProducer",                                      
                                          jetSource = cms.InputTag('goodPatJetsPFlow'),
                                          Tagger = cms.string('combinedSecondaryVertexBJetTags'),
                                          DiscriminantValue = cms.double(0.679)
                                          )

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('jets.root'),
                               outputCommands = cms.untracked.vstring('drop *')
                               )

process.out.outputCommands += ['keep *_*_*_btagProducer']

process.p = cms.Path(process.btaggingProducer)

process.e = cms.EndPath(process.out)
