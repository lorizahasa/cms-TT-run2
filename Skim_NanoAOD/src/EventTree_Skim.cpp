#include<iostream>
#include "../interface/EventTree_Skim.h"

EventTree::EventTree(int nFiles, bool xRootDAccess, string year, char** fileNames, bool isMC){
    chain = new TChain("Events");

    std::cout << "Start EventTree" << std::endl;
    chain->SetCacheSize(100*1024*1024);
    if (xRootDAccess){
	//string dir = "root://cms-xrd-global.cern.ch/";
	string dir = "root://cmsxrootd.fnal.gov/";
	for(int fileI=0; fileI<nFiles; fileI++){
	    string fName = (string) fileNames[fileI];
	    chain->Add( (dir + fileNames[fileI]).c_str() );
	    //cout << dir+fName << "  " << chain->GetEntries() << endl;
	    cout << (dir + fileNames[fileI]).c_str() << "  " << chain->GetEntries() << endl;
	}
    }
    else{
	for(int fileI=0; fileI<nFiles; fileI++){
	    chain->Add(fileNames[fileI]);
	    cout <<fileNames[fileI]<<endl;
	}
    }
    std::cout << "Begin" << std::endl;
    chain->SetBranchStatus("*",0);
	
    // keep some important branches
    chain->SetBranchStatus("PV_ndof",1);
    chain->SetBranchStatus("PV_x",1);
    chain->SetBranchStatus("PV_y",1);
    chain->SetBranchStatus("PV_z",1);
    chain->SetBranchStatus("PV_chi2",1);
    chain->SetBranchStatus("PV_npvs",1);
    chain->SetBranchStatus("PV_npvsGood",1);


    if (isMC){
	chain->SetBranchStatus("Pileup_nPU",1);
	chain->SetBranchAddress("Pileup_nPU", &nPU_);
	chain->SetBranchStatus("Pileup_nTrueInt",1);
	chain->SetBranchAddress("Pileup_nTrueInt", &nPUTrue_);
    }
	
    // event
    chain->SetBranchStatus("run",1);
    chain->SetBranchStatus("event",1);
    chain->SetBranchStatus("luminosityBlock",1);

    // MET
    chain->SetBranchStatus("MET_pt",1);
    chain->SetBranchStatus("MET_phi",1);

    if (isMC){
	chain->SetBranchStatus("GenMET_pt",1);
	chain->SetBranchStatus("GenMET_phi",1);
    }

    // electrons	
    chain->SetBranchStatus("nElectron",1);
    chain->SetBranchStatus("Electron_charge",1);
    chain->SetBranchStatus("Electron_pt",1);
    chain->SetBranchStatus("Electron_deltaEtaSC",1);
    chain->SetBranchStatus("Electron_eta",1);
    chain->SetBranchStatus("Electron_phi",1);
    chain->SetBranchStatus("Electron_mass",1);
    chain->SetBranchStatus("Electron_pfRelIso03_chg",1);
    chain->SetBranchStatus("Electron_pfRelIso03_all",1);
    chain->SetBranchStatus("Electron_sieie",1);
    chain->SetBranchStatus("Electron_cutBased",1); 
    chain->SetBranchStatus("Electron_vidNestedWPBitmap",1);
    chain->SetBranchStatus("Electron_dxy",1);
    chain->SetBranchStatus("Electron_dz",1);
    chain->SetBranchStatus("Electron_dr03EcalRecHitSumEt",1);
    chain->SetBranchStatus("Electron_dr03HcalDepth1TowerSumEt",1);
    chain->SetBranchStatus("Electron_dr03TkSumPt",1);
    chain->SetBranchStatus("Electron_photonIdx",1);

    // muons
    chain->SetBranchStatus("nMuon",1);
    chain->SetBranchStatus("Muon_charge",1);
    chain->SetBranchStatus("Muon_pt",1);
    chain->SetBranchStatus("Muon_eta",1);
    chain->SetBranchStatus("Muon_phi",1);
    chain->SetBranchStatus("Muon_mass",1);
    chain->SetBranchStatus("Muon_pfRelIso04_all",1);
    chain->SetBranchStatus("Muon_tightId",1);
    chain->SetBranchStatus("Muon_mediumId",1);
    chain->SetBranchStatus("Muon_isPFcand",1);
    chain->SetBranchStatus("Muon_isGlobal",1);
    chain->SetBranchStatus("Muon_isTracker",1);

    // jets
    chain->SetBranchStatus("nJet",1);
    chain->SetBranchStatus("Jet_pt",1);
    chain->SetBranchStatus("Jet_rawFactor",1);
    chain->SetBranchStatus("Jet_eta",1);
    chain->SetBranchStatus("Jet_phi",1);
    chain->SetBranchStatus("Jet_mass",1);
    chain->SetBranchStatus("Jet_jetId",1);
    chain->SetBranchStatus("Jet_area",1);
    chain->SetBranchStatus("Jet_btagCMVA",1);
    chain->SetBranchStatus("Jet_btagCSVV2",1);
    chain->SetBranchStatus("Jet_btagDeepB",1);
    chain->SetBranchStatus("Jet_btagDeepC",1);
    chain->SetBranchStatus("Jet_btagDeepFlavB",1);
    chain->SetBranchStatus("Jet_chEmEF",1);
    chain->SetBranchStatus("Jet_neEmEF",1);
    if (isMC){
        chain->SetBranchStatus("Jet_hadronFlavour",1);
        chain->SetBranchStatus("Jet_genJetIdx",1);
    }

    //fat jets
    chain->SetBranchStatus("nFatJet",1);
    chain->SetBranchStatus("FatJet_pt",1);
    chain->SetBranchStatus("FatJet_eta",1);
    chain->SetBranchStatus("FatJet_phi",1);
    chain->SetBranchStatus("FatJet_mass",1);
    chain->SetBranchStatus("FatJet_msoftdrop",1);
    chain->SetBranchStatus("FatJet_jetId",1);
    chain->SetBranchStatus("FatJet_btagDeepB",1);
    chain->SetBranchStatus("FatJet_deepTagMD_TvsQCD",1);
    chain->SetBranchStatus("FatJet_deepTagMD_WvsQCD",1);
    chain->SetBranchStatus("FatJet_deepTag_TvsQCD",1);
    chain->SetBranchStatus("FatJet_deepTag_WvsQCD",1);
    chain->SetBranchStatus("FatJet_electronIdx3SJ",1);
    chain->SetBranchStatus("FatJet_muonIdx3SJ",1);
    chain->SetBranchStatus("FatJet_tau1",1);
    chain->SetBranchStatus("FatJet_tau2",1);
    chain->SetBranchStatus("FatJet_tau3",1);
    chain->SetBranchStatus("FatJet_tau4",1);
    if (isMC){
        chain->SetBranchStatus("FatJet_hadronFlavour",1);
        chain->SetBranchStatus("FatJet_genJetAK8Idx",1);
    }

    //photons
    chain->SetBranchStatus("nPhoton",1);
    chain->SetBranchStatus("Photon_pt",1);
    chain->SetBranchStatus("Photon_eta",1);
    chain->SetBranchStatus("Photon_phi",1);
    chain->SetBranchStatus("Photon_isScEtaEB",1);
    chain->SetBranchStatus("Photon_isScEtaEE",1);
    chain->SetBranchStatus("Photon_cutBased*",1);
    chain->SetBranchStatus("Photon_mvaID*",1);
    chain->SetBranchStatus("Photon_pfRelIso03_all",1);
    chain->SetBranchStatus("Photon_pfRelIso03_chg",1);
    chain->SetBranchStatus("Photon_vidNestedWPBitmap",1);
    chain->SetBranchStatus("Photon_pixelSeed",1);
    chain->SetBranchStatus("Photon_r9",1);
    chain->SetBranchStatus("Photon_sieie",1);
    chain->SetBranchStatus("Photon_hoe",1);
    if (isMC){
        chain->SetBranchStatus("Photon_genPartIdx",1);
    }
    chain->SetBranchStatus("Photon_electronVeto",1);
	
    if (isMC){
        // Gen Partons
        chain->SetBranchStatus("nGenPart",1);
        chain->SetBranchStatus("GenPart_pt",1);
        chain->SetBranchStatus("GenPart_eta",1);
        chain->SetBranchStatus("GenPart_phi",1);
        chain->SetBranchStatus("GenPart_mass",1);
        chain->SetBranchStatus("GenPart_genPartIdxMother",1);
        chain->SetBranchStatus("GenPart_pdgId",1);
        chain->SetBranchStatus("GenPart_status",1);
        chain->SetBranchStatus("GenPart_statusFlags",1);
        chain->SetBranchStatus("nGenJet",1);
        chain->SetBranchStatus("GenJet_pt",1);
        chain->SetBranchStatus("GenJet_eta",1);
        chain->SetBranchStatus("GenJet_phi",1);
        chain->SetBranchStatus("GenJet_mass",1);
        // weight
        chain->SetBranchStatus("Generator_weight",1);
        chain->SetBranchStatus("Generator_weight",&genWeight_);
        chain->SetBranchStatus("nLHEScaleWeight",1);
        chain->SetBranchStatus("LHEScaleWeight",1);
        chain->SetBranchStatus("nLHEPdfWeight",1);
        chain->SetBranchStatus("LHEPdfWeight",1);
        chain->SetBranchStatus("PSWeight",1);
        chain->SetBranchStatus("nPSWeight",1);
        chain->SetBranchStatus("LHEWeight_originalXWGTUP",1);
        if (year=="2016" || year=="2017"){
        chain->SetBranchStatus("L1PreFiringWeight*",1);
        }
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
    std::cout << "Triggers" << std::endl;
    if (year=="2016"){
        chain->SetBranchStatus("HLT_Ele27_WPTight_Gsf",1);
        chain->SetBranchAddress("HLT_Ele27_WPTight_Gsf",&HLT_Ele27_WPTight_Gsf_);
        chain->SetBranchStatus("HLT_IsoMu24",1);
        chain->SetBranchAddress("HLT_IsoMu24",&HLT_IsoMu24_);
        chain->SetBranchStatus("HLT_IsoTkMu24",1);
        chain->SetBranchAddress("HLT_IsoTkMu24",&HLT_IsoTkMu24_);
    }
    
    if (year=="2017"){
        chain->SetBranchStatus("HLT_Ele32_WPTight_Gsf_L1DoubleEG",1);
        chain->SetBranchAddress("HLT_Ele32_WPTight_Gsf_L1DoubleEG",&HLT_Ele32_WPTight_Gsf_L1DoubleEG_);
        chain->SetBranchStatus("HLT_IsoMu24",1);
        chain->SetBranchAddress("HLT_IsoMu24",&HLT_IsoMu24_);
        chain->SetBranchStatus("HLT_IsoMu27",1);
        chain->SetBranchAddress("HLT_IsoMu27",&HLT_IsoMu27_);
    }

    if (year=="2018"){
        chain->SetBranchStatus("HLT_Ele32_WPTight_Gsf",1);
        chain->SetBranchAddress("HLT_Ele32_WPTight_Gsf",&HLT_Ele32_WPTight_Gsf_);
        chain->SetBranchStatus("HLT_IsoMu24",1);
        chain->SetBranchAddress("HLT_IsoMu24",&HLT_IsoMu24_);
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
