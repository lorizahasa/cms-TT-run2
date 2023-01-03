#include<TH1F.h>
#include<TFile.h>
#include<iostream>
#include<vector>
#include<string>

//https://indico.cern.ch/event/1152827/contributions/4840404/attachments/2428856/4162159/ParticleNet_SFs_ULNanoV9_JMAR_25April2022_PK.pdf
//Other reader:
//https://twiki.cern.ch/twiki/bin/view/CMS/DeepAK8Tagging2018WPsSFs
//https://github.com/cms-jet/TopTaggingScaleFactors/blob/master/UL/readScaleFactor.cxx
class TopSF{
public:
	TopSF(){
        //300 < pT < 400 GeV: Currently for 0.5% mistag rate
        topSF_300To400["2016Pre"]  ={1.23-0.14, 1.23, 1.23+0.16}; 
        topSF_300To400["2016Post"] ={1.08-0.10, 1.08, 1.08+0.11}; 
        topSF_300To400["2017"]        ={1.11-0.08, 1.11, 1.11+0.12}; 
        topSF_300To400["2018"]        ={1.19-0.12, 1.19, 1.19+0.12}; 
        //400 < pT < 480 GeV
        topSF_400To480["2016Pre"]  ={1.07-0.05, 1.07, 1.07+0.10}; 
        topSF_400To480["2016Post"] ={0.99-0.05, 0.99, 0.99+0.06}; 
        topSF_400To480["2017"]        ={1.01-0.04, 1.01, 1.01+0.04}; 
        topSF_400To480["2018"]        ={0.98-0.04, 0.98, 0.98+0.04}; 
        //480 < pT < 600 GeV
        topSF_480To600["2016Pre"]  ={1.04-0.05, 1.04, 1.04+0.14}; 
        topSF_480To600["2016Post"] ={1.03-0.05, 1.03, 1.03+0.07}; 
        topSF_480To600["2017"]        ={1.05-0.04, 1.05, 1.05+0.09}; 
        topSF_480To600["2018"]        ={0.96-0.03, 0.96, 0.96+0.04}; 
        //600 < pT < 1200 GeV
        topSF_600To1200["2016Pre"] ={1.06-0.10, 1.06, 1.06+0.18}; 
        topSF_600To1200["2016Post"]={1.29-0.23, 1.29, 1.29+0.25}; 
        topSF_600To1200["2017"]       ={1.00-0.05, 1.00, 1.00+0.06}; 
        topSF_600To1200["2018"]       ={0.97-0.05, 0.97, 0.97+0.05}; 
    }
	vector<double> getTopSFs(string year, double pt, bool print=false);
private:
    std::map<std::string, vector<double>> topSF_300To400;
    std::map<std::string, vector<double>> topSF_400To480;
    std::map<std::string, vector<double>> topSF_480To600;
    std::map<std::string, vector<double>> topSF_600To1200;
};

vector<double>TopSF::getTopSFs(string year, double pt, bool print){
    vector<double> topSFs = {1., 1., 1.};
    if(pt>=300 && pt<400) topSFs = topSF_300To400[year];
    if(pt>=400 && pt<480) topSFs = topSF_400To480[year];
    if(pt>=480 && pt<600) topSFs = topSF_480To600[year];
    if(pt>=600 && pt<1200)topSFs = topSF_600To1200[year];
    if (print){ 
        cout<<"----------------------------"<<endl;
        cout << "Top-tagging Scale Factors: " << endl;
        cout<<  "    Year   = " <<year<<endl;
        cout<<  "    pT     = " <<pt<<endl;
        cout << "    sf_minus = " << topSFs[0] << endl;
        cout << "    sf_nom = " <<   topSFs[1] << endl;
        cout << "    sf_plus = " <<  topSFs[2] << endl;
    }
    return topSFs;
}
