#key is the histName in the ntuple, 
#value[0] is the title of x-axis
#value[1] is the number of bins, x-range
#value[2] decide if it is to be drawn for MC or data or both. Default value is for both.
def GetHistogramInfo():
    hDictTemp = {
             #"Muon_pt"              : ["Muon_pt"     , [30,0,1650], True],
             #"Muon_eta"             : ["Muon_eta"    , [12,-2.88,2.88], True],
             #"Electron_pt"          : ["Electron_pt"    , [30,0,1500], True],
             #"Electron_eta_sc"      : ["Electron_eta_sc" , [12,-2.88,2.88], True],
             ##"Jet_pt"               : ["Jet_pt"    , [30,-20,1480], True],
             #"Jet_eta"             : ["Jet_eta"    , [12,-2.88,2.88], True],
             #"Reco_met"             : ["Reco_met"      , [30,-20,1180], True],
             #"Reco_mass_lgamma"     : ["Reco_mass_lgamma", [30,0,300], True],
             #"Jet_size"             : ["Jet_size"     , [16,-0.5,15.5], True],
             #"Jet_b_size"           : ["Jet_b_size"     , [10,-0.5,9.5], True],
             #"Reco_ht"              : ["Reco_ht"        , [300,0,9000], True],
             "Reco_st"              : ["Reco_st"        , [300,0,9000], True],
             #"Photon_et"             : ["Photon_et"    , [100,0,2000], True],
             #"Reco_mass_T"          : ["Reco_mass_T", [300,0,6000], True]
             }
    return hDictTemp
allHistList = GetHistogramInfo().keys()

hForEffs = {} 
hForEffs["forMuEff"]       = ["hAll_MuTrig", "hPass_MuTrig", "hPass_MuTrigFlow"]
hForEffs["forEleEff"]      = ["hAll_EleTrig", "hPass_EleTrig", "hPass_EleTrigFlow"]
