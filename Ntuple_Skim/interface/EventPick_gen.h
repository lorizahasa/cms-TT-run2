#ifndef EVENTPICK_GEN_H
#define EVENTPICK_GEN_H

#include<vector>
#include<string>
#include<set>
#include<iostream>
#include<fstream>
#include<TH1F.h>
#include<TH1D.h>

#include"EventTree_gen.h"
#include"Selector.h"
//#include"Selector_gen.h"

class EventPick_gen{
public:
        EventPick_gen(std::string titleIn);
        ~EventPick_gen();

        void process_event(EventTree* inp_tree, Selector_gen* inp_selector, double weight=1.0);
        void print_cutflow_mu(TH1D* _cutflow);
        void print_cutflow_ele(TH1D* _cutflow);

        std::string title;

        bool saveCutflows;
        double MET_cut;
        bool no_trigger;

        int Nlep_eq;

        int Njet_ge;
        int NBjet_ge;
        int SkimNjet_ge;
        int SkimNBjet_ge;

        bool ZeroBExclusive;

        int Jet_Pt_cut_1;
        int Jet_Pt_cut_2;
        int Jet_Pt_cut_3;
        int Nele_eq;
        int Nmu_eq;
        int NEleVeto_le;

        int Npho_ge;
        int NlooseMuVeto_le;
        int NlooseEleVeto_le;
        int NmediumEleVeto_le;

        bool skimEle;
        bool skimMu;

	    bool passSkim;
        bool passPresel_ele; 
        bool passAll_ele; 
        bool passPresel_mu; 
        bool passAll_mu; 
        bool passFirstcut;
        TH1D* cutFlow_mu;
        TH1D* cutFlowWeight_mu;
        TH1D* cutFlow_ele;
        TH1D* cutFlowWeight_ele;


private:
        EventTree* tree;
        Selector* selector;

	void set_cutflow_labels_mu(TH1D* hist);
        void set_cutflow_labels_ele(TH1D* hist);
};


#endif
