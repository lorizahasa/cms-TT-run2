#include<TH2F.h>
#include<TFile.h>
#include <iostream>

using namespace std;
class PhotonSF
{
 public:
    PhotonSF(string id_fname, string eveto_fname, int _year){
        TFile* idFile = TFile::Open(id_fname.c_str(),"READ");
        idHist = (TH2F*) idFile->Get("EGamma_SF2D");
        year = _year;
        TFile* eVetoFile = TFile::Open(eveto_fname.c_str(),"READ");
        if (year==2016){
            eVetoHist_2D = (TH2F*) eVetoFile->Get("Scaling_Factors_HasPix_R9 Inclusive");
        } else if (year==2017){
            eVetoHist_1D = (TH1F*) eVetoFile->Get("Medium_ID");
        } else if (year==2018){
            eVetoHist_2D = (TH2F*) eVetoFile->Get("eleVeto_SF");
            eVetoHist_Unc_2D = (TH2F*) eVetoFile->Get("eleVeto_Unc");
        }
    }
    double getPhoSF(TH2F *h2, double pt, double eta, int systLevel);
    vector<double> getPhoSFs(double pt, double eta, int systLevel, bool print=false);

 private:
    TH2F* idHist;
    TH2F* eVetoHist_2D;
    TH2F* eVetoHist_Unc_2D;
    TH1F* eVetoHist_1D;
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

vector<double> PhotonSF::getPhoSFs(double pt, double eta, int systLevel, bool print){
    double idSF     = getPhoSF(idHist, pt, eta, systLevel);//eta: -2.4, 2.4
    double scaleSF  = 1.0;
    if(year==2016){
        scaleSF     = getPhoSF(eVetoHist_2D, pt, abs(eta), systLevel);//eta: 0.0, 2.4
    }
    else if(year==2017){
        Int_t bin = (abs(eta) < 1.5)? 1: 4;
	    double sf = eVetoHist_1D->GetBinContent(bin);
	    double err = eVetoHist_1D->GetBinError(bin);
        scaleSF = sf + (systLevel -1)*err;
	}
    else if(year==2018){//axes are interchanged
        scaleSF     = getPhoSF(eVetoHist_2D, abs(eta), pt, systLevel);//eta: 0.0, 2.4
    }
    std::vector<double> phoSFs  {idSF*scaleSF, idSF, scaleSF};
    if (print){ 
        cout<<"----------------------------"<<endl;
        cout << "Photon Scale Factors: " << endl;
        cout<<  "    pt     = " <<pt<<endl;
        cout<<  "    eta    = " <<eta<<endl;
        cout << "    ID     = " << idSF << endl;
        cout << "    Scale  = " << scaleSF << endl;
        cout << "    Total  = " << idSF*scaleSF<< endl;
    }
    return phoSFs;
}

