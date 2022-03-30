#include<iostream>
#include "../interface/EventTree.h"

EventTree::EventTree(int nFiles, bool xRootDAccess, string year, bool isData, char** fileNames){
    chain = new TChain("Events");

    isData_ = isData;

    //std::cout << chain->GetCacheSize() << std::endl;
    chain->SetCacheSize(100*1024*1024);
    if (xRootDAccess){
	//string dir = "root://cms-xrd-global.cern.ch/";
	string dir = "root://cmsxrootd.fnal.gov/";
	for(int fileI=0; fileI<nFiles; fileI++){
	    string fName = (string) fileNames[fileI];
	    chain->Add( (dir + fileNames[fileI]).c_str() );
	    cout << fName << "  " << chain->GetEntries() << endl;
	}
    }
    else{
	for(int fileI=0; fileI<nFiles; fileI++){
	    chain->Add(fileNames[fileI]);
	}
    }
    chain->SetBranchStatus("*",0);
	
    // keep some important branches
    chain->SetBranchStatus("PV_ndof",1);
    chain->SetBranchAddress("PV_ndof", &pvNDOF_);

    chain->SetBranchStatus("PV_x",1);
    chain->SetBranchAddress("PV_x", &pvX_);

    chain->SetBranchStatus("PV_y",1);
    chain->SetBranchAddress("PV_y", &pvY_);

    chain->SetBranchStatus("PV_z",1);
    chain->SetBranchAddress("PV_z", &pvZ_);

    chain->SetBranchStatus("PV_chi2",1);
    chain->SetBranchAddress("PV_chi2", &pvChi2_);

    if (!isData_){
	chain->SetBranchStatus("Pileup_nPU",1);
	chain->SetBranchAddress("Pileup_nPU", &nPU_);
	
	chain->SetBranchStatus("Pileup_nTrueInt",1);
	chain->SetBranchAddress("Pileup_nTrueInt", &nPUTrue_);
    }

	
    // event
	
    chain->SetBranchStatus("run",1);
    chain->SetBranchAddress("run", &run_);

    chain->SetBranchStatus("event",1);
    chain->SetBranchAddress("event", &event_);
	
    chain->SetBranchStatus("luminosityBlock",1);
    chain->SetBranchAddress("luminosityBlock", &lumis_);

    chain->SetBranchStatus("PV_npvs",1);
    chain->SetBranchAddress("PV_npvs", &nVtx_);

    chain->SetBranchStatus("PV_npvsGood",1);
    chain->SetBranchAddress("PV_npvsGood", &nGoodVtx_);


    if (!isData_){
	chain->SetBranchStatus("Generator_weight",1);
	chain->SetBranchAddress("Generator_weight", &genWeight_);

	chain->SetBranchStatus("nLHEScaleWeight",1);
	chain->SetBranchAddress("nLHEScaleWeight", &nLHEScaleWeight_);
	
	chain->SetBranchStatus("LHEScaleWeight",1);
	chain->SetBranchAddress("LHEScaleWeight", &LHEScaleWeight_);
	
	chain->SetBranchStatus("nLHEPdfWeight",1);
	chain->SetBranchAddress("nLHEPdfWeight", &nLHEPdfWeight_);
	
	chain->SetBranchStatus("LHEPdfWeight",1);
	chain->SetBranchAddress("LHEPdfWeight", &LHEPdfWeight_);
	
	chain->SetBranchStatus("PSWeight",1);
	chain->SetBranchAddress("PSWeight", &PSWeight_);
	
	chain->SetBranchStatus("nPSWeight",1);
	chain->SetBranchAddress("nPSWeight", &nPSWeight_);
	
	chain->SetBranchStatus("LHEWeight_originalXWGTUP",1);
	chain->SetBranchAddress("LHEWeight_originalXWGTUP", &LHEWeight_originalXWGTUP_);
	
    }

    // MET
    chain->SetBranchStatus("MET_pt",1);
    chain->SetBranchAddress("MET_pt", &MET_pt_);

    chain->SetBranchStatus("MET_phi",1);
    chain->SetBranchAddress("MET_phi", &MET_phi_);

    if (!isData_){
	chain->SetBranchStatus("GenMET_pt",1);
	chain->SetBranchAddress("GenMET_pt", &GenMET_pt_);
	
	chain->SetBranchStatus("GenMET_phi",1);
	chain->SetBranchAddress("GenMET_phi", &GenMET_phi_);
    }

    // electrons	
    chain->SetBranchStatus("nElectron",1);
    chain->SetBranchAddress("nElectron", &nEle_);

    chain->SetBranchStatus("Electron_charge",1);
    chain->SetBranchAddress("Electron_charge", &eleCharge_);	
    
    chain->SetBranchStatus("Electron_pt",1);
    chain->SetBranchAddress("Electron_pt", &elePt_);
    
    chain->SetBranchStatus("Electron_deltaEtaSC",1);
    chain->SetBranchAddress("Electron_deltaEtaSC", &eleDeltaEtaSC_);
    
    chain->SetBranchStatus("Electron_eta",1);
    chain->SetBranchAddress("Electron_eta", &eleEta_);
    
    chain->SetBranchStatus("Electron_phi",1);
    chain->SetBranchAddress("Electron_phi", &elePhi_);
    
    chain->SetBranchStatus("Electron_mass",1);
    chain->SetBranchAddress("Electron_mass", &eleMass_);
    
    chain->SetBranchStatus("Electron_miniPFRelIso_all",1);
    chain->SetBranchAddress("Electron_miniPFRelIso_all", &eleMiniPFRelIso_);

    chain->SetBranchStatus("Electron_mvaFall17V2noIso_WP90",1);
    chain->SetBranchAddress("Electron_mvaFall17V2noIso_WP90", &eleMVAFall17V2noIso_WP90_);

    chain->SetBranchStatus("Electron_mvaFall17V2noIso_WPL",1);
    chain->SetBranchAddress("Electron_mvaFall17V2noIso_WPL", &eleMVAFall17V2noIso_WPL_);

    chain->SetBranchStatus("Electron_dxy",1);
    chain->SetBranchAddress("Electron_dxy", &eleD0_);

    chain->SetBranchStatus("Electron_dz",1);
    chain->SetBranchAddress("Electron_dz", &eleDz_);


    // muons
    chain->SetBranchStatus("nMuon",1);
    chain->SetBranchAddress("nMuon", &nMuon_);

    chain->SetBranchStatus("Muon_charge",1);
    chain->SetBranchAddress("Muon_charge", &muCharge_);
	
    chain->SetBranchStatus("Muon_pt",1);
    chain->SetBranchAddress("Muon_pt", &muPt_);

    chain->SetBranchStatus("Muon_eta",1);
    chain->SetBranchAddress("Muon_eta", &muEta_);

    chain->SetBranchStatus("Muon_phi",1);
    chain->SetBranchAddress("Muon_phi", &muPhi_);

    chain->SetBranchStatus("Muon_mass",1);
    chain->SetBranchAddress("Muon_mass", &muMass_);

    chain->SetBranchStatus("Muon_miniPFRelIso_all",1);
    chain->SetBranchAddress("Muon_miniPFRelIso_all", &muMiniPFRelIso_);

    chain->SetBranchStatus("Muon_tightId",1);
    chain->SetBranchAddress("Muon_tightId", &muTightId_);

    chain->SetBranchStatus("Muon_isPFcand",1);
    chain->SetBranchAddress("Muon_isPFcand", &muIsPFMuon_);

    chain->SetBranchStatus("Muon_isGlobal",1);
    chain->SetBranchAddress("Muon_isGlobal", &muIsGlobal_);

    chain->SetBranchStatus("Muon_isTracker",1);
    chain->SetBranchAddress("Muon_isTracker", &muIsTracker_);


    // jets
    chain->SetBranchStatus("nJet",1);
    chain->SetBranchAddress("nJet", &nJet_);
 
    chain->SetBranchStatus("Jet_pt",1);
    chain->SetBranchAddress("Jet_pt", &jetPt_);
    chain->SetBranchAddress("Jet_qgl", &jetQGL_);

    chain->SetBranchStatus("Jet_rawFactor",1);
    chain->SetBranchAddress("Jet_rawFactor", &jetRawFactor_);
	
    chain->SetBranchStatus("Jet_eta",1);
    chain->SetBranchAddress("Jet_eta", &jetEta_);
	
    chain->SetBranchStatus("Jet_phi",1);
    chain->SetBranchAddress("Jet_phi", &jetPhi_);

    chain->SetBranchStatus("Jet_mass",1);
    chain->SetBranchAddress("Jet_mass", &jetMass_);

    chain->SetBranchStatus("Jet_jetId",1);
    chain->SetBranchAddress("Jet_jetId", &jetID_);

    chain->SetBranchStatus("Jet_area",1);
    chain->SetBranchAddress("Jet_area", &jetArea_);

    chain->SetBranchStatus("Jet_btagCMVA",1);
    chain->SetBranchAddress("Jet_btagCMVA", &jetBtagCMVA_);

    chain->SetBranchStatus("Jet_btagCSVV2",1);
    chain->SetBranchAddress("Jet_btagCSVV2", &jetBtagCSVV2_);

    chain->SetBranchStatus("Jet_btagDeepB",1);
    chain->SetBranchAddress("Jet_btagDeepB", &jetBtagDeepB_);

    chain->SetBranchStatus("Jet_btagDeepC",1);
    chain->SetBranchAddress("Jet_btagDeepC", &jetBtagDeepC_);

    chain->SetBranchStatus("Jet_btagDeepFlavB",1);
    chain->SetBranchAddress("Jet_btagDeepFlavB", &jetBtagDeepFlavB_);

    chain->SetBranchStatus("Jet_chEmEF",1);
    chain->SetBranchAddress("Jet_chEmEF", &jetchEmEF_);

    chain->SetBranchStatus("Jet_neEmEF",1);
    chain->SetBranchAddress("Jet_neEmEF", &jetneEmEF_);

    chain->SetBranchStatus("Jet_neEmEF",1);
    chain->SetBranchAddress("Jet_muEF", &jetmuEF_);

    if (!isData_){
	chain->SetBranchStatus("Jet_hadronFlavour",1);
	chain->SetBranchAddress("Jet_hadronFlavour", &jetHadFlvr_);
	
	chain->SetBranchStatus("Jet_genJetIdx",1);
	chain->SetBranchAddress("Jet_genJetIdx", &jetGenJetIdx_);
    }

    chain->SetBranchStatus("nFatJet",1);
    chain->SetBranchAddress("nFatJet", &nFatJet_);

    chain->SetBranchStatus("FatJet_pt",1);
    chain->SetBranchAddress("FatJet_pt", &fatJetPt_);

    chain->SetBranchStatus("FatJet_eta",1);
    chain->SetBranchAddress("FatJet_eta", &fatJetEta_);

    chain->SetBranchStatus("FatJet_phi",1);
    chain->SetBranchAddress("FatJet_phi", &fatJetPhi_);

    chain->SetBranchStatus("FatJet_area",1);
    chain->SetBranchAddress("FatJet_area", &fatJetArea_);

    chain->SetBranchStatus("FatJet_mass",1);
    chain->SetBranchAddress("FatJet_mass", &fatJetMass_);

    chain->SetBranchStatus("FatJet_msoftdrop",1);
    chain->SetBranchAddress("FatJet_msoftdrop", &fatJetMassSoftDrop_);

    chain->SetBranchStatus("FatJet_jetId",1);
    chain->SetBranchAddress("FatJet_jetId", &fatJetID_);

    chain->SetBranchStatus("FatJet_btagDeepB",1);
    chain->SetBranchAddress("FatJet_btagDeepB", &fatJetBtagDeepB_);

    chain->SetBranchStatus("FatJet_deepTagMD_TvsQCD",1);
    chain->SetBranchAddress("FatJet_deepTagMD_TvsQCD", &fatJetDeepTagMDT_);

    chain->SetBranchStatus("FatJet_deepTagMD_WvsQCD",1);
    chain->SetBranchAddress("FatJet_deepTagMD_WvsQCD", &fatJetDeepTagMDW_);

    chain->SetBranchStatus("FatJet_deepTag_TvsQCD",1);
    chain->SetBranchAddress("FatJet_deepTag_TvsQCD", &fatJetDeepTagT_);

    chain->SetBranchStatus("FatJet_deepTag_WvsQCD",1);
    chain->SetBranchAddress("FatJet_deepTag_WvsQCD", &fatJetDeepTagW_);

    chain->SetBranchStatus("FatJet_electronIdx3SJ",1);
    chain->SetBranchAddress("FatJet_electronIdx3SJ", &fatJetEleIdx_);

    chain->SetBranchStatus("FatJet_muonIdx3SJ",1);
    chain->SetBranchAddress("FatJet_muonIdx3SJ", &fatJetMuIdx_);

    if (!isData_){
        chain->SetBranchStatus("FatJet_genJetAK8Idx",1);
        chain->SetBranchAddress("FatJet_genJetAK8Idx", &fatJetGenJetAK8Idx_);
        chain->SetBranchStatus("FatJet_hadronFlavour",1);
        chain->SetBranchAddress("FatJet_hadronFlavour", &fatJetHadFlvr_);
    }

    // // photons
    chain->SetBranchStatus("nPhoton",1);
    chain->SetBranchAddress("nPhoton", &nPho_);

    chain->SetBranchStatus("Photon_pt",1);
    chain->SetBranchAddress("Photon_pt", &phoEt_);
	
    chain->SetBranchStatus("Photon_eta",1);
    chain->SetBranchAddress("Photon_eta", &phoEta_);

    chain->SetBranchStatus("Photon_phi",1);
    chain->SetBranchAddress("Photon_phi", &phoPhi_);
	
    chain->SetBranchStatus("Photon_isScEtaEB",1);
    chain->SetBranchAddress("Photon_isScEtaEB", &phoIsEB_);

    chain->SetBranchStatus("Photon_isScEtaEE",1);
    chain->SetBranchAddress("Photon_isScEtaEE", &phoIsEE_);

	chain->SetBranchStatus("Photon_cutBased",1);
	chain->SetBranchAddress("Photon_cutBased", &phoIDcutbased_);
    /*
    if (year=="2016"){
	chain->SetBranchStatus("Photon_cutBased",1);
	chain->SetBranchAddress("Photon_cutBased", &phoIDcutbased_);
    }
    if (year=="2017" || year=="2018"){
	chain->SetBranchStatus("Photon_cutBasedBitmap",1);//these does not exist
	chain->SetBranchAddress("Photon_cutBasedBitmap", &phoIDcutbased_);
    }
	*/
    chain->SetBranchStatus("Photon_pfRelIso03_all",1);
    chain->SetBranchAddress("Photon_pfRelIso03_all", &phoPFRelIso_);

    chain->SetBranchStatus("Photon_pfRelIso03_chg",1);
    chain->SetBranchAddress("Photon_pfRelIso03_chg", &phoPFRelChIso_);

    chain->SetBranchStatus("Photon_vidNestedWPBitmap",1);
    chain->SetBranchAddress("Photon_vidNestedWPBitmap", &phoVidWPBitmap_);

    chain->SetBranchStatus("Photon_pixelSeed",1);
    chain->SetBranchAddress("Photon_pixelSeed", &phoPixelSeed_);

    chain->SetBranchStatus("Photon_r9",1);
    chain->SetBranchAddress("Photon_r9", &phoR9_);

    chain->SetBranchStatus("Photon_sieie",1);
    chain->SetBranchAddress("Photon_sieie", &phoSIEIE_);

    chain->SetBranchStatus("Photon_hoe",1);
    chain->SetBranchAddress("Photon_hoe", &phoHoverE_);

    if (!isData_){
	chain->SetBranchStatus("Photon_genPartIdx",1);
	chain->SetBranchAddress("Photon_genPartIdx", &phoGenPartIdx_);
    }
    chain->SetBranchStatus("Photon_electronVeto",1);
    chain->SetBranchAddress("Photon_electronVeto", &phoEleVeto_);
	
    chain->SetBranchStatus("Photon_mvaID",1);
    chain->SetBranchAddress("Photon_mvaID", &phoMVAId_);
	chain->SetBranchStatus("Photon_mvaID_Fall17V1p1",1);
	chain->SetBranchAddress("Photon_mvaID_Fall17V1p1", &phoMVAId17V1_);

    // Gen Partons
    if (!isData_){
    chain->SetBranchStatus("nLHEPart",1);
    chain->SetBranchAddress("nLHEPart", &nLHEPart_);
    
    chain->SetBranchStatus("LHEPart_pt",1);
    chain->SetBranchAddress("LHEPart_pt", &LHEPart_pt_);
    
    chain->SetBranchStatus("LHEPart_pdgId",1);
    chain->SetBranchAddress("LHEPart_pdgId", &LHEPart_pdgId_);

	chain->SetBranchStatus("nGenPart",1);
	chain->SetBranchAddress("nGenPart", &nGenPart_);
	
	chain->SetBranchStatus("GenPart_pt",1);
	chain->SetBranchAddress("GenPart_pt", &GenPart_pt_);
	
	chain->SetBranchStatus("GenPart_eta",1);
	chain->SetBranchAddress("GenPart_eta", &GenPart_eta_);
	
	chain->SetBranchStatus("GenPart_phi",1);
	chain->SetBranchAddress("GenPart_phi", &GenPart_phi_);

	chain->SetBranchStatus("GenPart_mass",1);
	chain->SetBranchAddress("GenPart_mass", &GenPart_mass_);

	chain->SetBranchStatus("GenPart_genPartIdxMother",1);
	chain->SetBranchAddress("GenPart_genPartIdxMother", &GenPart_genPartIdxMother_);

	chain->SetBranchStatus("GenPart_pdgId",1);
	chain->SetBranchAddress("GenPart_pdgId", &GenPart_pdgId_);
	
	chain->SetBranchStatus("GenPart_status",1);
	chain->SetBranchAddress("GenPart_status", &GenPart_status_);
	
	chain->SetBranchStatus("GenPart_statusFlags",1);
	chain->SetBranchAddress("GenPart_statusFlags", &GenPart_statusFlags_);
    

	chain->SetBranchStatus("nGenJet",1);
	chain->SetBranchAddress("nGenJet", &nGenJet_);
	
	chain->SetBranchStatus("GenJet_pt",1);
	chain->SetBranchAddress("GenJet_pt", &GenJet_pt_);

	chain->SetBranchStatus("GenJet_eta",1);
	chain->SetBranchAddress("GenJet_eta", &GenJet_eta_);

	chain->SetBranchStatus("GenJet_phi",1);
	chain->SetBranchAddress("GenJet_phi", &GenJet_phi_);

	chain->SetBranchStatus("GenJet_mass",1);
	chain->SetBranchAddress("GenJet_mass", &GenJet_mass_);

	chain->SetBranchStatus("nGenJetAK8",1);
	chain->SetBranchAddress("nGenJetAK8", &nGenJetAK8_);
	
	chain->SetBranchStatus("GenJetAK8_pt",1);
	chain->SetBranchAddress("GenJetAK8_pt", &GenJetAK8_pt_);

	chain->SetBranchStatus("GenJetAK8_eta",1);
	chain->SetBranchAddress("GenJetAK8_eta", &GenJetAK8_eta_);

	chain->SetBranchStatus("GenJetAK8_phi",1);
	chain->SetBranchAddress("GenJetAK8_phi", &GenJetAK8_phi_);

	chain->SetBranchStatus("GenJetAK8_mass",1);
	chain->SetBranchAddress("GenJetAK8_mass", &GenJetAK8_mass_);
    }

    //Fliters
    chain->SetBranchStatus("Flag_goodVertices",1);
    chain->SetBranchAddress("Flag_goodVertices",&Flag_goodVertices_);
    chain->SetBranchStatus("Flag_globalSuperTightHalo2016Filter",1);
    chain->SetBranchAddress("Flag_globalSuperTightHalo2016Filter", &Flag_globalSuperTightHalo2016Filter_);
    chain->SetBranchStatus("Flag_HBHENoiseFilter",1);
    chain->SetBranchAddress("Flag_HBHENoiseFilter", &Flag_HBHENoiseFilter_);
    chain->SetBranchStatus("Flag_HBHENoiseIsoFilter",1);
    chain->SetBranchAddress("Flag_HBHENoiseIsoFilter", &Flag_HBHENoiseIsoFilter_);
    chain->SetBranchStatus("Flag_EcalDeadCellTriggerPrimitiveFilter",1);
    chain->SetBranchAddress("Flag_EcalDeadCellTriggerPrimitiveFilter", &Flag_EcalDeadCellTriggerPrimitiveFilter_);
    chain->SetBranchStatus("Flag_BadPFMuonFilter",1);
    chain->SetBranchAddress("Flag_BadPFMuonFilter",&Flag_BadPFMuonFilter_);
    if(year =="2017" || year == "2018"){
	    chain->SetBranchStatus("Flag_ecalBadCalibFilterV2",1);
	    chain->SetBranchAddress("Flag_ecalBadCalibFilterV2",&Flag_ecalBadCalibFilterV2_);
    }

    //TRIGGERS
    if (year=="2016"){
        //muon
	    chain->SetBranchStatus("HLT_Mu50",1);
	    chain->SetBranchAddress("HLT_Mu50",&HLT_Mu50_);
	    chain->SetBranchStatus("HLT_TkMu50",1);
	    chain->SetBranchAddress("HLT_TkMu50",&HLT_TkMu50_);
        //electron
	    chain->SetBranchStatus("HLT_Ele27_WPTight_Gsf",1);
	    chain->SetBranchAddress("HLT_Ele27_WPTight_Gsf",&HLT_Ele27_WPTight_Gsf_);
	    chain->SetBranchStatus("HLT_Ele115_CaloIdVT_GsfTrkIdT",1);
	    chain->SetBranchAddress("HLT_Ele115_CaloIdVT_GsfTrkIdT",&HLT_Ele115_CaloIdVT_GsfTrkIdT_);
	    chain->SetBranchStatus("HLT_Photon175",1);
	    chain->SetBranchAddress("HLT_Photon175",&HLT_Photon175_);
    }
    if (year=="2017"){
        //muon
	    chain->SetBranchStatus("HLT_Mu50",1);
	    chain->SetBranchAddress("HLT_Mu50",&HLT_Mu50_);
	    chain->SetBranchStatus("HLT_OldMu100",1);
	    chain->SetBranchAddress("HLT_OldMu100",&HLT_OldMu100_);
	    chain->SetBranchStatus("HLT_TkMu100",1);
	    chain->SetBranchAddress("HLT_TkMu100",&HLT_TkMu100_);
        //electron
	    chain->SetBranchStatus("HLT_Ele35_WPTight_Gsf",1);
	    chain->SetBranchAddress("HLT_Ele35_WPTight_Gsf",&HLT_Ele35_WPTight_Gsf_);
	    chain->SetBranchStatus("HLT_Ele115_CaloIdVT_GsfTrkIdT",1);
	    chain->SetBranchAddress("HLT_Ele115_CaloIdVT_GsfTrkIdT",&HLT_Ele115_CaloIdVT_GsfTrkIdT_);
	    chain->SetBranchStatus("HLT_Photon200",1);
	    chain->SetBranchAddress("HLT_Photon200",&HLT_Photon200_);
    }
    if (year=="2018"){
        //muons
	    chain->SetBranchStatus("HLT_Mu50",1);
	    chain->SetBranchAddress("HLT_Mu50",&HLT_Mu50_);
	    chain->SetBranchStatus("HLT_OldMu100",1);
	    chain->SetBranchAddress("HLT_OldMu100",&HLT_OldMu100_);
	    chain->SetBranchStatus("HLT_TkMu100",1);
	    chain->SetBranchAddress("HLT_TkMu100",&HLT_TkMu100_);
        //electrons
	    chain->SetBranchStatus("HLT_Ele32_WPTight_Gsf",1);
	    chain->SetBranchAddress("HLT_Ele32_WPTight_Gsf",&HLT_Ele32_WPTight_Gsf_);
	    chain->SetBranchStatus("HLT_Ele35_WPTight_Gsf",1);
	    chain->SetBranchAddress("HLT_Ele35_WPTight_Gsf",&HLT_Ele35_WPTight_Gsf_);
	    chain->SetBranchStatus("HLT_Ele115_CaloIdVT_GsfTrkIdT",1);
	    chain->SetBranchAddress("HLT_Ele115_CaloIdVT_GsfTrkIdT",&HLT_Ele115_CaloIdVT_GsfTrkIdT_);
	    chain->SetBranchStatus("HLT_Photon200",1);
	    chain->SetBranchAddress("HLT_Photon200",&HLT_Photon200_);
    }	
    chain->SetBranchStatus("fixedGridRhoFastjetAll",1);
    chain->SetBranchAddress("fixedGridRhoFastjetAll", &rho_);

}

EventTree::~EventTree(){
    delete chain;
    // will be some memory leak due to created vectors
}

Long64_t EventTree::GetEntries(){
    return chain->GetEntries();
}

Int_t EventTree::GetEntry(Long64_t entry){
    chain->GetEntry(entry);
    return chain->GetEntries();
}
