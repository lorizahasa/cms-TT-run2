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
	    string fName = (string) fileNames[fileI];
	    chain->Add(fileNames[fileI]);
	    cout << fName << "  " << chain->GetEntries() << endl;
	}
    }
    chain->SetBranchStatus("*",0);
    
    // keep some important branches
    chain->SetBranchStatus("PV_npvsGood",1);
    chain->SetBranchAddress("PV_npvsGood",&nGoodVtx_);
    chain->SetBranchStatus("passTrigMu",1);
    chain->SetBranchAddress("passTrigMu",&passTrigMu_);
    chain->SetBranchStatus("passTrigEle",1);
    chain->SetBranchAddress("passTrigEle",&passTrigEle_);

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
    }

    // MET
    chain->SetBranchStatus("MET_pt",1);
    chain->SetBranchAddress("MET_pt", &MET_pt_);

    chain->SetBranchStatus("MET_phi",1);
    chain->SetBranchAddress("MET_phi", &MET_phi_);


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

    chain->SetBranchStatus("Electron_cutBased",1);
    chain->SetBranchAddress("Electron_cutBased", &eleID_);
    
    chain->SetBranchStatus("Electron_miniPFRelIso_all",1);
    chain->SetBranchAddress("Electron_miniPFRelIso_all", &eleMiniPFRelIso_);

    chain->SetBranchStatus("Electron_mvaFall17V2Iso_WP80",1);
    chain->SetBranchAddress("Electron_mvaFall17V2Iso_WP80", &eleMVAFall17V2Iso_WP80_);

    chain->SetBranchStatus("Electron_mvaFall17V2Iso_WPL",1);
    chain->SetBranchAddress("Electron_mvaFall17V2Iso_WPL", &eleMVAFall17V2Iso_WPL_);


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

    chain->SetBranchStatus("Muon_mediumId",1);
    chain->SetBranchAddress("Muon_mediumId", &muMediumId_);

    chain->SetBranchStatus("Muon_tightId",1);
    chain->SetBranchAddress("Muon_tightId", &muTightId_);

    chain->SetBranchStatus("Muon_highPtId",1);
    chain->SetBranchAddress("Muon_highPtId", &muHighPtId_);
    
    chain->SetBranchStatus("Muon_highPurity",1);
    chain->SetBranchAddress("Muon_highPurity", &muHighPurity_);

    chain->SetBranchStatus("Muon_tkIsoId",1);
    chain->SetBranchAddress("Muon_tkIsoId", &muTkIsoId_);

    chain->SetBranchStatus("Muon_pfRelIso04_all",1);
    chain->SetBranchAddress("Muon_pfRelIso04_all", &muPFRelIso_);

    chain->SetBranchStatus("Muon_tkRelIso",1);
    chain->SetBranchAddress("Muon_tkRelIso", &muTkRelIso_);

    chain->SetBranchStatus("Muon_isPFcand",1);
    chain->SetBranchAddress("Muon_isPFcand", &muIsPFMuon_);

    chain->SetBranchStatus("Muon_isGlobal",1);
    chain->SetBranchAddress("Muon_isGlobal", &muIsGlobal_);

    chain->SetBranchStatus("Muon_isTracker",1);
    chain->SetBranchAddress("Muon_isTracker", &muIsTracker_);

    chain->SetBranchStatus("Muon_dxy",1);
    chain->SetBranchAddress("Muon_dxy", &muDxy_);

    chain->SetBranchStatus("Muon_dz",1);
    chain->SetBranchAddress("Muon_dz", &muDz_);

    // jets
    chain->SetBranchStatus("nJet",1);
    chain->SetBranchAddress("nJet", &nJet_);
 
    chain->SetBranchStatus("Jet_pt",1);
    chain->SetBranchAddress("Jet_pt", &jetPt_);
    
    chain->SetBranchStatus("Jet_qgl", 1);
    chain->SetBranchAddress("Jet_qgl", &jetQGL_);

    //chain->SetBranchStatus("Jet_qgl_0", 1);                                                                                                                          
    //chain->SetBranchAddress("Jet_qgl_0", &jetQGL0_);

    //chain->SetBranchStatus("Jet_qgl_1", 1);                                                                                                                          
    //chain->SetBranchAddress("Jet_qgl_1", &jetQGL1_);

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

    chain->SetBranchStatus("Jet_puId",1);
    chain->SetBranchAddress("Jet_puId", &puID_);

    chain->SetBranchStatus("Jet_area",1);
    chain->SetBranchAddress("Jet_area", &jetArea_);

    chain->SetBranchStatus("Jet_muEF",1);
    chain->SetBranchAddress("Jet_muEF", &jetmuEF_);

    chain->SetBranchStatus("Jet_btagDeepB",1);
    chain->SetBranchAddress("Jet_btagDeepB", &jetBtagDeepB_);
 
   // chain->SetBranchStatus("Jet_btagDeepB0",1);
   // chain->SetBranchAddress("Jet_btagDeepB0", &jetBtagDeepB0_);

    //chain->SetBranchStatus("Jet_btagDeepB1",1);
    //chain->SetBranchAddress("Jet_btagDeepB1", &jetBtagDeepB1_);

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

    //chain->SetBranchStatus("FatJet_pt_0",1);
    //chain->SetBranchAddress("FatJet_pt_0", &fatJetPt0_);

    chain->SetBranchStatus("FatJet_eta",1);
    chain->SetBranchAddress("FatJet_eta", &fatJetEta_);
    
    //chain->SetBranchStatus("FatJet_eta_0",1);
    //chain->SetBranchAddress("FatJet_eta_0", &fatJetEta0_);

    chain->SetBranchStatus("FatJet_phi",1);
    chain->SetBranchAddress("FatJet_phi", &fatJetPhi_);

    chain->SetBranchStatus("FatJet_area",1);
    chain->SetBranchAddress("FatJet_area", &fatJetArea_);

    chain->SetBranchStatus("FatJet_mass",1);
    chain->SetBranchAddress("FatJet_mass", &fatJetMass_);

    chain->SetBranchStatus("FatJet_msoftdrop",1);
    chain->SetBranchAddress("FatJet_msoftdrop", &fatJetMassSoftDrop_);

    //chain->SetBranchStatus("FatJet_msoftdrop_0",1);
    //chain->SetBranchAddress("FatJet_msoftdrop_0", &fatJetMassSoftDrop0_);

    chain->SetBranchStatus("FatJet_jetId",1);
    chain->SetBranchAddress("FatJet_jetId", &fatJetID_);

    chain->SetBranchStatus("FatJet_deepTagMD_TvsQCD",1);
    chain->SetBranchAddress("FatJet_deepTagMD_TvsQCD", &fatJetDeepTagMDT_);

    chain->SetBranchStatus("FatJet_deepTag_TvsQCD",1);
    chain->SetBranchAddress("FatJet_deepTag_TvsQCD", &fatJetDeepTagT_);

    chain->SetBranchStatus("FatJet_particleNet_TvsQCD",1);
    chain->SetBranchAddress("FatJet_particleNet_TvsQCD", &fatJetPNET_);


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
	
	chain->SetBranchStatus("Photon_cutBased",1);
	chain->SetBranchAddress("Photon_cutBased", &phoIDcutbased_);

    chain->SetBranchStatus("Photon_pfRelIso03_all",1);
    chain->SetBranchAddress("Photon_pfRelIso03_all", &phoPFRelIso_);

    chain->SetBranchStatus("Photon_pfRelIso03_chg",1);
    chain->SetBranchAddress("Photon_pfRelIso03_chg", &phoPFRelChIso_);

    chain->SetBranchStatus("Photon_vidNestedWPBitmap",1);
    chain->SetBranchAddress("Photon_vidNestedWPBitmap", &phoVidWPBitmap_);

    chain->SetBranchStatus("Photon_pixelSeed",1);
    chain->SetBranchAddress("Photon_pixelSeed", &phoPixelSeed_);

    if (!isData_){
	chain->SetBranchStatus("Photon_genPartIdx",1);
	chain->SetBranchAddress("Photon_genPartIdx", &phoGenPartIdx_);
    }
    chain->SetBranchStatus("Photon_electronVeto",1);
    chain->SetBranchAddress("Photon_electronVeto", &phoEleVeto_);
	
    chain->SetBranchStatus("Photon_mvaID_WP80",1);
    chain->SetBranchAddress("Photon_mvaID_WP80", &phoMVAId_WP80_);

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

    chain->SetBranchStatus("fixedGridRhoFastjetAll",1);
    chain->SetBranchAddress("fixedGridRhoFastjetAll", &rho_);

    chain->SetBranchStatus("L1PreFiringWeight_Dn",1);
    chain->SetBranchAddress("L1PreFiringWeight_Dn", &prefireDn_);

    chain->SetBranchStatus("L1PreFiringWeight_Nom",1);
    chain->SetBranchAddress("L1PreFiringWeight_Nom",&prefireNom_);

    chain->SetBranchStatus("L1PreFiringWeight_Up",1);
    chain->SetBranchAddress("L1PreFiringWeight_Up",&prefireUp_);

    TString  im24, itm24, im27, m50, tm50, m100, tm100;
    im24    = "HLT_IsoMu24"   ;
    itm24   = "HLT_IsoTkMu24" ;
    im27    = "HLT_IsoMu27"   ;
    m50     = "HLT_Mu50"      ;
    tm50    = "HLT_TkMu50"    ;
    m100    = "HLT_Mu100"     ;
    tm100   = "HLT_TkMu100"   ;
    if (year.find("2016")!=std::string::npos){
        chain->SetBranchStatus(im24 , 1);
        chain->SetBranchStatus(itm24, 1);
        chain->SetBranchStatus(m50  , 1);
        chain->SetBranchStatus(tm50 , 1);

        chain->SetBranchAddress(im24 , &im24_ );
        chain->SetBranchAddress(itm24, &itm24_);
        chain->SetBranchAddress(m50  , &m50_  );
        chain->SetBranchAddress(tm50 , &tm50_);
    }
    if (year.find("2017")!=std::string::npos){
        chain->SetBranchStatus(im27 , 1);
        chain->SetBranchStatus(m50  , 1);
        chain->SetBranchStatus(m100 , 1);
        chain->SetBranchStatus(tm100, 1);
        
        chain->SetBranchAddress(im27 , &im27_ );
        chain->SetBranchAddress(m50  , &m50_  );
        chain->SetBranchAddress(m100 , &m100_);
        chain->SetBranchAddress(tm100, &tm100_);
    }
    if (year.find("2018")!=std::string::npos){
        chain->SetBranchStatus(im24 , 1);
        chain->SetBranchStatus(m50  , 1);
        chain->SetBranchStatus(m100 , 1);
        chain->SetBranchStatus(tm100, 1);
        
        chain->SetBranchAddress(im24 , &im24_ );
        chain->SetBranchAddress(m50  , &m50_  );
        chain->SetBranchAddress(m100 , &m100_);
        chain->SetBranchAddress(tm100, &tm100_);
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
