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
#include "ParsePhotonID.h"

#include "EventTree.h"
#include "EventPick.h"
#include "Selector.h"

#include "JECvariation.h"

#include <iomanip>
#include <cmath>

//#include <boost/program_options.hpp>

// Standalone Btag scale factor tool from 
// https://twiki.cern.ch/twiki/bin/view/CMS/BTagCalibration
#include "BTagCalibrationStandalone.h"

// Header file for the classes stored in the TTree if any.
#include "vector"

#include "METzCalculator.h"
#include "TopEventCombinatorics.h"

#include "ReaderPileupSF.h"
#include "ReaderLumiSF.h"
#include "ReaderMuSF.h"
#include "ReaderEleSF.h"
#include "ReaderPhoSF.h"

#include "UncertaintySourcesList.h"

#include "OverlapRemove.h"

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

    MuonSF* muSF;
    ElectronSF* eleSF;
    PhotonSF* phoSF;

    TH2D* l_eff;
    TH2D* c_eff;
    TH2D* b_eff;

    // Declaration of leaf types
    Int_t    _run;
    Long64_t _event;
    Int_t    _lumis;
    Bool_t   _isData;

    Float_t  _PUweight;
    Float_t  _PUweight_Up;
    Float_t  _PUweight_Do;
	
    Float_t  _q2weight_Up;
    Float_t  _q2weight_Do;
    Float_t  _q2weight_nominal;
    Float_t   _genWeight;
	
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
    Float_t  _nu_pz;
    Float_t  _nu_pz_other;
    Float_t  _WtransMass;
    Float_t  _DilepMass;
    Float_t  _DiphoMass;
    Float_t  _DilepDelR;
    Float_t  _Reco_dr_TT;
    Float_t  _Reco_eta_hadT;
    Float_t  _Reco_pt_hadT;
    Float_t  _Reco_phi_hadT;
    Float_t  _Reco_eta_lepT;
    Float_t  _Reco_pt_lepT;
    Float_t  _Reco_phi_lepT;
    Float_t  _Reco_angle_leadPhoton_lepton;
    Float_t  _Reco_angle_lepton_met;
    Float_t  _Reco_angle_leadPhoton_met;
    Float_t  _Reco_angle_leadJet_met;
    Float_t  _Reco_angle_leadBjet_met;
    Float_t  _Reco_ratio_leadJetPt_met;
    Float_t  _Reco_ratio_leadJetPt_ht;
    Float_t  _Mt_blgammaMET;
    Float_t  _Mt_lgammaMET;
    Float_t  _M_bjj;
    Float_t  _M_bjjgamma;
    Float_t  _M_jj;
    Float_t  _TopHad_mass;
    Float_t  _TopTop_mass;
    Float_t  _TopLep_mass;
    Float_t  _TopStarLep_mass;
    Float_t  _TopStarHad_mass;
    Float_t  _TopStar_mass;
    Float_t  _tgtg_mass;
    Float_t  _chi2;

    Int_t    _nPho;
    Int_t    _nPhoBarrel;
    Int_t    _nPhoEndcap;
    std::vector<float>   _phoEt;
    std::vector<float>   _phoEta;
    std::vector<float>   _phoPhi;
    std::vector<bool>    _phoIsBarrel;
    std::vector<float>   _phoR9;
    std::vector<float>   _phoHoverE;
    std::vector<float>   _phoSIEIE;
    std::vector<float>   _phoPFRelIso;
    std::vector<float>   _phoPFRelChIso;
    std::vector<float>   _phoPFChIso;

    std::vector<bool>    _phoTightID;
    std::vector<bool>    _phoMediumID;
    std::vector<int>     _phoGenMatchInd;
    std::vector<float>   _phoMassLepGamma;

    std::vector<bool>  _photonIsGenuine;
    std::vector<bool>  _photonIsMisIDEle;
    std::vector<bool>  _photonIsHadronicPhoton;
    std::vector<bool>  _photonIsHadronicFake;

    std::vector<bool>    _photonNoIDIsGenuine;
    std::vector<bool>    _photonNoIDIsMisIDEle;
    std::vector<bool>    _photonNoIDIsHadronicPhoton;
    std::vector<bool>    _photonNoIDIsHadronicFake;

    std::vector<int>   _photonParentage;
    std::vector<int>   _photonParentPID;

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

    std::vector<float>   _dRPhotonJet;
    std::vector<float>   _dRPhotonLepton;
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

    std::vector<float>   _jetCSVV2;
    std::vector<float>   _jetDeepB;
    std::vector<Int_t>   _jetGenJetIdx;

    Int_t  _nGenJet;
    std::vector<float>   _genJetPt;
    std::vector<float>   _genJetEta;
    std::vector<float>   _genJetPhi;
    std::vector<float>   _genJetMass;

    Int_t  _nFatJet;
    std::vector<float>   _fatJetPt;
    std::vector<float>   _fatJetEta;
    std::vector<float>   _fatJetPhi;
    std::vector<float>   _fatJetMass;
    std::vector<float>   _fatJetMassSoftDrop;
    std::vector<float>   _fatJetBtagDeepB;
    std::vector<float>   _fatJetDeepTagT;
    std::vector<float>   _fatJetDeepTagW;
    std::vector<float>   _fatJetDeepTagMDT;
    std::vector<float>   _fatJetDeepTagMDW;
    std::vector<float>   _fatJetEleIdx;
    std::vector<float>   _fatJetMuIdx;
    std::vector<int>     _fatJetGenJetAK8Idx;
    std::vector<int>     _fatJetHadFlvr;
    std::vector<int>     _fatJetID;

    Int_t  _nGenPart;
    std::vector<float>   _genPt;
    std::vector<float>   _genEta;
    std::vector<float>   _genPhi;
    std::vector<float>   _genMass;
    std::vector<int>     _genStatus;
    std::vector<int>     _genStatusFlag;
    std::vector<int>     _genPDGID;
    std::vector<int>     _genMomIdx;

    double _HT;
    double _ST;
    bool  _passPresel_Ele;
    bool  _passPresel_Mu;
    bool  _passAll_Ele;
    bool  _passAll_Mu;
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
    float getBtagSF_1a(string sysType, BTagCalibrationReader reader, bool verbose=false);
    vector<float> getBtagSF_1c(string sysType, BTagCalibrationReader reader, vector<float> &btagSF);
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
    outputTree->Branch("Event_pass_all_ele"   , &_passAll_Ele ); 
    outputTree->Branch("Event_pass_all_mu"    , &_passAll_Mu );
    outputTree->Branch("Event_pass_hem_veto"  , &_inHEMVeto );

    //Weights: nominal
    outputTree->Branch("Weight_lumi"    , &_evtWeight );      
    outputTree->Branch("Weight_pu"      , &_PUweight );
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
    //Weights: up/down
    if (!isSystematicRun){
	    outputTree->Branch("Weight_pu_up"       , &_PUweight_Up );
	    outputTree->Branch("Weight_pu_down"     , &_PUweight_Do );
	    outputTree->Branch("Weight_prefire_up"  , &_prefireSF_Up );
	    outputTree->Branch("Weight_prefire_down", &_prefireSF_Do );
	    outputTree->Branch("Weight_btag_b_up"   , &_btagWeight_1a_b_Up );
	    outputTree->Branch("Weight_btag_b_down" , &_btagWeight_1a_b_Do );
	    outputTree->Branch("Weight_btag_l_up"   , &_btagWeight_1a_l_Up );
	    outputTree->Branch("Weight_btag_l_down" , &_btagWeight_1a_l_Do );
	    outputTree->Branch("Weight_mu_up"       , &_muEffWeight_Up);
	    outputTree->Branch("Weight_mu_down"     , &_muEffWeight_Do);
	    outputTree->Branch("Weight_mu_id_up"    , &_muEffWeight_Id_Up );
	    outputTree->Branch("Weight_mu_id_down"  , &_muEffWeight_Id_Do );
	    outputTree->Branch("Weight_mu_iso_up"   , &_muEffWeight_Iso_Up );
	    outputTree->Branch("Weight_mu_iso_down" , &_muEffWeight_Iso_Do );
	    outputTree->Branch("Weight_mu_trig_up"  , &_muEffWeight_Trig_Up );
	    outputTree->Branch("Weight_mu_trig_down", &_muEffWeight_Trig_Do );
	    outputTree->Branch("Weight_ele_up"      , &_eleEffWeight_Up );
	    outputTree->Branch("Weight_ele_down"    , &_eleEffWeight_Do );
	    outputTree->Branch("Weight_ele_id_up", &_eleEffWeight_Id_Up );
	    outputTree->Branch("Weight_ele_id_down"     , &_eleEffWeight_Id_Do );
	    outputTree->Branch("Weight_ele_reco_up", &_eleEffWeight_Reco_Up );
	    outputTree->Branch("Weight_ele_reco_down"     , &_eleEffWeight_Reco_Do );
	    outputTree->Branch("Weight_ele_trig_up" , &_eleEffWeight_Trig_Up );
	    outputTree->Branch("Weight_ele_trig_down", &_eleEffWeight_Trig_Do );
	    outputTree->Branch("Weight_pho_up"      , &_phoEffWeight_Up );
	    outputTree->Branch("Weight_pho_down"    , &_phoEffWeight_Do );
	    outputTree->Branch("Weight_pho_id_up"   , &_phoEffWeight_Id_Up );
	    outputTree->Branch("Weight_pho_id_down" , &_phoEffWeight_Id_Do );
	    outputTree->Branch("Weight_pho_ps_up"   , &_phoEffWeight_PS_Up);
	    outputTree->Branch("Weight_pho_ps_down" , &_phoEffWeight_PS_Do);
	    outputTree->Branch("Weight_pho_cs_up"   , &_phoEffWeight_CS_Up);
	    outputTree->Branch("Weight_pho_cs_down" , &_phoEffWeight_CS_Do);
	    outputTree->Branch("Weight_q2"          , &_q2weight_nominal );
	    outputTree->Branch("Weight_q2_up"       , &_q2weight_Up );
	    outputTree->Branch("Weight_q2_down"     , &_q2weight_Do );
	    outputTree->Branch("Weight_gen"         , &_genWeight );
	    outputTree->Branch("Weight_pdf"         , &_pdfWeight );
	    outputTree->Branch("Weight_pdf_up"      , &_pdfweight_Up );
	    outputTree->Branch("Weight_pdf_down"    , &_pdfweight_Do );
	    outputTree->Branch("Weight_isr_down"    , &_ISRweight_Do );
	    outputTree->Branch("Weight_isr"         , &_ISRweight );
	    outputTree->Branch("Weight_isr_up"      , &_ISRweight_Up );
	    outputTree->Branch("Weight_fsr_down"    , &_FSRweight_Do );
	    outputTree->Branch("Weight_fsr"         , &_FSRweight );
	    outputTree->Branch("Weight_fsr_up"      , &_FSRweight_Up );
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
    outputTree->Branch("Photon_barrel_size"   , &_nPhoBarrel );
    outputTree->Branch("Photon_endcap_size"   , &_nPhoEndcap );
    outputTree->Branch("Photon_et" , &_phoEt );
    outputTree->Branch("Photon_eta", &_phoEta );
    outputTree->Branch("Photon_r9" , &_phoR9 ); 
    outputTree->Branch("Photon_phi", &_phoPhi ); 
    outputTree->Branch("Photon_is_barrel"  , &_phoIsBarrel ); 
    outputTree->Branch("Photon_h_over_e"    , &_phoHoverE ); 
    outputTree->Branch("Photon_sieie"     , &_phoSIEIE ); 
    outputTree->Branch("Photon_iso"   , &_phoPFChIso ); 

    outputTree->Branch("Photon_genuine"             , &_photonIsGenuine            );
    outputTree->Branch("Photon_misid_ele"            , &_photonIsMisIDEle           );
    outputTree->Branch("Photon_hadronic_photon"        , &_photonIsHadronicPhoton     );
    outputTree->Branch("Photon_hadronic_fake"        , &_photonIsHadronicFake       );
    outputTree->Branch("Photon_noid_genuine"            , &_photonNoIDIsGenuine            );
    outputTree->Branch("Photon_noid_misid_ele"          , &_photonNoIDIsMisIDEle           );
    outputTree->Branch("Photon_noid_hadronic_photon"           , &_photonNoIDIsHadronicPhoton     );
    outputTree->Branch("Photon_noid_hadronic_fake"      , &_photonNoIDIsHadronicFake       );
    outputTree->Branch("Photon_parent_pid" , &_photonParentPID);
    outputTree->Branch("photon_parentage"        , &_photonParentage       );
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
    outputTree->Branch("FatJet_jetId", &_fatJetID);
    outputTree->Branch("FatJet_btagDeepB", &_fatJetBtagDeepB);
    outputTree->Branch("FatJet_deepTagMD_TvsQCD", &_fatJetDeepTagMDT);
    outputTree->Branch("FatJet_deepTagMD_WvsQCD", &_fatJetDeepTagMDW);
    outputTree->Branch("FatJet_deepTag_TvsQCD", &_fatJetDeepTagT);
    outputTree->Branch("FatJet_deepTag_WvsQCD", &_fatJetDeepTagW);
    outputTree->Branch("FatJet_hadronFlavour", &_fatJetHadFlvr);
    outputTree->Branch("FatJet_electronIdx3SJ", &_fatJetEleIdx);
    outputTree->Branch("FatJet_muonIdx3SJ", &_fatJetMuIdx);
    //Recondtructed variables
    outputTree->Branch("Reco_met" , &_pfMET );
    outputTree->Branch("Reco_met_phi"     , &_pfMETPhi ); 
    outputTree->Branch("Reco_met_pz" , &_nu_pz );
    outputTree->Branch("Reco_met_pz_other"  , &_nu_pz_other );
    outputTree->Branch("Reco_mass_trans_w"   , &_WtransMass );
    outputTree->Branch("Reco_ht"     , &_HT ); 
    outputTree->Branch("Reco_st"     , &_ST ); 
    outputTree->Branch("Reco_chi2"  , &_chi2 );
    outputTree->Branch("Reco_mass_dipho"                , &_DiphoMass                   ); 
    outputTree->Branch("Reco_mass_dilep"                , &_DilepMass                   );
    outputTree->Branch("Reco_dr_dilep"                  , &_DilepDelR                   );
    outputTree->Branch("Reco_dr_TT"                     , &_Reco_dr_TT                  );
    outputTree->Branch("Reco_eta_hadT"                  , &_Reco_eta_hadT               );
    outputTree->Branch("Reco_pt_hadT"                   , &_Reco_pt_hadT                );
    outputTree->Branch("Reco_phi_hadT"                  , &_Reco_phi_hadT               );
    outputTree->Branch("Reco_eta_lepT"                  , &_Reco_eta_lepT               );
    outputTree->Branch("Reco_pt_lepT"                   , &_Reco_pt_lepT                );
    outputTree->Branch("Reco_phi_lepT"                  , &_Reco_phi_lepT               );
    outputTree->Branch("Reco_mass_jj"  , &_M_jj );
    outputTree->Branch("Reco_mass_t_had"  , &_TopHad_mass );
    outputTree->Branch("Reco_mass_t_lep"  , &_TopLep_mass );
    outputTree->Branch("Reco_mass_tt"  , &_TopTop_mass );
    outputTree->Branch("Reco_mass_hadT"     , &_TopStarHad_mass );
    outputTree->Branch("Reco_mass_lepT"     , &_TopStarLep_mass );
    outputTree->Branch("Reco_mass_T"     , &_TopStar_mass );
    outputTree->Branch("Reco_mass_TT"  , &_tgtg_mass );
    outputTree->Branch("Reco_mass_bjj" , &_M_bjj );
    outputTree->Branch("Reco_mass_bjjgamma"   , &_M_bjjgamma );

    outputTree->Branch("Reco_angle_leadPhoton_lepton"   , &_Reco_angle_leadPhoton_lepton ); 
    outputTree->Branch("Reco_angle_lepton_met"   , &_Reco_angle_lepton_met    ); 
    outputTree->Branch("Reco_angle_leadPhoton_met"   , &_Reco_angle_leadPhoton_met    ); 
    outputTree->Branch("Reco_angle_leadJet_met"   , &_Reco_angle_leadJet_met      ); 
    outputTree->Branch("Reco_angle_leadBjet_met"   , &_Reco_angle_leadBjet_met     ); 
    outputTree->Branch("Reco_ratio_leadJetPt_met"   , &_Reco_ratio_leadJetPt_met      ); 
    outputTree->Branch("Reco_ratio_leadJetPt_ht"   , &_Reco_ratio_leadJetPt_ht      ); 

    outputTree->Branch("Reco_mass_lgamma"   , &_phoMassLepGamma ); 
    outputTree->Branch("Reco_mass_trans_blgammaMET", &_Mt_blgammaMET );
    outputTree->Branch("Reco_mass_trans_lgammaMET" , &_Mt_lgammaMET );
    outputTree->Branch("Reco_dr_photon_jet"   , &_dRPhotonJet );
    outputTree->Branch("Reco_dr_photon_lepton", &_dRPhotonLepton );
    outputTree->Branch("Reco_mass_photon_lepton" , &_MPhotonLepton );

    if (!tree->isData_ && !isSystematicRun){
        /*
	    outputTree->Branch("Gen_part_size"  	  , &_nGenPart ); 
	    outputTree->Branch("Gen_pt"	  , &_genPt	 );
	    outputTree->Branch("Gen_eta"	  , &_genEta	 ); 
	    outputTree->Branch("Gen_phi"	  , &_genPhi	 ); 
	    outputTree->Branch("Gen_mass"	  , &_genMass	 ); 
	    outputTree->Branch("Gen_status"    , &_genStatus );
	    outputTree->Branch("Gen_status_flag", &_genStatusFlag );
	    outputTree->Branch("Gen_pdg_id"	  , &_genPDGID	 ); 
	    outputTree->Branch("Gen_mom_idx"    , &_genMomIdx );
	    outputTree->Branch("Gen_jet_idx"  , &_jetGenJetIdx );
	    outputTree->Branch("Gen_jet_size"  	, &_nGenJet	 ); 
	    outputTree->Branch("Gen_jet_pt"	, &_genJetPt	 );
	    outputTree->Branch("Gen_jet_eta"	, &_genJetEta	 ); 
	    outputTree->Branch("Gen_jet_phi"	, &_genJetPhi	 ); 
	    outputTree->Branch("Gen_jet_mass"	, &_genJetMass	 ); 
        */
    }
}

void makeNtuple::InitVariables()
{

    _run      = -9999;
    _event    = -9999;
    _lumis		     = -9999;
    _isData		     = false;
    _pfMET		     = -9999;
    _pfMETPhi	     = -9999;
    _nu_pz    = -9999;
    _nu_pz_other     = -9999;
    _WtransMass      = -9999;
    
    _Reco_angle_leadPhoton_lepton  = -9999;
    _Reco_angle_lepton_met  = -9999;
    _Reco_angle_leadPhoton_met= -9999;
    _Reco_angle_leadJet_met  = -9999;
    _Reco_angle_leadBjet_met  = -9999;
    _Reco_ratio_leadJetPt_met  = -9999;
    _Reco_ratio_leadJetPt_ht  = -9999;

    _Mt_blgammaMET   = -9999;
    _Mt_lgammaMET    = -9999;
    _M_bjj    = -9999;
    _M_bjjgamma      = -9999;
    _M_jj     = -9999;
    _TopHad_mass     = -9999;
    _TopTop_mass     = -9999;
    _TopLep_mass     = -9999;
    _TopStarLep_mass     = -9999;
    _TopStarHad_mass     = -9999;
    _TopStar_mass     = -9999;
    _tgtg_mass     = -9999;
    _chi2   = -9999;
    _HT		 = -9999;
    _ST		 = -9999;
    _DilepMass   = -9999;
    _DilepDelR   = -9999;
    _Reco_dr_TT   = -9999;
    _Reco_eta_hadT = -9999;
    _Reco_pt_hadT = -9999;
    _Reco_phi_hadT = -9999;
    _Reco_eta_lepT = -9999;
    _Reco_pt_lepT = -9999;
    _Reco_phi_lepT = -9999;
    _DiphoMass       = -9999;

    _nPho		 = -9999;
    _nEle		     = -9999;
    _nMu		     = -9999;
    _nMuLoose 	     = -9999;
    _nEleLoose    = -9999;
    _nJet     = -9999;  
    _nFatJet  =-9999;  
    _nBJet    = -9999;    

    _nGenPart = -9999;
    _nGenJet  = -9999;

    _passPresel_Ele  = false;
    _passPresel_Mu   = false;
    _passAll_Ele     = false;
    _passAll_Mu      = false;


    _pdfWeight    = 1.;
    _pdfweight_Up = 1.;
    _pdfweight_Do = 1.;
    _genWeight = 0.;

    _q2weight_nominal = 1.;
    _q2weight_Up = 1.;
    _q2weight_Do = 1.;

    _ISRweight_Up = 1.;
    _ISRweight_Do = 1.;

    _FSRweight_Up = 1.;
    _FSRweight_Do = 1.;

    _eleEffWeight    = 1.;
    _eleEffWeight_Do = 1.;
    _eleEffWeight_Up = 1.;

    _muEffWeight    = 1.;
    _muEffWeight_Do = 1.;
    _muEffWeight_Up = 1.;

    _phoEffWeight.clear();
    _phoEffWeight_Do.clear();
    _phoEffWeight_Up.clear();
    _phoEffWeight_Id.clear();
    _phoEffWeight_Id_Do.clear();
    _phoEffWeight_Id_Up.clear();
    _phoEffWeight_PS.clear();
    _phoEffWeight_PS_Do.clear();
    _phoEffWeight_PS_Up.clear();
    _phoEffWeight_CS.clear();
    _phoEffWeight_CS_Do.clear();
    _phoEffWeight_CS_Up.clear();

    _btagWeight_1a = 1.;
    _btagWeight_1a_b_Up = 1.;
    _btagWeight_1a_b_Do = 1.;
    _btagWeight_1a_l_Up = 1.;
    _btagWeight_1a_l_Do = 1.;

    _elePt.clear();
    _elePhi.clear();
    _eleEta.clear();
    _eleSCEta.clear();
    _elePFRelIso.clear();

    _muPt.clear();
    _muEta.clear();
    _muPhi.clear();
    _muTkRelIso.clear();

    _phoEt.clear();
    _phoR9.clear();
    _phoEta.clear();
    _phoPhi.clear();
    _phoIsBarrel.clear();
    _phoHoverE.clear();
    _phoSIEIE.clear();
    _phoPFChIso.clear();

    _photonParentPID.clear();
    _phoMassLepGamma.clear();

    _photonIsGenuine.clear();
    _photonIsMisIDEle.clear();
    _photonIsHadronicPhoton.clear();
    _photonIsHadronicFake.clear();

    _photonNoIDIsGenuine.clear();
    _photonNoIDIsMisIDEle.clear();
    _photonNoIDIsHadronicPhoton.clear();
    _photonNoIDIsHadronicFake.clear();

    _jetPt.clear();
    _jetQGL.clear();
    /* _jetEn.clear(); */
    _jetEta.clear();
    _jetPhi.clear();
    _jetMass.clear();
    _jesWeight.clear();
    _jetRes.clear();
    _jerWeight.clear();
    /* _jetRawPt.clear(); */
    /* _jetArea.clear(); */
    _jetCSVV2.clear();
    _jetDeepB.clear();

    _jetGenJetIdx.clear();
    _fatJetPt.clear();
    _fatJetEta.clear();
    _fatJetPhi.clear();
    _fatJetMass.clear();
    _fatJetMassSoftDrop.clear();
    _fatJetBtagDeepB.clear();
    _fatJetDeepTagT.clear();
    _fatJetDeepTagW.clear();
    _fatJetDeepTagMDT.clear();
    _fatJetDeepTagMDW.clear();
    _fatJetEleIdx.clear();
    _fatJetMuIdx.clear();
    _fatJetGenJetAK8Idx.clear();
    _fatJetHadFlvr.clear();
    _fatJetID.clear();

    _dRPhotonJet.clear();
    _dRPhotonLepton.clear();
    _MPhotonLepton.clear();
	
    _genPt.clear();
    _genPhi.clear();
    _genEta.clear();
    _genMass.clear();
    _genStatus.clear();
    _genStatusFlag.clear();
    _genPDGID.clear();
    _genMomIdx.clear();
    _genJetPt.clear();
    _genJetEta.clear();
    _genJetPhi.clear();
    _genJetMass.clear();
}



#endif

