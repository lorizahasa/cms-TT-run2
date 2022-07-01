#include "../interface/EventPick_Skim.h"
#include <iostream> 
#include <iomanip>

EventPick::EventPick(std::string titleIn){
    title = titleIn;
    year = "2016";
}

EventPick::~EventPick(){
}

void EventPick::process_event(EventTree* tree){
    passSkim = false;
    bool passTrigMu  = false;
    bool passTrigEle = false;
    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgHLTRunIISummary
    //https://twiki.cern.ch/twiki/bin/view/CMS/MuonUL2016
    if (year.find("2016")!=std::string::npos){
        passTrigMu  = tree->HLT_Mu50_ || tree->HLT_TkMu50_;                 
        passTrigEle = tree->HLT_Photon175_ || tree->HLT_Ele27_WPTight_Gsf_;
    }                                                                           
    //https://twiki.cern.ch/twiki/bin/view/CMS/MuonUL2017
    //https://twiki.cern.ch/twiki/bin/view/CMS/MuonUL2018
    if (year.find("2017")!=std::string::npos){
        passTrigMu  = tree->HLT_Mu50_ || tree->HLT_TkMu100_ || tree->HLT_Mu100_;
        passTrigEle = tree->HLT_Photon200_ || tree->HLT_Ele35_WPTight_Gsf_;
    }
    if (year.find("2018")!=std::string::npos){
        passTrigMu  = tree->HLT_Mu50_ || tree->HLT_TkMu100_ || tree->HLT_Mu100_;
        passTrigEle = tree->HLT_Photon200_ || tree->HLT_Ele32_WPTight_Gsf_;
    }
    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
    bool filters = 
            (tree->Flag_goodVertices_ &&
		    tree->Flag_globalSuperTightHalo2016Filter_ &&
		    tree->Flag_HBHENoiseFilter_ &&
		    tree->Flag_HBHENoiseIsoFilter_ && 
		    tree->Flag_EcalDeadCellTriggerPrimitiveFilter_ &&
		    tree->Flag_BadPFMuonFilter_ &&
		    tree->Flag_eeBadScFilter_ );
    if (year=="2017" || year=="2018"){ 
        filters = filters && tree->Flag_ecalBadCalibFilter_ ;
    }
    //To reject events where neither muon nor electron is present
    bool zeroLep = (tree->nMu_ == 0) && (tree->nEle_ ==0);
    
    //Apply above selections along with additional cuts on PV, nJet, and MET
    cutflow["NanoAOD"] = 1;
    cutflow["LepTrig"] = 0;
    cutflow["Filters"] = 0;
    cutflow["g0Lep"]   = 0;
    cutflow["g0PV"]    = 0;
    cutflow["g0Jet"]   = 0;
    cutflow["g15MET"]  = 0;

    if(passTrigEle || passTrigMu){
        cutflow["LepTrig"] = 1;
        if(filters){
            cutflow["Filters"] = 1;
            if(tree->nGoodVtx_>0){ 
                cutflow["g0PV"] = 1;
                passSkim = true;
                if(!zeroLep){
                    cutflow["g0Lep"] = 1;
                    if(tree->nJet_>0){ 
                        cutflow["g0Jet"] = 1;
                        if(tree->MET_pt_ > 15){ 
                            cutflow["g15MET"] = 1;
    
                        }
                    }
                }
            }
        }
    }
    
}
