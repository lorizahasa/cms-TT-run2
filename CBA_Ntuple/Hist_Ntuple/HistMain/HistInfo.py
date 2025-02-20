
#key is the histName in the ntuple, 
#value[0] is the title of x-axis
#value[1] is the number of bins, x-range
#value[2] decide if it is to be drawn for MC or data or both. Default value is for both.
def GetHistogramInfo():
    hDict = { 
             "Muon_pt"              : ["Muon_pt"     , [30,0,1650], True],
             "Muon_eta"             : ["Muon_eta"    , [12,-2.88,2.88], True],
             "Muon_phi"             : ["Muon_phi"    , [20,-5.0,5.0], True],
             "Electron_pt"          : ["Electron_pt"    , [30,0,1500], True],
             "Electron_eta_sc"      : ["Electron_eta_sc" , [12,-2.88,2.88], True],
             "Electron_phi"         : ["Electron_phi"   , [20,-5.0,5.0], True],
             "Photon_et"             : ["Photon_et"    , [100,0,2000], True],
             "Photon_size"          : ["Photon_size"     , [10,-0.5,9.5], True],
             "Jet_size"             : ["Jet_size"     , [16,-0.5,15.5], True],
             "Jet_b_size"           : ["Jet_b_size"     , [10,-0.5,9.5], True],
             "Jet_pt"               : ["Jet_pt"    , [30,-20,1480], True],
             "Jet_eta"             : ["Jet_eta"    , [12,-2.88,2.88], True],
             "Reco_met"             : ["Reco_met"      , [30,-20,1180], True],
             "Reco_mass_lgamma"     : ["Reco_mass_lgamma", [30,0,300], True],
             "Reco_mass_t_had"      : ["Reco_mass_t_had", [30,0,3000], True],
             "Reco_mass_t_lep"      : ["Reco_mass_t_lep", [30,0,3000], True],
             "Reco_ht"              : ["Reco_ht"        , [30,0,6000], True],
             "Reco_st"              : ["Reco_st"        , [30,0,6000], True],
             "Reco_mass_T_had"      : ["Reco_mass_T_had", [30,0,6000], True],
             "Reco_mass_T_lep"      : ["Reco_mass_T_lep", [30,0,6000], True],
             "Reco_mass_T"          : ["Reco_mass_T", [30,0,6000], True],
             "Reco_mass_TT"         : ["Reco_mass_TT", [30,0,6000], True],
             "Reco_chi2"            : ["Reco_chi2", [30, 0,1200], True],
             "FatJet_size"             : ["FatJet_size"            , [5,-0.5,4.5], True],
             "FatJet_pt"               : ["FatJet_pt"              , [30,0,3000], True],
             "FatJet_eta"              : ["FatJet_eta"             , [12,-2.88,2.88], True],
             "FatJet_mass"             : ["FatJet_mass"            , [30,0,1200], True],
             "FatJet_msoftdrop"        : ["FatJet_msoftdrop"       , [30,0,1200], True],
             "FatJet_btagDeepB"        : ["FatJet_btagDeepB"       , [20,-0.5,1.5], True],
             "FatJet_deepTagMD_TvsQCD" : ["FatJet_deepTagMD_TvsQCD", [20,-0.5,1.5], True],
             "FatJet_deepTagMD_WvsQCD" : ["FatJet_deepTagMD_WvsQCD", [20,-0.5,1.5], True],
             "FatJet_deepTag_TvsQCD"   : ["FatJet_deepTag_TvsQCD"  , [20,-0.5,1.5], True],
             "FatJet_deepTag_WvsQCD"   : ["FatJet_deepTag_WvsQCD"  , [20,-0.5,1.5], True],
             }
    hDictTemp = {
             "Muon_pt"              : ["Muon_pt"     , [2000,-50,1950], True],
             "Electron_pt"          : ["Electron_pt" , [2000,-50,1950], True],
             "Jet_pt"               : ["Jet_pt"         , [2000,-50,1950], True],
             "Photon_et"            : ["Photon_et"      , [2000,-50,1950], True],
             "Reco_met"             : ["Reco_met"       , [200,-50,1950], True],
             "Muon_eta"             : ["Muon_eta"    , [12,-2.88,2.88], True],
             "Electron_eta_sc"      : ["Electron_eta_sc", [12,-2.88,2.88], True],
             "Jet_eta"              : ["Jet_eta"        , [12,-2.88,2.88], True],
             "Photon_eta"           : ["Photon_eta"     , [12,-2.88,2.88], True],
             "Jet_size"             : ["Jet_size"       , [16,-0.5,15.5], True],
             "Jet_b_size"           : ["Jet_b_size"     , [10,-0.5,9.5], True],
             "Reco_mass_lgamma"     : ["Reco_mass_lgamma", [2000,-50,1950], True],
             "Reco_st"              : ["Reco_st"        , [9000,-50,8950], True],
             #"Reco_ht"              : ["Reco_ht"        , [9000,-50,8950], True],
             #"Reco_mass_T"          : ["Reco_mass_T", [3000,-50,5950], True]
             }
    return hDictTemp
    #return hDict 

allHistList = GetHistogramInfo().keys()
allHistList2D = [
["Reco_mass_T"    , "Reco_chi2"],
["Reco_mass_t_had", "Reco_chi2"],
["Reco_mass_t_lep", "Reco_chi2"],
["Reco_mass_T_had", "Reco_chi2"],
["Reco_mass_T_lep", "Reco_chi2"],
["Reco_mass_t_had", "Reco_mass_t_lep"],
["Reco_mass_T_had", "Reco_mass_T_lep"],
]
