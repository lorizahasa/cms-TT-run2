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
	std::string title;
	std::string year;

	int printEvent;

	// cuts as parameters, to modify easily
	double MET_cut;
	int Nlep_eq;
	int Njet_ge;
	int NBjet_ge;
	int Nmu_eq;
	int Nele_eq;
	int Npho_eq;

	int NlooseMuVeto_le;
	int NlooseEleVeto_le;
	
	// variables showing passing or failing selections
    bool passPreselMu;
    bool passPreselEle;

private:
	EventTree* tree;
	Selector* selector;
};
#endif
