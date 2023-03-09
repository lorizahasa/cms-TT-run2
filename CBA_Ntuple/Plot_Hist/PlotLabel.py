
labelDict = { 
         "Muon_pt"              : "p^{#mu}_{T}",
         "Muon_eta"             : "#eta^{#mu}",
         "Muon_phi"             : "#phi^{#mu}", 
         "Electron_pt"          : "p^{e}_{T}",
         "Electron_eta_sc"      : "#eta^{e}_{SC}",
         "Electron_phi"         : "#phi^{e}", 
         "Photon_et"            : "E^{#gamma}_{T}",  
         "Photon_size"          : "N^{#gamma}",
         "Jet_size"             : "N^{j}",
         "Jet_b_size"           : "N^{b}",
         "Jet_pt"               : "p^{j}_{T}",
         "Jet_eta"              : "#eta^{j}",
         "Reco_met"             : "E^{miss}_{T}",
         "Reco_mass_lgamma"     : "m_{l#gamma}",
         "Reco_mass_t_had"      : "m_{t}^{had}",
         "Reco_mass_t_lep"      : "m_{t}^{lep}",
         "Reco_ht"              : "H_{T}",
         "Reco_st"              : "S_{T}",
         "Reco_mass_T_had"      : "m_{t^{#times}}^{had}",
         "Reco_mass_T_lep"      : "m_{t^{#times}}^{lep}",
         "Reco_mass_T"          : "m_{t^{#times}}",
         "Reco_mass_TT"         : "m_{t^{#times}#bar{t^{#times}}}",
         "Reco_mass_TT_diff"    : "m_{t^{#times}} - m_{#bar{t^{#times}}}",
         "Reco_chi2"            : "#chi^{2}",
         "Reco_mass_dilep"      : "m_{l^{+}l^{-}}",

         "Jet_qgl_leading"      : "Disc_{QGL}^{j_{1}}", 
         "Jet_qgl_subleading"   : "Disc_{QGL}^{j_{2}}",
         "Reco_mass_trans_w"    : "m^{W}_{T}",
         "Jet_deep_b"               : "b_{disc}^{deep}",
         "Reco_angle_lepton_met"        : "ACos(l, E^{miss}_{T})", 
         "Reco_angle_leadJet_met"       : "ACos(j_{1}, E^{miss}_{T})",
         "Reco_angle_leadBjet_met"      : "ACos(b_{1}, E^{miss}_{T})",
         "Reco_dr_pho_tstarHad"                 : "#Delta R (#gamma, t^{#times}_{had})", 
         "Reco_dr_pho_tHad"                     : "#Delta R (#gamma, t_{had})", 
         "Reco_dr_pho_tstarLep"                 : "#Delta R (#gamma, t^{#times}_{lep})", 
         "Reco_dr_pho_tLep"                     : "#Delta R (#gamma, t_{lep})", 
         "Reco_dr_pho_gluon"                    : "#Delta R (#gamma, g)", 
         "Reco_dr_pho_bLep"                     : "#Delta R (#gamma, b_{lep})", 
         "Reco_dr_pho_lep"                      : "#Delta R (#gamma, l)", 
         "Reco_dr_pho_nu"                       : "#Delta R (g, E^{miss}_{T})", 
         "Reco_dr_gluon_tstarHad"               : "#Delta R (g, t^{#times}_{had})", 
         "Reco_dr_gluon_tHad"                   : "#Delta R (g, t_{had})", 
         "Reco_dr_gluon_tstarLep"               : "#Delta R (g, t^{#times}_{lep})", 
         "Reco_dr_gluon_tLep"                   : "#Delta R (g, t_{lep})", 
         "Reco_dr_tHad_tstarHad"                : "#Delta R (t_{had}, t^{#times}_{had})", 
         "Reco_dr_tLep_tstarLep"                : "#Delta R (t_{lep}, t^{#times}_{had})", 
         "Reco_dr_tstarHad_tstarLep"            : "#Delta R (t^{#times}_{had}, t^{#times}_{lep})", 
        
         "FatJet_size"             : "N^{#bf{t}}",
         "FatJet_pt"               : "p^{#bf{t}}_{T}",
         "FatJet_eta"              : "#eta^{#bf{t}}",
         "FatJet_mass"             : "m^{#bf{t}}",
         "FatJet_msoftdrop"        : "m^{sd}",
         "FatJet_btagDeepB"        : "btagDeepB^{#bf{t}}",
         "FatJet_deepTagMD_TvsQCD" : "deepTagMD_TvsQCD^{#bf{t}}",
         "FatJet_deepTagMD_WvsQCD" : "deepTagMD_WvsQCD^{#bf{t}}",
         "FatJet_deepTag_TvsQCD"   : "deepTag_TvsQCD^{#bf{t}}",
         "FatJet_deepTag_WvsQCD"   : "deepTag_WvsQCD^{#bf{t}}",
         }

def getXLabel(hName):
    label = hName
    try:
        label = labelDict[hName]
    except:
        "The %s does not have x-axis label"%hName
    print("%s = %s "%(hName, label))
    return label

def getYLabel(hName):
    label = "Events"
    if hName in ["Jet_pt", "Jet_eta", "Jet_phi"]:
        label = "Jets"
    return label

if __name__ == '__main__':
    getXLabel("Reco_st")
    import ROOT
    ROOT.gROOT.SetBatch(True)
    canvas = ROOT.TCanvas()
    canvas.cd()
    latex = ROOT.TLatex()

    name = list(labelDict.values())
    print(len(name))
    longstring = ' '.join(name[0:10])
    latex.DrawLatex(.05,.8,longstring)

    longstring = ' '.join(name[10:20])
    latex.DrawLatex(.02,.7,longstring)

    longstring = ' '.join(name[20:30])
    latex.DrawLatex(.02,.6,longstring)

    longstring = ' '.join(name[30:40])
    latex.DrawLatex(.02,.5,longstring)

    longstring = ' '.join(name[40:50])
    latex.DrawLatex(.02,.4,longstring)

    longstring = ' '.join(name[50:len(name)])
    latex.DrawLatex(.02,.3,longstring)
    canvas.SaveAs("a.pdf")
