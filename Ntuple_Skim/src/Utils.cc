#include "../interface/Utils.h"

double dR(double eta1, double phi1, double eta2, double phi2){
    double dphi = phi2 - phi1;
    double deta = eta2 - eta1;
    static const double pi = TMath::Pi();
    dphi = TMath::Abs( TMath::Abs(dphi) - pi ) - pi;
    return TMath::Sqrt( dphi*dphi + deta*deta );
}

bool checkStr(std::string sentence, std::string wordToFind){
    size_t pos = sentence.find(wordToFind);
    if (pos != std::string::npos) return true;
    else return false;
}

std::string getElementByIndex(const std::string& inputString, int index) {
    std::istringstream iss(inputString);
    std::string element;
    int elementCount = 0;
    while (std::getline(iss, element, '_')) {
        elementCount++;
        if (elementCount == index) {
            return element;
        }
    }
    // Return an empty string if the index is out of range
    return "";
}

std::vector<bool> parsePhotonVIDCuts(int bitMap, int cutLevel){
    //    *         | Int_t VID compressed bitmap (MinPtCut,PhoSCEtaMultiRangeCut,PhoSingleTowerHadOverEmCut,PhoFull5x5SigmaIEtaIEtaCut,PhoAnyPFIsoWithEACut,PhoAnyPFIsoWithEAAndQuadScalingCut,PhoAnyPFIsoWithEACut), 2 bits per cut*
    bool passHoverE  = (bitMap>>4&3)  >= cutLevel;
    bool passSIEIE   = (bitMap>>6&3)  >= cutLevel;
    bool passChIso   = (bitMap>>8&3)  >= cutLevel;
    bool passNeuIso  = (bitMap>>10&3) >= cutLevel;
    bool passPhoIso  = (bitMap>>12&3) >= cutLevel;
    bool passID = passHoverE && passSIEIE && passChIso && passNeuIso && passPhoIso;
    std::vector<bool> cuts;
    cuts.push_back(passID);
    cuts.push_back(passHoverE);
    cuts.push_back(passSIEIE);
    cuts.push_back(passChIso);
    cuts.push_back(passNeuIso);
    cuts.push_back(passPhoIso);
    return cuts;

}

