#ifndef EVENTTREE_H
#define EVENTTREE_H

#include<TFile.h>
#include<TTree.h>
#include<TChain.h>
#include <map>

#include<vector>

using namespace std;
const Int_t maxP = 600;

class EventTree{
 public:
    EventTree(int nFiles, bool xRootDAccess, string year, char** fileNames, bool isMC);
    ~EventTree();
    Long64_t GetEntries();
    Int_t GetEntry(Long64_t entry);
    TChain* chain;
    
    UInt_t    run_;
    ULong64_t event_;
    UInt_t    lumis_;

    bool isData_;
    Int_t    nPU_;  
    Float_t  nPUTrue_;  
    Float_t genWeight_;
    
    UInt_t   nJet_;  
    UInt_t   nMu_;  
    UInt_t   nEle_;  
    Int_t   nGoodVtx_;  
    Int_t   jetID_[200];
    Float_t MET_pt_;
    
    Bool_t  im24_, itm24_, im27_, m50_, tm50_, m100_, tm100_;
    Bool_t  e27_, e32_, e35_, e45j200_, e50j165_, p175_, p200_;

    Bool_t   Flag_goodVertices_ ;
    Bool_t   Flag_globalSuperTightHalo2016Filter_ ;
    Bool_t   Flag_HBHENoiseFilter_ ;
    Bool_t   Flag_HBHENoiseIsoFilter_ ;
    Bool_t   Flag_EcalDeadCellTriggerPrimitiveFilter_ ;
    Bool_t   Flag_BadPFMuonFilter_ ;
    Bool_t   Flag_ecalBadCalibFilter_ ;
    Bool_t   Flag_eeBadScFilter_;
};

#endif
