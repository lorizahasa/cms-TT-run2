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
    topTagWP = 0.74;

    // whether to invert lepton requirements for 
    QCDselect = false;

    skipAK4AK8dr = false;

    smearJetPt = true;
    smearPho = true;
    smearEle = true;
    scaleEle = true;
    scalePho = true;
    isSignal = false;
    isQCD = false;

}

void Selector::init_JER(std::string inputPrefix){
    jetResolutionAK4 = new JME::JetResolution((inputPrefix+"_MC_PtResolution_AK4PFchs.txt").c_str());
    jetResolutionScaleFactorAK4 = new JME::JetResolutionScaleFactor((inputPrefix+"_MC_SF_AK4PFchs.txt").c_str());
    jetResolutionAK8 = new JME::JetResolution((inputPrefix+"_MC_PtResolution_AK8PFchs.txt").c_str());
    jetResolutionScaleFactorAK8 = new JME::JetResolutionScaleFactor((inputPrefix+"_MC_SF_AK8PFchs.txt").c_str());
}

//https://cms-nanoaod-integration.web.cern.ch/integration/cms-swCMSSW_10_6_19/mc102X_doc.html#Muon
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

    Jets.clear();
    bJets.clear();
    FatJets.clear();
    jet_resolution.clear();
    jet_smear.clear();
    jet_isTagged.clear();

}
//https://twiki.cern.ch/twiki/bin/view/CMS/MuonUL2016#High_pT_above_120_GeV
//https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2#HighPt_Muon
//https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonSelection#HighPt_Tracker_Muon
//https://github.com/cms-sw/cmssw/blob/master/DataFormats/MuonReco/src/MuonSelectors.cc#L933-L960
void Selector::filter_muons(){
    if (tree->event_==printEvent){
	    cout << "Found Event, Starting Muons" << endl;
	    cout << " nMu=" << tree->nMuon_ << endl;
    }
    for(UInt_t m = 0; m < tree->nMuon_; ++m){
        double eta = tree->muEta_[m];
        double pt = tree->muPt_[m];
        int tkIsoID = (int)tree->muTkIsoId_[m];//1 for loose, 2 for tight
        bool looseMuonID = tree->muIsPFMuon_[m] && 
            (tree->muIsTracker_[m] || tree->muIsGlobal_[m]);
        bool passPromptID = tree->muHighPurity_[m] && (int)tree->muHighPtId_[m]==2;
        if(isSignal) passPromptID = (int)tree->muHighPtId_[m]==2;//FIXME for UL signals
        //highPtID has IP cuts too:
        bool passPrompt = (pt >= 55.0 &&
        		  TMath::Abs(eta) <= 2.4 &&
        		  passPromptID && 
                  tkIsoID == 2 
        		  );
        bool passLoose = (pt >= 30.0 &&
                  TMath::Abs(eta) <= 2.4 &&
                  looseMuonID && 
                  !passPrompt &&
                  tkIsoID == 1
        		  );
        if(passPrompt) Muons.push_back(m);
        else if (passLoose) MuonsLoose.push_back(m);
        if (tree->event_==printEvent){
            cout << "-- " << m << " passPrompt="<<passPrompt<< " passLoose="<<passLoose << " pt="<<pt<< " eta="<<eta<< " phi="<<tree->muPhi_[m]<< " tightID="<<passPromptID<< " looseID="<<looseMuonID << " tkRelIsoID="<<tkIsoID << endl;
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
        // make sure it doesn't fall within the gap
        bool passEtaEBEEGap = (absSCEta < 1.4442) || (absSCEta > 1.566);

        bool passTightID = tree->eleMVAFall17V2Iso_WP80_[eleInd];
        bool passVetoID  = tree->eleMVAFall17V2Iso_WPL_[eleInd]; 

        bool eleSel = (passEtaEBEEGap && 
                       absEta <= 2.2 &&
                       pt >= 50.0 &&
                       passTightID);
        bool looseSel = (passEtaEBEEGap && 
                         absEta <= 2.2 &&
                         pt >= 35.0 &&
                         passVetoID &&
                         !eleSel);
        if(eleSel) Electrons.push_back(eleInd);
        else if(looseSel) ElectronsLoose.push_back(eleInd);
        if (tree->event_==printEvent){
            cout << "-- " << eleInd << " eleSel=" <<  eleSel << " looseSel=" <<  looseSel << " pt="<<pt<< " eta="<<eta<< " phi="<<tree->elePhi_[eleInd]<< " eleID="<<passTightID <<"looseID = "<<passVetoID << endl; 
        } 
    }
}
//https://twiki.cern.ch/twiki/bin/view/CMS/MultivariatePhotonIdentificationRun2
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
        bool passDR_lep_pho = true;
        //loop over selected electrons
        for(std::vector<int>::const_iterator eleInd = Electrons.begin(); eleInd != Electrons.end(); eleInd++) {
	    if (dR(eta, phi, tree->eleEta_[*eleInd], tree->elePhi_[*eleInd]) < 0.4) passDR_lep_pho = false;
        }
        //loop over selected muons
        for(std::vector<int>::const_iterator muInd = Muons.begin(); muInd != Muons.end(); muInd++) {
	    if (dR(eta, phi, tree->muEta_[*muInd], tree->muPhi_[*muInd]) < 0.4) passDR_lep_pho = false;
        }
        bool passPhoId      = tree->phoMVAId_WP80_[phoInd];//tight 
        bool hasPixelSeed   = tree->phoPixelSeed_[phoInd];
        bool phoEleVeto     = tree->phoEleVeto_[phoInd];
        bool phoPresel = (et >= 20.0 &&                          
                          absEta <= 1.4442 &&
                          !hasPixelSeed &&
                          phoEleVeto &&
                          passDR_lep_pho
			  );
        vector<bool> cutBasedID_split = parsePhotonVIDCuts(tree->phoVidWPBitmap_[phoInd], 2);
        bool passMediumIDNoChIsoOrSIEIE = cutBasedID_split[1] && cutBasedID_split[4] && cutBasedID_split[5]; // HoverE (1), NeuIso (4), and PhoIso (5) cuts, skip ChIso (3) and SIEIE (2)
        if(phoPresel && passPhoId) Photons.push_back(phoInd);
        if(phoPresel && passMediumIDNoChIsoOrSIEIE) LoosePhotons.push_back(phoInd);
        if (tree->event_==printEvent){
            cout << "-- " << phoInd << " pt="<<et<< " eta="<<eta<< " phi="<<phi<<"presel="<< phoPresel<< " drlepgamma="<<passDR_lep_pho<< " medID="<<passPhoId<<endl;
        } 
    }
}

void Selector::filter_jets(){
    if (tree->event_==printEvent){
    	cout << "Found Event Staring Jets" << endl;
        cout << " nJet=" << tree->nJet_ << endl;
    }
    if(tree->nJet_<200){//Some of the QCD events have very high nJet
    for(int jetInd = 0; jetInd < tree->nJet_; ++jetInd){
        double pt = tree->jetPt_[jetInd];
        double eta = tree->jetEta_[jetInd];
        double phi = tree->jetPhi_[jetInd];
        //https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVUL
        //https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJetIDUL
        //puID to be applied later on
        //bool jetID_pass = (tree->jetID_[jetInd]>=2 and (tree->jetPUID_[jetInd]>=1 or pt>=50.0)) ;
        bool jetID_pass = tree->jetID_[jetInd]>=2; 
        double resolution = 0.;
        double jetSmear = 1.;
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
            int genIdx = tree->jetGenJetIdx_[jetInd];
            if ( (genIdx>-1) && (genIdx < tree->nGenJet_)){
	        double genJetPt = tree->GenJet_pt_[genIdx];
	        jetSmear = 1. + (jetSF - 1.) * (pt - genJetPt)/pt;
            }else{
	        jetSmear = 1 + generator->Gaus(0, resolution) * sqrt( max(jetSF*jetSF - 1, 0.) );
            }
            if (tree->event_==printEvent){
            cout<<"------------------------"<<endl;
            cout << "  JetInd: "<<jetInd << endl;
	        cout << "  DoJetSmear: " << smearJetPt << endl;
	        cout << "  GenIdx: "<< genIdx << endl;
	        cout << "  jetEta: "<< tree->jetEta_[jetInd] << endl;
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
            if (dR(eta, phi, tree->phoEta_[*phoInd], tree->phoPhi_[*phoInd]) < 0.4) passDR_pho_jet = false;
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
            jet_smear.push_back(jetSmear);
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
}

//https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html
//https://indico.cern.ch/event/1152827/contributions/4840404/attachments/2428856/4162159/ParticleNet_SFs_ULNanoV9_JMAR_25April2022_PK.pdf
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
        //Float_t TvsQCD = tree->fatJetDeepTagT_[jetInd];
        Float_t TvsQCD = tree->fatJetPNET_[jetInd];
        if(isSignal) TvsQCD = tree->fatJetDeepTagT_[jetInd]; //FIXME for UL signals
        bool isId  = (id >= 1); 
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
            if(isSignal) jetSmear = 1.0;//FIXME for UL signals
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
        //https://twiki.cern.ch/twiki/bin/viewauth/CMS/DeepAK8Tagging2018WPsSFs
        //https://twiki.cern.ch/twiki/bin/view/CMS/JetTopTagging
        bool jetPresel = (pt >= 350.0 
                && TMath::Abs(eta) <= 2.4 
                && mSD >=105 && mSD <=210
                //&& TvsQCD >= 0.834
                && TvsQCD >= topTagWP
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
