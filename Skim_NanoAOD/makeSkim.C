#include<iostream>
#include<string>
#include "interface/EventTree_Skim.h"
#include<TFile.h>
#include<TTree.h>
#include<TH1F.h>
#include<TH1D.h>
#include<TDirectory.h>
#include<TObject.h>
#include<TCanvas.h>
#include<iomanip>
#include<cmath>

namespace {

std::string inputPath(const std::string& fileName, bool xRootDAccess){
    if (!xRootDAccess || fileName.rfind("root://", 0) == 0){
        return fileName;
    }
    const std::string separator =
        (!fileName.empty() && fileName.front() == '/') ? "" : "/";
    return "root://cmsxrootd.fnal.gov/" + separator + fileName;
}
bool readGenEventSumw(const std::vector<std::string>& fileNames,
                      bool xRootDAccess,
                      Long64_t& totalGenEventCount,
                      double& totalGenEventSumw){
    totalGenEventCount = 0;
    totalGenEventSumw = 0.0;

    for (const std::string& fileName : fileNames){
        const std::string path = inputPath(fileName, xRootDAccess);
        TFile* inputFile = TFile::Open(path.c_str(), "READ");

        if (!inputFile || inputFile->IsZombie()){
            std::cerr << "ERROR: cannot open input file while reading Runs metadata: "
                      << path << std::endl;
            if (inputFile) delete inputFile;
            return false;
        }

        TTree* runs = dynamic_cast<TTree*>(inputFile->Get("Runs"));
        if (!runs){
            std::cerr << "ERROR: Runs tree is missing from " << path << std::endl;
            inputFile->Close();
            delete inputFile;
            return false;
        }

        if (!runs->GetBranch("genEventCount") ||
            !runs->GetBranch("genEventSumw")){
            std::cerr << "ERROR: Runs/genEventCount or Runs/genEventSumw "
                      << "is missing from " << path
                      << std::endl;
            inputFile->Close();
            delete inputFile;
            return false;
        }

        Long64_t fileGenEventCount = 0;
        Double_t fileGenEventSumw = 0.0;
        runs->SetBranchStatus("*", 0);
        runs->SetBranchStatus("genEventCount", 1);
        runs->SetBranchStatus("genEventSumw", 1);
        runs->SetBranchAddress("genEventCount", &fileGenEventCount);
        runs->SetBranchAddress("genEventSumw", &fileGenEventSumw);

        for (Long64_t runEntry = 0; runEntry < runs->GetEntries(); ++runEntry){
            runs->GetEntry(runEntry);
            totalGenEventCount += fileGenEventCount;
            totalGenEventSumw += fileGenEventSumw;
        }

        inputFile->Close();
        delete inputFile;
    }

    // A single split job can, in principle, have an exactly cancelling
    // positive/negative generator-weight sum. Only a non-positive event
    // count or non-finite sum is invalid here. The full-sample sum is
    // checked for zero in makeNtuple.C.
    if (totalGenEventCount <= 0 || !std::isfinite(totalGenEventSumw)){
        std::cerr << "ERROR: invalid generator metadata for this skim job: "
                  << "genEventCount=" << totalGenEventCount
                  << ", genEventSumw=" << totalGenEventSumw << std::endl;
        return false;
    }

    return true;
}

} // namespace

int main(int ac, char** av){
    //ac is the total number of arguments
	if(ac < 3){
		std::cout << "usage: ./makeSkim year 1of2 outputFileName inputFile[s]" << std::endl;
		return -1;
	}
    //av[1] = year
	std::string year(av[1]);

    //av[2] = NofM
	int nJob = -1;
	int totJob = -1;
	std::string checkJobs(av[2]);
	size_t pos = checkJobs.find("of");
	if (pos != std::string::npos){
	    nJob = std::stoi(checkJobs.substr(0,pos));
	    totJob = std::stoi(checkJobs.substr(pos+2,checkJobs.length()));
    }
	cout << nJob << " of " << totJob << endl;

    //av[3] = Output.root 
	bool isMC = true;
	std::string outFileName(av[3]);
	if( outFileName.find("Data") != std::string::npos){
	    cout << "IsData" << endl;
	    isMC = false;
	}

    //av[4] = xrootd or local 
	bool xRootDAccess = false;
	if (std::string(av[4])=="xrootd"){
	    xRootDAccess=true;
	    std::cout << "Will access files from xRootD" << std::endl;
    }

    //av[5...] = string containing the input files separated by space
    std::vector<std::string> fileNames;
	for (int i = 5; i < ac; i++){
        fileNames.push_back(av[i]);
	}

    //--------------------------------
    // files to run for each job 
    //--------------------------------
	int nFiles  = fileNames.size(); 
    cout<<"Total files = "<<nFiles<<endl;
	if (nJob>0 && totJob>0 && nJob <= totJob && totJob <= nFiles){
		cout << "Processing " << (1.*nFiles)/totJob << " files per job on average" << endl;
	    pos = outFileName.find(".root");
	    outFileName = outFileName.substr(0,pos) + "_" + checkJobs + ".root";
	    cout << "new output file name: "<< outFileName << endl;
	}
    else{
        cout<<"\n ERROR: In MofN, M > 0 and N > 0 and M =< N and N=<nFiles\n ";
        return 0;
    }
	EventTree* tree;
    std::vector<std::vector<std::string>> smallVectors = tree->splitVector(fileNames, totJob);
	cout << "HERE" << endl;
	tree = new EventTree(xRootDAccess, year, smallVectors[nJob-1], isMC);
	tree->isData_ = !isMC;

    // Store pre-skim generator metadata for only the NanoAOD files assigned
    // to this skim job. Summing over all skim jobs then gives the full-sample
    // genEventCount and genEventSumw without double counting.
    Long64_t genEventCountThisJob = 0;
    double genEventSumwThisJob = 0.0;
    if (isMC && !readGenEventSumw(smallVectors[nJob-1],
                                  xRootDAccess,
                                  genEventCountThisJob,
                                  genEventSumwThisJob)){
        delete tree;
        return -1;
    }


	TFile* outFile = TFile::Open( outFileName.c_str() ,"RECREATE","",207 );
    outFile->cd();
	TTree* newTree = tree->chain->GetTree()->CloneTree(0);
	newTree->SetCacheSize(50*1024*1024);
	Long64_t nEntr = tree->GetEntries();

	int startEntry = 0;
	int endEntry = nEntr;
	int eventsPerJob = nEntr;
	std::cout << "Sample has "<<nEntr << " entries" << std::endl;
	cout << "Processing events "<<startEntry<< " to " << endEntry << endl;
	TH1F* hEvents_ = new TH1F("hEvents", "Cutflow", 5, -1.5, 3.5);
    hEvents_->GetXaxis()->SetBinLabel(2, "NanoAOD");
    hEvents_->GetXaxis()->SetBinLabel(3, "Filters");
    hEvents_->GetXaxis()->SetBinLabel(4, "MuonOREleTrig");
    TH1D* hGenEventSumw = new TH1D(
        "hGenEventSumw",
        "Generator-weight sum before skimming",
        1, 0.5, 1.5
    );
    hGenEventSumw->GetXaxis()->SetBinLabel(1, "genEventSumw");
    hGenEventSumw->SetBinContent(1, genEventSumwThisJob);
    TH1D* hGenEventCount = new TH1D(
        "hGenEventCount",
        "Generated-event count before skimming",
        1, 0.5, 1.5
    );
    hGenEventCount->GetXaxis()->SetBinLabel(1, "genEventCount");
    hGenEventCount->SetBinContent(1, genEventCountThisJob);
    //--------------------------------
    // Trigger flow histograms
    //--------------------------------
    TString  im24, itm24, im27, m50, tm50, m100, tm100;
    TString  e27, e32, e32D, e35, e115, e45j200, e50j165, p175, p200;
    im24    = "HLT_IsoMu24"   ;
    itm24   = "HLT_IsoTkMu24" ;
    im27    = "HLT_IsoMu27"   ;
    m50     = "HLT_Mu50"      ;
    tm50    = "HLT_TkMu50"    ;
    m100    = "HLT_OldMu100"  ;
    tm100   = "HLT_TkMu100"   ;
    
    e27     = "HLT_Ele27_WPTight_Gsf"                         ;
    e32     = "HLT_Ele32_WPTight_Gsf"                         ;
    e32D    = "HLT_Ele32_WPTight_Gsf_L1DoubleEG"              ;
    e35     = "HLT_Ele35_WPTight_Gsf"                         ;
    e115    = "HLT_Ele115_CaloIdVT_GsfTrkIdT"                 ;
    e45j200 = "HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50" ;
    e50j165 = "HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165"         ;
    p175    = "HLT_Photon175"                                 ;
    p200    = "HLT_Photon200"                                 ;

    std::map<TString, int> names, namesE;
    if (year.find("2016")!=std::string::npos){
        names[im24 ] = 1;
        names[itm24] = 2;
        names[m50  ] = 3;
        names[tm50 ] = 4;
        namesE[e27    ] = 1;
        namesE[e115    ] = 2;
        namesE[e45j200] = 3;
        namesE[e50j165] = 4;
        namesE[p175   ] = 5;
        
    }
    if (year.find("2017")!=std::string::npos){
        names[im27 ] = 1;
        names[m50  ] = 2;
        names[tm100] = 3;
        names[m100 ] = 4;
        namesE[e32D    ] = 1;
        namesE[e115    ] = 2;
        namesE[e50j165] = 3;
        namesE[p200   ] = 4;
        
    }
    if (year.find("2018")!=std::string::npos){
        names[im24 ] = 1;
        names[m50  ] = 2;
        names[tm100] = 3;
        names[m100 ] = 4;
        namesE[e32    ] = 1;
        namesE[e115    ] = 2;
        namesE[e50j165] = 3;
        namesE[p200   ] = 4;
        
    }
	TH1F* hAll           = new TH1F("hAll_MuTrig",  "events in NanoAOD",   6, 0.5, 6.5);
	TH1F* hAllE          = new TH1F("hAll_EleTrig", "events in NanoAOD",  6, 0.5, 6.5);
	TH1F* hPass_         = new TH1F("hPass_MuTrig", "exclusive events (passes one && fails others)",  6, 0.5, 6.5);
	TH1F* hPassE_        = new TH1F("hPass_EleTrig","exclusive events (passes one && fails others)", 6, 0.5, 6.5);
	TH1F* hPass          = new TH1F("hPass_MuTrigFlow", "OR flow of HLT paths",  6, 0.5, 6.5);
	TH1F* hPassE         = new TH1F("hPass_EleTrigFlow","OR flow of HLT paths", 6, 0.5, 6.5);
    for(const auto &pair:names){
        hAll->GetXaxis()->SetBinLabel(pair.second, TString(pair.first));
        hPass->GetXaxis()->SetBinLabel(pair.second, TString(pair.first));
        hPass_->GetXaxis()->SetBinLabel(pair.second, TString(pair.first));
    }
    for(const auto &pair:namesE){
        hAllE->GetXaxis()->SetBinLabel(pair.second, TString(pair.first));
        hPassE->GetXaxis()->SetBinLabel(pair.second, TString(pair.first));
        hPassE_->GetXaxis()->SetBinLabel(pair.second, TString(pair.first));
    }
    bool isTrig;
    bool isTrigE;
    bool isTrigTable9;
    bool isTrigETable9;
    Int_t passTrigMu, passTrigEle;
    Int_t passTrigMuTable9, passTrigEleTable9;
    TBranch* passTrigMu_  = newTree->Branch("passTrigMu",  &passTrigMu, "passTrigMu/I");
    TBranch* passTrigEle_ = newTree->Branch("passTrigEle", &passTrigEle, "passTrigEle/I");
    TBranch* passTrigMuTable9_ = newTree->Branch(
        "passTrigMuTable9", &passTrigMuTable9, "passTrigMuTable9/I"
    );
    TBranch* passTrigEleTable9_ = newTree->Branch(
        "passTrigEleTable9", &passTrigEleTable9, "passTrigEleTable9/I"
    );


    //---------------------
    //Event loop
    //---------------------
    std::cout<<"---------------------------"<<std::endl;
    std::cout<<setw(10)<<"Progress"<<setw(10)<<"Time"<<std::endl;
    std::cout<<"---------------------------"<<std::endl;
    double totalTime = 0.0;
	auto startClock = std::chrono::high_resolution_clock::now();
    int count_bad = 0;
	for(Long64_t entry= startEntry; entry < endEntry; entry++){
        //if(entry>4235) break; 
        //cout<<entry<<endl;
        //if(entry<4228) continue; 
		if(entry%(eventsPerJob/100) == 0){// print after every 1% of events
            totalTime+= std::chrono::duration<double>(std::chrono::high_resolution_clock::now()-startClock).count();
            int sec = (int)(totalTime)%60;
            int min = (int)(totalTime)/60;
	        std::cout<<setw(10)<<100*entry/endEntry<<" %"<<setw(10)<<min<<"m "<<sec<<"s"<<std::endl;
			startClock = std::chrono::high_resolution_clock::now();			
		}
		tree->GetEntry(entry);
        //tree->Show(entry);
		hEvents_->Fill(0.);
        if (tree->nTrigObj > 50 || tree->nMu > 50 || tree->nEle > 50 || tree->nJet > 50 || tree->nPho > 50){
            count_bad++;
            continue;
        }
        //--------------------------------
        // MET filters
        //--------------------------------
        bool filters = 
            (tree->Flag_goodVertices_ &&
		    tree->Flag_globalSuperTightHalo2016Filter_ &&
		    tree->Flag_HBHENoiseFilter_ &&
		    tree->Flag_HBHENoiseIsoFilter_ && 
		    tree->Flag_EcalDeadCellTriggerPrimitiveFilter_ &&
		    tree->Flag_BadPFMuonFilter_ &&
		    tree->Flag_eeBadScFilter_ );
        if (year=="2017" || year=="2018") filters = filters && tree->Flag_ecalBadCalibFilter_ ;

        //--------------------------------
        // TrigObj matching for 2017 
        //--------------------------------
        bool is32D = false;
        for(int j=0;j<tree->nTrigObj;j++){
            if (!(tree->TrigObj_pt[j]>31)) continue;
            if (!(abs(tree->TrigObj_id[j])==11)) continue;
            if (!(tree->TrigObj_filterBits[j] & 1024)) continue;
            for(int k=0; k<tree->nEle; k++){
                double dR = tree->deltaR(tree->eleEta[k],  tree->elePhi[k], tree->TrigObj_eta[j], tree->TrigObj_phi[j]);
                if(dR < 0.1){
                    is32D = true;
                    break;
                }
            }
        }


        //Fill hAll 
        for(const auto& pair: names)  hAll->Fill(pair.second);
        for(const auto& pair: namesE) hAllE->Fill(pair.second);
        //--------------------------------------
        // Fill exclusive trigger histograms 
        //--------------------------------------
        if (year.find("2016")!=std::string::npos){
            if(tree->im24_  && !(tree->itm24_ || tree->m50_ || tree->tm50_))      hPass_->Fill(1);
            if(tree->itm24_ && !(tree->im24_  || tree->m50_ || tree->tm50_))      hPass_->Fill(2);
            if(tree->m50_   && !(tree->im24_ || tree->itm24_ || tree->tm50_))     hPass_->Fill(3);
            if(tree->tm50_  && !(tree->im24_ || tree->itm24_ || tree->m50_))     hPass_->Fill(4);
            //Electron
            if(tree->e27_       && !(tree->e45j200_ || tree->e50j165_ || tree->p175_ || tree->e115_))   hPassE_->Fill(1);
            if(tree->e115_      && !(tree->e27_ ||  tree->e45j200_ || tree->e50j165_ || tree->p175_))   hPassE_->Fill(2);
            if(tree->e45j200_   && !(tree->e27_ || tree->e50j165_ || tree->p175_ || tree->e115_))       hPassE_->Fill(3);
            if(tree->e50j165_   && !(tree->e27_ || tree->e45j200_ || tree->p175_ || tree->e115_))       hPassE_->Fill(4);
            if(tree->p175_      && !(tree->e27_ || tree->e45j200_ || tree->e50j165_ || tree->e115_))    hPassE_->Fill(5);
        }
        if (year.find("2017")!=std::string::npos){
            if(tree->im27_   && !(tree->m50_ || tree->tm100_ || tree->m100_))    hPass_->Fill(1);
            if(tree->m50_    && !(tree->im27_ || tree->tm100_ || tree->m100_))   hPass_->Fill(2);
            if(tree->tm100_  && !(tree->im27_ || tree->m50_ ||  tree->m100_))    hPass_->Fill(3);
            if(tree->m100_   && !(tree->im27_ || tree->m50_ || tree->tm100_))    hPass_->Fill(4);
            //Electron
            if(is32D            && !(tree->e50j165_ || tree->p200_ || tree->e115_))   hPassE_->Fill(1);
            if(tree->e115_      && !(is32D  || tree->e50j165_ || tree->p200_))        hPassE_->Fill(2);
            if(tree->e50j165_   && !(is32D  || tree->p200_ || tree->e115_))           hPassE_->Fill(3);
            if(tree->p200_      && !(is32D  || tree->e50j165_ || tree->e115_ ))       hPassE_->Fill(4);
        }
        if (year.find("2018")!=std::string::npos){
            if(tree->im24_      && !(tree->m50_ || tree->tm100_ || tree->m100_ ))     hPass_->Fill(1);
            if(tree->m50_       && !(tree->im24_ || tree->tm100_ || tree->m100_ ))    hPass_->Fill(2);
            if(tree->tm100_     && !(tree->im24_ || tree->m50_ || tree->m100_ ))      hPass_->Fill(3);
            if(tree->m100_      && !(tree->im24_ || tree->m50_ || tree->tm100_ ))     hPass_->Fill(4);
            //Electron
            if(tree->e32_       && !(tree->e50j165_ || tree->p200_ || tree->e115_))   hPassE_->Fill(1);
            if(tree->e115_      && !(tree->e32_ || tree->e50j165_ || tree->p200_))    hPassE_->Fill(2);
            if(tree->e50j165_   && !(tree->e32_ || tree->p200_ || tree->e115_))       hPassE_->Fill(3);
            if(tree->p200_      && !(tree->e32_ || tree->e50j165_ || tree->e115_))    hPassE_->Fill(4);
        }
        //--------------------------------
        // Fill trigger FLOW  histograms 
        //--------------------------------
        //Fill hPass 
        isTrig        = false;
        isTrigE       = false;
        isTrigTable9  = false;
        isTrigETable9 = false;
        if (year.find("2016")!=std::string::npos){
            if(tree->im24_)      hPass->Fill(1);
            if(tree->im24_ || tree->itm24_)     hPass->Fill(2);
            if(tree->im24_ || tree->itm24_ || tree->m50_)       hPass->Fill(3);
            if(tree->im24_ || tree->itm24_ || tree->m50_ || tree->tm50_){
                isTrig = true;
                hPass->Fill(4);
            }
            //Electron
            if(tree->e27_)       hPassE->Fill(1);
            if(tree->e27_ || tree->e115_)       hPassE->Fill(2);
            if(tree->e27_ || tree->e115_ || tree->e45j200_)   hPassE->Fill(3);
            if(tree->e27_ || tree->e115_ || tree->e45j200_ || tree->e50j165_)   hPassE->Fill(4);
            if(tree->e27_ || tree->e115_ || tree->e45j200_ || tree->e50j165_ || tree->p175_){
                hPassE->Fill(5);
                isTrigE = true;
            }
            // Trigger OR documented in Table 9.
            isTrigTable9 = tree->m50_ || tree->tm50_;
            isTrigETable9 = tree->e27_ || tree->e115_ || tree->p175_;
        }
        if (year.find("2017")!=std::string::npos){
            if(tree->im27_)          hPass->Fill(1);
            if(tree->im27_ || tree->m50_)       hPass->Fill(2);
            if(tree->im27_ || tree->m50_ || tree->tm100_)     hPass->Fill(3);
            if(tree->im27_ || tree->m50_ || tree->tm100_ || tree->m100_ ){
                hPass->Fill(4);
                isTrig = true;
            }
            //Electron
            if(is32D)           hPassE->Fill(1);
            if(is32D || tree->e115_)           hPassE->Fill(2);
            if(is32D || tree->e115_ || tree->e50j165_)   hPassE->Fill(3);
            if(is32D || tree->e115_ || tree->e50j165_ || tree->p200_){
                hPassE->Fill(4);
                isTrigE = true;
            }
            // Trigger OR documented in Table 9.
            isTrigTable9 = tree->m50_ || tree->tm100_ || tree->m100_;
            isTrigETable9 = tree->e35_ || tree->e115_ || tree->p200_;
        }
        if (year.find("2018")!=std::string::npos){
            if(tree->im24_)          hPass->Fill(1);
            if(tree->im24_ || tree->m50_)       hPass->Fill(2);
            if(tree->im24_ || tree->m50_ || tree->tm100_)     hPass->Fill(3);
            if(tree->im24_ || tree->m50_ || tree->tm100_ || tree->m100_){
                hPass->Fill(4);
                isTrig = true;
            }
            //Electron
            if(tree->e32_)       hPassE->Fill(1);
            if(tree->e32_ || tree->e115_)       hPassE->Fill(2);
            if(tree->e32_ || tree->e115_ || tree->e50j165_)   hPassE->Fill(3);
            if(tree->e32_ || tree->e115_ || tree->e50j165_ || tree->p200_){
                hPassE->Fill(4);
                isTrigE = true;
            }
            // Trigger OR documented in Table 9.
            isTrigTable9 = tree->m50_ || tree->tm100_ || tree->m100_;
            isTrigETable9 = tree->e32_ || tree->e115_ || tree->p200_;
        }
        passTrigMu  = isTrig;
        passTrigEle = isTrigE;
        passTrigMuTable9  = isTrigTable9;
        passTrigEleTable9 = isTrigETable9;
        //--------------------------------
        //fill tree
        //--------------------------------
        if(!filters) continue;
            hEvents_->Fill(1);

		if(isTrig || isTrigE || isTrigTable9 || isTrigETable9){
			newTree->Fill();
            hEvents_->Fill(2);
		}
	}
    std::cout<<"nEvents_Skim = "<<newTree->GetEntries()<<endl;
    std::cout<<"Bad Events   = "<< count_bad <<endl;
    newTree->Write();
	hEvents_->Write();
    hGenEventSumw->Write();
    hGenEventCount->Write();
    hAll->Write();
    hAllE->Write();
    hPass_->Write();
    hPassE_->Write();
    hPass->Write();
    hPassE->Write();

	outFile->Close();
    delete outFile;
    outFile = nullptr;

    delete tree;
    tree = nullptr;

	
	return 0;
}
