import ROOT
f = ROOT.TFile.Open("root://cmseos.fnal.gov//store/user/lhasa/Output/cms-TT-run2/MVA_Ntuple/C/Disc_Ntuple/DiscMain/AdjustForMain/2016Pre__2016Post__2017__2018/Semilep/Spin32/Mu__Ele/CR/CombMass/BDTA/AllInc.root")
d = f.Get("SignalSpin32_M1000/ttyg_Enriched_CR_Resolved")
for k in d.GetListOfKeys():
    name = k.GetName()
    if name.startswith("JER_") or name.startswith("JEC_") or name.startswith("Weight_"):
        print(name)
