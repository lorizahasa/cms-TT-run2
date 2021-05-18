#include"../interface/Selector.h"

TRandom* generator = new TRandom3(0);

Selector::Selector(){
    year = "2016";
    printEvent = -1;

    looseJetID = false;
    JERsystLevel  = 1;
    JECsystLevel  = 1;
    phosmearLevel = 1;
    elesmearLevel = 1;
    phoscaleLevel = 1;
    elescaleLevel = 1;
    useDeepCSVbTag = false;
    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
    // CSVv2M
    btag_cut = 0.8484;  
    // DeepCSV
    btag_cut_DeepCSV = 0.6324;  

    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/DeepAK8Tagging2018WPsSFs
    toptag_cut_DeepAK8 = 0.834;

    // whether to invert lepton requirements for 
    QCDselect = false;

    skipAK4AK8dr = false;

    smearJetPt = true;
    smearPho = true;
    smearEle = true;
    scaleEle = true;
    scalePho = true;

}

void Selector::init_JER(std::string inputPrefix){
    jetResolutionAK4 = new JME::JetResolution((inputPrefix+"_MC_PtResolution_AK4PFchs.txt").c_str());
    jetResolutionScaleFactorAK4 = new JME::JetResolutionScaleFactor((inputPrefix+"_MC_SF_AK4PFchs.txt").c_str());
    jetResolutionAK8 = new JME::JetResolution((inputPrefix+"_MC_PtResolution_AK8PFchs.txt").c_str());
    jetResolutionScaleFactorAK8 = new JME::JetResolutionScaleFactor((inputPrefix+"_MC_SF_AK8PFchs.txt").c_str());
}

void Selector::process_objects(EventTree* inp_tree){
    tree = inp_tree;
    clear_vectors();

    generator->SetSeed(tree->event_ + tree->run_ + tree->lumis_);

    filter_muons();
    filter_electrons();
    filter_photons();
    filter_fatjets();
    filter_jets();
}

void Selector::clear_vectors(){
    Muons.clear();
    MuonsLoose.clear();
    Electrons.clear();
    ElectronsLoose.clear();
    Jets.clear();
    FatJets.clear();
    bJets.clear();
    Photons.clear();
    PhoPassChHadIso.clear();
    PhoPassPhoIso.clear();
    PhoPassSih.clear();
    LoosePhotons.clear();
    PhotonsNoID.clear();
    PhoChHadIso_corr.clear();
    PhoNeuHadIso_corr.clear();
    PhoPhoIso_corr.clear();
    PhoRandConeChHadIso_corr.clear();
}

void Selector::filter_muons(){
    if (tree->event_==printEvent){
	    cout << "Found Event, Starting Muons" << endl;
	    cout << " nMu=" << tree->nMuon_ << endl;
    }
    for(int muInd = 0; muInd < tree->nMuon_; ++muInd){
        double eta = tree->muEta_[muInd];
        double pt = tree->muPt_[muInd];
        double muMiniIso = tree->muMiniPFRelIso_[muInd];
        bool looseMuonID = tree->muIsPFMuon_[muInd] && (tree->muIsTracker_[muInd] || tree->muIsGlobal_[muInd]);
        bool tightMuonID = tree->muTightId_[muInd];
        bool passTight = (pt >= 55.0 &&
        		  TMath::Abs(eta) <= 2.4 &&
        		  tightMuonID && muMiniIso < 0.1
        		  );
        bool passLoose = (pt >= 30.0 &&
        		  TMath::Abs(eta) <= 2.4 &&
                          looseMuonID && !passTight &&
                          muMiniIso < 0.4
        		  );
        if(passTight) Muons.push_back(muInd);
        else if (passLoose) MuonsLoose.push_back(muInd);
        if (tree->event_==printEvent){
            cout << "-- " << muInd << " passTight="<<passTight<< " passLoose="<<passLoose << " pt="<<pt<< " eta="<<eta<< " phi="<<tree->muPhi_[muInd]<< " tightID="<<tightMuonID<< " looseID="<<looseMuonID << " pfRelIso="<<muMiniIso << endl;
        } 
    }
}

void Selector::filter_electrons(){
    if (tree->event_==printEvent){
	    cout << "Found Event, Starting Electrons" << endl;
	    cout << " nEle=" << tree->nEle_ << endl;
    }
    for(int eleInd = 0; eleInd < tree->nEle_; ++eleInd){
        double eta = tree->eleEta_[eleInd];
        double absEta = TMath::Abs(eta);
        double SCeta = eta + tree->eleDeltaEtaSC_[eleInd];
        double absSCEta = TMath::Abs(SCeta);
        double pt = tree->elePt_[eleInd];
        double eleMiniIso = tree->eleMiniPFRelIso_[eleInd];
        // make sure it doesn't fall within the gap
        bool passEtaEBEEGap = (absSCEta < 1.4442) || (absSCEta > 1.566);

        bool passTightID = tree->eleMVAFall17V2noIso_WP90_[eleInd];
        bool passVetoID  = tree->eleMVAFall17V2noIso_WPL_[eleInd]; 

        bool eleSel = (passEtaEBEEGap && 
                       absEta <= 2.2 &&
                       pt >= 50.0 &&
                       eleMiniIso <= 0.1 &&
                       passTightID);
        bool looseSel = (passEtaEBEEGap && 
                         absEta <= 2.2 &&
                         pt >= 35.0 &&
                         eleMiniIso <= 0.4 &&
                         passVetoID &&
                         !eleSel);
        if(eleSel) Electrons.push_back(eleInd);
        else if(looseSel) ElectronsLoose.push_back(eleInd);
        if (tree->event_==printEvent){
            cout << "-- " << eleInd << " eleSel=" <<  eleSel << " looseSel=" <<  looseSel << " pt="<<pt<< " eta="<<eta<< " phi="<<tree->elePhi_[eleInd]<< " eleID="<<passTightID <<"looseID = "<<passVetoID << endl; 
        } 
    }
}

void Selector::filter_photons(){
    if (tree->event_==printEvent){
	    cout << "Found Event Staring Photons" << endl;
	    cout << " nPho=" << tree->nPho_ << endl;
    }
    for(int phoInd = 0; phoInd < tree->nPho_; ++phoInd){
        double et = tree->phoEt_[phoInd];
        double eta = tree->phoEta_[phoInd];
        double absEta = TMath::Abs(eta);
        double phi = tree->phoPhi_[phoInd];
        bool isEB = tree->phoIsEB_[phoInd];
        bool isEE = tree->phoIsEE_[phoInd];
        uint photonID = tree->phoIDcutbased_[phoInd];
        bool passMediumPhotonID = photonID >= 2; //0:fail, 1:loose, 2:medium, 3:tight 
        double phoPFRelIso = tree->phoPFRelIso_[phoInd];
        double phoPFRelChIso = tree->phoPFRelChIso_[phoInd];
        bool passDR_lep_pho = true;
        //loop over selected electrons
        for(std::vector<int>::const_iterator eleInd = Electrons.begin(); eleInd != Electrons.end(); eleInd++) {
	    if (dR(eta, phi, tree->eleEta_[*eleInd], tree->elePhi_[*eleInd]) < 0.4) passDR_lep_pho = false;
        }
        //loop over selected muons
        for(std::vector<int>::const_iterator muInd = Muons.begin(); muInd != Muons.end(); muInd++) {
	    if (dR(eta, phi, tree->muEta_[*muInd], tree->muPhi_[*muInd]) < 0.4) passDR_lep_pho = false;
        }
        bool hasPixelSeed = tree->phoPixelSeed_[phoInd];
        bool phoPresel = (et >= 20.0 &&                          
                          absEta <= 1.4442 &&
                          passDR_lep_pho && 
                          !hasPixelSeed
			  );
        vector<bool> cutBasedID_split = parsePhotonVIDCuts(tree->phoVidWPBitmap_[phoInd], 2);
        bool passMediumIDNoChIsoOrSIEIE = cutBasedID_split[1] && cutBasedID_split[4] && cutBasedID_split[5]; // HoverE (1), NeuIso (4), and PhoIso (5) cuts, skip ChIso (3) and SIEIE (2)
        if(phoPresel && passMediumPhotonID) Photons.push_back(phoInd);
        if(phoPresel && passMediumIDNoChIsoOrSIEIE) LoosePhotons.push_back(phoInd);
        if (tree->event_==printEvent){
            cout << "-- " << phoInd << " pt="<<et<< " eta="<<eta<< " phi="<<phi<<"presel="<< phoPresel<< " drlepgamma="<<passDR_lep_pho<< " medID="<<passMediumPhotonID<<endl;
        } 
    }
}

void Selector::filter_jets(){
    if (tree->event_==printEvent){
    	cout << "Found Event Staring Jets" << endl;
        cout << " nJet=" << tree->nJet_ << endl;
    }
    for(int jetInd = 0; jetInd < tree->nJet_; ++jetInd){
        double pt = tree->jetPt_[jetInd];
        double eta = tree->jetEta_[jetInd];
        double phi = tree->jetPhi_[jetInd];
        //tight ID for 2016 (bit 0), tightLeptVeto for 2017 (bit 1)
        int jetID_cutBit = 1;
        if (year=="2016"){ jetID_cutBit = 0; }
        bool jetID_pass = (tree->jetID_[jetInd]>>0 & 1 && looseJetID) || (tree->jetID_[jetInd]>>jetID_cutBit & 1);

        double resolution = 0.;
        if (tree->event_==printEvent){
            cout << "------Jet "<<jetInd<< "------" << endl;
        }
        if (!tree->isData_){
            jetParamAK4.setJetEta(tree->jetEta_[jetInd]);
            jetParamAK4.setJetPt(tree->jetPt_[jetInd]);
            jetParamAK4.setJetArea(tree->jetArea_[jetInd]);
            jetParamAK4.setRho(tree->rho_);
            resolution = jetResolutionAK4->getResolution(jetParamAK4);
            double jetSF = 1.0;
            if (JERsystLevel==1) jetSF = jetResolutionScaleFactorAK4->getScaleFactor(jetParamAK4,Variation::NOMINAL);
            if (JERsystLevel==0) jetSF = jetResolutionScaleFactorAK4->getScaleFactor(jetParamAK4,Variation::DOWN);
            if (JERsystLevel==2) jetSF = jetResolutionScaleFactorAK4->getScaleFactor(jetParamAK4,Variation::UP);
            double jetSmear = 1;
            int genIdx = tree->jetGenJetIdx_[jetInd];
            if ( (genIdx>-1) && (genIdx < tree->nGenJet_)){
	        double genJetPt = tree->GenJet_pt_[genIdx];
	        jetSmear = 1. + (jetSF - 1.) * (pt - genJetPt)/pt;
            }else{
	        jetSmear = 1 + generator->Gaus(0, resolution) * sqrt( max(jetSF*jetSF - 1, 0.) );
            }
            if (tree->event_==printEvent){
	        cout << "  DoJetSmear: " << smearJetPt << endl;
	        cout << "  GenIdx: "<< genIdx << endl;
	        cout << "  jetSF: "<< jetSF << endl;
	        cout << "  JetSmear: "<<jetSmear << endl;
            }
            if (smearJetPt){
	        pt = pt*jetSmear;
	        tree->jetPt_[jetInd] = pt;
            }
        }
        bool passDR_lep_jet = true;
        //loop over selected electrons
        for(std::vector<int>::const_iterator eleInd = Electrons.begin(); eleInd != Electrons.end(); eleInd++) {
	    if (dR(eta, phi, tree->eleEta_[*eleInd], tree->elePhi_[*eleInd]) < 0.4) passDR_lep_jet = false;
        }
        //loop over selected muons
        for(std::vector<int>::const_iterator muInd = Muons.begin(); muInd != Muons.end(); muInd++) {
            if (dR(eta, phi, tree->muEta_[*muInd], tree->muPhi_[*muInd]) < 0.4) passDR_lep_jet = false;
        }
        bool passDR_pho_jet = true;
        //loop over selected photons
        for(std::vector<int>::const_iterator phoInd = Photons.begin(); phoInd != Photons.end(); phoInd++) {
            if (dR(eta, phi, tree->phoEta_[*phoInd], tree->phoPhi_[*phoInd]) < 0.1) passDR_pho_jet = false;
            if (tree->event_==printEvent){
	        cout << "       phoInd=" << *phoInd << "   dR=" << dR(eta, phi, tree->phoEta_[*phoInd], tree->phoPhi_[*phoInd]) << "  phoEta=" << tree->phoEta_[*phoInd] << "  phoPhi=" << tree->phoPhi_[*phoInd] << endl;
            }
        }

        bool passDR_ak8 = true;
        if (!skipAK4AK8dr){
            //loop over selected fat jets
            for(std::vector<int>::const_iterator fatJetInd = FatJets.begin(); fatJetInd != FatJets.end(); fatJetInd++) {
                if (dR(eta, phi, tree->fatJetEta_[*fatJetInd], tree->fatJetPhi_[*fatJetInd]) < 0.8) passDR_ak8 = false;
            }
        }

        bool jetPresel = (pt >= 30 &&
                          TMath::Abs(eta) <= 2.4 &&
                          jetID_pass &&
                          passDR_lep_jet &&
                          passDR_pho_jet &&
                          passDR_ak8
                          );
        if(jetPresel){
            Jets.push_back(jetInd);
            jet_resolution.push_back(resolution);
            if (!useDeepCSVbTag){
                if( tree->jetBtagCSVV2_[jetInd] > btag_cut){
                    bJets.push_back(jetInd);
                    jet_isTagged.push_back(true);
                } 
                else {
                    jet_isTagged.push_back(false);
                }
            }
            else {
                if( tree->jetBtagDeepB_[jetInd] > btag_cut_DeepCSV){
                    bJets.push_back(jetInd);
                    jet_isTagged.push_back(true);
                } 
                else {
                    jet_isTagged.push_back(false);
                }
            }				
        }// if jetPresel
        if (tree->event_==printEvent){
            cout << " pt=" << pt << "  eta=" << eta << " phi=" << phi << "  jetID=" << jetID_pass << endl;
            cout << " presel=" << jetPresel << endl;
            cout << " pt=" << pt <<endl;
            cout << " eta=" << TMath::Abs(eta) <<endl;
            cout << " jetID=" << jetID_pass <<endl;
            cout << " dRLep=" << passDR_lep_jet <<endl;
            cout << " dRPho=" << passDR_pho_jet << endl;
            cout << " btag="<<(tree->jetBtagDeepB_[jetInd] > btag_cut_DeepCSV) << endl; 
        }
    }//jet for loop
}

//https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html
//for 2016: id = 0, 1, 3 (1=loose, 2=tight, 3=tightLepVeto)
//for 2017,18, id = 0, 2, 6
void Selector::filter_fatjets(){
    if (tree->event_==printEvent){
        cout << endl;
        cout << "Found Event Staring Fat Jets" << endl;
        cout << "  nJet=" << tree->nFatJet_ << endl;
    }
    for(int jetInd = 0; jetInd < tree->nFatJet_; ++jetInd){
        double pt = tree->fatJetPt_[jetInd];
        double eta = tree->fatJetEta_[jetInd];
        double phi = tree->fatJetPhi_[jetInd];
        Int_t id   = tree->fatJetID_[jetInd];
        Float_t mSD = tree->fatJetMassSoftDrop_[jetInd];
        Float_t TvsQCD = tree->fatJetDeepTagT_[jetInd];
        bool isId  = id >=1 || id >=2;
        double resolution = 0.;
        if (tree->event_==printEvent){
            cout << "------FatJet "<<jetInd<< "------" << endl;
        }
        if (!tree->isData_){
            jetParamAK8.setJetEta(tree->fatJetEta_[jetInd]);
            jetParamAK8.setJetPt(tree->fatJetPt_[jetInd]);
            jetParamAK8.setJetArea(tree->fatJetArea_[jetInd]);
            jetParamAK8.setRho(tree->rho_);
            double jetSF = 1.0;
            resolution = jetResolutionAK8->getResolution(jetParamAK8);
            if (JERsystLevel==1) jetSF = jetResolutionScaleFactorAK8->getScaleFactor(jetParamAK8,Variation::NOMINAL);
            if (JERsystLevel==0) jetSF = jetResolutionScaleFactorAK8->getScaleFactor(jetParamAK8,Variation::DOWN);
            if (JERsystLevel==2) jetSF = jetResolutionScaleFactorAK8->getScaleFactor(jetParamAK8,Variation::UP);
	    
            double jetSmear = 1;
            int genIdx = tree->fatJetGenJetAK8Idx_[jetInd];
            if ( (genIdx>-1) && (genIdx < tree->nGenJetAK8_)){
	        double genJetPt = tree->GenJetAK8_pt_[genIdx];
	        jetSmear = 1. + (jetSF - 1.) * (pt - genJetPt)/pt;
            }else{
	        jetSmear = 1 + generator->Gaus(0, resolution) * sqrt( max(jetSF*jetSF - 1, 0.) );
            }
            if (tree->event_==printEvent){
	        cout << "  DoJetSmear: " << smearJetPt << endl;
	        cout << "  GenIdx: "<< genIdx << endl;
	        cout << "  jetSF: "<< jetSF << endl;
	        cout << "  JetSmear: "<<jetSmear << endl;
            }
            if (smearJetPt){
	        pt = pt*jetSmear;
	        tree->fatJetPt_[jetInd] = pt;
            }
        }
        bool passDR_lep_jet = true;
        for(std::vector<int>::const_iterator eleInd = Electrons.begin(); eleInd != Electrons.end(); eleInd++) {
	    if (dR(eta, phi, tree->eleEta_[*eleInd], tree->elePhi_[*eleInd]) < 0.8) passDR_lep_jet = false;
        }
        for(std::vector<int>::const_iterator muInd = Muons.begin(); muInd != Muons.end(); muInd++) {
          if (dR(eta, phi, tree->muEta_[*muInd], tree->muPhi_[*muInd]) < 0.8) passDR_lep_jet = false;
        }
        bool passDR_pho_jet = true;
        for(std::vector<int>::const_iterator phoInd = Photons.begin(); phoInd != Photons.end(); phoInd++) {
	        if (dR(eta, phi, tree->phoEta_[*phoInd], tree->phoPhi_[*phoInd]) < 0.8) passDR_pho_jet = false;
	    }
        bool jetPresel = (pt >= 350.0 
                && TMath::Abs(eta) <= 2.4 
                && mSD >=105 && mSD <=210
                && TvsQCD >=toptag_cut_DeepAK8
                && passDR_lep_jet
                && passDR_pho_jet
                && isId);
        if (jetPresel) FatJets.push_back(jetInd);
        if (tree->event_==printEvent){
            cout << "   -----" <<endl;
            cout << "   presel=" << jetPresel << endl;
            cout << "     " << (pt >= 350.0)            << " pt=" << pt <<endl;
            cout << "     " << (TMath::Abs(eta) <= 2.4) << " eta=" << eta <<endl;
            cout << "     " << (isId)                   << " fatJetID="   << isId <<endl;
            cout << "     " << (mSD >=105 && mSD <=210) << " mass SD=" << mSD <<endl;
            cout << "     " << (TvsQCD >=0.834)         << " TvsQCD" << TvsQCD << endl;
            cout << "      dRLep=" << passDR_lep_jet <<endl;
            cout << "      dRPho=" << passDR_pho_jet << endl;
        }
    }
}
Selector::~Selector(){
}
