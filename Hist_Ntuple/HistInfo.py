btagWeightCategory = ["1","(1-btagWeight[0])","(btagWeight[2])","(btagWeight[1])"]
def GetHistogramInfo(extraCuts="(passPresel_Mu && nJet>=4 && nBJet>=2)*", nBJets=1):

    histogramInfo = { 
                      "presel_Njet"                           : ["nJet"      , "presel_Njet"     ,        [16,-0.5,15.5], extraCuts      , "", True],
                      "presel_Nbjet"                          : ["nBJet"     , "presel_Nbjet"    ,        [10,0,10], extraCuts      , "", True],
                      "presel_muPt"                           : ["muPt"      , "presel_muPt"     ,      [100,0,1000], extraCuts      , "", True],
                      "presel_muEta"                          : ["muEta"     , "presel_muEta"    ,   [100,-2.4,2.4], extraCuts      , "", True],
                      "presel_muPhi"                          : ["muPhi"     , "presel_muPhi"    , [100,-3.15,3.15], extraCuts      , "", True],
                      "presel_elePt"                          : ["elePt"     , "presel_elePt"    ,      [100,0,1000], extraCuts      , "", True],
                      "presel_eleSCEta"                       : ["eleSCEta"  , "presel_eleSCEta" ,   [100,-2.4,2.4], extraCuts      , "", True],
                      "presel_elePhi"                         : ["elePhi"    , "presel_elePhi"   , [100,-3.15,3.15], extraCuts      , "", True],
                      "presel_M3"                             : ["M3"        , "presel_M3"       ,     [100,0,1000], extraCuts      , "", True],
                      "presel_MET"                            : ["pfMET"     , "presel_MET"      ,      [100,0,1000], extraCuts      , "", True],
                      "presel_nVtx"                           : ["nVtx"      , "presel_nVtx"     ,        [50,0,50], extraCuts      , "", True],
                      "presel_WtransMass"                     : ["WtransMass","presel_WtransMass",      [100,0,1000], extraCuts      , "", True],
                      "presel_HT"                             : ["HT"        ,"presel_HT"        ,   [150,0,1500], extraCuts      , "", True],
                      "presel_TopHad_mass"                    : ["TopHad_mass"        ,"presel_TopHad_mass"        ,   [150,0,1500], extraCuts      , "", True],
                      "presel_TopLep_mass"                    : ["TopLep_mass"        ,"presel_TopLep_mass"        ,   [150,0,1500], extraCuts      , "", True],
                      "presel_TopTop_mass"                    : ["TopTop_mass"        ,"presel_TopTop_mass"        ,   [150,0,1500], extraCuts      , "", True],
                      "presel_chi2"                           : ["chi2"        ,"presel_chi2"        ,   [100,0,100000], extraCuts      , "", True],
                      "presel_jetRes"                         : ["jetRes"        ,"presel_jetRes"        ,   [150,0,1.5], extraCuts      , "", True]
                      }
    return histogramInfo

allPlotList = [
"presel_Njet",      
"presel_Nbjet",     
"presel_muPt",      
"presel_muEta",     
"presel_muPhi",     
"presel_M3",        
"presel_MET",       
"presel_TopHad_mass",
"presel_TopTop_mass",
"presel_TopLep_mass",
"presel_chi2",
"presel_jetRes"]      

'''
allPlotList = [
"presel_Njet",      
"presel_Nbjet",     
"presel_muPt",      
"presel_muEta",     
"presel_muPhi",     
"presel_elePt",     
"presel_eleSCEta",  
"presel_elePhi",    
"presel_M3",        
"presel_MET",       
"presel_nVtx",      
"presel_WtransMass",
"presel_HT"]      
'''
