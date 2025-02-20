#ifndef EVENTTREE_H
#define EVENTTREE_H

#include<TFile.h>
#include<TTree.h>
#include<TChain.h>
#include<TMath.h>
#include <map>

#include<vector>

using namespace std;
const Int_t maxP = 600;

class EventTree{
 public:
    EventTree(bool xRootDAccess, string year, vector<string> fileNames, bool isMC);
    ~EventTree();
    Long64_t GetEntries();
    Int_t GetEntry(Long64_t entry);
    TChain* chain;
    
    UInt_t    run_;
    ULong64_t event_;
    UInt_t    lumis_;

    bool isData_;
    Bool_t  im24_, itm24_, im27_, m50_, tm50_, m100_, tm100_;
    Bool_t  e27_, e32_, e35_, e115_, e45j200_, e50j165_, p175_, p200_;

    Bool_t   Flag_goodVertices_ ;
    Bool_t   Flag_globalSuperTightHalo2016Filter_ ;
    Bool_t   Flag_HBHENoiseFilter_ ;
    Bool_t   Flag_HBHENoiseIsoFilter_ ;
    Bool_t   Flag_EcalDeadCellTriggerPrimitiveFilter_ ;
    Bool_t   Flag_BadPFMuonFilter_ ;
    Bool_t   Flag_ecalBadCalibFilter_ ;
    Bool_t   Flag_eeBadScFilter_;

   //For trigObj matching
    UInt_t          nEle;
    Int_t           eleID[1000];
    Float_t         elePhi[1000];
    Float_t         elePt[1000];
    Float_t         eleEta[1000];

    UInt_t          nTrigObj;
    Int_t           TrigObj_id[1000];   
    Float_t         TrigObj_pt[1000];   
    Float_t         TrigObj_eta[1000];   
    Float_t         TrigObj_phi[1000];  
    Int_t           TrigObj_filterBits[1000];   

    UInt_t          nMu;
    UInt_t          nJet;
    UInt_t          nPho;
    double deltaR(double eta1, double phi1, double eta2, double phi2){
        double dphi = phi2 - phi1;
        double deta = eta2 - eta1;
        static const double pi = TMath::Pi();
        dphi = TMath::Abs( TMath::Abs(dphi) - pi ) - pi;
        return TMath::Sqrt( dphi*dphi + deta*deta );
    }
    std::vector<std::vector<std::string>> splitVector(const std::vector<std::string>& strings, int n);
};

#endif
