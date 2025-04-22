#include "../interface/Selector.h"
#include <TLorentzVector.h>
#include <iostream>
#include <iomanip>
#include <cmath>
#include<stdexcept>  // For std::runtime_error

// Put the TRandom3 generator in an anonymous namespace as a local static instance.
namespace {
    TRandom3 generator(0);
}

Selector::Selector() {
    year = "2016";
    printEvent = -1;

    looseJetId   = false;
    systVariation = "nom"; 
    // https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
    btagCut = 0.8484;
    topTagWp = 0.74;

    qcdSelect = false;
    skipAk4Ak8Dr = false;

    smearJetPt = true;
    smearPho   = true;
    smearEle   = true;
    scaleEle   = true;
    scalePho   = true;
    isSignal   = false;
    isQCD      = false;
    sampForTopPt = false; // default if not set externally
}

Selector::~Selector() {
    // No dynamic memory owned by this class to delete.
}

void Selector::initJER(cRef jerRefSF, cRef jerRefSF8, cRef jerRefReso, cRef jerRefReso8) {
    jerRefSf_    = jerRefSF;
    jerRefSf8_   = jerRefSF8;
    jerRefReso_  = jerRefReso;
    jerRefReso8_ = jerRefReso8;
}

void Selector::processObjects(EventTree* inpTree) {
    if (!inpTree) {
        std::cerr << "Error in Selector::processObjects: Null event tree pointer!" << std::endl;
        return;
    }
    tree = inpTree;
    clearVectors();

    // Use a seed based on the event number, run number, and luminosity block.
    generator.SetSeed(tree->event_ + tree->run_ + tree->lumis_);

    filterMuons();
    filterElectrons();
    filterPhotons();
    filterFatJets();
    filterJets();
}

void Selector::clearVectors() {
    muons.clear();
    muonsLoose.clear();

    electrons.clear();
    electronsLoose.clear();

    photons.clear();
    phoPassChHadIso.clear();
    phoPassPhoIso.clear();
    phoPassSih.clear();
    loosePhotons.clear();
    photonsNoId.clear();

    phoChHadIsoCorr.clear();
    phoNeuHadIsoCorr.clear();
    phoPhoIsoCorr.clear();
    phoRandConeChHadIsoCorr.clear();

    jets.clear();
    bJets.clear();
    fatJets.clear();
    jetResolution.clear();
    jetSmear.clear();
    jetIsTagged.clear();

    dRPhoMu.clear();
    dRPhoEle.clear();
    dRJetMu.clear();
    dRJetEle.clear();
    dRJetPho.clear();
    dRJetAK8.clear();
}

void Selector::filterMuons() {
    if (tree->event_ == printEvent) {
        std::cout << "Found Event, Starting Muons" << std::endl;
        std::cout << " nMu = " << tree->nMuon_ << std::endl;
    }
    for (UInt_t m = 0; m < tree->nMuon_; ++m) {
        double eta = tree->muEta_[m];
        double pt  = tree->muPt_[m];
        // Loose muon selection
        bool looseMuonID = tree->muIsPFMuon_[m] && (tree->muIsTracker_[m] || tree->muIsGlobal_[m]);
        bool passLoose   = (pt >= 15.0 &&
                            std::abs(eta) <= 2.4 &&
                            looseMuonID &&
                            (int)tree->muTkIsoId_[m] == 1);

        // Prompt (medium) muon selection for pt > 30 GeV
        bool passPrompt = false;
        if (pt > 30.0) {
            passPrompt = (std::abs(eta) <= 2.4 &&
                          (int)tree->muTkIsoId_[m] == 2 && // 2 for tight (medium)
                          tree->muHighPurity_[m] &&
                          (int)tree->muHighPtId_[m] == 2 &&
                          tree->muDxy_[m] < 0.2 &&
                          tree->muDz_[m] < 0.5);
        }
        if (passPrompt)
            muons.push_back(m);
        else if (passLoose)
            muonsLoose.push_back(m);

        if (tree->event_ == printEvent) {
            std::cout << "-- Muon " << m
                      << " passPrompt = " << passPrompt
                      << " passLoose = "  << passLoose
                      << " pt = "         << pt
                      << " eta = "        << eta
                      << " looseID = "    << looseMuonID
                      << std::endl;
        }
    }
}

void Selector::filterElectrons() {
    if (tree->event_ == printEvent) {
        std::cout << "Found Event, Starting Electrons" << std::endl;
        std::cout << " nEle = " << tree->nEle_ << std::endl;
    }
    for (int eleInd = 0; eleInd < tree->nEle_; ++eleInd) {
        double eta     = tree->eleEta_[eleInd];
        double absEta  = std::abs(eta);
        double scEta   = eta + tree->eleDeltaEtaSC_[eleInd];
        double absScEta= std::abs(scEta);
        double pt      = tree->elePt_[eleInd];

        // Avoid the EB-EE gap.
        bool passEtaEBEEGap = (absScEta < 1.4442) || (absScEta > 1.566);

        // Medium electron IDs
        bool passVetoID  = tree->eleMVAFall17V2Iso_WPL_[eleInd];
        bool passTightID = tree->eleMVAFall17V2Iso_WP80_[eleInd];

        bool eleSel   = (passEtaEBEEGap &&
                         absEta <= 2.4 &&
                         pt >= 40.0 &&
                         passTightID);
        bool looseSel = (passEtaEBEEGap &&
                         absEta <= 2.4 &&
                         pt >= 30.0 &&
                         passVetoID &&
                         !eleSel);
        if (eleSel)
            electrons.push_back(eleInd);
        else if (looseSel)
            electronsLoose.push_back(eleInd);

        if (tree->event_ == printEvent) {
            std::cout << "-- Electron " << eleInd 
                      << " eleSel = "   << eleSel 
                      << " looseSel = " << looseSel 
                      << " pt = "       << pt 
                      << " eta = "      << eta 
                      << " phi = "      << tree->elePhi_[eleInd]
                      << " tightID = "  << passTightID 
                      << " vetoID = "   << passVetoID 
                      << std::endl;
        }
    }
}

void Selector::filterPhotons() {
    if (tree->event_ == printEvent) {
        std::cout << "Found Event, Starting Photons" << std::endl;
        std::cout << " nPho = " << tree->nPho_ << std::endl;
    }
    for (int phoInd = 0; phoInd < tree->nPho_; ++phoInd) {
        double et   = tree->phoEt_[phoInd];
        double eta  = tree->phoEta_[phoInd];
        double absEta = std::abs(eta);
        double phi  = tree->phoPhi_[phoInd];
        bool passDrLepPho = true;

        // Check dR between photon and selected electrons.
        for (const auto& eleInd : electrons) {
            double dRVal = dR(eta, phi, tree->eleEta_[eleInd], tree->elePhi_[eleInd]);
            dRPhoEle.push_back(dRVal);
            if (dRVal < 0.4)
                passDrLepPho = false;
        }
        // Check dR between photon and selected muons.
        for (const auto& muInd : muons) {
            double dRVal = dR(eta, phi, tree->muEta_[muInd], tree->muPhi_[muInd]);
            dRPhoMu.push_back(dRVal);
            if (dRVal < 0.4)
                passDrLepPho = false;
        }
        bool passPhoId    = tree->phoMVAId_WP80_[phoInd]; // tight photon ID
        bool hasPixelSeed = tree->phoPixelSeed_[phoInd];
        bool phoEleVeto   = tree->phoEleVeto_[phoInd];
        bool phoPresel    = (et >= 20.0 &&
                             absEta <= 1.4442 &&
                             !hasPixelSeed &&
                             phoEleVeto &&
                             passDrLepPho);
        // Parse additional cut bits (using a helper function from Utils).
        std::vector<bool> cutBasedID_split = parsePhotonVIDCuts(tree->phoVidWPBitmap_[phoInd], 2);
        bool passMediumIDNoChIsoOrSIEIE = cutBasedID_split[1] &&
                                          cutBasedID_split[4] &&
                                          cutBasedID_split[5];
        if (phoPresel && passPhoId)
            photons.push_back(phoInd);
        if (phoPresel && passMediumIDNoChIsoOrSIEIE)
            loosePhotons.push_back(phoInd);

        if (tree->event_ == printEvent) {
            std::cout << "-- Photon " << phoInd 
                      << " pt = " << et 
                      << " eta = " << eta 
                      << " phi = " << phi 
                      << " presel = " << phoPresel 
                      << " drLep = " << passDrLepPho 
                      << " medID = " << passPhoId 
                      << std::endl;
        }
    }
}

void Selector::filterJets() {
    if (tree->event_ == printEvent) {
        std::cout << "Found Event, Starting Jets" << std::endl;
        std::cout << " nJet = " << tree->nJet_ << std::endl;
    }
    // For some QCD events, nJet can be very high.
    if (tree->nJet_ < 200) {
        for (int jetInd = 0; jetInd < tree->nJet_; ++jetInd) {
            double pt  = tree->jetPt_[jetInd];
            double eta = tree->jetEta_[jetInd];
            double phi = tree->jetPhi_[jetInd];

            // Jet ID: require tight lepton veto ID (>=6) and (pileup ID >=1 or pt>=50).
            bool jetIdPass = (tree->jetID_[jetInd] >= 6 && (tree->puID_[jetInd] >= 1 || pt >= 50.0));

            double resolution = 0.0;
            double jetSmearFactor = 1.0;
            if (!tree->isData_) {
                double jetSF = 1.0;
                resolution = jerRefReso_->evaluate({tree->jetEta_[jetInd], tree->jetPt_[jetInd], tree->rho_});
                //std::cout<<"SystVariation : "<< systVariation <<std::endl;
                try{
                jetSF = jerRefSf_->evaluate({tree->jetEta_[jetInd], systVariation});}
                catch (const std::exception &e) {
                std::cerr << "\nEXCEPTION: in jerRefSf->evaluate(): " << e.what() << '\n';
                throw std::runtime_error("Failed to get jetSF");
                 }
                int genIdx = tree->jetGenJetIdx_[jetInd];
                bool isMatch = false;
                if ((genIdx > -1) && (genIdx < tree->nGenJet_)) {
                    double delR = dR(eta, phi, tree->GenJet_eta_[genIdx], tree->GenJet_phi_[genIdx]);
                    if (delR < 0.2 && std::abs(pt - tree->GenJet_pt_[genIdx]) < 3 * resolution * pt) {
                        isMatch = true;
                    }
                }
                if (isMatch) { // scaling method
                    jetSmearFactor = std::max(0.0, 1.0 + (jetSF - 1.0) * (pt - tree->GenJet_pt_[genIdx]) / pt);
                } else { // stochastic smearing
                    jetSmearFactor = std::max(0.0, 1.0 + generator.Gaus(0, resolution) *
                                                std::sqrt(std::max(jetSF * jetSF - 1.0, 0.0)));
                }
                if (tree->event_ == printEvent) {
                    std::cout << "------------------------" << std::endl;
                    std::cout << "  JetInd: " << jetInd << std::endl;
                    std::cout << "  DoJetSmear: " << smearJetPt << std::endl;
                    std::cout << "  GenIdx: " << genIdx << std::endl;
                    std::cout << "  jetEta: " << tree->jetEta_[jetInd] << std::endl;
                    std::cout << "  jetSF: "  << jetSF << std::endl;
                    std::cout << "  JetSmear: " << jetSmearFactor << std::endl;
                    std::cout<<"SystVariation : "<< systVariation <<std::endl; 
                }
                if (smearJetPt) {
                    pt = pt * jetSmearFactor;
                    tree->jetPt_[jetInd] = pt;
                }
            }

            // Check for overlap with selected leptons and photons.
            bool passDrLepJet = true;
            for (const auto& eleInd : electrons) {
                double dRVal = dR(eta, phi, tree->eleEta_[eleInd], tree->elePhi_[eleInd]);
                dRJetEle.push_back(dRVal);
                if (dRVal < 0.4)
                    passDrLepJet = false;
            }
            for (const auto& muInd : muons) {
                double dRVal = dR(eta, phi, tree->muEta_[muInd], tree->muPhi_[muInd]);
                dRJetMu.push_back(dRVal);
                if (dRVal < 0.4)
                    passDrLepJet = false;
            }
            bool passDrPhoJet = true;
            for (const auto& phoInd : photons) {
                double dRVal = dR(eta, phi, tree->phoEta_[phoInd], tree->phoPhi_[phoInd]);
                dRJetPho.push_back(dRVal);
                if (dRVal < 0.4)
                    passDrPhoJet = false;
            }
            bool passDrAk8 = true;
            if (!skipAk4Ak8Dr) {
                for (const auto& fatJetInd : fatJets) {
                    double dRVal = dR(eta, phi, tree->fatJetEta_[fatJetInd], tree->fatJetPhi_[fatJetInd]);
                    dRJetAK8.push_back(dRVal);
                    if (dRVal < 1.6)
                        passDrAk8 = false;
                }
            }
            bool jetPresel = (pt >= 30.0 &&
                              std::abs(eta) <= 2.4 &&
                              jetIdPass &&
                              passDrLepJet &&
                              passDrPhoJet &&
                              passDrAk8);
            if (jetPresel) {
                jets.push_back(jetInd);
                jetResolution.push_back(resolution);
                jetSmear.push_back(jetSmearFactor);
                if (tree->jetBtagDeepB_[jetInd] > btagCut) {
                    bJets.push_back(jetInd);
                    jetIsTagged.push_back(true);
                } else {
                    jetIsTagged.push_back(false);
                }
            }
            if (tree->event_ == printEvent) {
                std::cout << " jet pt = "  << pt
                          << " eta = "     << eta
                          << " phi = "     << phi
                          << " jetID = "   << jetIdPass
                          << " presel = "  << jetPresel
                          << " btag = "    << (tree->jetBtagDeepB_[jetInd] > btagCut)
                          << std::endl;
            }
        }
    }
}

void Selector::filterFatJets() {
    if (tree->event_ == printEvent) {
        std::cout << std::endl;
        std::cout << "Found Event, Starting Fat Jets" << std::endl;
        std::cout << " nFatJet = " << tree->nFatJet_ << std::endl;
    }
    for (int jetInd = 0; jetInd < tree->nFatJet_; ++jetInd) {
        double pt  = tree->fatJetPt_[jetInd];
        double eta = tree->fatJetEta_[jetInd];
        double phi = tree->fatJetPhi_[jetInd];
        int id     = tree->fatJetID_[jetInd];
        float mSD  = tree->fatJetMassSoftDrop_[jetInd];
        // For example, using ParticleNet score for top tagging.
        float tVsQCD = tree->fatJetPNET_[jetInd];
        bool isId = (id >= 1);
        double resolution = 0.0;
        if (!tree->isData_) {
            double jetSF = 1.0;
            jetSF = jerRefSf_->evaluate({tree->fatJetEta_[jetInd], systVariation});
            resolution = jerRefReso_->evaluate({tree->fatJetEta_[jetInd], tree->fatJetPt_[jetInd], tree->rho_});
            double jetSmearFactor = 1.0;
            int genIdx = tree->fatJetGenJetAK8Idx_[jetInd];
            bool isMatch = false;
            if ((genIdx > -1) && (genIdx < tree->nGenJetAK8_)) {
                double delR = dR(eta, phi, tree->GenJetAK8_eta_[genIdx], tree->GenJetAK8_phi_[genIdx]);
                if (delR < 0.2 && std::abs(pt - tree->GenJetAK8_pt_[genIdx]) < 3 * resolution * pt) {
                    isMatch = true;
                }
            }
            if (isMatch) { // scaling method
                jetSmearFactor = std::max(0.0, 1.0 + (jetSF - 1.0) * (pt - tree->GenJetAK8_pt_[genIdx]) / pt);
            } else { // stochastic smearing
                jetSmearFactor = std::max(0.0, 1.0 + generator.Gaus(0, resolution) *
                                              std::sqrt(std::max(jetSF * jetSF - 1.0, 0.0)));
            }
            if (tree->event_ == printEvent) {
                std::cout << "  DoJetSmear: " << smearJetPt << std::endl;
                std::cout << "  GenIdx: " << genIdx << std::endl;
                std::cout << "  jetSF: "  << jetSF << std::endl;
                std::cout << "  JetSmear: " << jetSmearFactor << std::endl;
            }
            if (smearJetPt) {
                pt = pt * jetSmearFactor;
                tree->fatJetPt_[jetInd] = pt;
            }
        }
        bool passDrLepJet = true;
        for (const auto& eleInd : electrons) {
            if (dR(eta, phi, tree->eleEta_[eleInd], tree->elePhi_[eleInd]) < 0.8)
                passDrLepJet = false;
        }
        for (const auto& muInd : muons) {
            if (dR(eta, phi, tree->muEta_[muInd], tree->muPhi_[muInd]) < 0.8)
                passDrLepJet = false;
        }
        bool passDrPhoJet = true;
        for (const auto& phoInd : photons) {
            if (dR(eta, phi, tree->phoEta_[phoInd], tree->phoPhi_[phoInd]) < 0.8)
                passDrPhoJet = false;
        }
        bool jetPresel = (pt >= 350.0 &&
                          std::abs(eta) <= 2.4 &&
                          mSD >= 105.0 && mSD <= 210.0 &&
                          tVsQCD >= topTagWp &&
                          passDrLepJet &&
                          passDrPhoJet &&
                          isId);
        if (jetPresel)
            fatJets.push_back(jetInd);
        if (tree->event_ == printEvent) {
            std::cout << "   -----" << std::endl;
            std::cout << "   presel = " << jetPresel << std::endl;
            std::cout << "     pt >= 350: " << (pt >= 350.0) << ", pt = " << pt << std::endl;
            std::cout << "     |eta| <= 2.4: " << (std::abs(eta) <= 2.4) << ", eta = " << eta << std::endl;
            std::cout << "     fatJetID: " << isId << std::endl;
            std::cout << "     mass SD in [105,210]: " << ((mSD >= 105.0 && mSD <= 210.0)) << ", mSD = " << mSD << std::endl;
            std::cout << "     TvsQCD >= topTagWp: " << (tVsQCD >= topTagWp) << ", TvsQCD = " << tVsQCD << std::endl;
            std::cout << "      dRLep = " << passDrLepJet << std::endl;
            std::cout << "      dRPho = " << passDrPhoJet << std::endl;
        }
    }
}

