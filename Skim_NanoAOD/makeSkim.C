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
#include <boost/program_options.hpp>
//to check RAM
#include "sys/types.h"

int main(int ac, char** av){
    if (std::string(av[1])=="git"){
        printf("Git Commit Number: %s\n", VERSION);
        printf("Git Commit Time: %s\n", COMMITTIME);
        printf("Git Branch: %s\n", BRANCH);
        printf("Git Status: %s\n", STATUS);
        bool gitStatus = std::string(STATUS)=="" ;
        if (!gitStatus){
            return 1;
        } else {
            return 0;
        }
    }

	if(ac < 3){
		std::cout << "usage: ./makeSkim year outputFileName inputFile[s]" << std::endl;
		return -1;
	}

	int eventNum = -1;
	std::string eventStr = "-1";

	std::cout << "Starting" << std::endl;

        printf("Git Commit Number: %s\n", VERSION);
        printf("Git Commit Time: %s\n", COMMITTIME);
        printf("Git Branch: %s\n", BRANCH);
        printf("Git Status: %s\n", STATUS);

        if (STATUS != ""){
            cout << endl;
            cout <<"=============================================" << endl;
            cout <<"=============================================" << endl;
            cout <<"Warning, files are missing from github" << endl;
            cout <<"=============================================" << endl;
            cout <<"=============================================" << endl;
            cout << endl;
        }

	// input: dealing with TTree first
	bool isMC = true;
	bool xRootDAccess = false;
    if (std::string(av[1])=="event"){
	    std::string tempEventStr(av[2]);
	    eventNum = std::stoi(tempEventStr);
	    for (int i = 1; i < ac-2; i++){
		av[i] = av[i+2];
		//cout << av[i] << " ";
	    }
	    ac = ac-2;
	    //cout  << endl;
	    eventStr = tempEventStr;
	    //cout << eventStr << "  "  << eventNum << endl;
	}

	std::string year(av[1]);	

	//check if NofM type format is before output name (for splitting jobs)
	int nJob = -1;
	int totJob = -1;
	std::string checkJobs(av[2]);
	size_t pos = checkJobs.find("of");
	if (pos != std::string::npos){
	    nJob = std::stoi(checkJobs.substr(0,pos));
	    totJob = std::stoi(checkJobs.substr(pos+2,checkJobs.length()));
	    for (int i = 2; i < ac-1; i++){
		av[i] = av[i+1];
		//cout << av[i] << " ";
	    }
	    ac = ac-1;
	}
	cout << nJob << " of " << totJob << endl;
 
	std::string outFileName(av[2]);
	if( outFileName.find("Data") != std::string::npos){
	    cout << "IsData" << endl;
	    isMC = false;
	}


	//check for xrootd argument before file list
	//
	if (std::string(av[3])=="xrootd"){
	    xRootDAccess=true;
	    std::cout << "Will access files from xRootD" << std::endl;
	    for (int i = 3; i < ac-1; i++){
		av[i] = av[i+1];
		//cout << av[i] << " ";
	    }
	    ac = ac-1;
	}

	//	cout << av+4 << endl;

	bool splitByEvents=false;

	
	int nFiles = ac-3;
	int startFile = 0;

	if (nJob>0 && totJob>1){
	    if (ac-3 >= totJob){
		double filesPerJob = 1.*(ac-3)/totJob;
		cout << "Processing " << filesPerJob << " files per job on average" << endl;
		startFile = int((nJob-1)*filesPerJob);
		nFiles = int(nJob*filesPerJob) - startFile;
		cout << "   total of " << (ac-3) << " files" << endl;
		cout << "   this job will process files " << startFile << " to " << startFile+nFiles << endl;
	    } else {
		splitByEvents = true;
	    }
	    
	}

	char** fileList(av+3+startFile);
	cout << "HERE" << endl;
	EventTree* tree;
	tree = new EventTree(nFiles, xRootDAccess, year, fileList, isMC);
	tree->isData_ = !isMC;

	if (eventNum > -1) {
	    string cut = "event=="+eventStr;
	    cout << "Selecting only entries with "<<cut << endl;
	    tree->chain = (TChain*) tree->chain->CopyTree(cut.c_str());
	}

	auto startClock = std::chrono::high_resolution_clock::now();

	if (nJob>0 && totJob>0){
	    pos = outFileName.find(".root");
	    outFileName = outFileName.substr(0,pos) + "_" + checkJobs + ".root";
	    cout << "new output file name: "<< outFileName << endl;
	}

	TFile* outFile = TFile::Open( outFileName.c_str() ,"RECREATE","",207 );
    outFile->cd();
	TTree* newTree = tree->chain->GetTree()->CloneTree(0);
	newTree->SetCacheSize(50*1024*1024);
	Long64_t nEntr = tree->GetEntries();
	std::cout << "Sample has "<<nEntr << " entries" << std::endl;
	if( outFileName.find("Test") != std::string::npos || outFileName.find("test") != std::string::npos || outFileName.find("TEST") != std::string::npos){
	    std::cout << "-------------------------------------------------------------------------" << std::endl;
	    std::cout << "Since this is a Test (based on output name) only running on 10,000 events" << std::endl;
	    std::cout << "-------------------------------------------------------------------------" << std::endl;
	    if (nEntr>10000){
		nEntr = 10000;
	    }
	}

	int startEntry = 0;
	int endEntry = nEntr;
	int eventsPerJob = nEntr;

	if (splitByEvents) {
	    eventsPerJob = int(1.*nEntr/totJob);
	    startEntry = (nJob-1)*eventsPerJob;
	    endEntry = nJob*eventsPerJob;
	    if (nJob==totJob){
		endEntry=nEntr;
	    }
	}
	cout << "Processing events "<<startEntry<< " to " << endEntry << endl;
	TH1F* hEvents_ = new TH1F("hEvents", "#events in NanoAOD", 3, -1.5, 1.5);
    //--------------------------------
    // Trigger flow histograms
    //--------------------------------
    TString  im24, itm24, im27, m50, tm50, m100, tm100;
    TString  e27, e32, e35, e45j200, e50j165, p175, p200;
    im24    = "HLT_IsoMu24"   ;
    itm24   = "HLT_IsoTkMu24" ;
    im27    = "HLT_IsoMu27"   ;
    m50     = "HLT_Mu50"      ;
    tm50    = "HLT_TkMu50"    ;
    m100    = "HLT_Mu100"     ;
    tm100   = "HLT_TkMu100"   ;
    
    e27     = "HLT_Ele27_WPTight_Gsf"                         ;
    e32     = "HLT_Ele32_WPTight_Gsf"                         ;
    e35     = "HLT_Ele35_WPTight_Gsf"                         ;
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
        names[p175   ] = 5;
        namesE[e27    ] = 1;
        namesE[e45j200] = 2;
        namesE[e50j165] = 3;
        namesE[p175   ] = 4;
        
    }
    if (year.find("2017")!=std::string::npos){
        names[im27 ] = 1;
        names[m50  ] = 2;
        names[m100 ] = 3;
        names[tm100] = 4;
        names[p200   ] = 5;
        namesE[e32    ] = 1;
        namesE[e50j165] = 2;
        namesE[p200   ] = 3;
        
    }
    if (year.find("2018")!=std::string::npos){
        names[im24 ] = 1;
        names[m50  ] = 2;
        names[m100 ] = 3;
        names[tm100] = 4;
        names[p200   ] = 5;
        namesE[e32    ] = 1;
        namesE[e50j165] = 2;
        namesE[p200   ] = 3;
        
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

        //Fill hAll 
        for(const auto& pair: names)  hAll->Fill(pair.second);
        for(const auto& pair: namesE) hAllE->Fill(pair.second);
        //--------------------------------------
        // Fill exclusive trigger histograms 
        //--------------------------------------
        if (year.find("2016")!=std::string::npos){
            if(tree->im24_  && !(tree->itm24_ || tree->m50_ || tree->tm50_|| tree->p175_))      hPass_->Fill(1);
            if(tree->itm24_ && !(tree->im24_  || tree->m50_ || tree->tm50_|| tree->p175_))      hPass_->Fill(2);
            if(tree->m50_   && !(tree->im24_ || tree->itm24_ || tree->tm50_|| tree->p175_))     hPass_->Fill(3);
            if(tree->tm50_  && !(tree->im24_ || tree->itm24_ || tree->m50_ || tree->p175_))     hPass_->Fill(4);
            if(tree->p175_  && !(tree->im24_ || tree->itm24_ || tree->m50_ || tree->tm50_))     hPass_->Fill(5);
            //Electron
            if(tree->e27_       && !(tree->e45j200_ || tree->e50j165_ || tree->p175_))          hPassE_->Fill(1);
            if(tree->e45j200_   && !(tree->e27_ || tree->e50j165_ || tree->p175_))              hPassE_->Fill(2);
            if(tree->e50j165_   && !(tree->e27_ || tree->e45j200_ || tree->p175_))              hPassE_->Fill(3);
            if(tree->p175_      && !(tree->e27_ || tree->e45j200_ || tree->e50j165_))           hPassE_->Fill(4);
        }
        if (year.find("2017")!=std::string::npos){
            if(tree->im27_   && !(tree->m50_ || tree->tm100_ || tree->m100_ || tree->p200_))    hPass_->Fill(1);
            if(tree->m50_    && !(tree->im27_ || tree->tm100_ || tree->m100_ || tree->p200_))   hPass_->Fill(2);
            if(tree->tm100_  && !(tree->im27_ || tree->m50_ ||  tree->m100_ || tree->p200_))    hPass_->Fill(3);
            if(tree->m100_   && !(tree->im27_ || tree->m50_ || tree->tm100_ || tree->p200_))    hPass_->Fill(4);
            if(tree->p200_   && !(tree->im27_ || tree->m50_ || tree->tm100_ || tree->m100_))    hPass_->Fill(5);
            //Electron
            if(tree->e32_       && !(tree->e50j165_ || tree->p200_))        hPassE_->Fill(1);
            if(tree->e50j165_   && !(tree->e32_  || tree->p200_))           hPassE_->Fill(2);
            if(tree->p200_      && !(tree->e32_ || tree->e50j165_ ))        hPassE_->Fill(3);
        }
        if (year.find("2018")!=std::string::npos){
            if(tree->im24_      && !(tree->m50_ || tree->tm100_ || tree->m100_ || tree->p200_))     hPass_->Fill(1);
            if(tree->m50_       && !(tree->im24_ || tree->tm100_ || tree->m100_ || tree->p200_))    hPass_->Fill(2);
            if(tree->tm100_     && !(tree->im24_ || tree->m50_ || tree->m100_ || tree->p200_))      hPass_->Fill(3);
            if(tree->m100_      && !(tree->im24_ || tree->m50_ || tree->tm100_ || tree->p200_))     hPass_->Fill(4);
            if(tree->p200_      && !(tree->im24_ || tree->m50_ || tree->tm100_ || tree->m100_ ))    hPass_->Fill(5);
            //Electron
            if(tree->e32_       && !(tree->e50j165_ || tree->p200_))    hPassE_->Fill(1);
            if(tree->e50j165_   && !(tree->e32_ || tree->p200_))        hPassE_->Fill(2);
            if(tree->p200_      && !(tree->e32_ || tree->e50j165_))     hPassE_->Fill(3);
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
            if(tree->im24_ || tree->itm24_ || tree->m50_ || tree->tm50_)       hPass->Fill(4);
            if(tree->im24_ || tree->itm24_ || tree->m50_ || tree->tm50_|| tree->p175_){
                isTrig = true;
                hPass->Fill(5);
            }
            //Electron
            if(tree->e27_)       hPassE->Fill(1);
            if(tree->e27_ || tree->e45j200_)   hPassE->Fill(2);
            if(tree->e27_ || tree->e45j200_ || tree->e50j165_)   hPassE->Fill(3);
            if(tree->e27_ || tree->e45j200_ || tree->e50j165_ || tree->p175_){
                hPassE->Fill(4);
                isTrigE = true;
            }
        }
        if (year.find("2017")!=std::string::npos){
            if(tree->im27_)          hPass->Fill(1);
            if(tree->im27_ || tree->m50_)       hPass->Fill(2);
            if(tree->im27_ || tree->m50_ || tree->tm100_)     hPass->Fill(3);
            if(tree->im27_ || tree->m50_ || tree->tm100_ || tree->m100_ )     hPass->Fill(4);
            if(tree->im27_ || tree->m50_ || tree->tm100_ || tree->m100_ || tree->p200_){
                hPass->Fill(5);
                isTrig = true;
            }
            //Electron
            if(tree->e32_)           hPassE->Fill(1);
            if(tree->e32_ || tree->e50j165_)   hPassE->Fill(2);
            if(tree->e32_ || tree->e50j165_ || tree->p200_){
                hPassE->Fill(3);
                isTrigE = true;
            }
        }
        if (year.find("2018")!=std::string::npos){
            if(tree->im24_)          hPass->Fill(1);
            if(tree->im24_ || tree->m50_)       hPass->Fill(2);
            if(tree->im24_ || tree->m50_ || tree->tm100_)     hPass->Fill(3);
            if(tree->im24_ || tree->m50_ || tree->tm100_ || tree->m100_)     hPass->Fill(4);
            if(tree->im24_ || tree->m50_ || tree->tm100_ || tree->m100_ || tree->p200_){
                hPass->Fill(5);
                isTrig = true;
            }
            //Electron
            if(tree->e32_)       hPassE->Fill(1);
            if(tree->e32_ || tree->e50j165_)   hPassE->Fill(2);
            if(tree->e32_ || tree->e50j165_ || tree->p200_){
                hPassE->Fill(3);
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


    TNamed gitCommit("Git_Commit", VERSION);
    TNamed gitTime("Git_Commit_Time", COMMITTIME);
    TNamed gitBranch("Git_Branch", BRANCH);
    TNamed gitStatus("Git_Status", STATUS);

    gitCommit.Write();
    gitTime.Write();
    gitBranch.Write();
    gitStatus.Write();
    
	outFile->Close();

	
	return 0;
}
