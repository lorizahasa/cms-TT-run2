#include<TH2F.h>
#include<TFile.h>
#include <iostream>

using namespace std;
class PhotonSF
{
 public:
    PhotonSF(string id_fname, string ps_fname, string cs_fname){
        //ID
        TFile* idFile = TFile::Open(id_fname.c_str(),"READ");
        idHist = (TH2F*) idFile->Get("EGamma_SF2D");
        //pixel seed
        TFile* psFile = TFile::Open(ps_fname.c_str(),"READ");
        psHist = (TH1F*) psFile->Get("MVAID/SF_HasPix_MVAID");
        //conversion safe electron veto
        TFile* csFile = TFile::Open(cs_fname.c_str(),"READ");
        csHist = (TH1F*) csFile->Get("MVAID/SF_CSEV_MVAID");
    }
    double getPhoSF(TH2F *h2, double pt, double eta, int systLevel);
    double getPhoSF_1D(TH1F *h1, double pt, double eta, int systLevel);
    vector<double> getPhoSFs(double pt, double eta, int systLevel, bool print=false);

 private:
    TH2F* idHist;
    TH1F* psHist;
    TH1F* csHist;
    int year;

};

double PhotonSF::getPhoSF(TH2F *h2, double pt, double eta, int systLevel){
    //Get max of x and y range
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

double PhotonSF::getPhoSF_1D(TH1F *h1, double pt, double eta, int systLevel){
    Int_t bin = (abs(eta) < 1.5)? 1: 4;
    double sf = h1->GetBinContent(bin);
    double err = h1->GetBinError(bin);
    return sf + (systLevel -1)*err;
}

vector<double> PhotonSF::getPhoSFs(double pt, double eta, int systLevel, bool print){
    double idSF     = getPhoSF(idHist, pt, eta, systLevel);
    double psSF     = getPhoSF_1D(psHist, pt, eta, systLevel);;
    double csSF     = getPhoSF_1D(csHist, pt, eta, systLevel);;
    std::vector<double> phoSFs  {idSF*psSF*csSF, idSF, psSF, csSF};
    if (print){ 
        cout<<"----------------------------"<<endl;
        cout << "Photon Scale Factors: " << endl;
        cout<<  "    pt     = " <<pt<<endl;
        cout<<  "    eta    = " <<eta<<endl;
        cout << "    ID     = " << idSF << endl;
        cout << "    PS  = " << psSF << endl;
        cout << "    CS  = " << csSF << endl;
        cout << "    Total  = " << idSF*psSF*csSF<< endl;
    }
    return phoSFs;
}

