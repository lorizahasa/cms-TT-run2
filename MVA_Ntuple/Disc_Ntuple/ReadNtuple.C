#include<iostream>
#include<unistd.h>
#include<cstdlib>
#include<string>
#include<TROOT.h>
#include"TMVA/Reader.h"
#include"TMVA/Tools.h"
#include<TFile.h>
#include<TTree.h>
#include<TH1F.h>
#include<TDirectory.h>
#include<TObject.h>
#include<TCanvas.h>
#include<iomanip>
#include <fstream>
#include <cstdlib>

#include <vector>
#include <array>

#include "src/NtupleTree.h"
#include <nlohmann/json.hpp>
#include <boost/algorithm/string.hpp>

#include <iostream>
#include <sstream>
#include <sys/stat.h>
#include <sys/types.h>
#include <filesystem>

int main(int argc, char* argv[]){

    std::map<std::string, std::vector<double>> dictSFs = {
    {"2016Pre", {1.34, 1.79, 1.11, 1.20}},
    {"2016Post", {1.47, 2.22, 0.54, 1.64}},
    {"2017", {1.38, 1.01, 1.17, 1.01}},
    {"2018", {1.38, 1.42, 0.66, 1.23}},
    {"2016Pre__2016Post__2017__2018", {1.38, 1.40, 0.96, 1.22}}
}; 

    std::string fileName = "sample/FilesNtuple_Grouped_cff.json";//default file
    nlohmann::json js; 
    cout<<"Input json: "<<fileName<<endl;
    std::ifstream fileName_(fileName.c_str());
    try{
        js = nlohmann::json::parse(fileName_);
    } catch (const std::exception& e) {
        cout<<"\nEXCEPTION: Check the input json fileName: "<<fileName<<endl;
        cout<<e.what()<<endl;
        std::abort();
    }

    std::string year = "2017";
    std::string decay = "Semilep";
    std::string channel = "Mu";
    std::string sample = "SignalSpin32_M800";
    std::string region = "ttyg_Enriched_SR_Resolved";
    std::string syst = "JetBase";
    std::string method = "BDTA";
    bool isCut = false;

    int opt;
    while ((opt = getopt(argc, argv, "y:d:c:s:r:z:m:i:h")) != -1) {
        switch (opt) {
            case 'y':
                year = optarg;
                break;
            case 'd':
                decay = optarg;
                break;
            case 'c':
                channel = optarg;
                break;
            case 's':
                sample = optarg;
                break;
            case 'r':
                region = optarg;
                break;
            case 'z':
                syst = optarg;
                break;
            case 'm':
                method = optarg;
                break;
            case 'i':
                isCut = true;
                break;
            case 'h':
                cout<<"Default input json: "<<fileName<<endl;
                std::cout << "Usage: ./runReadNtuple -o sK.root\n" << std::endl;
                cout<<"Choose sKey from the following:"<<endl;
                for (auto& element : js.items()) {
                    std::cout << element.key() << std::endl;
                }
            return 0;
            default:
                std::cerr << "Usage: " << argv[0] << " [-y year] [-d decay] [-c channel] [-s sample] [-r region] [--syst systematic] [--method method] [--isCut]" << std::endl;
                exit(EXIT_FAILURE);
        }
    }

    std::cout << "Year: " << year << std::endl;
    std::cout << "Decay: " << decay << std::endl;
    std::cout << "Channel: " << channel << std::endl;
    std::cout << "Sample: " << sample << std::endl;
    std::cout << "Region: " << region << std::endl;
    std::cout << "Systematic: " << syst << std::endl;
    std::cout << "Method: " << method << std::endl;
    std::cout << "isCut: " << std::boolalpha << isCut << std::endl;
 
	//----------------------------------------
	// Copy the xml weight file 
	//----------------------------------------
	std::string package = "TMVA";
	std::string inFileName = package + "_Classification_" + method + ".weights.xml";
    std::string inFileDir = "./" + year + "/" + decay + "/" + channel + "/" + method + "/" + "SR" + "/weights";
    std::string outFileDir = "./discs/Reader/" + year + "/" + decay + "/" + channel + "/" + method;

    system(("mkdir -p " + outFileDir).c_str());
    std::cout << inFileDir << std::endl;
    std::cout << outFileDir << std::endl;

    // Assuming method is defined elsewhere
    //system(("xrdcp -rf root://cmseos.fnal.gov/" + inFileDir + "/" + inFileName + " " + outFileDir).c_str());
    //std::string weightFile = outFileDir + "/" + inFileName;
    std::string weightFile = "TMVA_Classification_BDTA.weights.xml"; 

	//-----------------------------------------
	//TMVA specific
	//-----------------------------------------
	// Set batch mode
    ROOT::EnableThreadSafety();
    gROOT->SetBatch(true);
    TMVA::Tools::Instance();
    // Create a TMVA Reader
    TMVA::Reader reader("!Color:!Silent");
    
    //--------------------------------
    // Read input files
    //--------------------------------
    TString oName = "2023_Data.root";
    vector<string>fileNames; 	
    //fileNames.push_back("SignalSpin32_M800_Ntuple_1of1.root");
    string dirNtuple="/store/group/phys_b2g/lhasa/Output/cms-TT-run2/Ntuple_Skim";
    string inDirNtuple = "root://eoscms.cern.ch/"+dirNtuple+"/"+year+"/"+decay+"/JetBase/";
    if (syst.find("JE") != std::string::npos){
        inDirNtuple = "root://eoscms.cern.ch/"+dirNtuple+"/"+year+"/"+decay+"/"+syst+"/";
    }
    string sKey = "Semilep_"+syst+"__"+sample+"_FileList_"+year;
    //Semilep_JetBase__SignalSpin12_M800_FileList_2017
    try{
        js.at(sKey).get_to(fileNames);
    }catch (const std::exception & e){
        cout<<"\nEXCEPTION: Check the sKey: "<<sKey<<endl;
        cout<<e.what()<<endl;
        cout<<"Choose sKey from the following:"<<endl;
        for (auto& element : js.items()) {
            std::cout << element.key() << std::endl;
        }
        std::abort();
    }

    NtupleTree *tree = new NtupleTree(inDirNtuple, fileNames);

    reader.AddVariable("Reco_mass_T", &tree->Reco_mass_T);
    reader.AddVariable("Reco_mass_lgamma[0]", &tree->Reco_mass_lgamma0);
    reader.AddVariable("Reco_mass_trans_w", &tree->Reco_mass_trans_w);
    reader.AddVariable("Reco_st", &tree->Reco_stF);
    reader.AddVariable("Reco_mass_TT_diff", &tree->Reco_mass_TT_diff);
    reader.AddVariable("Jet_deep_b[0]", &tree->Jet_deep_b0);
    reader.AddVariable("Jet_deep_b[1]", &tree->Jet_deep_b1);
    reader.AddVariable("Reco_angle_lepton_met", &tree->Reco_angle_lepton_met);
    reader.AddVariable("Reco_angle_leadJet_met", &tree->Reco_angle_leadJet_met);
    reader.AddVariable("Reco_angle_leadBjet_met", &tree->Reco_angle_leadBjet_met);
    reader.AddVariable("Reco_chi2", &tree->Reco_chi2);
    reader.AddVariable("Jet_size", &tree->Jet_sizeF);
    reader.AddVariable("Jet_qgl[0]", &tree->Jet_qgl0);
    reader.AddVariable("Jet_qgl[1]", &tree->Jet_qgl1);
    reader.AddVariable("Reco_dr_pho_tstarHad", &tree->Reco_dr_pho_tstarHad);
    reader.AddVariable("Reco_dr_pho_tHad", &tree->Reco_dr_pho_tHad);
    reader.AddVariable("Reco_dr_pho_tstarLep", &tree->Reco_dr_pho_tstarLep);
    reader.AddVariable("Reco_dr_pho_tLep", &tree->Reco_dr_pho_tLep);
    reader.AddVariable("Reco_dr_pho_gluon", &tree->Reco_dr_pho_gluon);
    reader.AddVariable("Reco_dr_pho_bLep", &tree->Reco_dr_pho_bLep);
    reader.AddVariable("Reco_dr_pho_lep", &tree->Reco_dr_pho_lep);
    reader.AddVariable("Reco_dr_pho_nu", &tree->Reco_dr_pho_nu);
    reader.AddVariable("Reco_dr_gluon_tstarHad", &tree->Reco_dr_gluon_tstarHad);
    reader.AddVariable("Reco_dr_gluon_tHad", &tree->Reco_dr_gluon_tHad);
    reader.AddVariable("Reco_dr_gluon_tstarLep", &tree->Reco_dr_gluon_tstarLep);
    reader.AddVariable("Reco_dr_gluon_tLep", &tree->Reco_dr_gluon_tLep);
    reader.AddVariable("Reco_dr_tHad_tstarHad", &tree->Reco_dr_tHad_tstarHad);
    reader.AddVariable("Reco_dr_tLep_tstarLep", &tree->Reco_dr_tLep_tstarLep);
    reader.AddVariable("Reco_dr_tstarHad_tstarLep", &tree->Reco_dr_tstarHad_tstarLep);

	if (region.find("Boosted") != std::string::npos) {
		reader.AddVariable("FatJet_pt[0]", &tree->FatJet_pt0);
		reader.AddVariable("FatJet_msoftdrop[0]", &tree->FatJet_msoftdrop0);
	}
    //reader.AddSpectator("Weight_lumi", &tree->Weight_lumi);


    reader.BookMVA(method, weightFile.c_str()); // Assuming method and weightFile are defined elsewhere


	//-----------------------------------------
	//Define histogram
	//-----------------------------------------
    TH1F* hDisc = new TH1F("Disc", "Disc", 100, -1, 1);
	//
    TH1F* hReco_mass_T = new TH1F("Reco_mass_T", "Reco_mass_T", 6000, -50, 5950);
	TH1F* hReco_mass_lgamma = new TH1F("Reco_mass_lgamma", "Reco_mass_lgamma", 2000, -50, 1950);
	TH1F* hReco_mass_trans_w = new TH1F("Reco_mass_trans_w", "Reco_mass_trans_w", 2000, -50, 1950);
	TH1F* hReco_st = new TH1F("Reco_st", "Reco_st", 9000, -50, 8950);
	TH1F* hReco_mass_TT_diff = new TH1F("Reco_mass_TT_diff", "Reco_mass_TT_diff", 4000, -2000, 2000);
	TH1F* hJet_deep_b0 = new TH1F("Jet_deep_b0", "Jet_deep_b0", 20, 0, 1);
	TH1F* hJet_deep_b1 = new TH1F("Jet_deep_b1", "Jet_deep_b1", 20, 0, 1);
	TH1F* hReco_angle_lepton_met = new TH1F("Reco_angle_lepton_met", "Reco_angle_lepton_met", 20, 0, 5);
	TH1F* hReco_angle_leadJet_met = new TH1F("Reco_angle_leadJet_met", "Reco_angle_leadJet_met", 20, 0, 5);
	TH1F* hReco_angle_leadBjet_met = new TH1F("Reco_angle_leadBjet_met", "Reco_angle_leadBjet_met", 20, 0, 5);
	TH1F* hReco_chi2 = new TH1F("Reco_chi2", "Reco_chi2", 1000, 0, 1000);
	TH1F* hJet_size = new TH1F("Jet_size", "Jet_size", 16, -0.5, 15.5);
	TH1F* hJet_qgl_0 = new TH1F("Jet_qgl_0", "Jet_qgl_0", 20, -0.5, 1.5);
	TH1F* hJet_qgl_1 = new TH1F("Jet_qgl_1", "Jet_qgl_1", 20, -0.5, 1.5);
	TH1F* hReco_dr_pho_tstarHad = new TH1F("Reco_dr_pho_tstarHad", "Reco_dr_pho_tstarHad", 20, 0, 10);
	TH1F* hReco_dr_pho_tHad = new TH1F("Reco_dr_pho_tHad", "Reco_dr_pho_tHad", 20, 0, 10);
	TH1F* hReco_dr_pho_tstarLep = new TH1F("Reco_dr_pho_tstarLep", "Reco_dr_pho_tstarLep", 20, 0, 10);
	TH1F* hReco_dr_pho_tLep = new TH1F("Reco_dr_pho_tLep", "Reco_dr_pho_tLep", 20, 0, 10);
	TH1F* hReco_dr_pho_gluon = new TH1F("Reco_dr_pho_gluon", "Reco_dr_pho_gluon", 20, 0, 10);
	TH1F* hReco_dr_pho_bLep = new TH1F("Reco_dr_pho_bLep", "Reco_dr_pho_bLep", 20, 0, 10);
	TH1F* hReco_dr_pho_lep = new TH1F("Reco_dr_pho_lep", "Reco_dr_pho_lep", 20, 0, 10);
	TH1F* hReco_dr_pho_nu = new TH1F("Reco_dr_pho_nu", "Reco_dr_pho_nu", 20, 0, 10);
	TH1F* hReco_dr_gluon_tstarHad = new TH1F("Reco_dr_gluon_tstarHad", "Reco_dr_gluon_tstarHad", 20, 0, 10);
	TH1F* hReco_dr_gluon_tHad = new TH1F("Reco_dr_gluon_tHad", "Reco_dr_gluon_tHad", 20, 0, 10);
	TH1F* hReco_dr_gluon_tstarLep = new TH1F("Reco_dr_gluon_tstarLep", "Reco_dr_gluon_tstarLep", 20, 0, 10);
	TH1F* hReco_dr_gluon_tLep = new TH1F("Reco_dr_gluon_tLep", "Reco_dr_gluon_tLep", 20, 0, 10);
	TH1F* hReco_dr_tHad_tstarHad = new TH1F("Reco_dr_tHad_tstarHad", "Reco_dr_tHad_tstarHad", 20, 0, 10);
	TH1F* hReco_dr_tLep_tstarLep = new TH1F("Reco_dr_tLep_tstarLep", "Reco_dr_tLep_tstarLep", 20, 0, 10);
	TH1F* hReco_dr_tstarHad_tstarLep = new TH1F("Reco_dr_tstarHad_tstarLep", "Reco_dr_tstarHad_tstarLep", 20, 0, 10); 
	TH1F* hFatJet_pt = new TH1F("FatJet_pt", "FatJet_pt", 9000, -50, 8950);
	TH1F* FatJet_msoftdrop = new TH1F("FatJet_msoftdrop", "FatJet_msoftdrop", 9000, -50, 8950);

	Float_t w_lumi 	= 1.0;
	Float_t w_pu 	= 1.0;
	Float_t w_mu 	= 1.0;
	Float_t w_ele	= 1.0; 
	Float_t w_q2 	= 1.0; 
	Float_t w_pdf 	= 1.0;
	Float_t w_prefire =1.0;
	Float_t w_isr 	= 1.0;
	Float_t w_fsr 	= 1.0;
	Float_t w_btag 	= 1.0;
	Float_t w_pho   = 1.0;
	Float_t w_ttag  = 1.0;

	std::string outDir = "output/Reader/"+year+"/Semilep/"+channel+"/CombMass/BDTA";
    std::filesystem::create_directories(outDir);
    
//mkdir(outDir.c_str(), S_IRWXU);

    std::string str = syst;
    std::string findStr = "_up";
    std::string replaceStr = "Up";
    if(syst.find("_down") != std::string::npos){
        findStr = "_down";
        replaceStr = "Down"; 
    }
    size_t startPos = str.find(findStr);
    if (startPos != std::string::npos) {
        str.replace(startPos, findStr.length(), replaceStr);
    }
    string outFileName = sample+"_"+region+"_"+str+".root";
    string outPath = outDir+"/"+outFileName; 
	TFile* outFile = TFile::Open(outPath.c_str() ,"RECREATE");
    outFile->cd();
	Long64_t nEntr = tree->GetEntries();

	int startEntry = 0;
	int endEntry = nEntr;
	int eventsPerJob = nEntr;
	std::cout << "Sample has "<<nEntr << " entries" << std::endl;
	cout << "Processing events "<<startEntry<< " to " << endEntry << endl;
    
    //--------------------------------
    //Event loop
    //--------------------------------
    std::cout<<"---------------------------"<<std::endl;
    std::cout<<setw(10)<<"Progress"<<setw(10)<<"Time"<<std::endl;
    std::cout<<"---------------------------"<<std::endl;
    double totalTime = 0.0;
	auto startClock = std::chrono::high_resolution_clock::now();
    bool passTrig = false;
	for(Long64_t entry= startEntry; entry < endEntry; entry++){
		if(endEntry > 100  && entry%(eventsPerJob/100) == 0){// print after every 1% of events
            totalTime+= std::chrono::duration<double>(std::chrono::high_resolution_clock::now()-startClock).count();
            int sec = (int)(totalTime)%60;
            int min = (int)(totalTime)/60;
	        std::cout<<setw(10)<<100*entry/endEntry<<" %"<<setw(10)<<min<<"m "<<sec<<"s"<<std::endl;
			startClock = std::chrono::high_resolution_clock::now();
		}
        
        //Channel selection	
        if(channel.find("Mu") != std::string::npos){
            tree->b_Event_pass_presel_mu->GetEntry(entry);
            if(!tree->Event_pass_presel_mu) continue;
        }
        
        if(channel.find("Ele") != std::string::npos){
            tree->b_Event_pass_presel_ele->GetEntry(entry);
            if(!tree->Event_pass_presel_ele) continue;
        }
        //photon selection
        tree->b_Photon_size->GetEntry(entry);
        if(tree->Photon_size !=1) continue;

        //b-jet selection
        tree->b_Jet_b_size->GetEntry(entry);
        if(tree->Jet_b_size < 1) continue;
    
        //Region selection
        if(region.find("Resolved") != std::string::npos) {
            //jet selection
            tree->b_Jet_size->GetEntry(entry);
            if(tree->Jet_size < 5) continue;
            //Fatjet selection
            tree->b_FatJet_size->GetEntry(entry);
            if(tree->FatJet_size !=0) continue;
        }

        if(region.find("Boosted") != std::string::npos) {
            //jet selection
            tree->b_Jet_size->GetEntry(entry);
            if(tree->Jet_size < 2) continue;

            //Fatjet selection
            tree->b_FatJet_size->GetEntry(entry);
            if(tree->FatJet_size <1) continue;
        }
        if(region.find("SR") != std::string::npos){
            tree->b_Photon_et->GetEntry(entry);
            if(tree->Photon_et->at(0) <100) continue;
        }
        if(region.find("CR") != std::string::npos){
            tree->b_Photon_et->GetEntry(entry);
            if(tree->Photon_et->at(0) >100) continue;
        }
        
        Float_t combWt = 1.0;
        if(!(sample.find("Data") != std::string::npos)){
            // Read weight branches now
            tree->b_Weight_lumi->GetEntry(entry);
            tree->b_Weight_pu->GetEntry(entry);
            tree->b_Weight_mu->GetEntry(entry);
            tree->b_Weight_ele->GetEntry(entry);
            tree->b_Weight_prefire->GetEntry(entry);
            tree->b_Weight_btag->GetEntry(entry);
            tree->b_Weight_ttag->GetEntry(entry);
            tree->b_Weight_pho->GetEntry(entry);

            w_lumi      = tree->Weight_lumi;
            w_pu        = tree->Weight_pu;
            w_mu        = tree->Weight_mu;
            w_ele       = tree->Weight_ele;
            w_prefire   = tree->Weight_prefire;
            w_btag 	    = tree->Weight_btag;
            w_ttag 	    = tree->Weight_ttag;
            w_pho 	    = tree->Weight_pho->at(0);

            //Systematics
            if(syst.find("puUp") != std::string::npos){
                tree->b_Weight_puUp->GetEntry(entry);
                w_pu        = tree->Weight_puUp;
            }
            if(syst.find("puDown") != std::string::npos){
                tree->b_Weight_puDown->GetEntry(entry);
                w_pu        = tree->Weight_puDown;
            }
            if(syst.find("muUp") != std::string::npos){
                tree->b_Weight_muUp->GetEntry(entry);
                w_mu        = tree->Weight_muUp;
            }
            if(syst.find("muDown") != std::string::npos){
                tree->b_Weight_muDown->GetEntry(entry);
                w_mu        = tree->Weight_muDown;
            }
            if(syst.find("q2Up") != std::string::npos){
                tree->b_Weight_q2Up->GetEntry(entry);
                w_q2        = tree->Weight_q2Up;
            }
            if(syst.find("q2Down") != std::string::npos){
                tree->b_Weight_q2Down->GetEntry(entry);
                w_q2        = tree->Weight_q2Down;
            }
            if(syst.find("pdfUp") != std::string::npos){
                tree->b_Weight_pdfUp->GetEntry(entry);
                w_pdf        = tree->Weight_pdfUp;
            }
            if(syst.find("pdfDown") != std::string::npos){
                tree->b_Weight_pdfDown->GetEntry(entry);
                w_pdf        = tree->Weight_pdfDown;
            }
            if(syst.find("eleUp") != std::string::npos){
                tree->b_Weight_eleUp->GetEntry(entry);
                w_ele        = tree->Weight_eleUp;
            }
            if(syst.find("eleDown") != std::string::npos){
                tree->b_Weight_eleDown->GetEntry(entry);
                w_ele        = tree->Weight_eleDown;
            }
            //PROB//with pho
            if(syst.find("phoUp") != std::string::npos){
                tree->b_Weight_phoUp->GetEntry(entry);
                w_pho        = tree->Weight_phoUp->at(0);
            }
            if(syst.find("phoDown") != std::string::npos){
                tree->b_Weight_phoDown->GetEntry(entry);
                w_pho        = tree->Weight_phoDown->at(0);
            }
            if(syst.find("fsrUp") != std::string::npos){
                tree->b_Weight_fsrUp->GetEntry(entry);
                w_fsr        = tree->Weight_fsrUp;
            }
            if(syst.find("fsrDown") != std::string::npos){
                tree->b_Weight_fsrDown->GetEntry(entry);
                w_fsr        = tree->Weight_fsrDown;
            }
            if(syst.find("isrUp") != std::string::npos){
                tree->b_Weight_isrUp->GetEntry(entry);
                w_isr        = tree->Weight_isrUp;
            }
            if(syst.find("isrDown") != std::string::npos){
                tree->b_Weight_isrDown->GetEntry(entry);
                w_isr        = tree->Weight_isrDown;
            }
            if(syst.find("prefireUp") != std::string::npos){
                tree->b_Weight_prefireUp->GetEntry(entry);
                w_prefire        = tree->Weight_prefireUp;
            }
            if(syst.find("prefireDown") != std::string::npos){
                tree->b_Weight_prefireDown->GetEntry(entry);
                w_prefire        = tree->Weight_prefireDown;
            }
            if(syst.find("btag_bUp") != std::string::npos){
                tree->b_Weight_btag_bUp->GetEntry(entry);
                w_btag        = tree->Weight_btag_bUp;
            }
            if(syst.find("btag_bDown") != std::string::npos){
                tree->b_Weight_btag_bDown->GetEntry(entry);
                w_btag        = tree->Weight_btag_bDown;
            }
            if(syst.find("btag_lUp") != std::string::npos){
                tree->b_Weight_btag_lUp->GetEntry(entry);
                w_btag        = tree->Weight_btag_lUp;
            }
            if(syst.find("btag_lDown") != std::string::npos){
                tree->b_Weight_btag_lDown->GetEntry(entry);
                w_btag        = tree->Weight_btag_lDown;
            }
            if(syst.find("ttagUp") != std::string::npos){
                tree->b_Weight_ttagUp->GetEntry(entry);
                w_ttag        = tree->Weight_ttagUp;
            }
            if(syst.find("ttagDown") != std::string::npos){
                tree->b_Weight_ttagDown->GetEntry(entry);
                w_ttag        = tree->Weight_ttagDown;
            }

            combWt = w_lumi
            		* w_pu 
            		* w_mu 
            		* w_ele 
            		* w_q2 
            		* w_pdf 
            		* w_prefire 
            		* w_isr 
            		* w_fsr 
            		* w_btag 
            		* w_pho 
            		* w_ttag;
        
            if(sample.find("DYJets") != std::string::npos){
                double sf = dictSFs[year][0];
                combWt    = combWt*sf; 
            }
            tree->b_Photon_misid_ele->GetEntry(entry);
            bool isMisID = tree->Photon_misid_ele->at(0);
            if (isMisID){
                double sf = dictSFs[year][1];
                combWt    = combWt*sf; 
            }
            else{
                if(sample.find("ZGamma") != std::string::npos){
                    double sf = dictSFs[year][2];
                    combWt    = combWt*sf; 
                }
                if(sample.find("WGamma") != std::string::npos){
                    double sf = dictSFs[year][3];
                    combWt    = combWt*sf; 
                }
            }
        }//for loop not Data        
		tree->b_Reco_mass_T->GetEntry(entry);
        hReco_mass_T->Fill(tree->Reco_mass_T, combWt);
        
        //Evaluate MVA now
        tree->b_Jet_deep_b->GetEntry(entry);
        if (tree->Jet_deep_b->size()>1){
            tree->Jet_deep_b0 = tree->Jet_deep_b->at(0);
            tree->Jet_deep_b1 = tree->Jet_deep_b->at(1);
        }
        else{//FIX this in future
            tree->Jet_deep_b0 = tree->Jet_deep_b->at(0);
            tree->Jet_deep_b1 = tree->Jet_deep_b->at(0);
        }
        tree->b_Jet_qgl->GetEntry(entry);
        //tree->Jet_deep_b0 = tree->Jet_deep_b->at(0);
        //tree->Jet_deep_b1 = tree->Jet_deep_b->at(1);
        tree->Jet_qgl0 = tree->Jet_qgl->at(0);
        tree->Jet_qgl0 = tree->Jet_qgl->at(1);
        auto disc = reader.EvaluateMVA(method);  
        hDisc->Fill(disc, combWt);
	}
    cout<<"Entry of Reco_mass_T = "<<hReco_mass_T->GetEntries()<<endl;
    cout<<"Integral of Reco_mass_T = "<<hReco_mass_T->Integral()<<endl;
    string outDirInFile = sample+"/"+region+"/"+str+"/";
    outFile->mkdir(outDirInFile.c_str());
    outFile->cd(outDirInFile.c_str());
	hReco_mass_T->Write();
    hDisc->Write();
	outFile->Close();
	return 0;
}
