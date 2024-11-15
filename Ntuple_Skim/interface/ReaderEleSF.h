#include<TH2F.h>
#include<TH1F.h>
#include<TFile.h>
#include <iostream>

using namespace std;
class ElectronSF
{
 public:
    ElectronSF(string id_fname, string reco_fname, string trig_fname){

	TFile* idFile = TFile::Open(id_fname.c_str(),"READ");
	idHist = (TH2F*) idFile->Get("EGamma_SF2D");

	TFile* recoFile = TFile::Open(reco_fname.c_str(),"READ");
	recoHist = (TH2F*) recoFile->Get("EGamma_SF2D");

	TFile* trigFile = TFile::Open(trig_fname.c_str(),"READ");
	//trigHist = (TH2F*) trigFile->Get("EGamma_SF2D");
    trigHistCentral_lowpt = (TH1F*) trigFile->Get("Central_eta_lowpt");
    trigHistUp_lowpt = (TH1F*) trigFile->Get("Up_eta_lowpt");
    trigHistDown_lowpt = (TH1F*) trigFile->Get("Down_eta_lowpt");

    trigHistCentral_midpt = (TH1F*) trigFile->Get("Central_eta_midpt");
    trigHistUp_midpt = (TH1F*) trigFile->Get("Up_eta_midpt");
    trigHistDown_midpt = (TH1F*) trigFile->Get("Down_eta_midpt");

    trigHistCentral_highpt = (TH1F*) trigFile->Get("Central_eta_highpt");
    trigHistUp_highpt = (TH1F*) trigFile->Get("Up_eta_highpt");
    trigHistDown_highpt = (TH1F*) trigFile->Get("Down_eta_highpt");    
    }
    double getEleSF(TH2F *h2, double pt, double eta, int systLevel);
    double getTrigSF(double pt, double eta, int systLevel);
    vector<double> getEleSFs(double pt, double eta, int systLevel, bool print=false);
    
 private:
    TH2F* idHist;
    TH2F* recoHist;
    //TH2F* trigHist;

    // Separate 1D histograms for trigger SF in different pt bins
    TH1F* trigHistCentral_lowpt;
    TH1F* trigHistUp_lowpt;
    TH1F* trigHistDown_lowpt;

    TH1F* trigHistCentral_midpt;
    TH1F* trigHistUp_midpt;
    TH1F* trigHistDown_midpt;

    TH1F* trigHistCentral_highpt;
    TH1F* trigHistUp_highpt;
    TH1F* trigHistDown_highpt;
  };

double ElectronSF::getEleSF(TH2F *h2, double pt, double eta, int systLevel){
    //Get low edge of the last bins 
    double maxX = h2->GetXaxis()->GetBinLowEdge(h2->GetNbinsX());
    double maxY = h2->GetYaxis()->GetBinLowEdge(h2->GetNbinsY());
    TAxis *axisX = h2->GetXaxis();
    TAxis *axisY = h2->GetYaxis();
    //Get the bin numbers for a given pt, eta
    //If pt or eta value is out of hist range, choose the last bin
    Int_t binX = (eta<= maxX) ? axisX->FindBin(eta): axisX->FindBin(maxX);
    Int_t binY = (pt <= maxY) ? axisY->FindBin(pt): axisY->FindBin(maxY);
    //Get the scale factor and error for that bin
    double sf = h2->GetBinContent(binX, binY);
    double err = h2->GetBinError(binX, binY);
    if(sf==0.0 && err==0.0)
        return 1.0;
    else
        return sf + (systLevel -1)*err;
}
double ElectronSF::getTrigSF(double pt, double eta, int systLevel) {
    // Choose the correct TH1 histogram based on pt range
    TH1* h1 = nullptr;
    if (pt <= 120) {
        h1 = (systLevel == 0) ? trigHistDown_lowpt : (systLevel == 2) ? trigHistUp_lowpt : trigHistCentral_lowpt;
    } else if (pt > 120 && pt <= 200) {
        h1 = (systLevel == 0) ? trigHistDown_midpt : (systLevel == 2) ? trigHistUp_midpt : trigHistCentral_midpt; 
    } else {
        h1 = (systLevel == 0) ? trigHistDown_highpt : (systLevel == 2) ? trigHistUp_highpt : trigHistCentral_highpt;
    }

    // Get low edge of the last bin for eta
    TAxis *axisX = h1->GetXaxis(); 
    double maxX = h1->GetXaxis()->GetBinLowEdge(h1->GetNbinsX());
   
    // Get the bin number for the given eta
    Int_t binX = (eta <= maxX) ? axisX->FindBin(eta) : axisX->FindBin(maxX);

    // Get the scale factor and error for that bin
    double sf = h1->GetBinContent(binX);
    double err = h1->GetBinError(binX);

    if (sf == 0.0 && err == 0.0)
        return 1.0;
    else
        return sf + (systLevel - 1) * err;
}

vector<double> ElectronSF::getEleSFs(double pt, double eta, int systLevel, bool print){
    double idSF     = getEleSF(idHist, pt, eta, systLevel);
    double recoSF   = getEleSF(recoHist, pt, eta, systLevel);//eta: -2.4, 2.4
    double trigSF   = getTrigSF(pt, eta, systLevel);
    vector<double> eleSFs {idSF*recoSF*trigSF, idSF, recoSF, trigSF};
    if (print){ 
        cout<<"----------------------------"<<endl;
        cout << "Electron Scale Factors: " << endl;
        cout<<  "    pt   = " <<pt<<endl;
        cout<<  "    eta  = " <<eta<<endl;
        cout << "    ID   = " << idSF << endl;
        cout << "    Reco = " << recoSF << endl;
        cout << "    Trig = " << trigSF << endl;
        cout << "    Total= " << idSF*recoSF*trigSF << endl;
    }
    return eleSFs;
}
