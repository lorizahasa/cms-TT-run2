#include<TH2D.h>
#include<TFile.h>
#include <iostream>

using namespace std;
class MuonSF
{
 public:
    MuonSF(string id_filename, string id_histName,
	   string iso_filename, string iso_histName,
	   string trig_filename, string trig_histName){

	TFile* idFile = TFile::Open(id_filename.c_str(),"READ");
	idHist = (TH2D*) idFile->Get(id_histName.c_str());

	TFile* isoFile = TFile::Open(iso_filename.c_str(),"READ");
	isoHist = (TH2D*) isoFile->Get(iso_histName.c_str());

	TFile* trigFile = TFile::Open(trig_filename.c_str(),"READ");
	trigHist = (TH2D*) trigFile->Get(trig_histName.c_str());
	
    }
    double getMuSF(TH2D *h2, double pt, double eta, int systLevel);
    vector<double> getMuSFs(double pt, double eta, int systLevel, int year, bool print=false);

 private:
    TH2D* idHist;
    TH2D* isoHist;
    TH2D* trigHist;
};


double MuonSF::getMuSF(TH2D *h2, double pt, double eta, int systLevel){
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

vector<double> MuonSF::getMuSFs(double pt, double eta, int systLevel, int year, bool print){
    double idSF    = 1.0;
    double isoSF   = 1.0; 
    double trigSF  = 1.0;
    if (year==2017 || year==2018){//axes are interchanged
        idSF    = getMuSF(idHist, abs(eta), pt, systLevel);//eta: 0, 2.4
        isoSF   = getMuSF(isoHist, abs(eta), pt, systLevel);
    }
    else{
        idSF    = getMuSF(idHist, pt, eta, systLevel);//eta: -2.4, 2.4
        isoSF   = getMuSF(isoHist, pt, eta, systLevel);
    }
    trigSF  = getMuSF(trigHist, pt, abs(eta), systLevel);//eta: 0, 2.4
    vector<double> muSFs {idSF*isoSF*trigSF, idSF, isoSF, trigSF};
    if (print){ 
        cout<<"----------------------------"<<endl;
        cout << "Muon Scale Factors: " << endl;
        cout<<  "    pt   = " <<pt<<endl;
        cout<<  "    eta   = " <<eta<<endl;
        cout << "    ID   = " << idSF << endl;
        cout << "    Iso  = " << isoSF << endl;
        cout << "    Trig = " << trigSF << endl;
        cout << "    Total= " << idSF*isoSF*trigSF << endl;
    }
    return muSFs;
}

