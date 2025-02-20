
def GetVarInfo(region, channel):
    varOther = { 
             "Muon_pt"              : ["Muon_pt"     , [30,0,1650], True],
             "Electron_pt"          : ["Electron_pt"    , [30,0,1500], True],
             "Photon_et"             : ["Photon_et[0]"    , [100,0,2000], True],
             "Photon_size"          : ["Photon_size"     , [10,-0.5,9.5], True],
             "Photon_h_over_e"       : ["Photon_h_over_e[0]"    , [20,0,0.4], True],
             "Jet_size"             : ["Jet_size"     , [16,-0.5,15.5], True],
             "Jet_b_size"           : ["Jet_b_size"     , [10,-0.5,9.5], True],
             "Jet_pt"                : ["Jet_pt[0]"    , [30,-20,1480], True],
             "Jet_eta"             : ["Jet_eta"    , [12,-2.88,2.88], True],
             "Reco_met"             : ["Reco_met"      , [30,-20,1180], True],
             "Reco_mass_lgamma"     : ["Reco_mass_lgamma", [30,0,3000], True],
             "Reco_mass_t_had"      : ["Reco_mass_t_had", [30,0,3000], True],
             "Reco_mass_t_lep"      : ["Reco_mass_t_lep", [30,0,3000], True],
             "Reco_ht"              : ["Reco_ht"        , [300,0,9000], True],
             "Reco_st"              : ["Reco_st"        , [30,0,6000], True],
             "Reco_mass_T_had"      : ["Reco_mass_T_had", [30,0,6000], True],
             "Reco_mass_T_lep"      : ["Reco_mass_T_lep", [30,0,6000], True],
             "Reco_mass_T"          : ["Reco_mass_T", [30,0,6000], True],
             "Reco_mass_TT"          : ["Reco_mass_TT", [300,0,9000], True],
             "Reco_dr_photon_lepton" : ["Reco_dr_photon_lepton[0]", [20,0,5], True],
             "Reco_eta_hadT"    : ["Reco_eta_hadT", [20,-5,5], True],
             "Reco_pt_hadT"     : ["Reco_pt_hadT" , [30,0,3000], True],
             "Reco_pt_lepT"     : ["Reco_pt_lepT" , [30,0,3000], True],
             "Reco_angle_leadPhoton_lepton"     : ["Reco_angle_leadPhoton_lepton", [20,0,5], True],
             "Reco_ratio_leadJetPt_met"         : ["Reco_ratio_leadJetPt_met", [20,0,20], True],
             "Reco_angle_leadPhoton_met"        : ["Reco_angle_leadPhoton_met", [20,0,5], True],
             "Reco_angle_leadBjet_met"          : ["Reco_angle_leadBjet_met", [20,0,5], True],
             "Jet_qgl"                  : ["Jet_qgl[0]", [20,-0.6,1.4], True],
             "FatJet_size"             : ["FatJet_size"            , [5,-0.5,4.5], True],
             "FatJet_deepTagMD_WvsQCD" : ["FatJet_deepTagMD_WvsQCD[0]", [20,-0.5,1.5], True],
             "FatJet_btagDeepB"        : ["FatJet_btagDeepB[0]"       , [20,-0.5,1.5], True],
             "FatJet_deepTagMD_TvsQCD" : ["FatJet_deepTagMD_TvsQCD[0]", [20,-0.5,1.5], True],
             "FatJet_deepTag_TvsQCD"   : ["FatJet_deepTag_TvsQCD[0]"  , [20,-0.5,1.5], True],
             "FatJet_deepTag_WvsQCD"   : ["FatJet_deepTag_WvsQCD[0]"  , [20,-0.5,1.5], True],
             #"Jet1_qgl"      : ["Jet_qgl[0]"    , [20,-0.5,1.5], True],
             #"Jet2_qgl"      : ["Jet_qgl[1]"    , [20,-0.5,1.5], True],
             }
    varMu = {
             #"Muon_eta"             : ["Muon_eta[0]"    , [12,-2.88,2.88], True],
            }
    varEle = {
             #"Electron_eta_sc"      : ["Electron_eta_sc[0]" , [12,-2.88,2.88], True],
            }
    varFatJet = {
             "FatJet_pt_0"               : ["FatJet_pt_0"              , [9000,-50,8950], True],
             #"FatJet_eta"              : ["FatJet_eta[0]"             , [12,-2.88,2.88], True],
             "FatJet_msoftdrop_0"        : ["FatJet_msoftdrop_0"       , [9000,-50,8950], True],
            }
    varBase = {
             "Reco_mass_T"          : ["Reco_mass_T", [6000,-50,5950], True],
             "Reco_mass_lgamma_0"     : ["Reco_mass_lgamma_0", [2000,-50,1950], True],
             "Reco_mass_trans_w"    : ["Reco_mass_trans_w", [2000,-50,1950], True],
             "Reco_st"              : ["Reco_st"        , [9000,-50,8950], True],
             "Reco_mass_TT_diff"          : ["Reco_mass_TT_diff", [4000,-2000,2000], True],
             "Jet_deep_b0"               : ["Jet_deep_b0", [20,0,1], True],
             "Jet_deep_b1"               : ["Jet_deep_b1", [20,0,1], True],
             "Reco_angle_lepton_met"        : ["Reco_angle_lepton_met", [20,0,5], True],
             "Reco_angle_leadJet_met"       : ["Reco_angle_leadJet_met", [20,0,5], True],
             "Reco_angle_leadBjet_met"      : ["Reco_angle_leadBjet_met", [20,0,5], True],
             "Reco_chi2"            : ["Reco_chi2", [1000,0,1000], True],
             "Jet_size"             : ["Jet_size"     , [16,-0.5,15.5], True],
             "Jet_qgl_0"      : ["Jet_qgl_0"    , [20,-0.5,1.5], True],
             "Jet_qgl_1"      : ["Jet_qgl_1"    , [20,-0.5,1.5], True],
             "Reco_dr_pho_tstarHad"                 : ["Reco_dr_pho_tstarHad"     , [20,0,10], True],
             "Reco_dr_pho_tHad"                     : ["Reco_dr_pho_tHad"         , [20,0,10], True],
             "Reco_dr_pho_tstarLep"                 : ["Reco_dr_pho_tstarLep"     , [20,0,10], True],
             "Reco_dr_pho_tLep"                     : ["Reco_dr_pho_tLep"         , [20,0,10], True],
             "Reco_dr_pho_gluon"                    : ["Reco_dr_pho_gluon"        , [20,0,10], True],
             "Reco_dr_pho_bLep"                     : ["Reco_dr_pho_bLep"         , [20,0,10], True],
             "Reco_dr_pho_lep"                      : ["Reco_dr_pho_lep"          , [20,0,10], True],
             "Reco_dr_pho_nu"                       : ["Reco_dr_pho_nu"           , [20,0,10], True],
             "Reco_dr_gluon_tstarHad"               : ["Reco_dr_gluon_tstarHad"   , [20,0,10], True],
             "Reco_dr_gluon_tHad"                   : ["Reco_dr_gluon_tHad"       , [20,0,10], True],
             "Reco_dr_gluon_tstarLep"               : ["Reco_dr_gluon_tstarLep"   , [20,0,10], True],
             "Reco_dr_gluon_tLep"                   : ["Reco_dr_gluon_tLep"       , [20,0,10], True],
             "Reco_dr_tHad_tstarHad"                : ["Reco_dr_tHad_tstarHad"    , [20,0,10], True],
             "Reco_dr_tLep_tstarLep"                : ["Reco_dr_tLep_tstarLep"    , [20,0,10], True],
             "Reco_dr_tstarHad_tstarLep"            : ["Reco_dr_tstarHad_tstarLep", [20,0,10], True],
             }
    if "Boosted" in region: 
        #pass
        varBase.update(varFatJet)
    if "u" in channel:
        varBase.update(varMu)
    else:
        varBase.update(varEle)
    return varBase

#allVarList = GetVarInfo().keys()
#print(len(allVarList))
