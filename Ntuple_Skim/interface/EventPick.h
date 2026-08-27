#ifndef EVENTPICK_H
#define EVENTPICK_H

#include <vector>
#include <array>
#include <string>
#include <set>
#include <iostream>
#include <fstream>
#include <TH1F.h>
#include <TH1D.h>
#include <cmath>  // for std::abs

#include "EventTree.h"
#include "Selector.h"

class EventPick {
public:
    /// \brief Constructor taking the event pick title.
    explicit EventPick(const std::string& titleIn);
    ~EventPick() = default;  // no special cleanup needed

    /// \brief Process an event using the given tree and selector.
    void processEvent(EventTree* tree, Selector* selector);

    // Basic event info (modifiable as needed)
    std::string title;
    std::string year{"2016"};

    /// If tree->event_ equals printEvent, detailed information is printed.
    int printEvent{-1};

    // Selection cut parameters (modify these to change the event selection)
    double metCut{20.0};
    int nLepEq{1};
    int nJetGe{3};
    int nBJetGe{1};
    int nMuEq{1};
    int nEleEq{1};
    int nPhoEq{1};

    int nLooseMuVetoLe{0};
    int nLooseEleVetoLe{0};

    // Flags indicating if the event passed the muon or electron pre-selection
    bool passPreselMu{false};
    bool passPreselEle{false};

    // Per-event cumulative selection decisions used by the ntuple cutflow.
    // Stages: trigger+PV, tight lepton (including dilepton charge/Z cuts),
    // loose-lepton veto, and MET.
    std::array<bool, 4> cutFlowMu{{false, false, false, false}};
    std::array<bool, 4> cutFlowEle{{false, false, false, false}};

private:
    // (Optionally, you could store pointers to tree/selector here if needed.)
};

#endif // EVENTPICK_H
