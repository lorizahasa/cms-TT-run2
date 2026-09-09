#include "../interface/EventPick.h"
#include <TLorentzVector.h>
#include <iostream>
#include <iomanip>

EventPick::EventPick(const std::string& titleIn)
    : title(titleIn)
{
    // Other members are already initialized in-class.
}

void EventPick::processEvent(EventTree* tree, Selector* selector) {
    // Check for valid pointers.
    if (!tree || !selector) {
        std::cerr << "Error: Null pointer passed to EventPick::processEvent." << std::endl;
        return;
    }

    // Initialize selection flags.
    passPreselMu  = true;
    passPreselEle = true;
    cutFlowMu.fill(false);
    cutFlowEle.fill(false);

    // Process physics objects (this fills the vectors in selector).
    selector->processObjects(tree);

    // Apply trigger and primary vertex cuts.
   // passPreselMu  = passPreselMu  && tree->passTrigMu_  && tree->nGoodVtx_;
   // passPreselEle = passPreselEle && tree->passTrigEle_ && tree->nGoodVtx_;
    // Select either the Table 9 or expanded skim trigger decision.
    const bool passMuTrigger = useTable9Triggers
        ? static_cast<bool>(tree->passTrigMuTable9_)
        : static_cast<bool>(tree->passTrigMu_);

    const bool passEleTrigger = useTable9Triggers
        ? static_cast<bool>(tree->passTrigEleTable9_)
        : static_cast<bool>(tree->passTrigEle_);

    passPreselMu = passPreselMu && passMuTrigger && tree->nGoodVtx_;
    passPreselEle = passPreselEle && passEleTrigger && tree->nGoodVtx_;
    cutFlowMu[0] = passPreselMu;
    cutFlowEle[0] = passPreselEle;

    // If neither channel passes these basic cuts, exit early.
    if (!passPreselMu && !passPreselEle) {
        return;
    }

    // Debug printing if this event matches the requested event number.
    if (tree->event_ == printEvent) {
        std::cout << "Muons     " << selector->muons.size() << "\n"
                  << "  Loose   " << selector->muonsLoose.size() << "\n"
                  << "Electrons " << selector->electrons.size() << "\n"
                  << "  Loose   " << selector->electronsLoose.size() << "\n"
                  << "Jets      " << selector->jets.size() << "\n"
                  << "BJets     " << selector->bJets.size() << "\n"
                  << "Photons   " << selector->photons.size() << "\n"
                  << "  Loose   " << selector->loosePhotons.size() << "\n"
                  << "-------------------" << std::endl;
    }

    // ----- Tight Muon Selection -----
    // Require exactly nMuEq tight muons.
    if (passPreselMu) {
        if (selector->muons.size() != static_cast<size_t>(nMuEq)) {
            passPreselMu = false;
        } else if (nMuEq == 2) {
            // For dilepton events, require opposite charge and that the invariant mass
            // is within 10 GeV of the Z boson mass (91.1876 GeV).
            int idxMu1 = selector->muons.at(0);
            int idxMu2 = selector->muons.at(1);
            if (tree->muCharge_[idxMu1] * tree->muCharge_[idxMu2] > 0) {
                passPreselMu = false;
            }
            TLorentzVector mu1, mu2;
            mu1.SetPtEtaPhiM(tree->muPt_[idxMu1],
                             tree->muEta_[idxMu1],
                             tree->muPhi_[idxMu1],
                             tree->muMass_[idxMu1]);
            mu2.SetPtEtaPhiM(tree->muPt_[idxMu2],
                             tree->muEta_[idxMu2],
                             tree->muPhi_[idxMu2],
                             tree->muMass_[idxMu2]);
            if (tree->event_ == printEvent) {
                std::cout << "DilepMass:    " << (mu1 + mu2).M() << "\n"
                          << "Lep 1 Charge: " << tree->muCharge_[idxMu1] << "\n"
                          << "Lep 2 Charge: " << tree->muCharge_[idxMu2] << "\n"
                          << "-------------------" << std::endl;
            }
            if (std::abs((mu1 + mu2).M() - 91.1876) > 10) {
                passPreselMu = false;
            }
        }
    }
    cutFlowMu[1] = passPreselMu;

    // Veto events that have extra loose muons or electrons (if applicable).
    if (passPreselMu) {
        if (selector->muonsLoose.size() > static_cast<size_t>(nLooseMuVetoLe) ||
            (selector->electronsLoose.size() + selector->electrons.size()) > static_cast<size_t>(nLooseEleVetoLe)) {
            passPreselMu = false;
        }
    }
    cutFlowMu[2] = passPreselMu;

    // ----- Tight Electron Selection -----
    // Require exactly nEleEq tight electrons.
    if (passPreselEle) {
        if (selector->electrons.size() != static_cast<size_t>(nEleEq)) {
            passPreselEle = false;
        } else if (nEleEq == 2) {
            int idxEle1 = selector->electrons.at(0);
            int idxEle2 = selector->electrons.at(1);
            if (tree->eleCharge_[idxEle1] * tree->eleCharge_[idxEle2] > 0) {
                passPreselEle = false;
            }
            TLorentzVector ele1, ele2;
            ele1.SetPtEtaPhiM(tree->elePt_[idxEle1],
                              tree->eleEta_[idxEle1],
                              tree->elePhi_[idxEle1],
                              tree->eleMass_[idxEle1]);
            ele2.SetPtEtaPhiM(tree->elePt_[idxEle2],
                              tree->eleEta_[idxEle2],
                              tree->elePhi_[idxEle2],
                              tree->eleMass_[idxEle2]);
            if (tree->event_ == printEvent) {
                std::cout << "DilepMass:    " << (ele1 + ele2).M() << "\n"
                          << "Lep 1 Charge: " << tree->eleCharge_[idxEle1] << "\n"
                          << "Lep 2 Charge: " << tree->eleCharge_[idxEle2] << "\n"
                          << "-------------------" << std::endl;
            }
            if (std::abs((ele1 + ele2).M() - 91.1876) > 10) {
                passPreselEle = false;
            }
        }
    }
    cutFlowEle[1] = passPreselEle;

    // Veto events that have extra loose electrons or muons.
    if (passPreselEle) {
        if (selector->electronsLoose.size() > static_cast<size_t>(nLooseEleVetoLe) ||
            (selector->muonsLoose.size() + selector->muons.size()) > static_cast<size_t>(nLooseMuVetoLe)) {
            passPreselEle = false;
        }
    }
    cutFlowEle[2] = passPreselEle;

    // ----- MET Cut -----
    if (passPreselMu && tree->MET_pt_ < metCut) {
        passPreselMu = false;
    }
    if (passPreselEle && tree->MET_pt_ < metCut) {
        passPreselEle = false;
    }
    cutFlowMu[3] = passPreselMu;
    cutFlowEle[3] = passPreselEle;
}
