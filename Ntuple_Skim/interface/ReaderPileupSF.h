#include<TH1F.h>
#include<TFile.h>
#include<iostream>
#include<vector>
#include<string>

class PileupSF{
public:
	PileupSF(string data_fname, string mc_fname){
        TFile* dataFile = TFile::Open(data_fname.c_str(), "READ");
        TFile* mcFile = TFile::Open(mc_fname.c_str(), "READ");
        //data nominal, plus, minus hists
        hData_nom = (TH1D*) dataFile->Get("pileup");
        hData_minus = (TH1D*) dataFile->Get("pileup_minus");
        hData_plus = (TH1D*) dataFile->Get("pileup_plus");
        hData_nom->Scale(1.0/hData_nom->Integral());
        hData_plus->Scale(1.0/hData_plus->Integral());
        hData_minus->Scale(1.0/hData_minus->Integral());
        //only nominal hist from mc
        hMC = (TH1D*) mcFile->Get("pu_mc");
	    hMC->Scale(1.0/hMC->Integral());
        //weight is hData/hMC
        hData_nom->Divide(hMC);
        hData_plus->Divide(hMC);
        hData_minus->Divide(hMC);
    }
    double getPuSF(TH1D* hRatio, Float_t nPV);
	vector<double> getPuSFs(Float_t nPV, bool print=false);
private:
	TH1D* hData_nom; 
	TH1D* hData_minus; 
	TH1D* hData_plus; 
	TH1D* hMC; 
};

double PileupSF::getPuSF(TH1D* hRatio, Float_t nPV){
    double maxX = hRatio->GetXaxis()->GetBinLowEdge(hRatio->GetNbinsX());
    TAxis *axisX = hRatio->GetXaxis();
    Int_t binX = (nPV<= maxX) ? axisX->FindBin(nPV): axisX->FindBin(maxX);
    double sf = hRatio->GetBinContent(binX);
    return sf;
}

vector<double>PileupSF::getPuSFs(Float_t nPV, bool print){
    double sf_minus = getPuSF(hData_minus, nPV); 
    double sf_nom   = getPuSF(hData_nom, nPV); 
    double sf_plus  = getPuSF(hData_plus, nPV); 
    vector<double> pileupSFs {sf_minus, sf_nom, sf_plus};
    if (print){ 
        cout<<"----------------------------"<<endl;
        cout << "Pileup Scale Factors: " << endl;
        cout<<  "    nPV   = " <<nPV<<endl;
        cout << "    sf_minus = " << sf_minus << endl;
        cout << "    sf_nom = " << sf_nom << endl;
        cout << "    sf_plus = " << sf_plus << endl;
    }
    return pileupSFs;
}
