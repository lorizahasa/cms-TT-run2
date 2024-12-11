#include "NtupleTree.h"

NtupleTree::NtupleTree(string dir, vector<string>fileNames){
    fChain = new TChain("AnalysisTree");
    std::cout << "Start NtupleTree" << std::endl;
    fChain->SetCacheSize(100*1024*1024);
    bool isCopy = false;
    int nFiles = fileNames.size();
    //string dir = "root://cms-xrd-global.cern.ch/";
    //string dir = "root://cmsxrootd.fnal.gov/";
    //string dir = "";
    //string dirNtuple="/store/group/phys_b2g/lhasa/Output/cms-TT-run2/Ntuple_Skim";                                                                                                              
    //string dir = "root://eoscms.cern.ch/"+dirNtuple+"/"+year+"/"+decay+"/JetBase/";
    for(int fileI=0; fileI<nFiles; fileI++){
        string fName = fileNames[fileI];
        if(isCopy){
            string singleFile = fName.substr(fName.find_last_of("/")+1,fName.size());
            string xrdcp_command = "xrdcp " + dir + fName + " " + singleFile ;
            cout << xrdcp_command.c_str() << endl;
            system(xrdcp_command.c_str());
            fChain->Add(singleFile.c_str());
            cout << singleFile << "  " << fChain->GetEntries() << endl;
        }
        else{
            fChain->Add((dir + fName).c_str());
            cout << dir+fName << "  " << fChain->GetEntries() << endl;
        }   
    }
    //----------------------------
    // Initialize vectors
    //----------------------------
    fCurrent = -1;
    Weight_pho = 0;
    Weight_pho_id = 0;
    Weight_pho_ps = 0;
    Weight_pho_cs = 0;
    Weight_pho_leading = 0;
    Weight_jer = 0;
    Weight_jes = 0;
    Weight_phoUp = 0;
    Weight_phoDown = 0;
    Weight_pho_idUp = 0;
    Weight_pho_idDown = 0;
    Weight_pho_psUp = 0;
    Weight_pho_psDown = 0;
    Weight_pho_csUp = 0;
    Weight_pho_csDown = 0;
    Muon_pt = 0;
    Muon_eta = 0;
    Muon_phi = 0;
    Muon_iso = 0;
    Electron_pt = 0;
    Electron_phi = 0;
    Electron_eta = 0;
    Electron_eta_sc = 0;
    Electron_iso = 0;
    Photon_et = 0;
    Photon_et_leading = 0;
    Photon_eta = 0;
    Photon_phi = 0;
    Photon_iso = 0;
    Photon_genuine = 0;
    Photon_misid_ele = 0;
    Photon_hadronic_photon = 0;
    Photon_hadronic_fake = 0;
    Jet_deep_b = 0;
    Jet_deep_b0 = 0;
    Jet_deep_b1 = 0;
    Jet_pt = 0;
    Jet_qgl = 0;
    Jet_qgl_0 = 0;
    Jet_qgl_1 = 0;
    Jet_eta = 0;
    Jet_phi = 0;
    Jet_mass = 0;
    Jet_res = 0;
    FatJet_pt = 0;
    FatJet_pt_0 = 0;
    FatJet_eta = 0;
    //FatJet_eta_0 = 0;
    FatJet_phi = 0;
    FatJet_mass = 0;
    FatJet_msoftdrop = 0;
    FatJet_msoftdrop_0 = 0;
    Reco_mass_lgamma = 0;
    Reco_mass_lgamma_0 = 0;
    Reco_mass_photon_lepton = 0;

    std::cout << "Begin" << std::endl;
    fChain->SetBranchStatus("*",1);

    fChain->SetBranchAddress("Event_is_data", &Event_is_data, &b_Event_is_data);
    fChain->SetBranchAddress("Event_pass_presel_ele", &Event_pass_presel_ele, &b_Event_pass_presel_ele);
    fChain->SetBranchAddress("Event_pass_presel_mu", &Event_pass_presel_mu, &b_Event_pass_presel_mu);
    fChain->SetBranchAddress("Event_pass_hem_veto", &Event_pass_hem_veto, &b_Event_pass_hem_veto);
    fChain->SetBranchAddress("Weight_lumi", &Weight_lumi, &b_Weight_lumi);
    fChain->SetBranchAddress("Weight_pu", &Weight_pu, &b_Weight_pu);
    fChain->SetBranchAddress("Weight_ttag", &Weight_ttag, &b_Weight_ttag);
    fChain->SetBranchAddress("Weight_tpt", &Weight_tpt, &b_Weight_tpt);
    fChain->SetBranchAddress("Weight_prefire", &Weight_prefire, &b_Weight_prefire);
    fChain->SetBranchAddress("Weight_btag", &Weight_btag, &b_Weight_btag);
    fChain->SetBranchAddress("Weight_mu", &Weight_mu, &b_Weight_mu);
    fChain->SetBranchAddress("Weight_mu_id", &Weight_mu_id, &b_Weight_mu_id);
    fChain->SetBranchAddress("Weight_mu_iso", &Weight_mu_iso, &b_Weight_mu_iso);
    fChain->SetBranchAddress("Weight_mu_trig", &Weight_mu_trig, &b_Weight_mu_trig);
    fChain->SetBranchAddress("Weight_ele", &Weight_ele, &b_Weight_ele);
    fChain->SetBranchAddress("Weight_ele_id", &Weight_ele_id, &b_Weight_ele_id);
    fChain->SetBranchAddress("Weight_ele_reco", &Weight_ele_reco, &b_Weight_ele_reco);
    fChain->SetBranchAddress("Weight_ele_trig", &Weight_ele_trig, &b_Weight_ele_trig);
    fChain->SetBranchAddress("Weight_pho", &Weight_pho, &b_Weight_pho);
    fChain->SetBranchAddress("Weight_pho_leading", &Weight_pho_leading, &b_Weight_pho_leading);
    fChain->SetBranchAddress("Weight_pho_id", &Weight_pho_id, &b_Weight_pho_id);
    fChain->SetBranchAddress("Weight_pho_ps", &Weight_pho_ps, &b_Weight_pho_ps);
    fChain->SetBranchAddress("Weight_pho_cs", &Weight_pho_cs, &b_Weight_pho_cs);
    fChain->SetBranchAddress("Weight_jer", &Weight_jer, &b_Weight_jer);
    fChain->SetBranchAddress("Weight_jes", &Weight_jes, &b_Weight_jes);
    fChain->SetBranchAddress("Weight_q2", &Weight_q2, &b_Weight_q2);
    fChain->SetBranchAddress("Weight_gen", &Weight_gen, &b_Weight_gen);
    fChain->SetBranchAddress("Weight_pdf", &Weight_pdf, &b_Weight_pdf);
    fChain->SetBranchAddress("Weight_isr", &Weight_isr, &b_Weight_isr);
    fChain->SetBranchAddress("Weight_fsr", &Weight_fsr, &b_Weight_fsr);
    fChain->SetBranchAddress("Weight_puUp", &Weight_puUp, &b_Weight_puUp);
    fChain->SetBranchAddress("Weight_puDown", &Weight_puDown, &b_Weight_puDown);
    fChain->SetBranchAddress("Weight_ttagUp", &Weight_ttagUp, &b_Weight_ttagUp);
    fChain->SetBranchAddress("Weight_ttagDown", &Weight_ttagDown, &b_Weight_ttagDown);
    fChain->SetBranchAddress("Weight_tptUp", &Weight_tptUp, &b_Weight_tptUp);
    fChain->SetBranchAddress("Weight_tptDown", &Weight_tptDown, &b_Weight_tptDown);
    fChain->SetBranchAddress("Weight_prefireUp", &Weight_prefireUp, &b_Weight_prefireUp);
    fChain->SetBranchAddress("Weight_prefireDown", &Weight_prefireDown, &b_Weight_prefireDown);
    fChain->SetBranchAddress("Weight_btag_bUp", &Weight_btag_bUp, &b_Weight_btag_bUp);
    fChain->SetBranchAddress("Weight_btag_bDown", &Weight_btag_bDown, &b_Weight_btag_bDown);
    fChain->SetBranchAddress("Weight_btag_lUp", &Weight_btag_lUp, &b_Weight_btag_lUp);
    fChain->SetBranchAddress("Weight_btag_lDown", &Weight_btag_lDown, &b_Weight_btag_lDown);
    fChain->SetBranchAddress("Weight_muUp", &Weight_muUp, &b_Weight_muUp);
    fChain->SetBranchAddress("Weight_muDown", &Weight_muDown, &b_Weight_muDown);
    fChain->SetBranchAddress("Weight_mu_idUp", &Weight_mu_idUp, &b_Weight_mu_idUp);
    fChain->SetBranchAddress("Weight_mu_idDown", &Weight_mu_idDown, &b_Weight_mu_idDown);
    fChain->SetBranchAddress("Weight_mu_isoUp", &Weight_mu_isoUp, &b_Weight_mu_isoUp);
    fChain->SetBranchAddress("Weight_mu_isoDown", &Weight_mu_isoDown, &b_Weight_mu_isoDown);
    fChain->SetBranchAddress("Weight_mu_trigUp", &Weight_mu_trigUp, &b_Weight_mu_trigUp);
    fChain->SetBranchAddress("Weight_mu_trigDown", &Weight_mu_trigDown, &b_Weight_mu_trigDown);
    fChain->SetBranchAddress("Weight_eleUp", &Weight_eleUp, &b_Weight_eleUp);
    fChain->SetBranchAddress("Weight_eleDown", &Weight_eleDown, &b_Weight_eleDown);
    fChain->SetBranchAddress("Weight_ele_idUp", &Weight_ele_idUp, &b_Weight_ele_idUp);
    fChain->SetBranchAddress("Weight_ele_idDown", &Weight_ele_idDown, &b_Weight_ele_idDown);
    fChain->SetBranchAddress("Weight_ele_recoUp", &Weight_ele_recoUp, &b_Weight_ele_recoUp);
    fChain->SetBranchAddress("Weight_ele_recoDown", &Weight_ele_recoDown, &b_Weight_ele_recoDown);
    fChain->SetBranchAddress("Weight_ele_trigUp", &Weight_ele_trigUp, &b_Weight_ele_trigUp);
    fChain->SetBranchAddress("Weight_ele_trigDown", &Weight_ele_trigDown, &b_Weight_ele_trigDown);
    fChain->SetBranchAddress("Weight_phoUp", &Weight_phoUp, &b_Weight_phoUp);
    fChain->SetBranchAddress("Weight_phoDown", &Weight_phoDown, &b_Weight_phoDown);
    fChain->SetBranchAddress("Weight_pho_idUp", &Weight_pho_idUp, &b_Weight_pho_idUp);
    fChain->SetBranchAddress("Weight_pho_idDown", &Weight_pho_idDown, &b_Weight_pho_idDown);
    fChain->SetBranchAddress("Weight_pho_psUp", &Weight_pho_psUp, &b_Weight_pho_psUp);
    fChain->SetBranchAddress("Weight_pho_psDown", &Weight_pho_psDown, &b_Weight_pho_psDown);
    fChain->SetBranchAddress("Weight_pho_csUp", &Weight_pho_csUp, &b_Weight_pho_csUp);
    fChain->SetBranchAddress("Weight_pho_csDown", &Weight_pho_csDown, &b_Weight_pho_csDown);
    fChain->SetBranchAddress("Weight_q2Up", &Weight_q2Up, &b_Weight_q2Up);
    fChain->SetBranchAddress("Weight_q2Down", &Weight_q2Down, &b_Weight_q2Down);
    fChain->SetBranchAddress("Weight_pdfUp", &Weight_pdfUp, &b_Weight_pdfUp);
    fChain->SetBranchAddress("Weight_q2_NN", &Weight_q2_NN, &b_Weight_q2_NN);
    fChain->SetBranchAddress("Weight_q2_UN", &Weight_q2_UN, &b_Weight_q2_UN);
    fChain->SetBranchAddress("Weight_q2_DN", &Weight_q2_DN, &b_Weight_q2_DN);
    fChain->SetBranchAddress("Weight_q2_NU", &Weight_q2_NU, &b_Weight_q2_NU);
    fChain->SetBranchAddress("Weight_q2_ND", &Weight_q2_ND, &b_Weight_q2_ND);
    fChain->SetBranchAddress("Weight_q2_DD", &Weight_q2_DD, &b_Weight_q2_DD);
    fChain->SetBranchAddress("Weight_q2_UU", &Weight_q2_UU, &b_Weight_q2_UU);
    fChain->SetBranchAddress("Weight_pdfDown", &Weight_pdfDown, &b_Weight_pdfDown);
    fChain->SetBranchAddress("Weight_isrUp", &Weight_isrUp, &b_Weight_isrUp);
    fChain->SetBranchAddress("Weight_isrDown", &Weight_isrDown, &b_Weight_isrDown);
    fChain->SetBranchAddress("Weight_fsrUp", &Weight_fsrUp, &b_Weight_fsrUp);
    fChain->SetBranchAddress("Weight_fsrDown", &Weight_fsrDown, &b_Weight_fsrDown);
    fChain->SetBranchAddress("Muon_size", &Muon_size, &b_Muon_size);
    fChain->SetBranchAddress("Muon_pt", &Muon_pt, &b_Muon_pt);
    fChain->SetBranchAddress("Muon_eta", &Muon_eta, &b_Muon_eta);
    fChain->SetBranchAddress("Muon_phi", &Muon_phi, &b_Muon_phi);
    fChain->SetBranchAddress("Muon_iso", &Muon_iso, &b_Muon_iso);
    fChain->SetBranchAddress("Electron_size", &Electron_size, &b_Electron_size);
    fChain->SetBranchAddress("Electron_pt", &Electron_pt, &b_Electron_pt);
    fChain->SetBranchAddress("Electron_phi", &Electron_phi, &b_Electron_phi);
    fChain->SetBranchAddress("Electron_eta", &Electron_eta, &b_Electron_eta);
    fChain->SetBranchAddress("Electron_eta_sc", &Electron_eta_sc, &b_Electron_eta_sc);
    fChain->SetBranchAddress("Electron_iso", &Electron_iso, &b_Electron_iso);
    fChain->SetBranchAddress("Photon_size", &Photon_size, &b_Photon_size);
    //PROB
    fChain->SetBranchAddress("Photon_et", &Photon_et, &b_Photon_et);
    fChain->SetBranchAddress("Photon_et_leading", &Photon_et_leading, &b_Photon_et_leading);
    fChain->SetBranchAddress("Photon_eta", &Photon_eta, &b_Photon_eta);
    fChain->SetBranchAddress("Photon_phi", &Photon_phi, &b_Photon_phi);
    fChain->SetBranchAddress("Photon_iso", &Photon_iso, &b_Photon_iso);
    fChain->SetBranchAddress("Photon_genuine", &Photon_genuine, &b_Photon_genuine);
    fChain->SetBranchAddress("Photon_misid_ele", &Photon_misid_ele, &b_Photon_misid_ele);
    fChain->SetBranchAddress("Photon_hadronic_photon", &Photon_hadronic_photon, &b_Photon_hadronic_photon);
    fChain->SetBranchAddress("Photon_hadronic_fake", &Photon_hadronic_fake, &b_Photon_hadronic_fake);
    fChain->SetBranchAddress("Photon_loose_size", &Photon_loose_size, &b_Photon_loose_size);
    fChain->SetBranchAddress("Jet_size", &Jet_size, &b_Jet_size);
    fChain->SetBranchAddress("Jet_b_size", &Jet_b_size, &b_Jet_b_size);
    fChain->SetBranchAddress("Jet_deep_b", &Jet_deep_b, &b_Jet_deep_b);
    fChain->SetBranchAddress("Jet_deep_b0", &Jet_deep_b0, &b_Jet_deep_b0);
    fChain->SetBranchAddress("Jet_deep_b1", &Jet_deep_b1, &b_Jet_deep_b1);
    fChain->SetBranchAddress("Jet_pt", &Jet_pt, &b_Jet_pt);
    fChain->SetBranchAddress("Jet_qgl", &Jet_qgl, &b_Jet_qgl);
    fChain->SetBranchAddress("Jet_qgl_0", &Jet_qgl_0, &b_Jet_qgl_0);
    fChain->SetBranchAddress("Jet_qgl_1", &Jet_qgl_1, &b_Jet_qgl_1);
    fChain->SetBranchAddress("Jet_eta", &Jet_eta, &b_Jet_eta);
    fChain->SetBranchAddress("Jet_phi", &Jet_phi, &b_Jet_phi);
    fChain->SetBranchAddress("Jet_mass", &Jet_mass, &b_Jet_mass);
    fChain->SetBranchAddress("Jet_res", &Jet_res, &b_Jet_res);
    fChain->SetBranchAddress("FatJet_size", &FatJet_size, &b_FatJet_size);
    //PROB
    fChain->SetBranchAddress("FatJet_pt", &FatJet_pt, &b_FatJet_pt);
    fChain->SetBranchAddress("FatJet_pt_0", &FatJet_pt_0, &b_FatJet_pt_0);
    fChain->SetBranchAddress("FatJet_eta", &FatJet_eta, &b_FatJet_eta);
    fChain->SetBranchAddress("FatJet_phi", &FatJet_phi, &b_FatJet_phi);
    fChain->SetBranchAddress("FatJet_mass", &FatJet_mass, &b_FatJet_mass);
    //PROB
    fChain->SetBranchAddress("FatJet_msoftdrop", &FatJet_msoftdrop, &b_FatJet_msoftdrop);
    fChain->SetBranchAddress("FatJet_msoftdrop_0", &FatJet_msoftdrop_0, &b_FatJet_msoftdrop_0);
    fChain->SetBranchAddress("Reco_met", &Reco_met, &b_Reco_met);
    fChain->SetBranchAddress("Reco_met_phi", &Reco_met_phi, &b_Reco_met_phi);
    fChain->SetBranchAddress("Reco_mass_trans_w", &Reco_mass_trans_w, &b_Reco_mass_trans_w);
    fChain->SetBranchAddress("Reco_ht", &Reco_ht, &b_Reco_ht);
    fChain->SetBranchAddress("Reco_st", &Reco_st, &b_Reco_st);
    fChain->SetBranchAddress("Reco_chi2", &Reco_chi2, &b_Reco_chi2);
    fChain->SetBranchAddress("Reco_mass_dipho", &Reco_mass_dipho, &b_Reco_mass_dipho);
    fChain->SetBranchAddress("Reco_mass_dilep", &Reco_mass_dilep, &b_Reco_mass_dilep);
    fChain->SetBranchAddress("Reco_dr_dilep", &Reco_dr_dilep, &b_Reco_dr_dilep);
    fChain->SetBranchAddress("Reco_dr_pho_tstarHad", &Reco_dr_pho_tstarHad, &b_Reco_dr_pho_tstarHad);
    fChain->SetBranchAddress("Reco_dr_pho_tHad", &Reco_dr_pho_tHad, &b_Reco_dr_pho_tHad);
    fChain->SetBranchAddress("Reco_dr_pho_bHad", &Reco_dr_pho_bHad, &b_Reco_dr_pho_bHad);
    fChain->SetBranchAddress("Reco_dr_pho_Wj1", &Reco_dr_pho_Wj1, &b_Reco_dr_pho_Wj1);
    fChain->SetBranchAddress("Reco_dr_pho_Wj2", &Reco_dr_pho_Wj2, &b_Reco_dr_pho_Wj2);
    fChain->SetBranchAddress("Reco_dr_pho_tstarLep", &Reco_dr_pho_tstarLep, &b_Reco_dr_pho_tstarLep);
    fChain->SetBranchAddress("Reco_dr_pho_tLep", &Reco_dr_pho_tLep, &b_Reco_dr_pho_tLep);
    fChain->SetBranchAddress("Reco_dr_pho_gluon", &Reco_dr_pho_gluon, &b_Reco_dr_pho_gluon);
    fChain->SetBranchAddress("Reco_dr_pho_bLep", &Reco_dr_pho_bLep, &b_Reco_dr_pho_bLep);
    fChain->SetBranchAddress("Reco_dr_pho_lep", &Reco_dr_pho_lep, &b_Reco_dr_pho_lep);
    fChain->SetBranchAddress("Reco_dr_pho_nu", &Reco_dr_pho_nu, &b_Reco_dr_pho_nu);
    fChain->SetBranchAddress("Reco_dr_gluon_tstarHad", &Reco_dr_gluon_tstarHad, &b_Reco_dr_gluon_tstarHad);
    fChain->SetBranchAddress("Reco_dr_gluon_tHad", &Reco_dr_gluon_tHad, &b_Reco_dr_gluon_tHad);
    fChain->SetBranchAddress("Reco_dr_gluon_tstarLep", &Reco_dr_gluon_tstarLep, &b_Reco_dr_gluon_tstarLep);
    fChain->SetBranchAddress("Reco_dr_gluon_tLep", &Reco_dr_gluon_tLep, &b_Reco_dr_gluon_tLep);
    fChain->SetBranchAddress("Reco_dr_tHad_tstarHad", &Reco_dr_tHad_tstarHad, &b_Reco_dr_tHad_tstarHad);
    fChain->SetBranchAddress("Reco_dr_tLep_tstarLep", &Reco_dr_tLep_tstarLep, &b_Reco_dr_tLep_tstarLep);
    fChain->SetBranchAddress("Reco_dr_tstarHad_tstarLep", &Reco_dr_tstarHad_tstarLep, &b_Reco_dr_tstarHad_tstarLep);
    fChain->SetBranchAddress("Reco_eta_hadT", &Reco_eta_hadT, &b_Reco_eta_hadT);
    fChain->SetBranchAddress("Reco_pt_hadT", &Reco_pt_hadT, &b_Reco_pt_hadT);
    fChain->SetBranchAddress("Reco_phi_hadT", &Reco_phi_hadT, &b_Reco_phi_hadT);
    fChain->SetBranchAddress("Reco_eta_lepT", &Reco_eta_lepT, &b_Reco_eta_lepT);
    fChain->SetBranchAddress("Reco_pt_lepT", &Reco_pt_lepT, &b_Reco_pt_lepT);
    fChain->SetBranchAddress("Reco_phi_lepT", &Reco_phi_lepT, &b_Reco_phi_lepT);
    fChain->SetBranchAddress("Reco_mass_jj", &Reco_mass_jj, &b_Reco_mass_jj);
    fChain->SetBranchAddress("Reco_mass_t_had", &Reco_mass_t_had, &b_Reco_mass_t_had);
    fChain->SetBranchAddress("Reco_mass_t_lep", &Reco_mass_t_lep, &b_Reco_mass_t_lep);
    fChain->SetBranchAddress("Reco_mass_hadT", &Reco_mass_hadT, &b_Reco_mass_hadT);
    fChain->SetBranchAddress("Reco_mass_lepT", &Reco_mass_lepT, &b_Reco_mass_lepT);
    fChain->SetBranchAddress("Reco_mass_T", &Reco_mass_T, &b_Reco_mass_T);
    fChain->SetBranchAddress("Reco_mass_TT", &Reco_mass_TT, &b_Reco_mass_TT);
    fChain->SetBranchAddress("Reco_mass_TT_diff", &Reco_mass_TT_diff, &b_Reco_mass_TT_diff);
    fChain->SetBranchAddress("Reco_angle_pho_lepton", &Reco_angle_pho_lepton, &b_Reco_angle_pho_lepton);
    fChain->SetBranchAddress("Reco_angle_lepton_met", &Reco_angle_lepton_met, &b_Reco_angle_lepton_met);
    fChain->SetBranchAddress("Reco_angle_pho_met", &Reco_angle_pho_met, &b_Reco_angle_pho_met);
    fChain->SetBranchAddress("Reco_angle_leadJet_met", &Reco_angle_leadJet_met, &b_Reco_angle_leadJet_met);
    fChain->SetBranchAddress("Reco_angle_leadBjet_met", &Reco_angle_leadBjet_met, &b_Reco_angle_leadBjet_met);
    //PROB
    fChain->SetBranchAddress("Reco_mass_lgamma", &Reco_mass_lgamma, &b_Reco_mass_lgamma);
    fChain->SetBranchAddress("Reco_mass_lgamma_0", &Reco_mass_lgamma_0, &b_Reco_mass_lgamma_0);
    fChain->SetBranchAddress("Reco_mass_photon_lepton", &Reco_mass_photon_lepton, &b_Reco_mass_photon_lepton);
    

}

NtupleTree::~NtupleTree(){
    delete fChain;
}

Long64_t NtupleTree::GetEntries(){
    return fChain->GetEntries();
}

Int_t NtupleTree::GetEntry(Long64_t entry){
    return fChain->GetEntry(entry);
}

Long64_t NtupleTree::LoadTree(Long64_t entry)                                  
{                                                                              
// Set the environment to read one entry                                                  
   if (!fChain) return -5;                                                     
   Long64_t centry = fChain->LoadTree(entry);                                  
   if (centry < 0) return centry;                                              
   if (fChain->GetTreeNumber() != fCurrent) {                                  
      fCurrent = fChain->GetTreeNumber();                                      
   }                                                                           
   return centry;                                                              
}

std::vector<std::vector<std::string>> NtupleTree::splitVector(const std::vector<std::string>& strings, int n) {
    int size = strings.size() / n;  // Size of each small vector
    int remainder = strings.size() % n;  // Remaining elements
    std::vector<std::vector<std::string>> smallVectors;
    int index = 0;
    for (int i = 0; i < n; ++i) {
        if (i < remainder) {
            smallVectors.push_back(std::vector<std::string>(
                        strings.begin() + index, strings.begin() + index + size + 1));
            index += size + 1;
        } else {
            smallVectors.push_back(std::vector<std::string>(
                        strings.begin() + index, strings.begin() + index + size));
            index += size;
        }
    }
    return smallVectors;
}

std::vector<std::string> NtupleTree::splitString(const std::string& s, const std::string& delimiter) {
    std::vector<std::string> tokens;
    size_t start = 0, end = 0;
    
    while ((end = s.find(delimiter, start)) != std::string::npos) {
        tokens.push_back(s.substr(start, end - start));
        start = end + delimiter.length();
    }
    tokens.push_back(s.substr(start)); // Last token
    
    return tokens;
}
