#ifndef EVENTTREE_H
#define EVENTTREE_H

#include<TFile.h>
#include<TTree.h>
#include<TChain.h>

#include<vector>

using namespace std;
const Int_t maxP = 600;

class EventTree{
 public:
    EventTree(int nFiles, bool xRootDAccess, string year, bool isData, char** fileNames);
    ~EventTree();
    Long64_t GetEntries();
    Int_t GetEntry(Long64_t entry);
    
    TChain* chain;
    
    // include all variables just in case
    UInt_t    run_;
    ULong64_t event_;
    UInt_t    lumis_;
    
    Float_t  genWeight_;

    UInt_t nLHEScaleWeight_;
    Float_t LHEScaleWeight_[400];
    
    UInt_t nLHEPdfWeight_;
    Float_t LHEPdfWeight_[400];
    
    UInt_t nPSWeight_;
    Float_t PSWeight_[400];

    Float_t LHEWeight_originalXWGTUP_;

    Float_t prefireDn_;
    Float_t prefireNom_;
    Float_t prefireUp_;
    
    bool isData_;
    // genParticle
    UInt_t    nLHEPart_;
    Float_t   LHEPart_pt_[400];
    Int_t     LHEPart_pdgId_[400];

    UInt_t    nGenPart_;
    Float_t   GenPart_pt_[400];
    Float_t   GenPart_eta_[400];
    Float_t   GenPart_phi_[400];
    Float_t   GenPart_mass_[400];
    Int_t     GenPart_genPartIdxMother_[400];
    Int_t     GenPart_pdgId_[400];
    Int_t     GenPart_status_[400];
    Int_t     GenPart_statusFlags_[400];
    
    UInt_t    nGenJet_;
    Float_t   GenJet_pt_[400];
    Float_t   GenJet_eta_[400];
    Float_t   GenJet_phi_[400];
    Float_t   GenJet_mass_[400];
    
    UInt_t    nGenJetAK8_;
    Float_t   GenJetAK8_pt_[400];
    Float_t   GenJetAK8_eta_[400];
    Float_t   GenJetAK8_phi_[400];
    Float_t   GenJetAK8_mass_[400];
    
    // PU
    Int_t    nPU_;  
    Float_t  nPUTrue_;  
    Float_t  MET_pt_;
    Float_t  MET_phi_;
    Int_t    nGoodVtx_;
    Int_t   passTrigMu_;
    Int_t   passTrigEle_;

    // Electron
    UInt_t          nEle_;
    Float_t         elePhi_[100];
    Float_t         elePt_[100];
    Float_t         eleEta_[100];
    Float_t         eleDeltaEtaSC_[100];
    Int_t           eleCharge_[100];
    Float_t         eleMass_[100];
    Int_t           eleID_[100];
    Float_t         eleMiniPFRelIso_[100];
    Bool_t          eleMVAFall17V2Iso_WP80_[100];
    Bool_t          eleMVAFall17V2Iso_WPL_[100];

    // Photon
    UInt_t          nPho_;
    Float_t         phoEt_[100];
    Float_t         phoEta_[100];
    Float_t         phoPhi_[100];
    Bool_t          phoIsEB_[100];
    Bool_t          phoIsEE_[100];
    Float_t         phoPFRelIso_[100];
    Float_t         phoPFRelChIso_[100];
    Int_t           phoIDcutbased_[100];
    Int_t           phoVidWPBitmap_[100];
    Bool_t           phoPixelSeed_[100];
    Bool_t           phoEleVeto_[100];
    Bool_t           phoMVAId_WP80_[100];

    Float_t         phoR9_[100];
    Float_t         phoSIEIE_[100];
    Float_t         phoHoverE_[100];
    
    Int_t           phoGenPartIdx_[100];
    

    // I don't know why, but these two lines are needed to avoid possible memory issue with nMuon (segfault when it thinks there are 2**32-1 muons in an event
    // These vectors are not used
    vector<float>*  PFClustdEta_;
    vector<float>*  PFClustdPhi_;


    // Muon
    UInt_t          nMuon_;
    Float_t         muPhi_[100];
    Float_t         muPt_[100];
    Float_t         muEta_[100];
    Int_t           muCharge_[100];
    Float_t         muMass_[100];
    Float_t         muPFRelIso_[100];
    Float_t         muTkRelIso_[100];
    Bool_t          muMediumId_[100];
    Bool_t          muTightId_[100];
    UChar_t         muHighPtId_[100];
    Bool_t          muHighPurity_[100];
    UChar_t         muTkIsoId_[100];
    Bool_t          muIsPFMuon_[100];
    Bool_t          muIsGlobal_[100];
    Bool_t          muIsTracker_[100];
    Float_t         muDxy_[100];
    Float_t         muDz_[100];

    // Jet
    UInt_t          nJet_;
    Float_t         jetPt_[200];
    Float_t         jetQGL_[200];
    Float_t         jetQGL0_;
    Float_t         jetQGL1_;
    Float_t         jetEta_[200];
    Float_t         jetPhi_[200];
    Float_t         jetMass_[200];
    Float_t         jetRawFactor_[200];
    Int_t           jetID_[200];
    Int_t           puID_[200];
    Float_t         jetArea_[200];
    Float_t         fatJetArea_[200];
    Float_t         jetBtagDeepB_[200];
    Float_t         jetBtagDeepB0_;
    Float_t         jetBtagDeepB1_;
    Float_t         jetchEmEF_[200];
    Float_t         jetneEmEF_[200];
    Float_t         jetmuEF_[200];
    Int_t           jetHadFlvr_[200];
    Int_t           jetGenJetIdx_[200];
    
    //fat jets
    UInt_t          nFatJet_;
    Float_t         fatJetPt_[200];
    Float_t         fatJetPt0_;
    Float_t         fatJetEta_[200];
    Float_t         fatJetEta0_;
    Float_t         fatJetPhi_[200];
    Float_t         fatJetMass_[200];
    Float_t         fatJetMassSoftDrop_[200];
    Float_t         fatJetMassSoftDrop0_;
    Int_t           fatJetID_[200];
    Float_t         fatJetDeepTagT_[200];
    Float_t         fatJetDeepTagW_[200];
    Float_t         fatJetDeepTagMDT_[200];
    Float_t         fatJetDeepTagMDW_[200];
    Float_t         fatJetPNET_[200];
    Int_t           fatJetHadFlvr_[200];
    Float_t         fatJetEleIdx_[200];
    Float_t         fatJetMuIdx_[200];
    Int_t           fatJetGenJetAK8Idx_[200];
    Float_t  rho_;
    
    Bool_t  im24_, itm24_, im27_, m50_, tm50_, m100_, tm100_;

};
#endif
