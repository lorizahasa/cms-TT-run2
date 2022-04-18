#ifndef EVENTPICK_H
#define EVENTPICK_H

#include<vector>
#include<string>
#include<set>
#include<iostream>
#include<fstream>
#include<TH1F.h>
#include<TH1D.h>

#include"EventTree.h"
#include"Selector.h"
//#include"Selector_gen.h"

class EventPick{
public:
	EventPick(std::string titleIn);
	~EventPick();
	
	void process_event(EventTree* inp_tree, Selector* inp_selector, double weight=1.0);
        //void process_event_gen(EventTree* inp_tree, Selector_gen* inp_selector, double weight=1.0);
	std::string title;
	
	std::string year;

	int printEvent;

	// cuts as parameters, to modify easily
	double MET_cut;

	bool loosePhotonVeto;

	int Nlep_eq;
	
	int Njet_ge;
	int NBjet_ge;
	int SkimNjet_ge;
	int SkimNBjet_ge;

	bool ZeroBExclusive;

	bool QCDselect;

	int Jet_Pt_cut_1;
	int Jet_Pt_cut_2;
	int Jet_Pt_cut_3;	
	int Nele_eq;
	int Nmu_eq;
	int NEleVeto_le;
	
	int Npho_eq;
	int NlooseMuVeto_le;
	int NlooseEleVeto_le;
	int NmediumEleVeto_le;
	
	bool skimEle;
	bool skimMu;

	// variables showing passing or failing selections
	bool passSkim;
    bool passPreselMu;
    bool passPreselEle;
    bool passAllMu;
    bool passAllEle;
	bool passFirstcut; // pass the sync cut	

private:
	EventTree* tree;
	Selector* selector;
};
#endif
