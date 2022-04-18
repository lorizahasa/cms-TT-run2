#include"../interface/EventPick.h"
#include <TLorentzVector.h>
#include <iostream>
#include <iomanip>

EventPick::EventPick(std::string titleIn){
    title = titleIn;
    year = "2016";
    printEvent = -1;
    loosePhotonVeto=true;

    // Cut levels
    Nmu_eq = 1;
    Nele_eq = 1;
    NlooseMuVeto_le = 0;
    NlooseEleVeto_le = 0;

    MET_cut = 20.0;
    skimEle = false;
    skimMu = false;

    Njet_ge = 3;
    SkimNjet_ge = 2;

    NBjet_ge = 1;
    SkimNBjet_ge = 1;
    Nlep_eq = 1;

    ZeroBExclusive = false;

    QCDselect = false;

    Npho_eq = 1;

}

EventPick::~EventPick(){
}

void EventPick::process_event(EventTree* tree, Selector* selector, double weight){
    passSkim = false;
    passAllEle = false;
    passAllMu = false;
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
}

