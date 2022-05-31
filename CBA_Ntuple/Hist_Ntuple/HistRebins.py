
import numpy as np

dictRebin = {}#first element in the list should be a float
muPt  = [-50.,54,80,100,120,140,160,190,230,280,350,450,1000,1950]
elePt = [-50.,49,80,100,120,140,160,190,230,280,350,450,1000,1950]
jetPt = [-50.,29,60,90,120,150,190,230,280,350,450,1000,1950]
metPt = [-50.,19,60,90,120,150,190,230,280,350,450,1000,1950]
phoPt = [-50.,19,40,60,80,100,120,150,190,230,280,350,450,1000,1950]
ST    = [-50.,200,500,700,900,1100,1300,1500,1700,1900,2200,2500,3000,5000,8950]
HT    = [-50.,200,500,700,900,1100,1300,1500,1700,1900,2200,2500,3000,5000,8950]
mTT   = [-50.,200,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1800,2500,5950]
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

#mly   = [-50.,-1,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350,360,370,380,390,440,500,800]
mly   = [-50.,-1,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,450,500,600,800]
dictRebin["Reco_mass_lgamma"]                = np.array(mly)
dictRebin["Reco_mass_lgamma_genuine"]        = np.array(mly)
dictRebin["Reco_mass_lgamma_misid_ele"]      = np.array(mly)
dictRebin["Reco_mass_lgamma_hadronic_photon"]= np.array(mly)
dictRebin["Reco_mass_lgamma_hadronic_fake"]  = np.array(mly)

