#include"../interface/EventPick.h"
#include <TLorentzVector.h>
#include <iostream>
#include <iomanip>

EventPick::EventPick(std::string titleIn){
    title = titleIn;
    year = "2016";
    printEvent = -1;

    // Cut levels
    MET_cut = 20.0;
    Nlep_eq = 1;
    Njet_ge = 3;
    NBjet_ge = 1;
    Nmu_eq = 1;
    Nele_eq = 1;
    Npho_eq = 1;
    
    NlooseMuVeto_le = 0;
    NlooseEleVeto_le = 0;


}

EventPick::~EventPick(){
}

void EventPick::process_event(EventTree* tree, Selector* selector){
    passPreselMu  = true;
    passPreselEle = true;
	selector->process_objects(tree);
    if (tree->event_==printEvent){
	cout << "Muons     "<< selector->Muons.size() << endl;
	cout << "  Loose   "<< selector->MuonsLoose.size() << endl;
	cout << "Electrons "<< selector->Electrons.size() << endl;
	cout << "  Loose   "<< selector->ElectronsLoose.size() << endl;
	cout << "Jets      "<< selector->Jets.size() << endl;
	cout << "BJets     "<< selector->bJets.size() << endl;
	cout << "Photons   "<< selector->Photons.size() << endl;
	cout << "  Loose   "<< selector->LoosePhotons.size() << endl;
	cout << "-------------------"<< endl;
    }

    //check if an event has a tight muon
	if( passPreselMu && selector->Muons.size() == Nmu_eq){
	    if (Nmu_eq==2) {
		    int idx_mu1 = selector->Muons.at(0);
		    int idx_mu2 = selector->Muons.at(1);
		    if(tree->muCharge_[idx_mu1]*tree->muCharge_[idx_mu2] ==1){
		        passPreselMu = false;
		    }
		    TLorentzVector mu1;
		    TLorentzVector mu2;
		    mu1.SetPtEtaPhiM(tree->muPt_[idx_mu1],
				 tree->muEta_[idx_mu1],
				 tree->muPhi_[idx_mu1],
				 tree->muMass_[idx_mu1]);
		    mu2.SetPtEtaPhiM(tree->muPt_[idx_mu2],
				 tree->muEta_[idx_mu2],
				 tree->muPhi_[idx_mu2],
				 tree->muMass_[idx_mu2]);
		    if (tree->event_==printEvent){
		        cout << "DilepMass:    " << (mu1 + mu2).M() << endl;
		        cout << "Lep 1 Charge: " << tree->muCharge_[idx_mu1] << endl;
		        cout << "Lep 2 Charge: " << tree->muCharge_[idx_mu2] << endl;
		        cout << "-------------------"<< endl;
		    }
		    if ( abs((mu1 + mu2).M() - 91.1876) > 10 ){
		        passPreselMu = false;
		    }
	    }
	}
	else { 
        passPreselMu = false;
    }
    //Next make sure that the event does not have 2nd loose muon or tight electron	
    if( passPreselMu && selector->MuonsLoose.size() >  NlooseMuVeto_le ){
        passPreselMu = false;
    }
	if( passPreselMu && (selector->ElectronsLoose.size() + selector->Electrons.size()) > NlooseEleVeto_le){ 
	    passPreselMu = false;
    }

    //Similarly check if an event has a tight electron
    if( passPreselEle && selector->Electrons.size() == Nele_eq) {
	    if (Nele_eq==2) {
		    int idx_ele1 = selector->Electrons.at(0);
		    int idx_ele2 = selector->Electrons.at(1);
		    if((tree->eleCharge_[idx_ele1])*(tree->eleCharge_[idx_ele2]) == 1){
		        passPreselEle = false;
		    }
		    TLorentzVector ele1;
		    TLorentzVector ele2;
		    ele1.SetPtEtaPhiM(tree->elePt_[idx_ele1],
				  tree->eleEta_[idx_ele1],
				  tree->elePhi_[idx_ele1],
				  tree->eleMass_[idx_ele1]);
		    ele2.SetPtEtaPhiM(tree->elePt_[idx_ele2],
				  tree->eleEta_[idx_ele2],
				  tree->elePhi_[idx_ele2],
				  tree->eleMass_[idx_ele2]);
		    if (tree->event_==printEvent){
		        cout << "DilepMass:    " << (ele1 + ele2).M() << endl;
		        cout << "Lep 1 Charge: " << tree->eleCharge_[idx_ele1] << endl;
		        cout << "Lep 2 Charge: " << tree->eleCharge_[idx_ele2] << endl;
		        cout << "-------------------"<< endl;
		    }
		    if ( abs((ele1 + ele2).M() - 91.1876) > 10 ){
		        passPreselEle = false;
		    }
	    }
    }
    else { 
        passPreselEle = false;
    }
    //Next make sure that the event does not have 2nd loose electron or tight muon	
	if( passPreselEle && selector->ElectronsLoose.size() >  NlooseEleVeto_le ){ 
	    passPreselEle = false;
    }
	if( passPreselEle && (selector->MuonsLoose.size() + selector->Muons.size()) >  NlooseMuVeto_le ) { 
	    passPreselEle = false;
    }
    
    // MET cut for muons
    if(passPreselMu && tree->MET_pt_ < MET_cut) { 
        passPreselMu = false;
    }
    // MET cut for electrons
    if(passPreselEle && tree->MET_pt_ < MET_cut) { 
        passPreselEle = false;
    }
}

