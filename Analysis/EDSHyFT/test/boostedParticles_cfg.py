import FWCore.ParameterSet.Config as cms

process = cms.Process("GenInfo")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.MessageLogger.cerr.FwkJob.limit=1
process.MessageLogger.cerr.ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) )

###############################
####### Parameters ############
############################### 
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('runOntWtW',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run on BB->tWtW sample"),

options.register ('runOnbZtW',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run on BB->bZtW sample")

options.register ('runOnbHtW',
                  1,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run on BB->bHtW sample")

options.parseArguments()            
                                    
print options

readFiles = cms.untracked.vstring()

if options.runOnbHtW:
    readFiles.extend( [
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BprimeBprimeToBHTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_99_1_7Lv.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BprimeBprimeToBHTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_139_1_fvp.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BprimeBprimeToBHTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_144_1_Fvy.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BprimeBprimeToBHTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_190_1_ZNm.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BprimeBprimeToBHTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_19_1_mnu.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BprimeBprimeToBHTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_123_1_fvY.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BprimeBprimeToBHTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_2_1_zFf.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BprimeBprimeToBHTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_26_1_l6x.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BprimeBprimeToBHTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_63_2_VGa.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BprimeBprimeToBHTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_104_1_krO.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BprimeBprimeToBHTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_115_1_Jmo.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BprimeBprimeToBHTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_177_3_eWu.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BprimeBprimeToBHTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_18_1_4SD.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BprimeBprimeToBHTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_196_1_89p.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BprimeBprimeToBHTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_193_1_njn.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BprimeBprimeToBHTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_155_1_cRj.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BprimeBprimeToBHTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_93_1_ciT.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBHTWinc_M-600_TuneZ2star_8TeV-madgraph/BprimeBprimeToBHTWinc_M600_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_39_1_wg4.root',
        ]);
    
elif options.runOnbZtW:
    readFiles.extend( [
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_183_3_Akn.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_63_3_I2v.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_68_3_dEz.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_118_3_N1L.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_72_3_p5I.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_88_3_Po1.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_154_3_JuS.root',
        '/store/user/lpctlbsm/cjenkins/BprimeBprimeToBZTWinc_M-750_TuneZ2star_8TeV-madgraph/BprimeBprimeToBZTWinc_M750_TuneZ2star_8TeVmadgraphSum12_DR53X_PU_S10_START53_V7A_TLBSMv2/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_69_3_zA8.root',
        ]);

elif options.runOntWtW:
    readFiles.extend( [
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_10_3_lNR.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_11_4_iPL.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_12_3_kmL.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_13_3_Etl.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_14_4_VWT.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_1_4_qzI.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_15_3_Vg0.root',
        '/store/user/lpctlbsm/skhalil/BprimeBprimeToTWTWinc_M-700_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v1/fe5dcf8cf2a24180bf030f68a7d97dda/ttbsm_tlbsm_53x_v1_mc_16_1_hvB.root',
        ]);

if len(options.inputFiles) == 0 :
    process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(readFiles),
                                ## eventsToProcess = cms.untracked.VEventRange(
##         '1:215583-215584:1',
##         #'1:15:4471',
##         #'1:1617:484808',
##         #'1:333:99729',
##         #'1:257:76943',
##         )
                                )
else:
    filelist = []
    with open( options.inputFiles[0], 'r' ) as input_:
        for line in input_:
            filelist.append(line.strip())
            
        print 'filelist', filelist
        process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(filelist)
                                    )
        
process.GenInfo = cms.EDProducer('BoostedParticles')
                                         
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
                                   src = cms.InputTag("prunedGenParticles"),
                                   printP4 = cms.untracked.bool(False),
                                   printPtEtaPhi = cms.untracked.bool(False),
                                   printVertex = cms.untracked.bool(False),
                                   printStatus = cms.untracked.bool(False),
                                   printIndex = cms.untracked.bool(False),
                                   status = cms.untracked.vint32( 3 )
                                   )

process.printList = cms.EDAnalyzer("ParticleListDrawer",
  maxEventsToPrint = cms.untracked.int32(-1),
  printVertex = cms.untracked.bool(False),
  src = cms.InputTag("prunedGenParticles")
)

process.p = cms.Path(process.GenInfo)# * process.printTree * process.printList)

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('genOutputFileTest.root'),
                               outputCommands = cms.untracked.vstring('drop *',
                                                                      'keep *_GenInfo*_*_*',)
                               )

process.e = cms.EndPath(process.out)
