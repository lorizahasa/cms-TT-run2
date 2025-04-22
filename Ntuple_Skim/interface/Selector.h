#ifndef SELECTOR_H
#define SELECTOR_H

#include <vector>
#include <iostream>
#include <iomanip>
#include <algorithm>
#include <string>
#include <TH1F.h>
#include <TMath.h>
#include <TLorentzVector.h>
#include "EventTree.h"
#include "Utils.h"
#include "TRandom3.h"
#include <bitset>
#include <random>

#include "correction.h"
typedef correction::Correction::Ref cRef;

// Global constants for photon ID and effective areas (not changed here)
const int    photonID_IsConv[2][3]                = { {0, 0, 0} ,             {0, 0, 0}             };
const double photonID_HoverE[2][3]                = { {0.05, 0.05, 0.05} ,    {0.05, 0.05, 0.05}    };
const double photonID_SigmaIEtaIEta[2][3]         = { {0.012, 0.011, 0.011} , {0.034, 0.033, 0.031} };
const double photonID_RhoCorrR03ChHadIso[2][3]    = { {2.6, 1.5, 0.7} ,       {2.3, 1.2, 0.5}       };
const double photonID_RhoCorrR03NeuHadIso_0[2][3] = { {3.5, 1.0, 0.4} ,       {2.9, 1.5, 1.5}       };
const double photonID_RhoCorrR03NeuHadIso_1[2][3] = { {0.04, 0.04, 0.04} ,    {0.04, 0.04, 0.04}    };
const double photonID_RhoCorrR03PhoIso_0[2][3]    = { {1.3, 0.7, 0.5} ,       {999, 1.0, 1.0}       };
const double photonID_RhoCorrR03PhoIso_1[2][3]    = { {0.005, 0.005, 0.005} , {0.005, 0.005, 0.005} };

// Effective areas for photon rho correction
// First index is the egammaRegion, second is whether it is ChHad, NeuHad, or Pho 
// (chhadEA, nhadEA, photEA)
// See: https://indico.cern.ch/event/491548/contributions/2384977/attachments/1377936/2117789/CutBasedPhotonID_25-11-2016.pdf
static const double photonEA[7][3] = {
    {0.0360, 0.0597, 0.1210},
    {0.0377, 0.0807, 0.1107},
    {0.0306, 0.0629, 0.0699},
    {0.0283, 0.0197, 0.1056},
    {0.0254, 0.0184, 0.1457},
    {0.0217, 0.0284, 0.1719},
    {0.0167, 0.0591, 0.1998}
};

class Selector {
public:
    Selector();
    ~Selector();

    /// Process objects from the given event tree.
    void processObjects(EventTree* inpTree);

    // Selected physics objects (indices into the EventTree arrays)
    std::vector<int> muons;
    std::vector<int> muonsLoose;

    std::vector<int> electrons;
    std::vector<int> electronsLoose;

    std::vector<int> photons;
    std::vector<bool> phoPassChHadIso;
    std::vector<bool> phoPassPhoIso;
    std::vector<bool> phoPassSih;
    std::vector<int> loosePhotons;
    std::vector<int> photonsNoId;
    std::vector<double> phoChHadIsoCorr;
    std::vector<double> phoNeuHadIsoCorr;
    std::vector<double> phoPhoIsoCorr;
    std::vector<std::vector<float>> phoRandConeChHadIsoCorr;

    std::vector<int> jets;
    std::vector<int> bJets;
    std::vector<int> fatJets;
    std::vector<double> jetResolution;
    std::vector<double> jetSmear;
    std::vector<bool> jetIsTagged;

    std::vector<double> dRPhoMu;
    std::vector<double> dRPhoEle;
    std::vector<double> dRJetMu;
    std::vector<double> dRJetEle;
    std::vector<double> dRJetPho;
    std::vector<double> dRJetAK8;

    // Configuration parameters
    double btagCut;
    double topTagWp;
    std::string systVariation;
    bool smearJetPt;
    bool scaleEle;
    bool smearEle;
    bool scalePho;
    bool smearPho;
    bool looseJetId;
    bool qcdSelect;
    bool isSignal;
    bool isQCD;
    bool sampForTopPt;
    bool skipAk4Ak8Dr;

    std::string year;
    int printEvent;

    /// Clear all object vectors (to be called at the start of each event).
    void clearVectors();

    /// Initialize the jet energy resolution (JER) corrections.
    void initJER(cRef jerRefSF, cRef jerRefSF8, cRef jerRefReso, cRef jerRefReso8);

private:
    // Pointer to the event tree (set in processObjects)
    EventTree* tree;

    // Object filters
    void filterPhotons();
    void filterElectrons();
    void filterMuons();
    void filterJets();
    void filterFatJets();

    // Effective area functions (for electrons, muons, and photons)
    double eleEffArea03(double scEta);
    double muEffArea04(double muEta);
    double phoEffArea03ChHad(double phoScEta);
    double phoEffArea03NeuHad(double phoScEta);
    double phoEffArea03Pho(double phoScEta);
    int getEgammaRegion(double absEta);

    bool passPhoMediumId(int phoInd, bool cutHoverE, bool cutSIEIE, bool cutIso);

    // JER correction references
    cRef jerRefSf_;
    cRef jerRefSf8_;
    cRef jerRefReso_;
    cRef jerRefReso8_;
};

#endif // SELECTOR_H

