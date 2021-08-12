
#key is the histName in the ntuple, 
#value[0] is the title of x-axis
#value[1] is the number of bins, x-range
#value[2] decide if it is to be drawn for MC or data or both. Default value is for both.
def GetHistogramInfo():
    hDict = {
             "Reco_mass_lgamma"     : ["Reco_mass_lgamma", [300,0,300], True],
             #"Weight_pho"               : ["Weight_pho"             , [30,0.0,1.5], True],
             }
    return hDict

allHistList = GetHistogramInfo().keys()
