#ifndef SKIM_BRANCH_CONFIG_H
#define SKIM_BRANCH_CONFIG_H

#include <set>
#include <stdexcept>
#include <string>
#include <vector>

// Explicit production RDF branch contract. This list
// follows Ntuple_Skim/src/EventTree.cpp, including its systematic inputs.
// Skim-only controls remain for trigger/filter decisions and reproducibility.
namespace SkimBranchConfig {
inline void validateYear(const std::string& year) {
    if (year != "2016Pre" && year != "2016Post" && year != "2017" && year != "2018")
        throw std::invalid_argument("Unsupported skim era: " + year);
}

inline std::vector<std::string> payloadBranches(bool mc) {
    std::vector<std::string> result = {
        "PV_npvsGood", "run", "event",
        "luminosityBlock", "MET_pt", "MET_phi",
        "nElectron", "Electron_charge", "Electron_pt",
        "Electron_deltaEtaSC", "Electron_eta", "Electron_phi",
        "Electron_mass", "Electron_cutBased", "Electron_miniPFRelIso_all",
        "Electron_mvaFall17V2Iso_WP80", "Electron_mvaFall17V2Iso_WPL", "nMuon",
        "Muon_charge", "Muon_pt", "Muon_eta",
        "Muon_phi", "Muon_mass", "Muon_mediumId",
        "Muon_tightId", "Muon_highPtId", "Muon_highPurity",
        "Muon_tkIsoId", "Muon_pfRelIso04_all", "Muon_tkRelIso",
        "Muon_isPFcand", "Muon_isGlobal", "Muon_isTracker",
        "Muon_dxy", "Muon_dz", "nJet",
        "Jet_pt", "Jet_qgl", "Jet_rawFactor",
        "Jet_eta", "Jet_phi", "Jet_mass",
        "Jet_jetId", "Jet_puId", "Jet_area",
        "Jet_muEF", "Jet_btagDeepB", "Jet_btagDeepFlavB",
        "nFatJet", "FatJet_pt", "FatJet_eta",
        "FatJet_phi", "FatJet_area", "FatJet_mass",
        "FatJet_msoftdrop", "FatJet_jetId", "FatJet_deepTagMD_TvsQCD",
        "FatJet_deepTag_TvsQCD", "FatJet_particleNet_TvsQCD", "nPhoton",
        "Photon_pt", "Photon_eta", "Photon_phi",
        "Photon_cutBased", "Photon_pfRelIso03_all", "Photon_pfRelIso03_chg",
        "Photon_vidNestedWPBitmap", "Photon_pixelSeed", "Photon_electronVeto",
        "Photon_mvaID_WP80", "fixedGridRhoFastjetAll"
    };
    // Retain both b-tag scores until the downstream DeepB/DeepJet mismatch is
    // resolved; branch cleanup must not silently change the tagging algorithm.
    if (mc) {
        const std::vector<std::string> extra = {
        "Pileup_nPU", "Pileup_nTrueInt", "Generator_weight",
        "nLHEScaleWeight", "LHEScaleWeight", "nLHEPdfWeight",
        "LHEPdfWeight", "PSWeight", "nPSWeight",
        "Jet_hadronFlavour", "Jet_genJetIdx", "FatJet_genJetAK8Idx",
        "FatJet_hadronFlavour", "Photon_genPartIdx", "nLHEPart",
        "LHEPart_pt", "LHEPart_pdgId", "nGenPart",
        "GenPart_pt", "GenPart_eta", "GenPart_phi",
        "GenPart_mass", "GenPart_genPartIdxMother", "GenPart_pdgId",
        "GenPart_status", "GenPart_statusFlags", "nGenJet",
        "GenJet_pt", "GenJet_eta", "GenJet_phi",
        "GenJet_mass", "nGenJetAK8", "GenJetAK8_pt",
        "GenJetAK8_eta", "GenJetAK8_phi", "GenJetAK8_mass",
        "L1PreFiringWeight_Dn", "L1PreFiringWeight_Nom", "L1PreFiringWeight_Up"
        };
        result.insert(result.end(), extra.begin(), extra.end());
    }
    return result;
}

inline std::vector<std::string> selectionBranches(const std::string& year) {
    validateYear(year);
    std::vector<std::string> result = {
        "nTrigObj",
        "Flag_goodVertices", "Flag_globalSuperTightHalo2016Filter",
        "Flag_HBHENoiseFilter", "Flag_HBHENoiseIsoFilter",
        "Flag_EcalDeadCellTriggerPrimitiveFilter", "Flag_BadPFMuonFilter",
        "Flag_eeBadScFilter"
    };
    if (year == "2017" || year == "2018") result.push_back("Flag_ecalBadCalibFilter");
    return result;
}

inline std::vector<std::string> muonTriggers(const std::string& year) {
    validateYear(year);
    if (year == "2016Pre" || year == "2016Post")
        return {"HLT_Mu50", "HLT_TkMu50"};
    return {"HLT_Mu50", "HLT_TkMu100", "HLT_OldMu100"};
}

inline std::vector<std::string> electronTriggers(const std::string& year) {
    validateYear(year);
    if (year == "2016Pre" || year == "2016Post")
        return {"HLT_Ele27_WPTight_Gsf", "HLT_Ele115_CaloIdVT_GsfTrkIdT", "HLT_Photon175"};
    if (year == "2017")
        return {"HLT_Ele35_WPTight_Gsf", "HLT_Ele115_CaloIdVT_GsfTrkIdT", "HLT_Photon200"};
    return {"HLT_Ele32_WPTight_Gsf", "HLT_Ele115_CaloIdVT_GsfTrkIdT", "HLT_Photon200"};
}

inline std::vector<std::string> triggerBranches(const std::string& year) {
    auto result = muonTriggers(year);
    const auto electron = electronTriggers(year);
    result.insert(result.end(), electron.begin(), electron.end());
    return result;
}

inline std::vector<std::string> branches(bool mc, const std::string& year) {
    auto result = payloadBranches(mc);
    const auto controls = selectionBranches(year), triggers = triggerBranches(year);
    result.insert(result.end(), controls.begin(), controls.end());
    result.insert(result.end(), triggers.begin(), triggers.end());
    std::set<std::string> seen;
    std::vector<std::string> unique;
    for (const auto& name : result)
        if (seen.insert(name).second) unique.push_back(name);
    return unique;
}
} // namespace SkimBranchConfig
#endif
