
#key is the histName in the ntuple, 
#value[0] is the title of x-axis
#value[1] is the number of bins, x-range
#value[2] decide if it is to be drawn for MC or data or both. Default value is for both.
def GetHistogramInfo():
    hDict = {
             "Reco_mass_dilep"       : ["Reco_mass_dilep", [300,0,300], True],
             }
    return hDict

allHistList = GetHistogramInfo().keys()
