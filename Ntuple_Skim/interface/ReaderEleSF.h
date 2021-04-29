#include<TH2F.h>
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
	trigHist = (TH2F*) trigFile->Get("EGamma_SF2D");
    }
    double getEleSF(TH2F *h2, double pt, double eta, int systLevel);
    vector<double> getEleSFs(double pt, double eta, int systLevel, bool print=false);
    
 private:
    TH2F* idHist;
    TH2F* recoHist;
    TH2F* trigHist;
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
    return sf + (systLevel -1)*err;
}

vector<double> ElectronSF::getEleSFs(double pt, double eta, int systLevel, bool print){
    double idSF     = getEleSF(idHist, pt, eta, systLevel);
    double recoSF   = getEleSF(recoHist, pt, eta, systLevel);//eta: -2.4, 2.4
    double trigSF   = getEleSF(trigHist, pt, eta, systLevel);
    vector<double> eleSFs {idSF*recoSF*trigSF, idSF, recoSF, trigSF};
    if (print){ 
        cout<<"----------------------------"<<endl;
        cout << "Electron Scale Factors: " << endl;
        cout<<  "    pt   = " <<pt<<endl;
        cout<<  "    eta   = " <<eta<<endl;
        cout << "    ID   = " << idSF << endl;
        cout << "    Iso  = " << recoSF << endl;
        cout << "    Trig = " << trigSF << endl;
        cout << "    Total= " << idSF*recoSF*trigSF << endl;
    }
    return eleSFs;
}
