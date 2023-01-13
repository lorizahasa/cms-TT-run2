#ifndef SELECTOR_H
#define SELECTOR_H

#include<vector>
#include<iostream>
#include <iomanip>
#include<algorithm>
#include<TH1F.h>
#include<TMath.h>
#include<TLorentzVector.h>
#include"EventTree.h"
#include"ParsePhotonID.h"
#include"Utils.h"
#include"TRandom3.h"
#include<bitset>

#include"JetResolution.h"
#include"JetResolution.h"
#include"JetResolutionObject.h"

#include <random>


// https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedPhotonID2012
// photon ID is not going to be changed every time this code runs
// barrel/endcap, Loose/Medium/Tight
const int    photonID_IsConv[2][3]                = { {0, 0, 0} ,             {0, 0, 0}             };
const double photonID_HoverE[2][3]                = { {0.05, 0.05, 0.05} ,    {0.05, 0.05, 0.05}    };
const double photonID_SigmaIEtaIEta[2][3]         = { {0.012, 0.011, 0.011} , {0.034, 0.033, 0.031} };
const double photonID_RhoCorrR03ChHadIso[2][3]    = { {2.6, 1.5, 0.7} ,       {2.3, 1.2, 0.5}       };
const double photonID_RhoCorrR03NeuHadIso_0[2][3] = { {3.5, 1.0, 0.4} ,       {2.9, 1.5, 1.5}       };
const double photonID_RhoCorrR03NeuHadIso_1[2][3] = { {0.04, 0.04, 0.04} ,    {0.04, 0.04, 0.04}    };
const double photonID_RhoCorrR03PhoIso_0[2][3]    = { {1.3, 0.7, 0.5} ,       {999, 1.0, 1.0}       };
const double photonID_RhoCorrR03PhoIso_1[2][3]    = { {0.005, 0.005, 0.005} , {0.005, 0.005, 0.005} };

// Effective areas for photon rho correction
// First index is the egammaRegion (from above) second is whether it isChHad, NeuHad, or Pho 
///                                   chhadEA, nhadEA, photEA
///https://indico.cern.ch/event/491548/contributions/2384977/attachments/1377936/2117789/CutBasedPhotonID_25-11-2016.pdf
static const double photonEA[7][3] = {{0.0360, 0.0597, 0.1210},
									  {0.0377, 0.0807, 0.1107},
									  {0.0306, 0.0629, 0.0699},
									  {0.0283, 0.0197, 0.1056},
									  {0.0254, 0.0184, 0.1457},
									  {0.0217, 0.0284, 0.1719},
									  {0.0167, 0.0591, 0.1998}};
class Selector{
public:
	Selector();
	~Selector();
	void process_objects(EventTree* inp_tree);
	std::vector<int> Muons;
	std::vector<int> MuonsLoose;

	std::vector<int> Electrons;
	std::vector<int> ElectronsLoose;

	std::vector<int> Photons;
	std::vector<bool> PhoPassChHadIso;
	std::vector<bool> PhoPassPhoIso;
	std::vector<bool> PhoPassSih;
	std::vector<int> LoosePhotons;
	std::vector<int> PhotonsNoID;
	std::vector<double> PhoChHadIso_corr;
	std::vector<double> PhoNeuHadIso_corr;
	std::vector<double> PhoPhoIso_corr;
	std::vector<std::vector<float>> PhoRandConeChHadIso_corr;

	std::vector<int> Jets;
	std::vector<int> bJets;
    std::vector<int> FatJets;
	std::vector<double> jet_resolution;
	std::vector<double> jet_smear;
	std::vector<bool>   jet_isTagged;
	
	double btag_cut;
    double topTagWP;
	int JERsystLevel; //0= syst down, 1 = central, 2 = syst up
	int JECsystLevel;//0= syst down, 1 = central, 2 = syst up
	int phosmearLevel;
	int elesmearLevel;
	int phoscaleLevel;
	int elescaleLevel;
	bool   smearJetPt;
	bool scaleEle;
	bool smearEle;
	bool scalePho;
	bool smearPho;
	bool   looseJetID;
	bool   useDeepCSVbTag;
	bool   QCDselect;
    bool isSignal;
    bool isQCD;
    bool skipAK4AK8dr;

	std::string year;
	int printEvent;
	void clear_vectors();
	void init_JER(std::string inputPrefix);

private:
	EventTree* tree;
	void filter_photons();
	void filter_electrons();
	void filter_muons();
	void filter_jets();
    void filter_fatjets();
	// effective areas, see Selector.cpp for more information
	double eleEffArea03(double SCEta);
	double muEffArea04(double muEta);
	double phoEffArea03ChHad(double phoSCEta);
	double phoEffArea03NeuHad(double phoSCEta);
	double phoEffArea03Pho(double phoSCEta);
	int egammaRegion(double absEta);

	bool passPhoMediumID(int phoInd, bool cutHoverE, bool cutSIEIE, bool cutIso);
	JME::JetResolution *jetResolutionAK4;
	JME::JetResolutionScaleFactor *jetResolutionScaleFactorAK4;
	JME::JetResolution *jetResolutionAK8;
	JME::JetResolutionScaleFactor *jetResolutionScaleFactorAK8;
	JME::JetParameters jetParamAK4;
	JME::JetParameters jetParamAK8;

};
#endif
