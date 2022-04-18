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
	    cout << (dir + fileNames[fileI]).c_str() << "  " << chain->GetEntries() << endl;
	    //cout << dir+fName << "  " << chain->GetEntries() << endl;
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
    chain->SetBranchStatus("PV_npvsGood",1);
    chain->SetBranchAddress("PV_npvsGood",&nGoodVtx_);

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
    chain->SetBranchAddress("MET_pt",&MET_pt_);
    chain->SetBranchStatus("MET_phi",1);

    // electrons	
    chain->SetBranchStatus("nElectron",1);
    chain->SetBranchAddress("nElectron",&nEle_);
    chain->SetBranchStatus("Electron_charge",1);
    chain->SetBranchStatus("Electron_pt",1);
    chain->SetBranchStatus("Electron_deltaEtaSC",1);
    chain->SetBranchStatus("Electron_eta",1);
    chain->SetBranchStatus("Electron_phi",1);
    chain->SetBranchStatus("Electron_mass",1);
    chain->SetBranchStatus("Electron_pfRelIso03_chg",1);
    chain->SetBranchStatus("Electron_pfRelIso03_all",1);
    chain->SetBranchStatus("Electron_miniPFRelIso_all",1);
    chain->SetBranchStatus("Electron_miniPFRelIso_chg",1);
    chain->SetBranchStatus("Electron_sieie",1);
    chain->SetBranchStatus("Electron_cutBased",1); 
    chain->SetBranchStatus("Electron_mvaFall17V2noIso_WP90",1); 
    chain->SetBranchStatus("Electron_mvaFall17V2noIso_WPL",1);
    chain->SetBranchStatus("Electron_vidNestedWPBitmap",1);
    chain->SetBranchStatus("Electron_photonIdx",1);

    // muons
    chain->SetBranchStatus("nMuon",1);
    chain->SetBranchAddress("nMuon",&nMu_);
    chain->SetBranchStatus("Muon_charge",1);
    chain->SetBranchStatus("Muon_pt",1);
    chain->SetBranchStatus("Muon_eta",1);
    chain->SetBranchStatus("Muon_phi",1);
    chain->SetBranchStatus("Muon_mass",1);
    chain->SetBranchStatus("Muon_pfRelIso04_all",1);
    chain->SetBranchStatus("Muon_miniPFRelIso_all",1);
    chain->SetBranchStatus("Muon_miniPFRelIso_chg",1);
    chain->SetBranchStatus("Muon_tightId",1);
    chain->SetBranchStatus("Muon_mediumId",1);
    chain->SetBranchStatus("Muon_isPFcand",1);
    chain->SetBranchStatus("Muon_isGlobal",1);
    chain->SetBranchStatus("Muon_isTracker",1);

    // jets
    chain->SetBranchAddress("nJet",&nJet_);
    chain->SetBranchStatus("Jet_pt",1);
    chain->SetBranchStatus("Jet_rawFactor",1);
    chain->SetBranchStatus("Jet_eta",1);
    chain->SetBranchStatus("Jet_phi",1);
    chain->SetBranchStatus("Jet_mass",1);
    chain->SetBranchStatus("Jet_jetId",1);
    chain->SetBranchStatus("Jet_area",1);
    chain->SetBranchStatus("Jet_qgl",1);
    chain->SetBranchStatus("Jet_btagCSVV2",1);
    chain->SetBranchStatus("Jet_btagDeepB",1);
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
    chain->SetBranchStatus("FatJet_jetId",1);
    chain->SetBranchStatus("FatJet_area",1);
    chain->SetBranchStatus("FatJet_msoftdrop",1);
    chain->SetBranchStatus("FatJet_deepTagMD_TvsQCD",1);
    chain->SetBranchStatus("FatJet_deepTag_TvsQCD",1);
    chain->SetBranchStatus("FatJet_particleNet_TvsQCD",1);
    if (isMC){
        chain->SetBranchStatus("FatJet_hadronFlavour",1);
        chain->SetBranchStatus("FatJet_genJetAK8Idx",1);
    }
    chain->SetBranchStatus("fixedGridRhoFastjetAll",1);

    //photons
    chain->SetBranchStatus("nPhoton",1);
    chain->SetBranchStatus("Photon_pt",1);
    chain->SetBranchStatus("Photon_eta",1);
    chain->SetBranchStatus("Photon_phi",1);
    chain->SetBranchStatus("Photon_cutBased*",1);
    chain->SetBranchStatus("Photon_mvaID*",1);
    chain->SetBranchStatus("Photon_pfRelIso03_all",1);
    chain->SetBranchStatus("Photon_pfRelIso03_chg",1);
    chain->SetBranchStatus("Photon_vidNestedWPBitmap",1);
    chain->SetBranchStatus("Photon_pixelSeed",1);
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
        chain->SetBranchStatus("nGenJetAK8",1);
        chain->SetBranchStatus("GenJetAK8_*",1);
        // weight
        chain->SetBranchStatus("Generator_weight",1);
        chain->SetBranchAddress("Generator_weight",&genWeight_);
        chain->SetBranchStatus("nLHEScaleWeight",1);
        chain->SetBranchStatus("LHEScaleWeight",1);
        chain->SetBranchStatus("nLHEPdfWeight",1);
        chain->SetBranchStatus("nLHEPart",1);
        chain->SetBranchStatus("LHEPart_pt",1);
        chain->SetBranchStatus("LHEPart_pdgId",1);
        chain->SetBranchStatus("LHEPdfWeight",1);
        chain->SetBranchStatus("PSWeight",1);
        chain->SetBranchStatus("nPSWeight",1);
        chain->SetBranchStatus("L1PreFiringWeight_Dn",1);
        chain->SetBranchStatus("L1PreFiringWeight_Nom",1);
        chain->SetBranchStatus("L1PreFiringWeight_Up",1);
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
	    chain->SetBranchStatus("Flag_ecalBadCalibFilter",1);
	    chain->SetBranchAddress("Flag_ecalBadCalibFilter",&Flag_ecalBadCalibFilter_);
    }

    //High Level Triggers
    std::cout << "Triggers" << std::endl;
    if (year.find("2016")!=std::string::npos){
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
        chain->SetBranchStatus("HLT_TkMu100",1);
        chain->SetBranchAddress("HLT_TkMu100",&HLT_TkMu100_);
        chain->SetBranchStatus("HLT_OldMu100",1);
        chain->SetBranchAddress("HLT_OldMu100",&HLT_OldMu100_);
        //electron
        chain->SetBranchStatus("HLT_Ele35_WPTight_Gsf",1);
        chain->SetBranchAddress("HLT_Ele35_WPTight_Gsf",&HLT_Ele35_WPTight_Gsf_);
        chain->SetBranchStatus("HLT_Ele115_CaloIdVT_GsfTrkIdT",1);
        chain->SetBranchAddress("HLT_Ele115_CaloIdVT_GsfTrkIdT",&HLT_Ele115_CaloIdVT_GsfTrkIdT_);
        chain->SetBranchStatus("HLT_Photon200",1);
        chain->SetBranchAddress("HLT_Photon200",&HLT_Photon200_);
    }

    if (year=="2018"){
        //muon
        chain->SetBranchStatus("HLT_Mu50",1);
        chain->SetBranchAddress("HLT_Mu50",&HLT_Mu50_);
        chain->SetBranchStatus("HLT_TkMu100",1);
        chain->SetBranchAddress("HLT_TkMu100",&HLT_TkMu100_);
        chain->SetBranchStatus("HLT_OldMu100",1);
        chain->SetBranchAddress("HLT_OldMu100",&HLT_OldMu100_);
        //electrom
        chain->SetBranchStatus("HLT_Ele35_WPTight_Gsf",1);
        chain->SetBranchAddress("HLT_Ele35_WPTight_Gsf",&HLT_Ele35_WPTight_Gsf_);
        chain->SetBranchStatus("HLT_Ele115_CaloIdVT_GsfTrkIdT",1);
        chain->SetBranchAddress("HLT_Ele115_CaloIdVT_GsfTrkIdT",&HLT_Ele115_CaloIdVT_GsfTrkIdT_);
        chain->SetBranchStatus("HLT_Photon200",1);
        chain->SetBranchAddress("HLT_Photon200",&HLT_Photon200_);
    }	
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
