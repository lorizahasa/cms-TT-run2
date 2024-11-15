#ifndef NTUPLETREE_H
#define NTUPLETREE_H

#include<iostream>
#include<TFile.h>
#include<TTree.h>
#include<TChain.h>
#include<TMath.h>
#include <map>

#include<vector>

using namespace std;
const Int_t maxP = 600;

class NtupleTree{
 public:
    NtupleTree(string dir, vector<string> fileNames);
    ~NtupleTree();
    Long64_t GetEntries();
    virtual Long64_t LoadTree(Long64_t entry);
    Int_t GetEntry(Long64_t entry);
    TChain* fChain;

    // Declaration of leaf types
    Int_t           Event_run;
    Int_t           fCurrent; //!current Tree number in a TChain
    Long64_t        Event_number;
    Int_t           Event_lumi;
    Bool_t          Event_is_data;
    Bool_t          Event_pass_presel_ele;
    Bool_t          Event_pass_presel_mu;
    Bool_t          Event_pass_hem_veto;
    Float_t         Weight_lumi;
    Float_t         Weight_pu;
    Float_t         Weight_ttag;
    Float_t         Weight_tpt;
    Float_t         Weight_prefire;
    Float_t         Weight_btag;
    Float_t         Weight_mu;
    Float_t         Weight_mu_id;
    Float_t         Weight_mu_iso;
    Float_t         Weight_mu_trig;
    Float_t         Weight_ele;
    Float_t         Weight_ele_id;
    Float_t         Weight_ele_reco;
    Float_t         Weight_ele_trig;
    vector<float>   *Weight_pho;
    vector<float>   *Weight_pho_id;
    vector<float>   *Weight_pho_ps;
    vector<float>   *Weight_pho_cs;
    vector<float>   *Weight_jer;
    vector<float>   *Weight_jes;
    Float_t         Weight_q2;
    Float_t         Weight_gen;
    Float_t         Weight_pdf;
    Float_t         Weight_isr;
    Float_t         Weight_fsr;
    Float_t         Weight_puUp;
    Float_t         Weight_puDown;
    Float_t         Weight_ttagUp;
    Float_t         Weight_ttagDown;
    Float_t         Weight_tptUp;
    Float_t         Weight_tptDown;
    Float_t         Weight_prefireUp;
    Float_t         Weight_prefireDown;
    Float_t         Weight_btag_bUp;
    Float_t         Weight_btag_bDown;
    Float_t         Weight_btag_lUp;
    Float_t         Weight_btag_lDown;
    Float_t         Weight_muUp;
    Float_t         Weight_muDown;
    Float_t         Weight_mu_idUp;
    Float_t         Weight_mu_idDown;
    Float_t         Weight_mu_isoUp;
    Float_t         Weight_mu_isoDown;
    Float_t         Weight_mu_trigUp;
    Float_t         Weight_mu_trigDown;
    Float_t         Weight_eleUp;
    Float_t         Weight_eleDown;
    Float_t         Weight_ele_idUp;
    Float_t         Weight_ele_idDown;
    Float_t         Weight_ele_recoUp;
    Float_t         Weight_ele_recoDown;
    Float_t         Weight_ele_trigUp;
    Float_t         Weight_ele_trigDown;
    vector<float>   *Weight_phoUp;
    vector<float>   *Weight_phoDown;
    vector<float>   *Weight_pho_idUp;
    vector<float>   *Weight_pho_idDown;
    vector<float>   *Weight_pho_psUp;
    vector<float>   *Weight_pho_psDown;
    vector<float>   *Weight_pho_csUp;
    vector<float>   *Weight_pho_csDown;
    Float_t         Weight_q2Up;
    Float_t         Weight_q2Down;
    Float_t         Weight_pdfUp;
    Float_t         Weight_q2_NN;
    Float_t         Weight_q2_UN;
    Float_t         Weight_q2_DN;
    Float_t         Weight_q2_NU;
    Float_t         Weight_q2_ND;
    Float_t         Weight_q2_DD;
    Float_t         Weight_q2_UU;
    Float_t         Weight_pdfDown;
    Float_t         Weight_isrUp;
    Float_t         Weight_isrDown;
    Float_t         Weight_fsrUp;
    Float_t         Weight_fsrDown;
    Int_t           Muon_size;
    vector<float>   *Muon_pt;
    vector<float>   *Muon_eta;
    vector<float>   *Muon_phi;
    vector<float>   *Muon_iso;
    Int_t           Electron_size;
    vector<float>   *Electron_pt;
    vector<float>   *Electron_phi;
    vector<float>   *Electron_eta;
    vector<float>   *Electron_eta_sc;
    vector<float>   *Electron_iso;
    Int_t           Photon_size;
    vector<float>   *Photon_et;
    vector<float>   *Photon_eta;
    vector<float>   *Photon_phi;
    vector<float>   *Photon_iso;
    vector<int>     *Photon_genuine;
    vector<int>     *Photon_misid_ele;
    vector<int>     *Photon_hadronic_photon;
    vector<int>     *Photon_hadronic_fake;
    Int_t           Photon_loose_size;
    Int_t           Jet_size;
    Int_t           Jet_b_size;
    Float_t         Jet_sizeF;
    vector<float>   *Jet_deep_b;
    Float_t  Jet_deep_b0;
    Float_t  Jet_deep_b1;
    vector<float>   *Jet_pt;
    vector<float>   *Jet_qgl;
    Float_t  Jet_qgl_0;
    Float_t  Jet_qgl_1;
    vector<float>   *Jet_eta;
    vector<float>   *Jet_phi;
    vector<float>   *Jet_mass;
    vector<float>   *Jet_res;
    Int_t           FatJet_size;
    vector<float>   *FatJet_pt;
    Float_t FatJet_pt_0;
    vector<float>   *FatJet_eta;
    vector<float>   *FatJet_phi;
    vector<float>   *FatJet_mass;
    vector<float>   *FatJet_msoftdrop;
    Float_t FatJet_msoftdrop_0;
    Float_t         Reco_met;
    Float_t         Reco_met_phi;
    Float_t         Reco_mass_trans_w;
    Double_t        Reco_ht;
    Double_t        Reco_st;
    Float_t         Reco_stF;
    Float_t         Reco_chi2;
    Float_t         Reco_mass_dipho;
    Float_t         Reco_mass_dilep;
    Float_t         Reco_dr_dilep;
    Float_t         Reco_dr_pho_tstarHad;
    Float_t         Reco_dr_pho_tHad;
    Float_t         Reco_dr_pho_bHad;
    Float_t         Reco_dr_pho_Wj1;
    Float_t         Reco_dr_pho_Wj2;
    Float_t         Reco_dr_pho_tstarLep;
    Float_t         Reco_dr_pho_tLep;
    Float_t         Reco_dr_pho_gluon;
    Float_t         Reco_dr_pho_bLep;
    Float_t         Reco_dr_pho_lep;
    Float_t         Reco_dr_pho_nu;
    Float_t         Reco_dr_gluon_tstarHad;
    Float_t         Reco_dr_gluon_tHad;
    Float_t         Reco_dr_gluon_tstarLep;
    Float_t         Reco_dr_gluon_tLep;
    Float_t         Reco_dr_tHad_tstarHad;
    Float_t         Reco_dr_tLep_tstarLep;
    Float_t         Reco_dr_tstarHad_tstarLep;
    Float_t         Reco_eta_hadT;
    Float_t         Reco_pt_hadT;
    Float_t         Reco_phi_hadT;
    Float_t         Reco_eta_lepT;
    Float_t         Reco_pt_lepT;
    Float_t         Reco_phi_lepT;
    Float_t         Reco_mass_jj;
    Float_t         Reco_mass_t_had;
    Float_t         Reco_mass_t_lep;
    Float_t         Reco_mass_hadT;
    Float_t         Reco_mass_lepT;
    Float_t         Reco_mass_T;
    Float_t         Reco_mass_TT;
    Float_t         Reco_mass_TT_diff;
    Float_t         Reco_angle_pho_lepton;
    Float_t         Reco_angle_lepton_met;
    Float_t         Reco_angle_pho_met;
    Float_t         Reco_angle_leadJet_met;
    Float_t         Reco_angle_leadBjet_met;
    vector<float>   *Reco_mass_lgamma;
    Float_t  Reco_mass_lgamma_0;
    vector<float>   *Reco_mass_photon_lepton;

    // List of branches
    TBranch        *b_Event_run;   //!
    TBranch        *b_Event_number;   //!
    TBranch        *b_Event_lumi;   //!
    TBranch        *b_Event_is_data;   //!
    TBranch        *b_Event_pass_presel_ele;   //!
    TBranch        *b_Event_pass_presel_mu;   //!
    TBranch        *b_Event_pass_hem_veto;   //!
    TBranch        *b_Weight_lumi;   //!
    TBranch        *b_Weight_pu;   //!
    TBranch        *b_Weight_ttag;   //!
    TBranch        *b_Weight_tpt;   //!
    TBranch        *b_Weight_prefire;   //!
    TBranch        *b_Weight_btag;   //!
    TBranch        *b_Weight_mu;   //!
    TBranch        *b_Weight_mu_id;   //!
    TBranch        *b_Weight_mu_iso;   //!
    TBranch        *b_Weight_mu_trig;   //!
    TBranch        *b_Weight_ele;   //!
    TBranch        *b_Weight_ele_id;   //!
    TBranch        *b_Weight_ele_reco;   //!
    TBranch        *b_Weight_ele_trig;   //!
    TBranch        *b_Weight_pho;   //!
    TBranch        *b_Weight_pho_id;   //!
    TBranch        *b_Weight_pho_ps;   //!
    TBranch        *b_Weight_pho_cs;   //!
    TBranch        *b_Weight_jer;   //!
    TBranch        *b_Weight_jes;   //!
    TBranch        *b_Weight_q2;   //!
    TBranch        *b_Weight_gen;   //!
    TBranch        *b_Weight_pdf;   //!
    TBranch        *b_Weight_isr;   //!
    TBranch        *b_Weight_fsr;   //!
    TBranch        *b_Weight_puUp;   //!
    TBranch        *b_Weight_puDown;   //!
    TBranch        *b_Weight_ttagUp;   //!
    TBranch        *b_Weight_ttagDown;   //!
    TBranch        *b_Weight_tptUp;   //!
    TBranch        *b_Weight_tptDown;   //!
    TBranch        *b_Weight_prefireUp;   //!
    TBranch        *b_Weight_prefireDown;   //!
    TBranch        *b_Weight_btag_bUp;   //!
    TBranch        *b_Weight_btag_bDown;   //!
    TBranch        *b_Weight_btag_lUp;   //!
    TBranch        *b_Weight_btag_lDown;   //!
    TBranch        *b_Weight_muUp;   //!
    TBranch        *b_Weight_muDown;   //!
    TBranch        *b_Weight_mu_idUp;   //!
    TBranch        *b_Weight_mu_idDown;   //!
    TBranch        *b_Weight_mu_isoUp;   //!
    TBranch        *b_Weight_mu_isoDown;   //!
    TBranch        *b_Weight_mu_trigUp;   //!
    TBranch        *b_Weight_mu_trigDown;   //!
    TBranch        *b_Weight_eleUp;   //!
    TBranch        *b_Weight_eleDown;   //!
    TBranch        *b_Weight_ele_idUp;   //!
    TBranch        *b_Weight_ele_idDown;   //!
    TBranch        *b_Weight_ele_recoUp;   //!
    TBranch        *b_Weight_ele_recoDown;   //!
    TBranch        *b_Weight_ele_trigUp;   //!
    TBranch        *b_Weight_ele_trigDown;   //!
    TBranch        *b_Weight_phoUp;   //!
    TBranch        *b_Weight_phoDown;   //!
    TBranch        *b_Weight_pho_idUp;   //!
    TBranch        *b_Weight_pho_idDown;   //!
    TBranch        *b_Weight_pho_psUp;   //!
    TBranch        *b_Weight_pho_psDown;   //!
    TBranch        *b_Weight_pho_csUp;   //!
    TBranch        *b_Weight_pho_csDown;   //!
    TBranch        *b_Weight_q2Up;   //!
    TBranch        *b_Weight_q2Down;   //!
    TBranch        *b_Weight_pdfUp;   //!
    TBranch        *b_Weight_q2_NN;   //!
    TBranch        *b_Weight_q2_UN;   //!
    TBranch        *b_Weight_q2_DN;   //!
    TBranch        *b_Weight_q2_NU;   //!
    TBranch        *b_Weight_q2_ND;   //!
    TBranch        *b_Weight_q2_DD;   //!
    TBranch        *b_Weight_q2_UU;   //!
    TBranch        *b_Weight_pdfDown;   //!
    TBranch        *b_Weight_isrUp;   //!
    TBranch        *b_Weight_isrDown;   //!
    TBranch        *b_Weight_fsrUp;   //!
    TBranch        *b_Weight_fsrDown;   //!
    TBranch        *b_Muon_size;   //!
    TBranch        *b_Muon_pt;   //!
    TBranch        *b_Muon_eta;   //!
    TBranch        *b_Muon_phi;   //!
    TBranch        *b_Muon_iso;   //!
    TBranch        *b_Electron_size;   //!
    TBranch        *b_Electron_pt;   //!
    TBranch        *b_Electron_phi;   //!
    TBranch        *b_Electron_eta;   //!
    TBranch        *b_Electron_eta_sc;   //!
    TBranch        *b_Electron_iso;   //!
    TBranch        *b_Photon_size;   //!
    TBranch        *b_Photon_et;   //!
    TBranch        *b_Photon_eta;   //!
    TBranch        *b_Photon_phi;   //!
    TBranch        *b_Photon_iso;   //!
    TBranch        *b_Photon_genuine;   //!
    TBranch        *b_Photon_misid_ele;   //!
    TBranch        *b_Photon_hadronic_photon;   //!
    TBranch        *b_Photon_hadronic_fake;   //!
    TBranch        *b_Photon_loose_size;   //!
    TBranch        *b_Jet_size;   //!
    TBranch        *b_Jet_b_size;   //!
    TBranch        *b_Jet_deep_b;   //!
    TBranch        *b_Jet_deep_b0;   //!
    TBranch        *b_Jet_deep_b1;   //!
    TBranch        *b_Jet_pt;   //!
    TBranch        *b_Jet_qgl;   //!
    TBranch        *b_Jet_qgl_0;   //!
    TBranch        *b_Jet_qgl_1;   //!
    TBranch        *b_Jet_eta;   //!
    TBranch        *b_Jet_phi;   //!
    TBranch        *b_Jet_mass;   //!
    TBranch        *b_Jet_res;   //!
    TBranch        *b_FatJet_size;   //!
    TBranch        *b_FatJet_pt;   //!
    TBranch        *b_FatJet_pt_0;   //!
    TBranch        *b_FatJet_eta;   //!
    TBranch        *b_FatJet_phi;   //!
    TBranch        *b_FatJet_mass;   //!
    TBranch        *b_FatJet_msoftdrop;   //!
    TBranch        *b_FatJet_msoftdrop_0;   //!
    TBranch        *b_Reco_met;   //!
    TBranch        *b_Reco_met_phi;   //!
    TBranch        *b_Reco_mass_trans_w;   //!
    TBranch        *b_Reco_ht;   //!
    TBranch        *b_Reco_st;   //!
    TBranch        *b_Reco_chi2;   //!
    TBranch        *b_Reco_mass_dipho;   //!
    TBranch        *b_Reco_mass_dilep;   //!
    TBranch        *b_Reco_dr_dilep;   //!
    TBranch        *b_Reco_dr_pho_tstarHad;   //!
    TBranch        *b_Reco_dr_pho_tHad;   //!
    TBranch        *b_Reco_dr_pho_bHad;   //!
    TBranch        *b_Reco_dr_pho_Wj1;   //!
    TBranch        *b_Reco_dr_pho_Wj2;   //!
    TBranch        *b_Reco_dr_pho_tstarLep;   //!
    TBranch        *b_Reco_dr_pho_tLep;   //!
    TBranch        *b_Reco_dr_pho_gluon;   //!
    TBranch        *b_Reco_dr_pho_bLep;   //!
    TBranch        *b_Reco_dr_pho_lep;   //!
    TBranch        *b_Reco_dr_pho_nu;   //!
    TBranch        *b_Reco_dr_gluon_tstarHad;   //!
    TBranch        *b_Reco_dr_gluon_tHad;   //!
    TBranch        *b_Reco_dr_gluon_tstarLep;   //!
    TBranch        *b_Reco_dr_gluon_tLep;   //!
    TBranch        *b_Reco_dr_tHad_tstarHad;   //!
    TBranch        *b_Reco_dr_tLep_tstarLep;   //!
    TBranch        *b_Reco_dr_tstarHad_tstarLep;   //!
    TBranch        *b_Reco_eta_hadT;   //!
    TBranch        *b_Reco_pt_hadT;   //!
    TBranch        *b_Reco_phi_hadT;   //!
    TBranch        *b_Reco_eta_lepT;   //!
    TBranch        *b_Reco_pt_lepT;   //!
    TBranch        *b_Reco_phi_lepT;   //!
    TBranch        *b_Reco_mass_jj;   //!
    TBranch        *b_Reco_mass_t_had;   //!
    TBranch        *b_Reco_mass_t_lep;   //!
    TBranch        *b_Reco_mass_hadT;   //!
    TBranch        *b_Reco_mass_lepT;   //!
    TBranch        *b_Reco_mass_T;   //!
    TBranch        *b_Reco_mass_TT;   //!
    TBranch        *b_Reco_mass_TT_diff;   //!
    TBranch        *b_Reco_angle_pho_lepton;   //!
    TBranch        *b_Reco_angle_lepton_met;   //!
    TBranch        *b_Reco_angle_pho_met;   //!
    TBranch        *b_Reco_angle_leadJet_met;   //!
    TBranch        *b_Reco_angle_leadBjet_met;   //!
    TBranch        *b_Reco_mass_lgamma;   //!
    TBranch        *b_Reco_mass_lgamma_0;   //!
    TBranch        *b_Reco_mass_photon_lepton;   //!

    std::vector<std::vector<std::string>> splitVector(const std::vector<std::string>& strings, int n);
    std::vector<std::string> splitString(const std::string& s, const std::string& delimiter);

};

#endif
