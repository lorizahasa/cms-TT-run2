#include<iostream>
#include "../interface/EventTree_Skim.h"

EventTree::EventTree(bool xRootDAccess, string year, vector<string>fileNames, bool isMC){
    chain = new TChain("Events");

    std::cout << "Start EventTree" << std::endl;
    chain->SetCacheSize(100*1024*1024);
    bool isCopy = false;
    int nFiles = fileNames.size();
    if (xRootDAccess){
        //string dir = "root://cms-xrd-global.cern.ch/";
        string dir = "root://cmsxrootd.fnal.gov/";
        //string dir = "root://xrootd-cms.infn.it/";
        for(int fileI=0; fileI<nFiles; fileI++){
            string fName = fileNames[fileI];
            if(isCopy){
                string singleFile = fName.substr(fName.find_last_of("/")+1,fName.size());
                string xrdcp_command = "xrdcp " + dir + fName + " " + singleFile ;
                cout << xrdcp_command.c_str() << endl;
                //system(xrdcp_command.c_str());
                chain->Add( singleFile.c_str());
                cout << singleFile << "  " << chain->GetEntries() << endl;
            }
            else{
                TFile* fCheck = TFile::Open((dir+fName).c_str());
                if(!fCheck || fCheck->IsZombie() || fCheck->GetSize()<100){
                    cout<<"fCheck: issue with file: "<<dir+fName<<endl;
                    continue;
                }
                if(!fCheck->GetListOfKeys()->Contains("Events")){
                    cout<<"fCheck: issue with tree Events: "<<dir+fName<<endl;
                    continue;
                }
                fCheck->Close();
                chain->Add( (dir + fName).c_str());
                cout << dir+fName << "  " << chain->GetEntries() << endl;
            }
        }
    }
    else{
        for(int fileI=0; fileI<nFiles; fileI++){
            chain->Add(fileNames[fileI].c_str());
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
    chain->SetBranchAddress("nElectron",&nEle);
    chain->SetBranchStatus("Electron_charge",1);
    chain->SetBranchStatus("Electron_pt",1);
    chain->SetBranchAddress("Electron_pt",&elePt);
    chain->SetBranchStatus("Electron_deltaEtaSC",1);
    chain->SetBranchStatus("Electron_eta",1);
    chain->SetBranchAddress("Electron_eta",&eleEta);
    chain->SetBranchStatus("Electron_phi",1);
    chain->SetBranchAddress("Electron_phi",&elePhi);
    chain->SetBranchStatus("Electron_mass",1);
    chain->SetBranchStatus("Electron_pfRelIso03_chg",1);
    chain->SetBranchStatus("Electron_pfRelIso03_all",1);
    chain->SetBranchStatus("Electron_miniPFRelIso_all",1);
    chain->SetBranchStatus("Electron_miniPFRelIso_chg",1);
    chain->SetBranchStatus("Electron_sieie",1);
    chain->SetBranchStatus("Electron_cutBased",1); 
    chain->SetBranchAddress("Electron_cutBased",&eleID);
    chain->SetBranchStatus("Electron_mvaFall17V2noIso_WP80",1); 
    chain->SetBranchStatus("Electron_mvaFall17V2noIso_WP90",1); 
    chain->SetBranchStatus("Electron_mvaFall17V2noIso_WPL",1);
    chain->SetBranchStatus("Electron_mvaFall17V2Iso_WP80",1); 
    chain->SetBranchStatus("Electron_mvaFall17V2Iso_WP90",1); 
    chain->SetBranchStatus("Electron_mvaFall17V2Iso_WPL",1);
    chain->SetBranchStatus("Electron_vidNestedWPBitmap",1);
    chain->SetBranchStatus("Electron_photonIdx",1);

    //TrigObj
    chain->SetBranchStatus("nTrigObj",1);
    chain->SetBranchAddress("nTrigObj", &nTrigObj);
    chain->SetBranchStatus("TrigObj_pt",1);
    chain->SetBranchAddress("TrigObj_pt", &TrigObj_pt);
    chain->SetBranchStatus("TrigObj_eta",1);
    chain->SetBranchAddress("TrigObj_eta", &TrigObj_eta);
    chain->SetBranchStatus("TrigObj_phi",1);
    chain->SetBranchAddress("TrigObj_phi", &TrigObj_phi);
    chain->SetBranchStatus("TrigObj_id",1);
    chain->SetBranchAddress("TrigObj_id", &TrigObj_id);
    chain->SetBranchStatus("TrigObj_filterBits",1);
    chain->SetBranchAddress("TrigObj_filterBits", &TrigObj_filterBits);

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
    chain->SetBranchStatus("Muon_highPtId",1);
    chain->SetBranchStatus("Muon_highPurity",1);
    chain->SetBranchStatus("Muon_tkIsoId",1);
    chain->SetBranchStatus("Muon_tkRelIso",1);

    // jets
    chain->SetBranchStatus("nJet",1);
    chain->SetBranchAddress("nJet",&nJet_);
    chain->SetBranchStatus("Jet_pt",1);
    chain->SetBranchStatus("Jet_rawFactor",1);
    chain->SetBranchStatus("Jet_eta",1);
    chain->SetBranchStatus("Jet_phi",1);
    chain->SetBranchStatus("Jet_mass",1);
    chain->SetBranchStatus("Jet_jetId",1);
    chain->SetBranchStatus("Jet_puId",1);
    chain->SetBranchStatus("Jet_area",1);
    chain->SetBranchStatus("Jet_muEF",1);
    chain->SetBranchStatus("Jet_qgl",1);
    chain->SetBranchStatus("Jet_btag*",1);
    chain->SetBranchStatus("Jet_pu*",1);
    if (isMC){
        chain->SetBranchStatus("Jet_genJetIdx",1);
        chain->SetBranchStatus("Jet_hadronFlavour",1);
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
        chain->SetBranchStatus("LHEPart_*",1);
        chain->SetBranchStatus("LHEPdfWeight",1);
        chain->SetBranchStatus("PSWeight",1);
        chain->SetBranchStatus("nPSWeight",1);
        chain->SetBranchStatus("L1PreFiringWeight_Dn",1);
        chain->SetBranchStatus("L1PreFiringWeight_Nom",1);
        chain->SetBranchStatus("L1PreFiringWeight_Up",1);
    }

    //Filters
    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
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
    chain->SetBranchStatus("Flag_eeBadScFilter",1);
    chain->SetBranchAddress("Flag_eeBadScFilter", &Flag_eeBadScFilter_);
    if(year =="2017" || year == "2018"){
	    chain->SetBranchStatus("Flag_ecalBadCalibFilter",1);
	    chain->SetBranchAddress("Flag_ecalBadCalibFilter",&Flag_ecalBadCalibFilter_);
    }

    //High Level Triggers
    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgHLTRunIISummary
    //https://twiki.cern.ch/twiki/bin/view/CMS/MuonHLT2016
    //https://twiki.cern.ch/twiki/bin/view/CMS/MuonHLT2017
    //https://twiki.cern.ch/twiki/bin/view/CMS/MuonHLT2018
    std::cout << "Triggers" << std::endl;
    TString  im24, itm24, im27, m50, tm50, m100, tm100;
    TString  e27, e32, e32D, e115, e45j200, e50j165, p175, p200;
    im24    = "HLT_IsoMu24"   ;
    itm24   = "HLT_IsoTkMu24" ;
    im27    = "HLT_IsoMu27"   ;
    m50     = "HLT_Mu50"      ;
    tm50    = "HLT_TkMu50"    ;
    m100    = "HLT_Mu100"     ;
    tm100   = "HLT_TkMu100"   ;
    
    e27     = "HLT_Ele27_WPTight_Gsf"                         ;
    e32     = "HLT_Ele32_WPTight_Gsf"                         ;
    e32D    = "HLT_Ele32_WPTight_Gsf_L1DoubleEG"              ;
    e115    = "HLT_Ele115_CaloIdVT_GsfTrkIdT"                 ;
    e45j200 = "HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50" ;
    e50j165 = "HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165"         ;
    p175    = "HLT_Photon175"                                 ;
    p200    = "HLT_Photon200"                                 ;
    
    if (year.find("2016")!=std::string::npos){
        chain->SetBranchStatus(im24 , 1);
        chain->SetBranchStatus(itm24, 1);
        chain->SetBranchStatus(m50  , 1);
        chain->SetBranchStatus(tm50 , 1);
        chain->SetBranchStatus(e27    , 1);
        chain->SetBranchStatus(e115    , 1);
        chain->SetBranchStatus(e45j200, 1);
        chain->SetBranchStatus(e50j165, 1);
        chain->SetBranchStatus(p175   , 1);
        
        chain->SetBranchAddress(im24 , &im24_ );
        chain->SetBranchAddress(itm24, &itm24_);
        chain->SetBranchAddress(m50  , &m50_  );
        chain->SetBranchAddress(tm50 , &tm50_);
        chain->SetBranchAddress(e27    , &e27_);
        chain->SetBranchAddress(e115    , &e115_);
        chain->SetBranchAddress(e45j200, &e45j200_);
        chain->SetBranchAddress(e50j165, &e50j165_);
        chain->SetBranchAddress(p175   , &p175_);
    }
    if (year.find("2017")!=std::string::npos){
        chain->SetBranchStatus(im27 , 1);
        chain->SetBranchStatus(m50  , 1);
        chain->SetBranchStatus(m100 , 1);
        chain->SetBranchStatus(tm100, 1);
        chain->SetBranchStatus(e32D    , 1);
        chain->SetBranchStatus(e115    , 1);
        chain->SetBranchStatus(e50j165, 1);
        chain->SetBranchStatus(p200, 1);
        
        chain->SetBranchAddress(im27 , &im27_ );
        chain->SetBranchAddress(m50  , &m50_  );
        chain->SetBranchAddress(m100 , &m100_);
        chain->SetBranchAddress(tm100, &tm100_);
        chain->SetBranchAddress(e32D    , &e32_);
        chain->SetBranchAddress(e115    , &e115_);
        chain->SetBranchAddress(e50j165, &e50j165_);
        chain->SetBranchAddress(p200   , &p200_);
    }
    if (year.find("2018")!=std::string::npos){
        chain->SetBranchStatus(im24 , 1);
        chain->SetBranchStatus(m50  , 1);
        chain->SetBranchStatus(m100 , 1);
        chain->SetBranchStatus(tm100, 1);
        chain->SetBranchStatus(e32    , 1);
        chain->SetBranchStatus(e115    , 1);
        chain->SetBranchStatus(e50j165, 1);
        chain->SetBranchStatus(p200   , 1);
        
        chain->SetBranchAddress(im24 , &im24_ );
        chain->SetBranchAddress(m50  , &m50_  );
        chain->SetBranchAddress(m100 , &m100_);
        chain->SetBranchAddress(tm100, &tm100_);
        chain->SetBranchAddress(e32    , &e32_);
        chain->SetBranchAddress(e115    , &e115_);
        chain->SetBranchAddress(e50j165, &e50j165_);
        chain->SetBranchAddress(p200   , &p200_);
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
    //chain->GetEntry(entry);
    //return chain->GetEntries();
    return chain->GetEntry(entry);
}
std::vector<std::vector<std::string>> EventTree::splitVector(const std::vector<std::string>& strings, int n) {//from ChatGPT
    int size = strings.size() / n;  // Size of each small vector
    int remainder = strings.size() % n;  // Remaining elements
    
    std::vector<std::vector<std::string>> smallVectors;
    int index = 0;
    
    for (int i = 0; i < n; ++i) {
        if (i < remainder) {
            smallVectors.push_back(std::vector<std::string>(strings.begin() + index, strings.begin() + index + size + 1));
            index += size + 1;
        } else {
            smallVectors.push_back(std::vector<std::string>(strings.begin() + index, strings.begin() + index + size));
            index += size;
        }
    }
    
    return smallVectors;
}
