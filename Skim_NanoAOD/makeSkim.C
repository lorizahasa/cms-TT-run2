#include<iostream>
#include<string>
#include "interface/EventTree_Skim.h"
#include<TFile.h>
#include<TTree.h>
#include<TH1F.h>
#include<TDirectory.h>
#include<TObject.h>
#include<TCanvas.h>
#include<iomanip>

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
    //--------------------------------
    // Trigger flow histograms
    //--------------------------------
    TString  im24, itm24, im27, m50, tm50, m100, tm100;
    TString  e27, e32, e32D, e115, e45j200, e50j165, p175, p200;
    im24    = "HLT_IsoMu24"   ;
    itm24   = "HLT_IsoTkMu24" ;
    im27    = "HLT_IsoMu27"   ;
    m50     = "HLT_Mu50"      ;
    tm50    = "HLT_TkMu50"    ;
    m100    = "HLT_Mu100"     ;
    tm100   = "HLT_TkMu100"   ;
    
    e27     = "HLT_Ele27_WPTight_Gsf"                         ;
    e32     = "HLT_Ele32_WPTight_Gsf"                         ;
    e32D    = "HLT_Ele32_WPTight_Gsf_L1DoubleEG"              ;
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
        names[m100 ] = 3;
        names[tm100] = 4;
        namesE[e32D    ] = 1;
        namesE[e115    ] = 2;
        namesE[e50j165] = 3;
        namesE[p200   ] = 4;
        
    }
    if (year.find("2018")!=std::string::npos){
        names[im24 ] = 1;
        names[m50  ] = 2;
        names[m100 ] = 3;
        names[tm100] = 4;
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
    Int_t passTrigMu, passTrigEle;
    TBranch* passTrigMu_  = newTree->Branch("passTrigMu",  &passTrigMu, "passTrigMu/I");
    TBranch* passTrigEle_ = newTree->Branch("passTrigEle", &passTrigEle, "passTrigEle/I");


    //---------------------
    //Event loop
    //---------------------
    std::cout<<"---------------------------"<<std::endl;
    std::cout<<setw(10)<<"Progress"<<setw(10)<<"Time"<<std::endl;
    std::cout<<"---------------------------"<<std::endl;
    double totalTime = 0.0;
	auto startClock = std::chrono::high_resolution_clock::now();
	for(Long64_t entry= startEntry; entry < endEntry; entry++){
        //if(entry>4235) break; 
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
        if(!filters) continue;
        hEvents_->Fill(1);


        //--------------------------------
        // TrigObj matching for 2017 
        //--------------------------------
        bool is32D = false;
        for(int j=0;j<tree->nTrigObj;j++){
            if (tree->nTrigObj > 100) continue; //initial size
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
        isTrig  = false;
        isTrigE = false;
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
        }
        passTrigMu  = isTrig;
        passTrigEle = isTrigE;
        //--------------------------------
        //fill tree
        //--------------------------------
		if(isTrig || isTrigE){
			newTree->Fill();
            hEvents_->Fill(2);
		}
	}
    std::cout<<"nEvents_Skim = "<<newTree->GetEntries()<<endl;
    newTree->Write();
	hEvents_->Write();
    hAll->Write();
    hAllE->Write();
    hPass_->Write();
    hPassE_->Write();
    hPass->Write();
    hPassE->Write();

	outFile->Close();

	
	return 0;
}
