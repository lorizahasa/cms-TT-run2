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
    //	clear_vectors();
    passSkim = false;
    passPresel_ele = false;
    passPresel_mu = false;
    passAll_ele = false;
    passAll_mu = false;

    bool applyMetFilter   = false;
    bool Pass_trigger_mu  = false;
    bool Pass_trigger_ele = false;

    if (year=="2016") {
	    Pass_trigger_mu = (tree->HLT_IsoMu24_ || tree->HLT_IsoTkMu24_);
	    Pass_trigger_ele = (tree->HLT_Ele27_WPTight_Gsf_);
    }
    if (year=="2017"){
	    Pass_trigger_mu = (tree->HLT_IsoMu24_ || tree->HLT_IsoMu27_);
	    Pass_trigger_ele = (tree->HLT_Ele32_WPTight_Gsf_L1DoubleEG_ || tree->HLT_Ele32_WPTight_Gsf_);
    }
    if (year=="2018"){
	    Pass_trigger_mu = (tree->HLT_IsoMu24_ || tree->HLT_IsoMu27_);
	    Pass_trigger_ele = (tree->HLT_Ele32_WPTight_Gsf_ || tree->HLT_Ele35_WPTight_Gsf_);
    }

    bool filters = (tree->Flag_goodVertices_ &&
		    tree->Flag_globalSuperTightHalo2016Filter_ &&
		    tree->Flag_HBHENoiseFilter_ &&
		    tree->Flag_HBHENoiseIsoFilter_ && 
		    tree->Flag_EcalDeadCellTriggerPrimitiveFilter_ &&
		    tree->Flag_BadPFMuonFilter_ );

    if (year=="2017" || year=="2018"){ filters = filters && tree->Flag_ecalBadCalibFilterV2_ ;}

    if(applyMetFilter){
	    Pass_trigger_mu = Pass_trigger_mu && filters ;     
	    Pass_trigger_ele = Pass_trigger_ele && filters ;     
    }
    passSkim = (Pass_trigger_ele || Pass_trigger_mu) && filters;
}

