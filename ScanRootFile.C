#include "TFile.h"
#include "TKey.h"
#include "TMacro.h"
//root -b -q "ScanRootFile.C(\"fileName.root\")"

void readHist(TH1F *h, TString hName){
    int entries  = h->GetEntries();
    double yield = h->Integral();
    double weight = yield/entries;
    double mean  = h->GetMean();
    double rms = h->GetRMS();
    string name (hName);
    printf("%10.2f, %10.2f, %10.2f, %10.2f, %10s \n", yield, weight, mean, rms, name.c_str());
    //for(int i = 1; i<h->GetNbinsX()+1; i++){
    //printf("\t %5d %10.0f %10.0f\n", i, h->GetBinCenter(i), h->GetBinContent(i));
}

void readTree(TTree * t){
  //t->Print();
  TObjArray *branchList; 
  branchList  = t->GetListOfBranches();
  int nBranch  = t->GetNbranches();
  vector<string> brNames;
  for(int i=0;i<nBranch;i++){
    brNames.push_back(branchList->At(i)->GetName());
  }
  sort(brNames.begin(), brNames.end());
  for(int i=0;i<nBranch;i++){
    TBranch *br = t->GetBranch(TString(brNames[i]));
    t->Draw(TString(brNames[i]));
    TH1F *htemp = (TH1F*)gPad->GetPrimitive("htemp");
    if(htemp) readHist(htemp, TString(brNames[i]));
  }
}

void readDir(TDirectory *dir) {
    TDirectory *dirsav = gDirectory;
    gDirectory->pwd();
    TIter next(dir->GetListOfKeys());
    TKey *key;
    while ((key = (TKey*)next())){
        if (key->IsFolder() && TString(key->GetClassName())!="TTree"){
            cout<<key->GetName()<<endl;
            cout<<key->GetClassName()<<endl;
            dir->cd(key->GetName());
            //dir->ls();
            //dir->GetListOfKeys()->Print();
            TDirectory *subdir = gDirectory;
            readDir(subdir);
            dirsav->cd();
            continue;
        }
        else{
            if(TString(key->GetClassName())=="TH1F"){
                TH1F *h; gDirectory->GetObject(key->GetName(),h);
                readHist(h, h->GetName());
            }
            if(TString(key->GetClassName())=="TTree"){
                TTree *t; gDirectory->GetObject(key->GetName(),t);
                readTree(t);
            }
        }
    }
}

void readFile(TFile * file){
    TDirectory *dirsav = gDirectory;
    TIter next(file->GetListOfKeys());
    TKey *key;
    while ((key = (TKey*)next())){
        if (key->IsFolder() && TString(key->GetClassName())!="TTree") {
            file->cd(key->GetName());
            TDirectory *subdir = gDirectory;
            readDir(subdir);
            dirsav->cd();
            continue;
        }
        else{
            readDir(gDirectory);
        }
    }
}

void ScanRootFile(TString fileName){
    TFile *f = new TFile(fileName);
    //TFile *f = TFile::Open("root://cmsxrootd.fnal.gov/"+fileName);
    if (f->IsZombie()) {
        printf("The input root file is corrupted");
      return;
   }
   readFile(f);
}
