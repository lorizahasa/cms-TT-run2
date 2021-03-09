#ifndef EVENTPICK_H
#define EVENTPICK_H

#include<vector>
#include<string>
#include<set>
#include<iostream>
#include<TH1F.h>
#include<TH1D.h>

#include"EventTree_Skim.h"

class EventPick{
public:
	EventPick(std::string titleIn);
	~EventPick();
	void process_event(EventTree* inp_tree);
	std::string title;
	std::string year;
	// variables showing passing or failing selections
	bool passSkim;
	bool passPresel_ele; // passed preselection
	bool passAll_ele; // single flag: event passed all cuts: preselection + photon
	bool passPresel_mu; // passed preselection
	bool passAll_mu; // single flag: event passed all cuts: preselection + photon

private:
	EventTree* tree;
};

#endif
