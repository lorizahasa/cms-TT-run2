#key is the histName in the ntuple, 
#value[0] is the title of x-axis
#value[1] is the number of bins, x-range
#value[2] decide if it is to be drawn for MC or data or both. Default value is for both.
def GetHistogramInfo():
    hDictTemp = {
             #"Muon_pt"              : ["Muon_pt"     , [30,0,1650], True],
             #"Electron_pt"          : ["Electron_pt"    , [30,0,1500], True],
             #"Jet_pt"               : ["Jet_pt"    , [30,-20,1480], True],
             #"Reco_met"             : ["Reco_met"      , [30,-20,1180], True],
             #"Photon_et"             : ["Photon_et"    , [100,0,2000], True],
             "Reco_st"               : ["Reco_st"        , [300,0,9000], True],
             }
    return hDictTemp
allHistList = GetHistogramInfo().keys()

hForEffs = {} 
hForEffs["forMuEff"]       = ["hAll_MuTrig", "hPass_MuTrig", "hPass_MuTrigFlow"]
hForEffs["forEleEff"]      = ["hAll_EleTrig", "hPass_EleTrig", "hPass_EleTrigFlow"]
hForEffs["forVeto"]        = ["hCount"]
