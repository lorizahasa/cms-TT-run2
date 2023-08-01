
import numpy as np

dictRebin = {}#first element in the list should be a float
muPt  = [-50.,54,80,100,120,140,160,190,230,280,350,450,1000,1950]
elePt = [-50.,49,80,100,120,140,160,190,230,280,350,450,1000,1950]
jetPt = [-50.,29,60,90,120,150,190,230,280,350,450,1000,1950]
metPt = [-50.,19,60,90,120,150,190,230,280,350,450,1000,1950]
phoPt = [-50.,19,40,60,80,100,120,150,190,230,280,350,450,1000,1950]
ST    = [-50.,200,500,700,900,1100,1300,1500,1700,1900,2200,2500,3000,5000,8950]
HT    = [-50.,200,500,700,900,1100,1300,1500,1700,1900,2200,2500,3000,5000,8950]
mTT   = [-50.,200,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1800,3600] #default
#mTT   = [-50.,200,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1800,2500,5950] #default
#mTT   = [-50.0, 291.0, 325.0, 352.0, 377.0, 402.0, 426.0, 452.0, 482.0, 517.0, 557.0, 605.0, 679.0, 828.0, 5949.0]#40%
mll   = [80.,82,84,86,88,90,92,94,96,98,100]

dictRebin["Muon_pt"]         = np.array(muPt)
dictRebin["Electron_pt"]     = np.array(elePt)
dictRebin["Jet_pt"]          = np.array(jetPt)
dictRebin["Reco_met"]        = np.array(metPt)
dictRebin["Photon_et"]       = np.array(phoPt)
dictRebin["Reco_st"]         = np.array(ST)
dictRebin["Reco_ht"]         = np.array(HT)
dictRebin["Reco_mass_T"]     = np.array(mTT)
dictRebin["Reco_mass_dilep"] = np.array(mll)

mly   = [-50.,-1,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,430,460,490,520,560,600,640,680,720,770,820,860,1000]
#mly    = [0.,20,40,60,80,100,120,140,160,180,200,220,240]
dictRebin["Reco_mass_lgamma"]                = np.array(mly)
dictRebin["Reco_mass_lgamma_genuine"]        = np.array(mly)
dictRebin["Reco_mass_lgamma_misid_ele"]      = np.array(mly)
dictRebin["Reco_mass_lgamma_hadronic_photon"]= np.array(mly)
dictRebin["Reco_mass_lgamma_hadronic_fake"]  = np.array(mly)

dictRebin["Reco_mass_trans_w"]                = np.array(mly)

#disc = [-1.01, -0.89, -0.87, -0.85, -0.81, -0.73, -0.63, -0.51, -0.39, -0.25, -0.07, 0.27, 0.99]
disc = [-1.0, -0.9, -0.88, -0.86, -0.82, -0.74, -0.64, -0.52, -0.4, -0.26, -0.08, 0.26, 0.98] #40%
#disc = [-1.,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
dictRebin["Disc"] = np.array(disc)
dictRebin["FatJet_pt"] = np.array(ST)
dictRebin["FatJet_msoftdrop"] = np.array(mly)

if __name__=='__main__':
    from ROOT import TFile
    inFile = TFile.Open("root://cmseos.fnal.gov//store/user/rverma/Output/cms-TT-run2/CBA_Ntuple/Hist_Ntuple/HistWeight/Merged/2018/Semilep/Mu/AllInc.root")
    #hist = inFile.Get("TTGamma/ttyg_Enriched_CR_Resolved/Base/Disc")
    hist = inFile.Get("TTGamma/tty_Enriched_le4j_a1b_e1y/Uncorr/Reco_st")
    #hist = inFile.Get("TTGamma/ttyg_Enriched_CR_Resolved/Base/Reco_mass_T")

    def getRebins(hist, uncThresh):
        bins = hist.GetNbinsX()
        content = 0.0
        reBins = []
        indexBins = []
        uncBins = []
        startBin = 1
        endBin   = bins
        reBins.append(hist.GetBinLowEdge(startBin))
        indexBins.append(startBin)
        for i in range(bins):
            evt = hist.GetBinContent(i)
            content = content + evt
            if content>0.0 and 100/(content)**0.5 < uncThresh:
                print(i, hist.GetBinLowEdge(i), content)
                reBins.append(round(hist.GetBinLowEdge(i), 2))
                uncBins.append(round(100/(content)**0.5, 2))
                indexBins.append(i)
                content = 0.0
        indexBins.append(endBin)
        reBins.append(hist.GetBinLowEdge(bins))
        uncBins.append(round(100/(content)**0.5, 2))
        print("Bin Center = \n", reBins)
        print("Bin Index  = \n",indexBins)
        print("Bin unc(%) = \n", uncBins)
        return reBins
    getRebins(hist, 10)
     


