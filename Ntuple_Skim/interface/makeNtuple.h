//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Mon May  8 04:09:17 2017 by ROOT version 6.06/01
// from TTree EventTree/Event data (tag V08_00_24_00)
// found on file: skim_TTbar_100k.root
//////////////////////////////////////////////////////////

#ifndef makeNtuple_h
#define makeNtuple_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TH2.h>
#include <TLorentzVector.h>
#include <iostream>
#include <algorithm>
#include <ctime>

#include "TRandom3.h"
#include "EventTree.h"
#include "EventPick.h"
#include "Selector.h"

#include "JECvariation.h"

#include <iomanip>
#include <cmath>

//#include <boost/program_options.hpp>

// Header file for the classes stored in the TTree if any.
#include "vector"

#include "METzCalculator.h"
#include "TopEventCombinatorics.h"

#include "ReaderLumiSF.h"
#include "ReaderMuSF.h"
#include "ReaderEleSF.h"
#include "ReaderPhoSF.h"
#include "ReaderLumiMask.h"

#include "OverlapRemove.h"

#include "correction.h"
class makeNtuple {
 public :

    makeNtuple(char* outputFileName,char** inputFileName);
    makeNtuple(int ac, char** av);

 private :

    EventTree* tree;   
    EventPick* evtPick;   
    Selector* selector;   
	
    bool isMC;

    TTree* outputTree;

    string sampleType;
    string systematicType;

    int eventNum = -1;

    bool isSystematicRun;

    bool useGenWeightScaling;

    bool getGenScaleWeights;
    bool applypdfweight;
    bool applyqsquare;

    correction::Correction::Ref tTagRef; 
    MuonSF* muSF;
    ElectronSF* eleSF;
    LumiMask* lumiMask;
    PhotonSF* phoSF;

    TH2D* l_eff;
    TH2D* c_eff;
    TH2D* b_eff;
    std::unique_ptr<correction::CorrectionSet> btvFF;

    // Declaration of leaf types
    Int_t    _run;
    Long64_t _event;
    Int_t    _lumis;
    Bool_t   _isData;

    Float_t  _PUweight;
    Float_t  _PUweight_Up;
    Float_t  _PUweight_Do;

    Float_t  _TopWeight;
    Float_t  _TopWeight_Up;
    Float_t  _TopWeight_Do;
    
    Float_t  _TopPtWeight;
    Float_t  _TopPtWeight_Up;
    Float_t  _TopPtWeight_Do;
	
    Float_t  _q2weight_Up;
    Float_t  _q2weight_Do;
    Float_t  _q2weight_nominal;
    Float_t   _genWeight;
	//8 separate weights of q2
    Float_t  _q2weight_NN;//muR = nominal (N), muF = N
    Float_t  _q2weight_UN;
    Float_t  _q2weight_DN;
    Float_t  _q2weight_UU;//muR =Up, muF = Up
    Float_t  _q2weight_NU;
    Float_t  _q2weight_ND;
    Float_t  _q2weight_DD;

    Float_t   _pdfWeight;
    Float_t   _pdfweight_Up;
    Float_t	  _pdfweight_Do;

    Float_t  _ISRweight_Do;
    Float_t  _ISRweight;
    Float_t  _ISRweight_Up;

    Float_t  _FSRweight_Do;
    Float_t  _FSRweight;
    Float_t  _FSRweight_Up;


    float _prefireSF;
    float _prefireSF_Up;
    float _prefireSF_Do;

    float _btagWeight_1a;
    float _btagWeight_1a_b_Up;
    float _btagWeight_1a_b_Do;
    float _btagWeight_1a_l_Up;
    float _btagWeight_1a_l_Do;

    Float_t  _muEffWeight;
    Float_t  _muEffWeight_Up;
    Float_t  _muEffWeight_Do;

    Float_t  _muEffWeight_Id;
    Float_t  _muEffWeight_Id_Up;
    Float_t  _muEffWeight_Id_Do;

    Float_t  _muEffWeight_Iso;
    Float_t  _muEffWeight_Iso_Up;
    Float_t  _muEffWeight_Iso_Do;
    
    Float_t  _muEffWeight_Trig;
    Float_t  _muEffWeight_Trig_Up;
    Float_t  _muEffWeight_Trig_Do;
    
    //electron
    Float_t  _eleEffWeight;
    Float_t  _eleEffWeight_Up;
    Float_t  _eleEffWeight_Do;

    Float_t  _eleEffWeight_Id;
    Float_t  _eleEffWeight_Id_Up;
    Float_t  _eleEffWeight_Id_Do;

    Float_t  _eleEffWeight_Reco;
    Float_t  _eleEffWeight_Reco_Up;
    Float_t  _eleEffWeight_Reco_Do;

    Float_t  _eleEffWeight_Trig;
    Float_t  _eleEffWeight_Trig_Up;
    Float_t  _eleEffWeight_Trig_Do;

    Float_t  _evtWeight;
    Float_t  _lumiWeight;

    Float_t  _pfMET;
    Float_t  _pfMETPhi;
    Float_t  _WtransMass;
    Float_t  _DilepMass;
    Float_t  _DiphoMass;
    Float_t  _DilepDelR;

    //DeltaR between photon and other particles
    //hadronic side
    Float_t _Reco_dr_pho_tstarHad     ;
    Float_t _Reco_dr_pho_tHad         ;
    Float_t _Reco_dr_pho_bHad         ;
    Float_t _Reco_dr_pho_Wj1          ;
    Float_t _Reco_dr_pho_Wj2          ;
    //leptonic side
    Float_t _Reco_dr_pho_tstarLep     ;
    Float_t _Reco_dr_pho_tLep         ;
    Float_t _Reco_dr_pho_gluon        ;
    Float_t _Reco_dr_pho_bLep         ;
    Float_t _Reco_dr_pho_lep          ;
    Float_t _Reco_dr_pho_nu           ;
    //DeltaR between gluon and others 
    Float_t _Reco_dr_gluon_tstarHad   ;
    Float_t _Reco_dr_gluon_tHad       ;
    Float_t _Reco_dr_gluon_tstarLep   ;
    Float_t _Reco_dr_gluon_tLep       ;
    //DeltaR between t and t* 
    Float_t _Reco_dr_tHad_tstarHad    ;
    Float_t _Reco_dr_tLep_tstarLep    ;
    Float_t _Reco_dr_tstarHad_tstarLep;

    Float_t  _Reco_eta_hadT;
    Float_t  _Reco_pt_hadT;
    Float_t  _Reco_phi_hadT;
    Float_t  _Reco_eta_lepT;
    Float_t  _Reco_pt_lepT;
    Float_t  _Reco_phi_lepT;
    Float_t  _Reco_angle_lepton_met;
    Float_t  _Reco_angle_pho_lepton;
    Float_t  _Reco_angle_pho_met;
    Float_t  _Reco_angle_leadJet_met;
    Float_t  _Reco_angle_leadBjet_met;
    Float_t  _M_jj;
    Float_t  _TopHad_mass;
    Float_t  _TopLep_mass;
    Float_t  _TopStarLep_mass;
    Float_t  _TopStarHad_mass;
    Float_t  _TopStar_mass;
    Float_t  _tgtg_mass;
    Float_t  _tgtg_mass_diff;
    Float_t  _chi2;

    Int_t    _nPho;
    std::vector<float>   _phoEt;
    std::vector<float>   _phoEta;
    std::vector<float>   _phoPhi;
    std::vector<float>   _phoPFRelIso;
    std::vector<float>   _phoMassLepGamma;

    std::vector<bool>    _phoTightID;
    std::vector<bool>    _phoMediumID;
    std::vector<int>     _phoGenMatchInd;

    std::vector<int>  _photonIsGenuine;
    std::vector<int>  _photonIsMisIDEle;
    std::vector<int>  _photonIsHadronicPhoton;
    std::vector<int>  _photonIsHadronicFake;

    std::vector<float>    _phoEffWeight;
    std::vector<float>    _phoEffWeight_Up;
    std::vector<float>    _phoEffWeight_Do;

    std::vector<float>    _phoEffWeight_Id;
    std::vector<float>    _phoEffWeight_Id_Up;
    std::vector<float>    _phoEffWeight_Id_Do;

    std::vector<float>    _phoEffWeight_PS;
    std::vector<float>    _phoEffWeight_PS_Up;
    std::vector<float>    _phoEffWeight_PS_Do;

    std::vector<float>    _phoEffWeight_CS;
    std::vector<float>    _phoEffWeight_CS_Up;
    std::vector<float>    _phoEffWeight_CS_Do;

    std::vector<float>   _MPhotonLepton;
    std::vector<float>   _AnglePhotonLepton;

    Int_t    _nLoosePho;
    Int_t    _nPhoNoID;
    Int_t    _nEle;
    Int_t    _nEleLoose;

    std::vector<float>   _elePt;
    std::vector<float>   _elePhi;
    std::vector<float>   _eleEta;
    std::vector<float>   _eleSCEta;
    std::vector<float>   _elePFRelIso;
    Int_t    _nMu;
    Int_t    _nMuLoose;
    std::vector<float>   _muPt;
    std::vector<float>   _muEta;
    std::vector<float>   _muPhi;
    std::vector<float>   _muTkRelIso;
	
    Int_t  _nJet;
    Int_t  _nBJet;
    std::vector<float>   _jetPt;
    std::vector<float>   _jetQGL;
    std::vector<float>   _jetEta;
    std::vector<float>   _jetPhi;
    std::vector<float>   _jetMass;
    std::vector<float>   _jetRes;
    std::vector<float>   _jerWeight;
    std::vector<float>   _jesWeight;

    std::vector<float>   _jetDeepB;
    std::vector<Int_t>   _jetGenJetIdx;

    Int_t  _nFatJet;
    std::vector<float>   _fatJetPt;
    std::vector<float>   _fatJetEta;
    std::vector<float>   _fatJetPhi;
    std::vector<float>   _fatJetMass;
    std::vector<float>   _fatJetMassSoftDrop;

    double _HT;
    double _ST;
    bool  _passPresel_Ele;
    bool  _passPresel_Mu;
    bool  dileptonsample;
    bool  _inHEMVeto;

    METzCalculator metZ;
    TopEventCombinatorics topEvent;
    TLorentzVector jetVector;
    TLorentzVector fatJetVector;
    TLorentzVector lepVector;
    TLorentzVector lepVector2;
    TLorentzVector phoVector;
    TLorentzVector METVector;
    TLorentzVector phoVector1;
    TLorentzVector phoVector2;
    std::vector<TLorentzVector> ljetVectors;
    std::vector<TLorentzVector> bjetVectors;
    std::vector<TLorentzVector> jetVectors;
    std::vector<TLorentzVector> fatJetVectors;
    std::vector<TLorentzVector> phoVectors;

    float lepCharge;

    std::vector<double> ljetResVectors;
    std::vector<double> bjetResVectors;

    std::vector<double> jetResolutionVectors;
    std::vector<double> jetBtagVectors;

    TLorentzVector topHad;
    TLorentzVector bhad;
    TLorentzVector blep;
    TLorentzVector Wj1;
    TLorentzVector Wj2;
    TLorentzVector hadDecay;
    TLorentzVector lepDecay;

    void InitVariables();
    void FillEvent(std::string year);
    //void FillEvent(std::string year, bool isHemVetoObj); //HEM test
    void InitBranches();
    double SFtop(double pt);
    double topPtWeight();
    void loadBtagEff(string sampleType, string year);
    float getBtagSF_1a(string sysType, bool verbose=false);
    void findPhotonCategory(int phoInd, EventTree* tree, bool* genuine, bool *misIDele, bool *hadronicphoton, bool* hadronicfake, bool* puPhoton, bool verbose=false);
    /* int findPhotonParentage(int phoInd, EventTree* tree); */
    int findPhotonGenMatch(int phoInd, EventTree* tree);

    vector<bool> passPhoMediumID(int phoInd);
    vector<bool> passPhoTightID(int phoInd);
};


void makeNtuple::InitBranches(){
    outputTree->Branch("Event_run"      , &_run );
    outputTree->Branch("Event_number"   , &_event );
    outputTree->Branch("Event_lumi"     , &_lumis );
    outputTree->Branch("Event_is_data"  , &_isData ); 
    outputTree->Branch("Event_pass_presel_ele", &_passPresel_Ele ); 
    outputTree->Branch("Event_pass_presel_mu" , &_passPresel_Mu);
    outputTree->Branch("Event_pass_hem_veto"  , &_inHEMVeto );

    //Weights: nominal
    outputTree->Branch("Weight_lumi"    , &_evtWeight );      
    outputTree->Branch("Weight_pu"      , &_PUweight );
    outputTree->Branch("Weight_ttag"      , &_TopWeight );
    outputTree->Branch("Weight_tpt"      , &_TopPtWeight );
    outputTree->Branch("Weight_prefire" , &_prefireSF );
    outputTree->Branch("Weight_btag" , &_btagWeight_1a );
    outputTree->Branch("Weight_mu"      , &_muEffWeight );
    outputTree->Branch("Weight_mu_id"   , &_muEffWeight_Id );
    outputTree->Branch("Weight_mu_iso"  , &_muEffWeight_Iso );
    outputTree->Branch("Weight_mu_trig" , &_muEffWeight_Trig );
    outputTree->Branch("Weight_ele"     , &_eleEffWeight );
    outputTree->Branch("Weight_ele_id" , &_eleEffWeight_Id );
    outputTree->Branch("Weight_ele_reco" , &_eleEffWeight_Reco );
    outputTree->Branch("Weight_ele_trig", &_eleEffWeight_Trig );
    outputTree->Branch("Weight_pho"     , &_phoEffWeight );
    outputTree->Branch("Weight_pho_id"  , &_phoEffWeight_Id );
    outputTree->Branch("Weight_pho_ps", &_phoEffWeight_PS );
    outputTree->Branch("Weight_pho_cs", &_phoEffWeight_CS );
    outputTree->Branch("Weight_jer" , &_jerWeight);
    outputTree->Branch("Weight_jes" , &_jesWeight);
	outputTree->Branch("Weight_q2"          , &_q2weight_nominal );
	outputTree->Branch("Weight_gen"         , &_genWeight );
	outputTree->Branch("Weight_pdf"         , &_pdfWeight );
	outputTree->Branch("Weight_isr"         , &_ISRweight );
	outputTree->Branch("Weight_fsr"         , &_FSRweight );
    //Weights: up/down
    if (!isSystematicRun){
	    outputTree->Branch("Weight_puUp"       , &_PUweight_Up );
	    outputTree->Branch("Weight_puDown"     , &_PUweight_Do );
	    outputTree->Branch("Weight_ttagUp"     , &_TopWeight_Up );
	    outputTree->Branch("Weight_ttagDown"   , &_TopWeight_Do );
	    outputTree->Branch("Weight_tptUp"      , &_TopPtWeight_Up );
	    outputTree->Branch("Weight_tptDown"    , &_TopPtWeight_Do );
	    outputTree->Branch("Weight_prefireUp"  , &_prefireSF_Up );
	    outputTree->Branch("Weight_prefireDown", &_prefireSF_Do );
	    outputTree->Branch("Weight_btag_bUp"   , &_btagWeight_1a_b_Up );
	    outputTree->Branch("Weight_btag_bDown" , &_btagWeight_1a_b_Do );
	    outputTree->Branch("Weight_btag_lUp"   , &_btagWeight_1a_l_Up );
	    outputTree->Branch("Weight_btag_lDown" , &_btagWeight_1a_l_Do );
	    outputTree->Branch("Weight_muUp"       , &_muEffWeight_Up);
	    outputTree->Branch("Weight_muDown"     , &_muEffWeight_Do);
	    outputTree->Branch("Weight_mu_idUp"    , &_muEffWeight_Id_Up );
	    outputTree->Branch("Weight_mu_idDown"  , &_muEffWeight_Id_Do );
	    outputTree->Branch("Weight_mu_isoUp"   , &_muEffWeight_Iso_Up );
	    outputTree->Branch("Weight_mu_isoDown" , &_muEffWeight_Iso_Do );
	    outputTree->Branch("Weight_mu_trigUp"  , &_muEffWeight_Trig_Up );
	    outputTree->Branch("Weight_mu_trigDown", &_muEffWeight_Trig_Do );
	    outputTree->Branch("Weight_eleUp"      , &_eleEffWeight_Up );
	    outputTree->Branch("Weight_eleDown"    , &_eleEffWeight_Do );
	    outputTree->Branch("Weight_ele_idUp", &_eleEffWeight_Id_Up );
	    outputTree->Branch("Weight_ele_idDown"     , &_eleEffWeight_Id_Do );
	    outputTree->Branch("Weight_ele_recoUp", &_eleEffWeight_Reco_Up );
	    outputTree->Branch("Weight_ele_recoDown"     , &_eleEffWeight_Reco_Do );
	    outputTree->Branch("Weight_ele_trigUp" , &_eleEffWeight_Trig_Up );
	    outputTree->Branch("Weight_ele_trigDown", &_eleEffWeight_Trig_Do );
	    outputTree->Branch("Weight_phoUp"      , &_phoEffWeight_Up );
	    outputTree->Branch("Weight_phoDown"    , &_phoEffWeight_Do );
	    outputTree->Branch("Weight_pho_idUp"   , &_phoEffWeight_Id_Up );
	    outputTree->Branch("Weight_pho_idDown" , &_phoEffWeight_Id_Do );
	    outputTree->Branch("Weight_pho_psUp"   , &_phoEffWeight_PS_Up);
	    outputTree->Branch("Weight_pho_psDown" , &_phoEffWeight_PS_Do);
	    outputTree->Branch("Weight_pho_csUp"   , &_phoEffWeight_CS_Up);
	    outputTree->Branch("Weight_pho_csDown" , &_phoEffWeight_CS_Do);
	    outputTree->Branch("Weight_q2Up"       , &_q2weight_Up );
	    outputTree->Branch("Weight_q2Down"     , &_q2weight_Do );
	    outputTree->Branch("Weight_pdfUp"      , &_pdfweight_Up );
        outputTree->Branch("Weight_q2_NN"          , &_q2weight_NN);
        outputTree->Branch("Weight_q2_UN"          , &_q2weight_UN);
        outputTree->Branch("Weight_q2_DN"          , &_q2weight_DN);
        outputTree->Branch("Weight_q2_NU"          , &_q2weight_NU);
        outputTree->Branch("Weight_q2_ND"          , &_q2weight_ND);
        outputTree->Branch("Weight_q2_DD"          , &_q2weight_DD);
        outputTree->Branch("Weight_q2_UU"          , &_q2weight_UU);
	    outputTree->Branch("Weight_pdfDown"    , &_pdfweight_Do );
	    outputTree->Branch("Weight_isrUp"      , &_ISRweight_Up );
	    outputTree->Branch("Weight_isrDown"    , &_ISRweight_Do );
	    outputTree->Branch("Weight_fsrUp"      , &_FSRweight_Up );
	    outputTree->Branch("Weight_fsrDown"    , &_FSRweight_Do );
    }
    //muons
    outputTree->Branch("Muon_size"    , &_nMu ); 
    outputTree->Branch("Muon_pt"   , &_muPt ); 
    outputTree->Branch("Muon_eta"  , &_muEta );
    outputTree->Branch("Muon_phi"  , &_muPhi );
    outputTree->Branch("Muon_iso"    , &_muTkRelIso );
    //electrons
    outputTree->Branch("Electron_size"   , &_nEle ); 
    outputTree->Branch("Electron_pt"  , &_elePt );
    outputTree->Branch("Electron_phi" , &_elePhi); 
    outputTree->Branch("Electron_eta" , &_eleEta);
    outputTree->Branch("Electron_eta_sc"      , &_eleSCEta ); 
    outputTree->Branch("Electron_iso"   , &_elePFRelIso ); 
    //photons
    outputTree->Branch("Photon_size"  , &_nPho ); 
    outputTree->Branch("Photon_et" , &_phoEt );
    outputTree->Branch("Photon_eta", &_phoEta );
    outputTree->Branch("Photon_phi", &_phoPhi ); 
    outputTree->Branch("Photon_iso"   , &_phoPFRelIso ); 

    outputTree->Branch("Photon_genuine"             , &_photonIsGenuine            );
    outputTree->Branch("Photon_misid_ele"            , &_photonIsMisIDEle           );
    outputTree->Branch("Photon_hadronic_photon"        , &_photonIsHadronicPhoton     );
    outputTree->Branch("Photon_hadronic_fake"        , &_photonIsHadronicFake       );
    outputTree->Branch("Photon_loose_size"  , &_nLoosePho ); 

    //jets
    outputTree->Branch("Jet_size"   , &_nJet ); 
    outputTree->Branch("Jet_b_size"  , &_nBJet ); 
	outputTree->Branch("Jet_deep_b"  , &_jetDeepB );
    outputTree->Branch("Jet_pt"  , &_jetPt );
    outputTree->Branch("Jet_qgl"  , &_jetQGL );
    outputTree->Branch("Jet_eta" , &_jetEta); 
    outputTree->Branch("Jet_phi" , &_jetPhi); 
    outputTree->Branch("Jet_mass", &_jetMass );
    outputTree->Branch("Jet_res" , &_jetRes);
    //fat jets 
    outputTree->Branch("FatJet_size", &_nFatJet);
    outputTree->Branch("FatJet_pt", &_fatJetPt);
    outputTree->Branch("FatJet_eta", &_fatJetEta);
    outputTree->Branch("FatJet_phi", &_fatJetPhi);
    outputTree->Branch("FatJet_mass", &_fatJetMass);
    outputTree->Branch("FatJet_msoftdrop", &_fatJetMassSoftDrop);
    //Recondtructed variables
    outputTree->Branch("Reco_met" , &_pfMET );
    outputTree->Branch("Reco_met_phi"     , &_pfMETPhi ); 
    outputTree->Branch("Reco_mass_trans_w"   , &_WtransMass );
    outputTree->Branch("Reco_ht"     , &_HT ); 
    outputTree->Branch("Reco_st"     , &_ST ); 
    outputTree->Branch("Reco_chi2"  , &_chi2 );
    outputTree->Branch("Reco_mass_dipho"            , &_DiphoMass                ); 
    outputTree->Branch("Reco_mass_dilep"            , &_DilepMass                );
    outputTree->Branch("Reco_dr_dilep"              , &_DilepDelR                );

    outputTree->Branch("Reco_dr_pho_tstarHad"       , &_Reco_dr_pho_tstarHad     );
    outputTree->Branch("Reco_dr_pho_tHad"           , &_Reco_dr_pho_tHad         );
    outputTree->Branch("Reco_dr_pho_bHad"           , &_Reco_dr_pho_bHad         );
    outputTree->Branch("Reco_dr_pho_Wj1"            , &_Reco_dr_pho_Wj1          );
    outputTree->Branch("Reco_dr_pho_Wj2"            , &_Reco_dr_pho_Wj2          );
    outputTree->Branch("Reco_dr_pho_tstarLep"       , &_Reco_dr_pho_tstarLep     );
    outputTree->Branch("Reco_dr_pho_tLep"           , &_Reco_dr_pho_tLep         );
    outputTree->Branch("Reco_dr_pho_gluon"          , &_Reco_dr_pho_gluon        );
    outputTree->Branch("Reco_dr_pho_bLep"           , &_Reco_dr_pho_bLep         );
    outputTree->Branch("Reco_dr_pho_lep"            , &_Reco_dr_pho_lep          );
    outputTree->Branch("Reco_dr_pho_nu"             , &_Reco_dr_pho_nu           );
    outputTree->Branch("Reco_dr_gluon_tstarHad"     , &_Reco_dr_gluon_tstarHad   );
    outputTree->Branch("Reco_dr_gluon_tHad"         , &_Reco_dr_gluon_tHad       );
    outputTree->Branch("Reco_dr_gluon_tstarLep"     , &_Reco_dr_gluon_tstarLep   );
    outputTree->Branch("Reco_dr_gluon_tLep"         , &_Reco_dr_gluon_tLep       );
    outputTree->Branch("Reco_dr_tHad_tstarHad"      , &_Reco_dr_tHad_tstarHad    );
    outputTree->Branch("Reco_dr_tLep_tstarLep"      , &_Reco_dr_tLep_tstarLep    );
    outputTree->Branch("Reco_dr_tstarHad_tstarLep"  , &_Reco_dr_tstarHad_tstarLep);

    outputTree->Branch("Reco_eta_hadT"              , &_Reco_eta_hadT            );
    outputTree->Branch("Reco_pt_hadT"               , &_Reco_pt_hadT             );
    outputTree->Branch("Reco_phi_hadT"              , &_Reco_phi_hadT            );
    outputTree->Branch("Reco_eta_lepT"              , &_Reco_eta_lepT            );
    outputTree->Branch("Reco_pt_lepT"               , &_Reco_pt_lepT             );
    outputTree->Branch("Reco_phi_lepT"              , &_Reco_phi_lepT            );
    outputTree->Branch("Reco_mass_jj"  , &_M_jj );
    outputTree->Branch("Reco_mass_t_had"  , &_TopHad_mass );
    outputTree->Branch("Reco_mass_t_lep"  , &_TopLep_mass );
    outputTree->Branch("Reco_mass_hadT"     , &_TopStarHad_mass );
    outputTree->Branch("Reco_mass_lepT"     , &_TopStarLep_mass );
    outputTree->Branch("Reco_mass_T"     , &_TopStar_mass );
    outputTree->Branch("Reco_mass_TT"  , &_tgtg_mass );
    outputTree->Branch("Reco_mass_TT_diff"  , &_tgtg_mass_diff );
    outputTree->Branch("Reco_angle_pho_lepton"   , &_Reco_angle_pho_lepton ); 
    outputTree->Branch("Reco_angle_lepton_met"   , &_Reco_angle_lepton_met    ); 
    outputTree->Branch("Reco_angle_pho_met"   , &_Reco_angle_pho_met    ); 
    outputTree->Branch("Reco_angle_leadJet_met"   , &_Reco_angle_leadJet_met      ); 
    outputTree->Branch("Reco_angle_leadBjet_met"   , &_Reco_angle_leadBjet_met     ); 
    outputTree->Branch("Reco_mass_lgamma"   , &_phoMassLepGamma ); 
    outputTree->Branch("Reco_mass_photon_lepton" , &_MPhotonLepton );
}

void makeNtuple::InitVariables()
{

    _run      = -9;
    _event    = -9;
    _lumis	  = -9;
    _isData	   = false;
    
    _PUweight = 1.;
    _PUweight_Up = 1.;
    _PUweight_Do = 1.;

    _TopWeight      = 1.;
    _TopWeight_Up   = 1.;
    _TopWeight_Do   = 1.;

    _TopPtWeight    = 1.;
    _TopPtWeight_Up = 1.;
    _TopPtWeight_Do = 1.;

    _q2weight_nominal = 1.;
    _q2weight_Up = 1.;
    _q2weight_Do = 1.;
    _q2weight_NN = 1.;
    _q2weight_UN = 1.;
    _q2weight_DN = 1.;
    _q2weight_NU = 1.;
    _q2weight_ND = 1.;
    _q2weight_UU = 1.;
    _q2weight_DD = 1.;
    _genWeight = 0.;

    _pdfWeight    = 1.;
    _pdfweight_Up = 1.;
    _pdfweight_Do = 1.;

    _ISRweight = 1.;
    _ISRweight_Up = 1.;
    _ISRweight_Do = 1.;

    _FSRweight    = 1.;
    _FSRweight_Up = 1.;
    _FSRweight_Do = 1.;

    _prefireSF = 1.;
    _prefireSF_Up = 1.;
    _prefireSF_Do = 1.;

    _btagWeight_1a = 1.;
    _btagWeight_1a_b_Up = 1.;
    _btagWeight_1a_b_Do = 1.;
    _btagWeight_1a_l_Up = 1.;
    _btagWeight_1a_l_Do = 1.;

    _muEffWeight    = 1.;
    _muEffWeight_Do = 1.;
    _muEffWeight_Up = 1.;

    _muEffWeight_Id    = 1.;
    _muEffWeight_Id_Do = 1.;
    _muEffWeight_Id_Up = 1.;

    _muEffWeight_Iso    = 1.;
    _muEffWeight_Iso_Do = 1.;
    _muEffWeight_Iso_Up = 1.;

    _muEffWeight_Trig    = 1.;
    _muEffWeight_Trig_Do = 1.;
    _muEffWeight_Trig_Up = 1.;

    _eleEffWeight    = 1.;
    _eleEffWeight_Do = 1.;
    _eleEffWeight_Up = 1.;

    _eleEffWeight_Trig    = 1.;
    _eleEffWeight_Trig_Do = 1.;
    _eleEffWeight_Trig_Up = 1.;

    _eleEffWeight_Id    = 1.;
    _eleEffWeight_Id_Do = 1.;
    _eleEffWeight_Id_Up = 1.;

    _eleEffWeight_Reco    = 1.;
    _eleEffWeight_Reco_Do = 1.;
    _eleEffWeight_Reco_Up = 1.;

    _evtWeight = 1.;

    _pfMET		     = -9.;
    _pfMETPhi	     = -9.;
    _WtransMass      = -9.;
    _DilepMass   = -9.;
    _DiphoMass       = -9.;
    _DilepDelR   = -9.;
    
    _Reco_dr_pho_tstarHad      = -9.;
    _Reco_dr_pho_tHad          = -9.;
    _Reco_dr_pho_bHad          = -9.;
    _Reco_dr_pho_Wj1           = -9.;
    _Reco_dr_pho_Wj2           = -9.;
    _Reco_dr_pho_tstarLep      = -9.;
    _Reco_dr_pho_tLep          = -9.;
    _Reco_dr_pho_gluon         = -9.;
    _Reco_dr_pho_bLep          = -9.;
    _Reco_dr_pho_lep           = -9.;
    _Reco_dr_pho_nu            = -9.;
    _Reco_dr_gluon_tstarHad    = -9.;
    _Reco_dr_gluon_tHad        = -9.;
    _Reco_dr_gluon_tstarLep    = -9.;
    _Reco_dr_gluon_tLep        = -9.;
    _Reco_dr_tHad_tstarHad     = -9.;
    _Reco_dr_tLep_tstarLep     = -9.;
    _Reco_dr_tstarHad_tstarLep = -9.;

    _Reco_eta_hadT = -9.;
    _Reco_pt_hadT = -9.;
    _Reco_phi_hadT = -9.;
    _Reco_eta_lepT = -9.;
    _Reco_pt_lepT = -9.;
    _Reco_phi_lepT = -9.;
    _Reco_angle_lepton_met  = -9.;
    _Reco_angle_pho_lepton  = -9.;
    _Reco_angle_pho_met= -9.;
    _Reco_angle_leadJet_met  = -9.;
    _Reco_angle_leadBjet_met  = -9.;
    _M_jj     = -9.;
    _TopHad_mass     = -9.;
    _TopLep_mass     = -9.;
    _TopStarLep_mass     = -9.;
    _TopStarHad_mass     = -9.;
    _TopStar_mass     = -9.;
    _tgtg_mass     = -9.;
    _tgtg_mass_diff     = -9.;
    _chi2   = -9.;

    _nPho		 = -9;
    _phoEt.clear();
    _phoEta.clear();
    _phoPhi.clear();
    _phoPFRelIso.clear();
    _phoMassLepGamma.clear();
    _phoTightID.clear();
    _phoMediumID.clear();
    _phoGenMatchInd.clear();
    _photonIsGenuine.clear();
    _photonIsMisIDEle.clear();
    _photonIsHadronicPhoton.clear();
    _photonIsHadronicFake.clear();

    _phoEffWeight.clear();
    _phoEffWeight_Up.clear();
    _phoEffWeight_Do.clear();
    _phoEffWeight_Id.clear();
    _phoEffWeight_Id_Up.clear();
    _phoEffWeight_Id_Do.clear();
    _phoEffWeight_PS.clear();
    _phoEffWeight_PS_Up.clear();
    _phoEffWeight_PS_Do.clear();
    _phoEffWeight_CS.clear();
    _phoEffWeight_CS_Up.clear();
    _phoEffWeight_CS_Do.clear();

    _MPhotonLepton.clear();
    _AnglePhotonLepton.clear();

    _nLoosePho    = -9;
    _nPhoNoID     = -9;
    _nEle		  = -9;
    _nEleLoose    = -9;
    _elePt.clear();
    _elePhi.clear();
    _eleEta.clear();
    _eleSCEta.clear();
    _elePFRelIso.clear();

    _nMu		     = -9;
    _nMuLoose 	     = -9;
    _muPt.clear();
    _muEta.clear();
    _muPhi.clear();
    _muTkRelIso.clear();

    _nJet     = -9;  
    _nBJet    = -9;    
    _jetPt.clear();
    _jetQGL.clear();
    _jetEta.clear();
    _jetPhi.clear();
    _jetMass.clear();
    _jetRes.clear();
    _jerWeight.clear();
    _jesWeight.clear();
    _jetGenJetIdx.clear();
    _jetDeepB.clear();

    _nFatJet  =-9;  
    _fatJetPt.clear();
    _fatJetEta.clear();
    _fatJetPhi.clear();
    _fatJetMass.clear();
    _fatJetMassSoftDrop.clear();

    _HT		 = -9.;
    _ST		 = -9.;
    _passPresel_Ele  = false;
    _passPresel_Mu   = false;
    dileptonsample   = false;

    lepCharge  = -9.;


}



#endif

