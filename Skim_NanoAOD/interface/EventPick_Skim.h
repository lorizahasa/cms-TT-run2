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
    std::map <std::string, int>cutflow;
	bool passSkim;
private:
	EventTree* tree;
};

#endif
