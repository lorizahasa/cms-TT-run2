#include "interface/makeNtuple.h"
#define makeNtuple_cxx


int jecvar012_g = 1; // 0:down, 1:norm, 2:up
int jervar012_g = 1; // 0:down, 1:norm, 2:up
int phosmear012_g = 1; // 0:down, 1:norm, 2:up
int musmear012_g = 1; // 0:down, 1:norm, 2: up
int elesmear012_g = 1; // 0:down, 1:norm, 2: up
int phoscale012_g = 1;
int elescale012_g = 1;
bool dilepSel;
bool semilepSel;
bool semileptonsample;
auto startClock = std::chrono::high_resolution_clock::now();

#ifdef makeNtuple_cxx
makeNtuple::makeNtuple(int ac, char** av)
{
    startClock = std::chrono::high_resolution_clock::now();
    std::string eventStr = "-1";

    if(ac < 5){
	std::cout << "usage: ./makeNtuple year sampleName outputFileDir inputFile[s]" << std::endl;
	return;
    }
    /*
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
    */
    if (std::string(av[1])=="event"){
	std::string tempEventStr(av[2]);
	eventNum = std::stoi(tempEventStr);
	for (int i = 1; i < ac-2; i++){
	    av[i] = av[i+2];
	    //cout << av[i] << " ";
	}
	ac = ac-2;
	//	cout  << endl;
	eventStr = tempEventStr;
	//cout << eventStr << "  "  << eventNum << endl;
    }
    dilepSel    = false;
    semilepSel  = false;

    if (std::string(av[1])=="semilepton" || 
        std::string(av[1])=="semilept" ||
        std::string(av[1])=="semilep" ||
        std::string(av[1])=="Semilepton" || 
        std::string(av[1])=="Semilept" ||
        std::string(av[1])=="Semilep"){
        semilepSel=true;
        for (int i = 1; i < ac-1; i++){
            av[i] = av[i+1];
	}
	ac = ac-1;
        cout << "---------------------------------------" << endl;
        cout << "Using Semilepton Selection" << endl;
        cout << "---------------------------------------" << endl;
    }
    if (std::string(av[1])=="dilepton" || 
        std::string(av[1])=="dilept" ||
        std::string(av[1])=="dilep" ||
        std::string(av[1])=="Dilepton" || 
        std::string(av[1])=="Dilept" ||
        std::string(av[1])=="Dilep"){
        dilepSel=true;
        for (int i = 1; i < ac-1; i++){
            av[i] = av[i+1];
	}
	ac = ac-1;
        cout << "---------------------------------------" << endl;
        cout << "Using Dilepton Selection" << endl;
        cout << "---------------------------------------" << endl;
    }

    if (std::string(av[1])=="qcd" || 
        std::string(av[1])=="qcdCR" ||
        std::string(av[1])=="QCDcr" ||
        std::string(av[1])=="QCD" ||
        std::string(av[1])=="QCDCR"){
  
        for (int i = 1; i < ac-1; i++){
            av[i] = av[i+1];
	}
	ac = ac-1;
        cout << "----------------------------------" << endl;
        cout << "Using QCD Control Region Selection" << endl;
        cout << "----------------------------------" << endl;
    }

    //check if NofM type format is before output name (for splitting jobs)
    int nJob = -1;
    int totJob = -1;
    std::string checkJobs(av[3]);
    size_t pos = checkJobs.find("of");
    if (pos != std::string::npos){
	nJob = std::stoi(checkJobs.substr(0,pos));
	totJob = std::stoi(checkJobs.substr(pos+2,checkJobs.length()));
	for (int i = 3; i < ac-1; i++){
	    av[i] = av[i+1];
	    //cout << av[i] << " ";
	}
	ac = ac-1;
    }
    cout << nJob << " of " << totJob << endl;
    bool splitByEvents = false;
    int nFiles = ac-4;                                                          
    int startFile = 0;                                                          
    if (nJob>0 && totJob>1){                                                    
        if (ac-4 >= totJob){                                                    
        double filesPerJob = 1.*(ac-4)/totJob;                                  
        cout << "Processing " << filesPerJob << " files per job on average" << endl;
        startFile = int((nJob-1)*filesPerJob);                                  
        nFiles = int(nJob*filesPerJob) - startFile;                             
        cout << "   total of " << (ac-4) << " files" << endl;                   
        cout << "   this job will process files " << startFile << " to " << startFile+nFiles << endl;
        } else {                                                                
        splitByEvents = true;                                                   
        }                                                                       
                                                                                
    }                                                                           
    char** fileList(av+4+startFile);                                            
    cout << "HERE" << endl;          

    sampleType = av[2];
    systematicType = "";
    cout << "Sample = "<<sampleType << endl;
    isMC = true;
    if (sampleType.find("Data") != std::string::npos){
	isMC = false;
    }

    std::string year(av[1]);
    tree = new EventTree(nFiles, false, year, !isMC, fileList);
    isSystematicRun = false;
    pos = sampleType.find("__");
    if (pos != std::string::npos){
	systematicType = sampleType.substr(pos+2,sampleType.length());
	sampleType = sampleType.substr(0,pos);
    }
    
    cout << sampleType << "  " << systematicType << endl;
    initCrossSections();
    if (isMC && crossSections.find(sampleType) == crossSections.end()) {
	if (sampleType.find("Test") == std::string::npos){
	    cout << "This is not an allowed sample, please specify one from this list (or add to this list in the code):" << endl;
	    for (auto const& pair: crossSections) {
		cout << "    " << pair.first << endl;
	    }
	    return;
	}
    }
    
    if (eventNum > -1) {
	string cut = "event=="+eventStr;
	cout << "Selecting only entries with " << cut << endl;
	tree->chain = (TChain*) tree->chain->CopyTree(cut.c_str());
    }
    //--------------------------
    //Pileup SFs
    //--------------------------
    //https://github.com/cms-nanoAOD/nanoAOD-tools/tree/master/python/postprocessing/data/pileup
    //PV data files
    std::map<std::string, string> puDataFiles;
    string comPuData = "weight/PileupSF/PileupHistogram-";
    puDataFiles["2016PreVFP"]  = comPuData+"UL2016-100bins_withVar.root"; 
    puDataFiles["2016PostVFP"] = comPuData+"UL2016-100bins_withVar.root";
    puDataFiles["2017"]        = comPuData+"UL2017-100bins_withVar.root";
    puDataFiles["2018"]        = comPuData+"UL2018-100bins_withVar.root";
    //PV MC files
    std::map<std::string, string> puMCFiles;
    string comPuMC = "weight/PileupSF/mcPileup";
    puMCFiles["2016PreVFP"]  = comPuMC+"UL2016.root";
    puMCFiles["2016PostVFP"] = comPuMC+"UL2016.root";
    puMCFiles["2017"]        = comPuMC+"UL2017.root";
    puMCFiles["2018"]        = comPuMC+"UL2018.root";
    //Initiate the pileup SF reader
	puSF = new PileupSF(puDataFiles[year], puMCFiles[year]);

    //--------------------------
    //Muon SFs
    //--------------------------
    //https://twiki.cern.ch/twiki/bin/view/CMS/MuonUL2016#High_pT_above_120_GeV
    //https://gitlab.cern.ch/cms-muonPOG/muonefficiencies/-/tree/master/Run2/UL
    //ID files
    std::map<std::string, string> muIDFiles;
    string comMu = "weight/MuSF/Efficiencies_muon_generalTracks_Z_"; 
    muIDFiles["2016PreVFP"]  = comMu+"Run2016_UL_HIPM_ID.root";
    muIDFiles["2016PostVFP"] = comMu+"Run2016_UL_ID.root";
    muIDFiles["2017"]        = comMu+"Run2017_UL_ID.root";
    muIDFiles["2018"]        = comMu+"Run2018_UL_ID.root";
    //Iso files
    std::map<std::string, string> muIsoFiles;
    muIsoFiles["2016PreVFP"]  = comMu+"Run2016_UL_HIPM_ISO.root";
    muIsoFiles["2016PostVFP"] = comMu+"Run2016_UL_ISO.root";
    muIsoFiles["2017"]        = comMu+"Run2017_UL_ISO.root";
    muIsoFiles["2018"]        = comMu+"Run2018_UL_ISO.root";
    //Trig file
    string muTrigFile = "weight/MuSF/OutFile-v20190510-Combined-Run2016BtoH_Run2017BtoF_Run2018AtoD-M120to10000.root";
    //Name of the histograms
    string muIDHist     = "NUM_HighPtID_DEN_TrackerMuons_abseta_pt";
    string muIsoHist    = "NUM_TightRelTkIso_DEN_HighPtIDandIPCut_abseta_pt";
    std::map<std::string, string> muTrigHists;
    muTrigHists["2016PreVFP"]  = "SF_2016";
    muTrigHists["2016PostVFP"] = "SF_2016";
    muTrigHists["2017"]        = "SF_2017";
    muTrigHists["2018"]        = "SF_2018";
    //Initiate the muon SF reader
	muSF = new MuonSF(muIDFiles[year], muIDHist, muIsoFiles[year], muIsoHist, muTrigFile, muTrigHists[year]);

    //--------------------------
    //Electron SFs
    //--------------------------
    //https://twiki.cern.ch/twiki/bin/view/CMS/EgammaUL2016To2018
    //ID files
    std::map<std::string, string> eIDFiles;
    string comEleID = "weight/EleSF/egammaEffi.txt_";
    eIDFiles["2016PreVFP"]  = comEleID+"Ele_wp80iso_preVFP_EGM2D.root"; 
    eIDFiles["2016PostVFP"] = comEleID+"Ele_wp80iso_postVFP_EGM2D.root"; 
    eIDFiles["2017"]        = comEleID+"EGM2D_MVA80iso_UL17.root"; 
    eIDFiles["2018"]        = comEleID+"Ele_wp80iso_EGM2D.root"; 
    //Reco files
    std::map<std::string, string> eRecoFiles;
    string comEleReco = "weight/EleSF/egammaEffi_ptAbove20.txt_EGM2D_"; 
    eRecoFiles["2016PreVFP"]  = comEleReco+"UL2016preVFP.root"; 
    eRecoFiles["2016PostVFP"] = comEleReco+"UL2016postVFP.root"; 
    eRecoFiles["2017"]        = comEleReco+"UL2017.root"; 
    eRecoFiles["2018"]        = comEleReco+"UL2018.root"; 
    //Trig files
    //These triggers are for legacy rereco. Need to evaluate them for UL using
    //https://hypernews.cern.ch/HyperNews/CMS/get/egamma-hlt/289.html
    std::map<std::string, string> eTrigFiles;
    eTrigFiles["2016PreVFP"]  = "weight/EleSF/electron_16.root";
    eTrigFiles["2016PostVFP"] = "weight/EleSF/electron_16.root";
    eTrigFiles["2017"]        = "weight/EleSF/electron_17.root";
    eTrigFiles["2018"]        = "weight/EleSF/electron_18.root";
    //Initiate the electron SF reader
	eleSF = new ElectronSF(eIDFiles[year], eRecoFiles[year], eTrigFiles[year]);

    //--------------------------
    //Photon SFs
    //--------------------------
    //https://twiki.cern.ch/twiki/bin/view/CMS/EgammaUL2016To2018
    //ID files
    std::map<std::string, string> phoIDFiles;
    string comPhoID = "weight/PhoSF/egammaEffi.txt_EGM2D_";
    phoIDFiles["2016PreVFP"]  = comPhoID+"Pho_wp80_UL16.root";
    phoIDFiles["2016PostVFP"] = comPhoID+"Pho_MVA80_UL16_postVFP.root";
    phoIDFiles["2017"]        = comPhoID+"PHO_MVA80_UL17.root";
    phoIDFiles["2018"]        = comPhoID+"Pho_wp80.root_UL18.root";
    //Electron veto (reject photon which has pixel seed)
    std::map<std::string, string> phoPSFiles;
    string comPhoPS = "weight/PhoSF/HasPix_SummaryPlot_";
    phoPSFiles["2016PreVFP"]  = comPhoPS+"UL16_preVFP.root";
    phoPSFiles["2016PostVFP"] = comPhoPS+"UL16_postVFP.root";
    phoPSFiles["2017"]        = comPhoPS+"UL17.root"; 
    phoPSFiles["2018"]        = comPhoPS+"UL18.root"; 
    //Electron veto (conversion safe EV)
    std::map<std::string, string> phoCSFiles;
    string comPhoCS = "weight/PhoSF/CSEV_SummaryPlot_";
    phoCSFiles["2016PreVFP"]  = comPhoCS+"UL16_preVFP.root";
    phoCSFiles["2016PostVFP"] = comPhoCS+"UL16_postVFP.root";
    phoCSFiles["2017"]        = comPhoCS+"UL17.root"; 
    phoCSFiles["2018"]        = comPhoCS+"UL18.root"; 
    //Initiate the phton SF reader
	phoSF = new PhotonSF(phoIDFiles[year], phoPSFiles[year], phoCSFiles[year]);

    //--------------------------
    //BTag SFs
    //--------------------------
    //https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation
    //https://gitlab.cern.ch/vanderli/btv-json-sf/-/tree/master/data
    //Hard coded the old calibration BTagCalibrationStandalone file and 
    //re-formatted the UL csv file: 
    //https://github.com/indra-ehep/KinFit_Skim/tree/9625ff1697693f4cc71813fe7f6b097643ae5166/CBA_Skim
    //deepCSV
    std::map<std::string, string> deepCSVFiles;
    string comCSV = "weight/BtagSF/wp_deepCSV_106X";
    deepCSVFiles["2016PreVFP"]  = comCSV+"UL16preVFP_v2_formatted.csv";
    deepCSVFiles["2016PostVFP"] = comCSV+"UL16postVFP_v3_formatted.csv";
    deepCSVFiles["2017"]        = comCSV+"UL17_v3_formatted.csv";
    deepCSVFiles["2018"]        = comCSV+"UL18_v2_formatted.csv";
    std::map<std::string, double> deepCSVWPs;//medium WPs
    deepCSVWPs["2016PreVFP"]  = 0.6001; 
    deepCSVWPs["2016PostVFP"] = 0.5847; 
    deepCSVWPs["2017"]        = 0.4506; 
    deepCSVWPs["2018"]        = 0.4168; 
    //deepJet
    std::map<std::string, string> deepJetFiles;
    string comJet = "weight/BtagSF/wp_deepJet_106X";
    deepJetFiles["2016PreVFP"]  = comJet+"UL16preVFP_v2_formatted.csv";
    deepJetFiles["2016PostVFP"] = comJet+"UL16postVFP_v3_formatted.csv";
    deepJetFiles["2017"]        = comJet+"UL17_v3_formatted.csv";
    deepJetFiles["2018"]        = comJet+"UL18_v2_formatted.csv";
    std::map<std::string, double> deepJetWPs;//medium WPs
    deepJetWPs["2016PreVFP"]  = 0.2598; 
    deepJetWPs["2016PostVFP"] = 0.2489; 
    deepJetWPs["2017"]        = 0.3040; 
    deepJetWPs["2018"]        = 0.2783; 
    
    //--------------------------
    //JES and JER SFs
    //--------------------------
    //https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC
    //https://github.com/cms-jet/JRDatabase/tree/master/textFiles
    //Partial file name here, full name in init_JER function
    std::map<std::string, string> jerFiles;
    string comJER = "weight/JetSF/JER/";
    jerFiles["2016PreVFP"]  = comJER+"Summer20UL16APV_JRV3";
    jerFiles["2016PostVFP"] = comJER+"Summer20UL16_JRV3";
    jerFiles["2017"]        = comJER+"Summer19UL17_JRV3";
    jerFiles["2018"]        = comJER+"Summer19UL18_JRV2";

    //https://github.com/cms-jet/JECDatabase/tree/master/textFiles
    std::map<std::string, string> jesFiles;
    string comJES = "weight/JetSF/JEC/"+year+"/";
    jesFiles["2016PreVFP"]  = comJES+"Summer19UL16APV_V7";
    jesFiles["2016PostVFP"] = comJES+"Summer19UL16_V7";
    jesFiles["2017"]        = comJES+"Summer19UL17_V5";
    jesFiles["2018"]        = comJES+"Summer19UL18_V5";
    
    //--------------------------
    //Luminosity
    //--------------------------
    std::map<std::string, double> lumiValues;
    lumiValues["2016PreVFP"]  = 19695.422959;
    lumiValues["2016PostVFP"] = 16226.452636;
    lumiValues["2017"]        = 41529.548819;
    lumiValues["2018"]        = 59740.565202;
    
    //--------------------------
    // t-tagging WPs
    //--------------------------
    //https://indico.cern.ch/event/1152827/contributions/4840404/attachments/2428856/4162159/ParticleNet_SFs_ULNanoV9_JMAR_25April2022_PK.pdf
    //For mis-tag rate of 0.5%
    std::map<std::string, double> topTagWPs;
    topTagWPs["2016PreVFP"]  = 0.74; 
    topTagWPs["2016PostVFP"] = 0.73; 
    topTagWPs["2017"]        = 0.80; 
    topTagWPs["2018"]        = 0.80; 
	topSF = new TopSF();
    
    selector = new Selector();
    evtPick = new EventPick("");
    selector->year = year;
    evtPick->year = year;
    selector->printEvent = eventNum;
    evtPick->printEvent = eventNum;
    evtPick->Njet_ge = 2;
    evtPick->NBjet_ge = 0;

    bool applyHemVeto=true; 
    selector->looseJetID = false;
    selector->useDeepCSVbTag = true;
    if (sampleType.find("Signal") != std::string::npos){
	selector->isSignal = true;
    }
    //FIXME//Use different UL samples for these
    bool isE0 = sampleType.find("QCD")!= std::string::npos;//nan in PDF
    bool isE1 = sampleType.find("WW") != std::string::npos;//nan in PDF
    bool isE2 = sampleType.find("WZ") != std::string::npos;//nan in PDF
    bool isE3 = sampleType.find("ZZ") != std::string::npos;//nan in PDF
    bool isE4 = sampleType.find("Signal_M") != std::string::npos;//ISR, FSR too large
    bool isE5 = sampleType.find("TTGamma_Hadronic_Pt200") != std::string::npos;//ISR, FSR too large
    selector->isQCD = isE0 || isE1 || isE2 || isE3 || isE4 || isE5; 

    selector->btag_cut_DeepCSV = deepCSVWPs[year]; 
    selector->topTagWP = topTagWPs[year];
    if (isMC){
    	selector->init_JER(jerFiles[year]);
    }
    BTagCalibration calib;
    if (!selector->useDeepCSVbTag){
	    calib = BTagCalibration("csvv2", deepJetFiles[year]); 
    } 
    else {
	    calib = BTagCalibration("csvv2", deepCSVFiles[year]); 
	    loadBtagEff(sampleType,year);
    }
    topEvent.SetBtagThresh(selector->btag_cut_DeepCSV);
    BTagCalibrationReader reader(BTagEntry::OP_MEDIUM,  // operating point
				 "central",             // central sys type
				 {"up", "down"});      // other sys types
    
    if (tree == 0) {
	std::cout <<"Tree not recognized" << endl;
    }
    reader.load(calib,                // calibration instance
		BTagEntry::FLAV_B,    // btag flavour
		"comb");               // measurement type
    reader.load(calib,                // calibration instance
		BTagEntry::FLAV_C,    // btag flavour
		"comb");               // measurement type
    reader.load(calib,                // calibration instance
		BTagEntry::FLAV_UDSG,    // btag flavour
		"incl");               // measurement type

    bool doOverlapInvert_TTG = false;
    bool doOverlapRemoval_TT = false;
    bool doOverlapInvert_WG = false;	
    bool doOverlapRemoval_W = false;	
    bool doOverlapInvert_ZG = false;	
    bool doOverlapRemoval_Z = false;	
    bool doOverlapInvert_TG = false;	
    bool doOverlapRemoval_Tchannel = false;	
    bool doOverlapRemoval_QCD = false;	
    bool doOverlapInvert_GJ = false;	
    
    bool invertOverlap = false;
    bool skipOverlap = false;
    bool lowPtTTGamma = false;
    if (sampleType.find("TTGamma")!= std::string::npos) {
        doOverlapInvert_TTG = true;
        if (sampleType=="TTGamma_SingleLept" || sampleType=="TTGamma_Dilepton" || sampleType=="TTGamma_Hadronic" ){
            lowPtTTGamma = true;
            cout << "Inclusive TTGamma sample, will remove high Pt photon events" << endl;
        }
    }    
    if (sampleType.find("TTbarPowheg")!= std::string::npos) {
	doOverlapRemoval_TT = true;
    }
    if (sampleType.find("TTGamma")!= std::string::npos) {
	doOverlapInvert_TTG = true;
    }    
    if( sampleType == "W1jets" || sampleType == "W2jets" ||  sampleType == "W3jets" || sampleType == "W4jets"){
	doOverlapRemoval_W = true;
    }
    if (sampleType.find("WGamma")!= std::string::npos) {
	doOverlapInvert_WG = true;
    }    
    if (sampleType=="DYjetsM10to50" || sampleType=="DYjetsM50" || sampleType=="DYjetsM10to50_MLM" || sampleType=="DYjetsM50_MLM"){
	doOverlapRemoval_Z = true;
    }
    if (sampleType.find("ZGamma")!= std::string::npos) {
	doOverlapInvert_ZG = true;
    }    
    
    if( sampleType == "ST_t-channel" || sampleType == "ST_tbar-channel") {
	doOverlapRemoval_Tchannel = true;
    }
    if (sampleType.find("TGJets")!= std::string::npos) {
	doOverlapInvert_TG = true;
    }    
    if (sampleType.find("GJets")!= std::string::npos) {
	doOverlapInvert_GJ = true;
    }    
    if ((sampleType.find("QCD")!= std::string::npos) ||(sampleType.find("bcToE")!= std::string::npos) ) {
	doOverlapRemoval_QCD = true;
    }    
    

    if(doOverlapRemoval_TT || doOverlapRemoval_W || doOverlapRemoval_Z || doOverlapRemoval_Tchannel || doOverlapRemoval_QCD) {
	std::cout << "########## Will apply overlap removal ###########" << std::endl;
    }
    if(doOverlapInvert_TTG || doOverlapInvert_WG || doOverlapInvert_ZG || doOverlapInvert_TG || doOverlapInvert_GJ) {
	std::cout << "##########   Will apply overlap inversion   ###########" << std::endl;
	std::cout << "########## Keeping only events with overlap ###########" << std::endl;
    }
    

    string JECsystLevel = "";
    if( systematicType.substr(0,3)=="JEC" ){
	int pos = systematicType.find("_");
	JECsystLevel = systematicType.substr(3,pos-3);
	if (std::end(allowedJECUncertainties) == std::find(std::begin(allowedJECUncertainties), std::end(allowedJECUncertainties), JECsystLevel)){
	    cout << "The JEC systematic source, " << JECsystLevel << ", is not in the list of allowed sources (found in JEC/UncertaintySourcesList.h" << endl;
	    cout << "Exiting" << endl;
	    return;
	}
	if (systematicType.substr(pos+1,2)=="up"){ jecvar012_g = 2; }
	if (systematicType.substr(pos+1,2)=="do"){ jecvar012_g = 0; }
	isSystematicRun = true;
    }
    
    bool isTTGamma = false;
    size_t ttgamma_pos = sampleType.find("TTGamma");
    if (ttgamma_pos != std::string::npos){
	isTTGamma = true;
    }
    if( systematicType=="JER_up")       {jervar012_g = 2; selector->JERsystLevel=2; isSystematicRun = true;}
    if( systematicType=="JER_down")     {jervar012_g = 0; selector->JERsystLevel=0; isSystematicRun = true;}
    if(systematicType=="phosmear_down") {phosmear012_g=0;selector->phosmearLevel=0; isSystematicRun = true;}
    if(systematicType=="phosmear_up")   {phosmear012_g=2;selector->phosmearLevel=2; isSystematicRun = true;}
    if(systematicType=="elesmear_down") {elesmear012_g=0;selector->elesmearLevel=0; isSystematicRun = true;}
    if(systematicType=="elesmear_up")   {elesmear012_g=2;selector->elesmearLevel=2; isSystematicRun = true;}
    if(systematicType=="phoscale_down") {phoscale012_g=0;selector->phoscaleLevel=0; isSystematicRun = true;} 
    if(systematicType=="phoscale_up")   {phoscale012_g=2;selector->phoscaleLevel=2; isSystematicRun = true;}
    if(systematicType=="elescale_down") {elescale012_g=0;selector->elescaleLevel=0; isSystematicRun = true;}
    if(systematicType=="elescale_up")   {elescale012_g=2;  selector->elescaleLevel=2; isSystematicRun = true;}

    // if( systematicType=="pho_up")       {phosmear012_g = 2;}
    // if( systematicType=="pho_down")     {phosmear012_g = 0;}
    if( systematicType=="musmear_up") {musmear012_g = 2; isSystematicRun = true;}
    if( systematicType=="musmear_do") {musmear012_g = 0; isSystematicRun = true;}
    //	if( systematicType=="elesmear_up")  {elesmear012_g = 2;}
    //	if( systematicType=="elesmear_down"){elesmear012_g = 0;}

    if(dilepSel)     {evtPick->Nmu_eq=2; evtPick->Nele_eq=2;}
    //    if( systematicType=="QCDcr")       {selector->QCDselect = true; evtPick->ZeroBExclusive=true; evtPick->QCDselect = true;}
    std::cout << "Dilepton Sample :" << dilepSel << std::endl;
    std::cout << "JEC: " << jecvar012_g << "  JER: " << jervar012_g << " eleScale "<< elescale012_g << " phoScale" << phoscale012_g << "   ";
    std::cout << "  PhoSmear: " << phosmear012_g << "  muSmear: " << musmear012_g << "  eleSmear: " << elesmear012_g << std::endl;
    if (dilepSel){
	evtPick->Njet_ge = 2;
	evtPick->NBjet_ge = 0;
    }

    if (isSystematicRun){
	std::cout << "  Systematic Run : Dropping genMC variables from tree" << endl;
    }

    std::string outputDirectory(av[3]);
    std::string outputFileName;
    if (nJob==-1){
	outputFileName = outputDirectory + "/" + sampleType+"_Ntuple.root";
    } else {
	outputFileName = outputDirectory + "/" + sampleType+"_Ntuple_"+to_string(nJob)+"of"+to_string(totJob)+".root";
    }
    // char outputFileName[100];
    cout << av[3] << " " << sampleType << " " << systematicType << endl;
    cout << outputDirectory<<"/"<<outputFileName << endl;
    TFile *outputFile = new TFile(outputFileName.c_str(),"recreate");
    outputTree = new TTree("AnalysisTree","AnalysisTree");
    cout << "HERE" << endl;
    tree->GetEntry(0);
    std::cout << "isMC: " << isMC << endl;

    InitBranches();
    JECvariation* jecvar;
    if (isMC && jecvar012_g!=1) {
	cout << "Applying JEC uncertainty variations : " << JECsystLevel << endl;
	jecvar = new JECvariation(jesFiles[year], isMC, JECsystLevel);
    }

    double nMC_total = 0.;
    char** fileNames = av+4;
    for(int fileI=0; fileI<ac-4; fileI++){
        TFile *_file = TFile::Open(fileNames[fileI],"read");
        TH1D *hEvents = (TH1D*) _file->Get("hEvents");
        nMC_total += (hEvents->GetBinContent(2)); 
    }
    if (nMC_total==0){
	    nMC_total=1;
    }
    _lumiWeight = getEvtWeight(sampleType, lumiValues[year], nMC_total);
    Long64_t nEntr = tree->GetEntries();
    bool saveAllEntries = false;
    if (sampleType=="Test") {
	if (nEntr > 20000) nEntr = 20000;
    }
    if (sampleType=="TestFull") {
	nEntr = tree->GetEntries();
    }
    if (sampleType=="TestAll") {
	if (nEntr > 1000) nEntr = 10;
	saveAllEntries = true;
    }

    int count_overlap=0;
    int count_HEM=0;

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
    //--------------------------
    //Event for loop
    //--------------------------
    cout << "Processing events "<<startEntry<< " to " << endEntry << endl;
    std::cout<<"nEvents_Skim = "<<endEntry<<endl;
    std::cout<<"---------------------------"<<std::endl;
    std::cout<<setw(10)<<"Progress"<<setw(10)<<"Time"<<std::endl;
    std::cout<<"---------------------------"<<std::endl;
    double totalTime = 0.0;
    for(Long64_t entry=startEntry; entry<endEntry; entry++){
        //if(entry>100000) break;;
        //--------------------------
        //print event after each 1%
        //--------------------------
        bool isPrint = false;
        if(eventsPerJob > 100){
            isPrint = (entry%(eventsPerJob/100) == 0);
        }else{
            isPrint = true;
        }
        if(isPrint){
            totalTime+= std::chrono::duration<double>(std::chrono::high_resolution_clock::now()-startClock).count();
            int sec = (int)(totalTime)%60;
            int min = (int)(totalTime)/60;
        	std::cout<<setw(10)<<100*entry/endEntry<<" %"<<setw(10)<<min<<"m "<<sec<<"s"<<std::endl;
            startClock = std::chrono::high_resolution_clock::now();			
        }
        tree->GetEntry(entry);

        //--------------------------
        //Apply overlap removal
        //--------------------------
        if( isMC && doOverlapInvert_TTG){
            if (!overlapRemoval(tree, 10., 5., 0.1, tree->event_==eventNum)){
        	    count_overlap++;			
        	    continue;
            }
            // remove events with LHEPart photon with pt>100 
            //GeV to avoid double counting with high pt samples
            if (lowPtTTGamma){
                for (int lheind = 0; lheind < tree->nLHEPart_; lheind++){
                    if (tree->LHEPart_pdgId_[lheind]==22 && tree->LHEPart_pt_[lheind]>100.){
                        continue;
                    }
                }
            }
        }
        if( isMC && doOverlapRemoval_TT){
            if (!invertOverlap){
                if (overlapRemoval(tree, 10., 5., 0.1, tree->event_==eventNum)){
                    count_overlap++;			
                    continue;
                }
            } else {
                if (!overlapRemoval(tree, 10., 5., 0.1, tree->event_==eventNum)){
                    count_overlap++;			
                    continue;
                }
            }
        }

        if( isMC && doOverlapRemoval_W){
            if (overlapRemoval(tree, 15., 2.6, 0.05, tree->event_==eventNum)){
                count_overlap++;
                continue;
            }
        }
        if( isMC && doOverlapInvert_WG){
            if (!overlapRemoval(tree, 15., 2.6, 0.05, tree->event_==eventNum)){
        	    count_overlap++;			
        	    continue;
            }
        }
        if( isMC && doOverlapRemoval_Z){
            if (overlapRemoval(tree, 15., 2.6, 0.05, tree->event_==eventNum)){
                count_overlap++;
                continue;
            }
        }
        if( isMC && doOverlapInvert_ZG){
            if (!overlapRemoval(tree, 15., 2.6, 0.05, tree->event_==eventNum)){
        	    count_overlap++;
        	    continue;
            }
        }
        if( isMC && doOverlapRemoval_Tchannel){
            if (overlapRemoval_2To3(tree, 10., 2.6, 0.05, tree->event_==eventNum)){
        	    count_overlap++;
        	    continue;
            }
        }
        if( isMC && doOverlapInvert_TG){
            if (!overlapRemoval_2To3(tree, 10., 2.6, 0.05, tree->event_==eventNum)){
        	    count_overlap++;
        	    continue;
            }
        }
        if( isMC && doOverlapInvert_GJ){
            if (!overlapRemoval(tree, 25., 2.5, 0.4, tree->event_==eventNum)){
        	    count_overlap++;
        	    continue;
            }
        }
        if( isMC && doOverlapRemoval_QCD){
            if (overlapRemoval(tree, 25., 2.5, 0.4, tree->event_==eventNum)){
        	    count_overlap++;
        	    continue;
            }
        }

        //--------------------------
        //Apply HEM veto
        //--------------------------
        _inHEMVeto = false;
        int nHEM_ele=0;
        bool HEM_ele_Veto=false;
        for(int eleInd = 0; eleInd < tree->nEle_; ++eleInd){
            double eta = tree->eleEta_[eleInd];
            double pt = tree->elePt_[eleInd];
            double phi = tree->elePhi_[eleInd];
            bool ele_HEM_pt_pass  = pt >= 15 ;
            bool ele_HEM_eta_pass = eta > -3.0 && eta < -1.4 ;
            bool ele_HEM_phi_pass = phi > -1.57 && phi < -0.87;
            if ( ele_HEM_pt_pass &&  ele_HEM_eta_pass &&  ele_HEM_phi_pass) nHEM_ele++;
        }
        HEM_ele_Veto=(nHEM_ele>=1);
        int nHEM_pho=0;
        bool HEM_pho_Veto=false;
        for(int phoInd = 0; phoInd < tree->nPho_; ++phoInd){
            double et = tree->phoEt_[phoInd];
            double eta = tree->phoEta_[phoInd];
            double phi = tree->phoPhi_[phoInd];
            bool pho_HEM_eta_pass =  eta > -3.0   && eta < -1.4 ;
            bool pho_HEM_et_pass =  et >= 15;
            bool pho_HEM_phi_pass = phi > -1.57  && phi < -0.87 ;
            if (pho_HEM_eta_pass && pho_HEM_phi_pass && pho_HEM_et_pass) {nHEM_pho++ ;}
        }
        HEM_pho_Veto= (nHEM_pho>=1);
        _inHEMVeto=(applyHemVeto && (HEM_pho_Veto || HEM_ele_Veto) && year=="2018");
        if(_isData &&  tree->run_>=319077 && _inHEMVeto){ 
            count_HEM++;
            continue; 
        }

        //--------------------------
        //Process events
        //--------------------------
        if( isMC ){
            if (jecvar012_g != 1){
        	jecvar->applyJEC(tree, jecvar012_g); // 0:down, 1:norm, 2:up
            }
        }
        selector->clear_vectors();
        evtPick->process_event(tree, selector);
        if (tree->event_==eventNum){
            cout << "EventSelection:" << endl;
            cout << "  PassPresel e " << evtPick->passPreselEle << endl;
            cout << "  PassPresel mu" << evtPick->passPreselMu<< endl;
        }
        //--------------------------
        //Presel for loop
        //--------------------------
        if ( evtPick->passPreselEle || evtPick->passPreselMu || saveAllEntries) {
            InitVariables();
            FillEvent(year); 
            //--------------------------
            //Apply MC weight
            //--------------------------
            if(isMC) {
                vector<double> puWeights; 
                puWeights = puSF->getPuSFs(tree->nPUTrue_, tree->event_==eventNum);
                _PUweight_Do = puWeights.at(0); 
                _PUweight    = puWeights.at(1); 
                _PUweight_Up = puWeights.at(2);
        
                _btagWeight_1a      = getBtagSF_1a("central", reader, tree->event_==eventNum);
                _btagWeight_1a_b_Up = getBtagSF_1a("b_up",    reader);
                _btagWeight_1a_b_Do = getBtagSF_1a("b_down",  reader);
                _btagWeight_1a_l_Up = getBtagSF_1a("l_up",    reader);
                _btagWeight_1a_l_Do = getBtagSF_1a("l_down",  reader);
                if (evtPick->passPreselMu) {
                    vector<double> muWeights;
                    vector<double> muWeights_Do;
                    vector<double> muWeights_Up;    
                    int muInd_ = selector->Muons.at(0);
                    muWeights    = muSF->getMuSFs(tree->muPt_[muInd_],tree->muEta_[muInd_],1, tree->event_==eventNum);
                	muWeights_Do = muSF->getMuSFs(tree->muPt_[muInd_],tree->muEta_[muInd_],0);
                	muWeights_Up = muSF->getMuSFs(tree->muPt_[muInd_],tree->muEta_[muInd_],2);
                    _muEffWeight    = muWeights.at(0);
                    _muEffWeight_Up = muWeights_Up.at(0);
                    _muEffWeight_Do = muWeights_Do.at(0);
                    
                    _muEffWeight_Id    = muWeights.at(1)    ;
                    _muEffWeight_Id_Up = muWeights_Up.at(1) ;
                    _muEffWeight_Id_Do = muWeights_Do.at(1) ;
                    
                    _muEffWeight_Iso    = muWeights.at(2)   ;
                    _muEffWeight_Iso_Up = muWeights_Up.at(2);
                    _muEffWeight_Iso_Do = muWeights_Do.at(2);
                    
                    _muEffWeight_Trig    = muWeights.at(3);
                    _muEffWeight_Trig_Up = muWeights_Up.at(3);
                    _muEffWeight_Trig_Do = muWeights_Do.at(3);
                }
                if (evtPick->passPreselEle) {
                    int eleInd_ = selector->Electrons.at(0);
                    vector<double> eleWeights    = eleSF->getEleSFs(tree->elePt_[eleInd_],tree->eleEta_[eleInd_] + tree->eleDeltaEtaSC_[eleInd_],1, tree->event_==eventNum);
                    vector<double> eleWeights_Do = eleSF->getEleSFs(tree->elePt_[eleInd_],tree->eleEta_[eleInd_] + tree->eleDeltaEtaSC_[eleInd_],0);
                    vector<double> eleWeights_Up = eleSF->getEleSFs(tree->elePt_[eleInd_],tree->eleEta_[eleInd_] + tree->eleDeltaEtaSC_[eleInd_],2);
                
                
                    _eleEffWeight    = eleWeights.at(0);
                    _eleEffWeight_Do = eleWeights_Do.at(0);
                    _eleEffWeight_Up = eleWeights_Up.at(0);
                
                    _eleEffWeight_Id    = eleWeights.at(1)   ;
                    _eleEffWeight_Id_Do = eleWeights_Do.at(1);
                    _eleEffWeight_Id_Up = eleWeights_Up.at(1);
                
                    _eleEffWeight_Reco    = eleWeights.at(2)    ;
                    _eleEffWeight_Reco_Do = eleWeights_Do.at(2) ;
                    _eleEffWeight_Reco_Up = eleWeights_Up.at(2) ;
                
                    _eleEffWeight_Trig    = eleWeights.at(3);
                    _eleEffWeight_Trig_Do = eleWeights_Do.at(3);
                    _eleEffWeight_Trig_Up = eleWeights_Up.at(3);
        	    }
                //https://twiki.cern.ch/twiki/bin/viewauth/CMS/L1ECALPrefiringWeightRecipe
                if (year=="2016PreVFP" || year=="2016PostVFP" || year=="2017"){
                    _prefireSF_Do   = tree->prefireDn_;
                    _prefireSF      = tree->prefireNom_; 
                    _prefireSF_Up   = tree->prefireUp_; 
                }
            }//isMC 
        
            //--------------------------
            //Fill tree
            //--------------------------
            outputTree->Fill();
            if (tree->event_==eventNum){
                cout << "--------------------------------------------" << endl;
                cout << "Scale Factor Summary" << endl;
                cout << std::setprecision(10) << "  evtWeight="<<_evtWeight <<  _btagWeight_1a << "  eleEffWeight="<<_eleEffWeight<<"  muEffWeight="<<_muEffWeight;
                if (_phoEffWeight.size()>0){
                    cout <<"  phoEffWeight="<<_phoEffWeight.at(0);
                }
                cout << "  prefire="<<_prefireSF;
                cout << "  PUscale="<<_PUweight;
                cout<<endl;
            }
        }//presel loop
    }//event for loop
   
    //--------------------------
    //Write tree to the outfile
    //--------------------------
    if (doOverlapRemoval_TT){
	std::cout << "Total number of events removed from TTbar:"<< count_overlap <<std::endl;
    }
    if(doOverlapRemoval_W || doOverlapRemoval_Z){
	std::cout << "Total number of events removed from W/ZJets:"<< count_overlap <<std::endl;
    }
    if(doOverlapRemoval_Tchannel){
	std::cout << "Total number of events removed from t-channel:"<< count_overlap <<std::endl;
    }
    if (doOverlapInvert_TTG){
	std::cout << "Total number of events removed from TTGamma:"<< count_overlap <<std::endl;
    }
    if (doOverlapInvert_WG || doOverlapInvert_ZG){
	std::cout << "Total number of events removed from W/Z+Gamma:"<< count_overlap <<std::endl;
    }
    if (doOverlapInvert_TG){
	std::cout << "Total number of events removed from TGJets:"<< count_overlap <<std::endl;
    }
    if (doOverlapRemoval_QCD){
	std::cout << "Total number of events removed from QCD:"<< count_overlap <<std::endl;
    }
    if (doOverlapInvert_GJ){
	std::cout << "Total number of events removed from GJets:"<< count_overlap <<std::endl;
    }
    std:cout << "Total number of HEM events removed from Data  = "<<count_HEM<<std::endl;
    outputFile->cd();
    std::cout<<"nEvents_Ntuple = "<<outputTree->GetEntries()<<endl;
    outputTree->Write();
   /* 
    TNamed gitCommit("Git_Commit", VERSION);
    TNamed gitTime("Git_Commit_Time", COMMITTIME);
    TNamed gitBranch("Git_Branch", BRANCH);
    TNamed gitStatus("Git_Status", STATUS);

    gitCommit.Write();
    gitTime.Write();
    gitBranch.Write();
    gitStatus.Write();
    */
    outputFile->Close();
}


void makeNtuple::FillEvent(std::string year){
    _run             = tree->run_;
    _event           = tree->event_;
    _lumis           = tree->lumis_;
    _isData	         = !isMC;
    if (isMC){
	    _genWeight       = tree->genWeight_/abs(tree->genWeight_); 
        _evtWeight       = _lumiWeight * _genWeight;
        if(_inHEMVeto)_evtWeight = _evtWeight*0.3518;
    }
    else{
	    _evtWeight= 1.;
    }

    _pfMET		     = tree->MET_pt_;
    _pfMETPhi    	 = tree->MET_phi_;
    
    _nPho		     = selector->Photons.size();
    _nLoosePho	     = selector->LoosePhotons.size();
    _nPhoNoID	     = selector->PhotonsNoID.size();
    _nEle		     = selector->Electrons.size();
    _nEleLoose       = selector->ElectronsLoose.size();
    _nMu		     = selector->Muons.size();
    _nMuLoose        = selector->MuonsLoose.size();
    
    _nJet            = selector->Jets.size();
    _nFatJet         = selector->FatJets.size();
    _nBJet           = selector->bJets.size();

    double ht = 0.0;
    for( int i_jet = 0; i_jet < _nJet; i_jet++){
	    ht += tree->jetPt_[i_jet];
    }
    _HT = ht; 

    double lt = 0.0;
    for (int i_ele = 0; i_ele <_nEle; i_ele++){
        int eleInd = selector->Electrons.at(i_ele);
        _elePt.push_back(tree->elePt_[eleInd]);
        _elePhi.push_back(tree->elePhi_[eleInd]);
        _eleEta.push_back(tree->eleEta_[eleInd]);
        _eleSCEta.push_back(tree->eleEta_[eleInd] + tree->eleDeltaEtaSC_[eleInd]);
        _elePFRelIso.push_back(tree->eleMiniPFRelIso_[eleInd]);
        lepVector.SetPtEtaPhiM(tree->elePt_[eleInd],
        		       tree->eleEta_[eleInd],
        		       tree->elePhi_[eleInd],
        		       tree->eleMass_[eleInd]);
        lepCharge=tree->eleCharge_[eleInd];
        lt += tree->elePt_[eleInd];
    }

    for (int i_mu = 0; i_mu <_nMu; i_mu++){
        int muInd = selector->Muons.at(i_mu);
        _muPt.push_back(tree->muPt_[muInd]);
        _muPhi.push_back(tree->muPhi_[muInd]);
        _muEta.push_back(tree->muEta_[muInd]);
        _muTkRelIso.push_back(tree->muTkRelIso_[muInd]);
        
        lepVector.SetPtEtaPhiM(tree->muPt_[muInd],
        		       tree->muEta_[muInd],
        		       tree->muPhi_[muInd],
        		       tree->muMass_[muInd]);
        lepCharge=tree->muCharge_[muInd];
        lt += tree->muPt_[muInd];
    }
    _ST = ht + lt + tree->MET_pt_;
	
    if (dilepSel){
	if (_nMu==2) {
	    int muInd1 = selector->Muons.at(0);
	    int muInd2 = selector->Muons.at(1);

	    lepVector.SetPtEtaPhiM(tree->muPt_[muInd1],
				   tree->muEta_[muInd1],
				   tree->muPhi_[muInd1],
				   tree->muMass_[muInd1]);
	    lepVector2.SetPtEtaPhiM(tree->muPt_[muInd2],
				    tree->muEta_[muInd2],
				    tree->muPhi_[muInd2],
				    tree->muMass_[muInd2]);	
        _DilepMass = (lepVector+lepVector2).M();
        _DilepDelR = lepVector.DeltaR(lepVector2);
	}
	
	
	if (_nEle==2){
	    int eleInd1 = selector->Electrons.at(0);
	    int eleInd2 = selector->Electrons.at(1);
	    
	    lepVector.SetPtEtaPhiM(tree->elePt_[eleInd1],
				   tree->eleEta_[eleInd1],
				   tree->elePhi_[eleInd1],
				   tree->eleMass_[eleInd1]);
	    lepVector2.SetPtEtaPhiM(tree->elePt_[eleInd2],
				    tree->eleEta_[eleInd2],
				    tree->elePhi_[eleInd2],
				    tree->eleMass_[eleInd2]);
        _DilepMass = (lepVector+lepVector2).M();
        _DilepDelR = lepVector.DeltaR(lepVector2);
	}
    }
    
    //dipho Mass
    if (_nPho>1){
        //	std::cout<<_nPho<<std::endl;
        int phoInd1 = selector->Photons.at(0);
        int phoInd2 = selector->Photons.at(1);
        
        phoVector1.SetPtEtaPhiM(tree->phoEt_[phoInd1],
        			tree->phoEta_[phoInd1],
        			tree->phoPhi_[phoInd1],
        			0.0);
        phoVector2.SetPtEtaPhiM(tree->phoEt_[phoInd2],
        			tree->phoEta_[phoInd2],
        			tree->phoPhi_[phoInd2],
        			0.0);
    _DiphoMass = (phoVector1+phoVector2).M();
    }
	
    _passPresel_Ele  = evtPick->passPreselEle;
    _passPresel_Mu   = evtPick->passPreselMu;
    int parentPID = -1;
    phoVectors.clear();
    if (tree->event_==eventNum) {
	cout <<"Photon Info" << endl; 
    }
    for (int i_pho = 0; i_pho <_nPho; i_pho++){
        int phoInd = selector->Photons.at(i_pho);
        _ST += tree->phoEt_[phoInd];
        phoVector.SetPtEtaPhiM(tree->phoEt_[phoInd],
        		       tree->phoEta_[phoInd],
        		       tree->phoPhi_[phoInd],
        		       0.0);
        phoVectors.push_back(phoVector);
        _phoEt.push_back(tree->phoEt_[phoInd]);
        _phoEta.push_back(tree->phoEta_[phoInd]);
        _phoPhi.push_back(tree->phoPhi_[phoInd]);
        _phoPFRelIso.push_back( tree->phoPFRelIso_[phoInd]);
        
        if (tree->isData_){
            _phoEffWeight.push_back(1.);
            _phoEffWeight_Do.push_back(1.);
            _phoEffWeight_Up.push_back(1.);
        } else {
            vector<double> phoWeights = phoSF->getPhoSFs(tree->phoEt_[phoInd],tree->phoEta_[phoInd],1, tree->event_==eventNum);
            vector<double> phoWeights_Do = phoSF->getPhoSFs(tree->phoEt_[phoInd],tree->phoEta_[phoInd],0, tree->event_==eventNum);
            vector<double> phoWeights_Up = phoSF->getPhoSFs(tree->phoEt_[phoInd],tree->phoEta_[phoInd],2, tree->event_==eventNum);
        
            _phoEffWeight.push_back(phoWeights.at(0));
            _phoEffWeight_Do.push_back(phoWeights_Do.at(0));
            _phoEffWeight_Up.push_back(phoWeights_Up.at(0));
        
            _phoEffWeight_Id.push_back(phoWeights.at(1));
            _phoEffWeight_Id_Do.push_back(phoWeights_Do.at(1));
            _phoEffWeight_Id_Up.push_back(phoWeights_Up.at(1));
        
            _phoEffWeight_PS.push_back(phoWeights.at(2));
            _phoEffWeight_PS_Do.push_back(phoWeights_Do.at(2));
            _phoEffWeight_PS_Up.push_back(phoWeights_Up.at(2));

            _phoEffWeight_CS.push_back(phoWeights.at(3));
            _phoEffWeight_CS_Do.push_back(phoWeights_Do.at(3));
            _phoEffWeight_CS_Up.push_back(phoWeights_Up.at(3));
        }
        _phoMassLepGamma.push_back( (phoVector+lepVector).M() );

        //Photon categorization
        bool isGenuine = false;
        bool isMisIDEle = false;
        bool isHadronicPhoton = false;
        bool isHadronicFake = false;
        bool isPUPhoton = false;
        int phoGenMatchInd = -1.;
        if (!tree->isData_){
            phoGenMatchInd = tree->phoGenPartIdx_[phoInd];
            _phoGenMatchInd.push_back(phoGenMatchInd);
            findPhotonCategory(phoInd, tree, &isGenuine, &isMisIDEle, &isHadronicPhoton, &isHadronicFake, &isPUPhoton,tree->event_==eventNum); //as we are using phogenmatch defined in nanontuple
            if (tree->event_==eventNum){
            cout << endl;
            cout << "        Genuine: "<<isGenuine << endl;
            cout << "        MisID:   "<<isMisIDEle << endl;
            cout << "        Hadronic:"<<isHadronicPhoton << endl;
            cout << "        Fake:    "<<isHadronicFake << endl;
            cout << "        PUPhoton:"<<isPUPhoton << endl;
            }
            _photonIsGenuine.push_back((int)isGenuine);
            _photonIsMisIDEle.push_back((int)isMisIDEle);
            _photonIsHadronicPhoton.push_back((int)isHadronicPhoton);
            _photonIsHadronicFake.push_back((int)(isHadronicFake || isPUPhoton));
            
        }//isMC
        _dRPhotonLepton.push_back(phoVector.DeltaR(lepVector));
        _MPhotonLepton.push_back((phoVector+lepVector).M());
    }//phoLoop
    
    for (int i_pho = 0; i_pho <_nLoosePho; i_pho++){
        int phoInd = selector->LoosePhotons.at(i_pho);
        phoVector.SetPtEtaPhiM(tree->phoEt_[phoInd],
        		       tree->phoEta_[phoInd],
        		       tree->phoPhi_[phoInd],
        		       0.0);
        
        int phoGenMatchInd = -1.;
        if (!tree->isData_){
            phoGenMatchInd = tree->phoGenPartIdx_[phoInd];
        }
    }

    for (int i_pho = 0; i_pho <_nPhoNoID; i_pho++){
        int phoInd = selector->PhotonsNoID.at(i_pho);
        phoVector.SetPtEtaPhiM(tree->phoEt_[phoInd],
        		       tree->phoEta_[phoInd],
        		       tree->phoPhi_[phoInd],
        		       0.0);
        int phoGenMatchInd = -1.;
    }

    jetVectors.clear();
    fatJetVectors.clear();
    jetResolutionVectors.clear();
    jetBtagVectors.clear();
    for (int i_fatJet = 0; i_fatJet <_nFatJet; i_fatJet++){
        int fatJetInd = selector->FatJets.at(i_fatJet);
        int topSFInd = selector->FatJets.at(0);
        //std::cout<<tree->fatJetPt_[fatJetInd]<<std::endl;
        _fatJetPt.push_back(          tree->fatJetPt_[fatJetInd]);
        _fatJetEta.push_back(         tree->fatJetEta_[fatJetInd]);
        _fatJetPhi.push_back(         tree->fatJetPhi_[fatJetInd]);
        _fatJetMass.push_back(        tree->fatJetMass_[fatJetInd]);
        _fatJetMassSoftDrop.push_back(tree->fatJetMassSoftDrop_[fatJetInd]);
        fatJetVector.SetPtEtaPhiM(tree->fatJetPt_[fatJetInd], 
                tree->fatJetEta_[fatJetInd], 
                tree->fatJetPhi_[fatJetInd], 
                tree->fatJetMass_[fatJetInd]);
        fatJetVectors.push_back(fatJetVector);
	    if(isMC) {
            vector<double> TopWeights; 
            TopWeights = topSF->getTopSFs(year,tree->fatJetPt_[topSFInd], tree->event_==eventNum);
            _TopWeight_Do = TopWeights.at(0); 
            _TopWeight    = TopWeights.at(1); 
            _TopWeight_Up = TopWeights.at(2);
        }
    }
    for (int i_jet = 0; i_jet <_nJet; i_jet++){
        int jetInd = selector->Jets.at(i_jet);
        _jetPt.push_back(tree->jetPt_[jetInd]);
        _jetQGL.push_back(tree->jetQGL_[jetInd]);
        _jetEta.push_back(tree->jetEta_[jetInd]);
        _jetPhi.push_back(tree->jetPhi_[jetInd]);
        _jetMass.push_back(tree->jetMass_[jetInd]);
        _jetCSVV2.push_back(tree->jetBtagCSVV2_[jetInd]);
        _jetDeepB.push_back(tree->jetBtagDeepB_[jetInd]);
        _jetGenJetIdx.push_back(tree->jetGenJetIdx_[jetInd]);
        double resolution = selector->jet_resolution.at(i_jet);
        _jetRes.push_back(resolution);
        _jerWeight.push_back(selector->jet_smear.at(i_jet));
	    if (jecvar012_g != 1)_jesWeight.push_back(tree->jetmuEF_[jetInd]);
        else _jesWeight.push_back(1.0);
        jetResolutionVectors.push_back(resolution);
        jetBtagVectors.push_back(tree->jetBtagDeepB_[jetInd]);
        jetVector.SetPtEtaPhiM(tree->jetPt_[jetInd], 
                tree->jetEta_[jetInd], 
                tree->jetPhi_[jetInd], 
                tree->jetMass_[jetInd]);
        jetVectors.push_back(jetVector);
        if (selector->jet_isTagged.at(i_jet)){
            bjetVectors.push_back(jetVector);
            bjetResVectors.push_back(resolution);
        } else {
            ljetVectors.push_back(jetVector);
            ljetResVectors.push_back(resolution);
        }
    }	
    // // // Calculate MET z
     metZ.SetLepton(lepVector);
    METVector.SetPtEtaPhiM(tree->MET_pt_,
    			   0.,
    			   tree->MET_phi_,
    			   0.);
     metZ.SetMET(METVector);
    _WtransMass = TMath::Sqrt(2*lepVector.Pt()*tree->MET_pt_*( 1.0 - TMath::Cos( lepVector.DeltaPhi(METVector))));
    double _met_px = METVector.Px();
    double _met_py = METVector.Py();
    topEvent.SetJetVector(jetVectors);
    topEvent.SetFatJetVector(fatJetVectors);
    topEvent.SetJetResVector(jetResolutionVectors);
    topEvent.SetBtagVector(jetBtagVectors);
    topEvent.SetLepton(lepVector);
    topEvent.SetMET(METVector);
    topEvent.SetPhotonVector(phoVectors);

    if (tree->event_==eventNum){
        cout << "------------------------------" << endl;
        cout << "Event Reconstruction" << endl;
        cout << "   nFatJet "<<_nFatJet << endl;
        cout << "   nJet    "<<_nJet << endl;
    }
    if (_nFatJet==0){
        topEvent.CalculateTstarGluGamma(5);
        if (topEvent.GoodCombinationTstarGluGamma()){
            bhad = jetVectors[topEvent.getBHad()];
            blep = jetVectors[topEvent.getBLep()];
            Wj1 = jetVectors[topEvent.getJ1()];
            Wj2 = jetVectors[topEvent.getJ2()];
            if (topEvent.getPhotonSide()){ //photon is on leptonic side
                hadDecay = jetVectors[topEvent.getG()];
                lepDecay = phoVectors[topEvent.getPho()];
            }else{ //photon is on hadronic side
                hadDecay = phoVectors[topEvent.getPho()];
                lepDecay = jetVectors[topEvent.getG()];
            }

            METVector.SetXYZM(METVector.Px(), METVector.Py(), topEvent.getNuPz(), 0);
            _chi2 = topEvent.getChi2_TstarGluGamma();
            _M_jj  = ( Wj1 + Wj2 ).M();
            _TopHad_mass = (bhad + Wj1 + Wj2).M();
            _TopLep_mass = (blep + lepVector + METVector).M();
            //Hadronic Tstar
            TLorentzVector Reco_hadT = bhad + Wj1 + Wj2 + hadDecay;
            _Reco_eta_hadT     = Reco_hadT.Eta();
            _Reco_pt_hadT      = Reco_hadT.Pt();
            _Reco_phi_hadT     = Reco_hadT.Phi();
            _TopStarHad_mass   = Reco_hadT.M();
            //Leptonic Tstar
            TLorentzVector Reco_lepT = blep + lepVector + METVector + lepDecay;
            _Reco_eta_lepT     = Reco_lepT.Eta();
            _Reco_pt_lepT      = Reco_lepT.Pt();
            _Reco_phi_lepT     = Reco_lepT.Phi();
            _TopStarLep_mass   = Reco_lepT.M();
            //Combined TT
            _Reco_dr_TT     = Reco_hadT.DeltaR(Reco_lepT);
            _tgtg_mass      = (Reco_hadT + Reco_lepT).M();
            _TopStar_mass   = (_TopStarHad_mass + _TopStarLep_mass)/2.;

            if (tree->event_==eventNum){
                cout << "  Resolved Case " << endl;
                cout << "    BHad: Idx=" << topEvent.getBHad() << " Pt=" << bhad.Pt() << endl;
                cout << "    BLep: Idx=" << topEvent.getBLep() << " Pt=" << blep.Pt() << endl;
                cout << "    Wj1: Idx=" << topEvent.getJ1() << " Pt=" << Wj1.Pt() << endl;
                cout << "    Wj2: Idx=" << topEvent.getJ2() << " Pt=" << Wj2.Pt() << endl;
                cout << "    Glu: Idx=" << topEvent.getG() << " Pt=" << jetVectors[topEvent.getG()].Pt() << endl;
                if (topEvent.getPhotonSide()){
                    cout << "    Photon on leptonic decay side" << endl;
                } else {
                    cout << "    Photon on hadronic decay side" << endl;
                }
                cout << "    ----" << endl;
                cout << "    chi2="<<_chi2 << endl;
                cout << "    Tmass(Had)="<<_TopStarHad_mass << endl;
                cout << "    Tmass(Lep)="<<_TopStarLep_mass << endl;
                cout << "    Tmass  = "<<_TopStar_mass << endl;
            }
        }
    } else {
        topEvent.CalculateTstarGluGamma_Boosted(2);
        if (topEvent.GoodCombinationTstarGluGamma()){
            blep = jetVectors[topEvent.getBLep()];
            topHad = fatJetVectors[topEvent.getTHad()];
            //std::cout<<"jetHadFlvr_= "<<abs(tree->jetHadFlvr_[topEvent.getBLep()])<<std::endl;

            if (topEvent.getPhotonSide()){ //photon is on leptonic side
                hadDecay = jetVectors[topEvent.getG()];
                lepDecay = phoVectors[topEvent.getPho()];
            }else{ //photon is on hadronic side
                hadDecay = phoVectors[topEvent.getPho()];
                lepDecay = jetVectors[topEvent.getG()];
            }

            METVector.SetXYZM(METVector.Px(), METVector.Py(), topEvent.getNuPz(), 0);
            _chi2 = topEvent.getChi2_TstarGluGamma();
            _TopHad_mass = (topHad).M();
            _TopLep_mass = (blep + lepVector + METVector).M();
            //Hadronic Tstar
            TLorentzVector Reco_hadT = topHad + hadDecay;
            _Reco_eta_hadT     = Reco_hadT.Eta();
            _Reco_pt_hadT      = Reco_hadT.Pt();
            _Reco_phi_hadT     = Reco_hadT.Phi();
            _TopStarHad_mass   = Reco_hadT.M();
            //Leptonic Tstar
            TLorentzVector Reco_lepT = blep + lepVector + METVector + lepDecay;
            _Reco_eta_lepT     = Reco_lepT.Eta();
            _Reco_pt_lepT      = Reco_lepT.Pt();
            _Reco_phi_lepT     = Reco_lepT.Phi();
            _TopStarLep_mass   = Reco_lepT.M();
            //Combined TT
            _Reco_dr_TT     = Reco_hadT.DeltaR(Reco_lepT);
            _tgtg_mass      = (Reco_hadT + Reco_lepT).M();
            _TopStar_mass   = (_TopStarHad_mass + _TopStarLep_mass)/2.;
            _M_jj  = -9999.0; //In the boosted category, we don't reconstruct W_had

            if (tree->event_==eventNum){
                cout << "  Resolved Case " << endl;
                cout << "    BLep: Idx=" << topEvent.getBLep() << " Pt=" << blep.Pt() << endl;
                cout << "    THad: Idx=" << topEvent.getTHad() << " Pt=" << topHad.Pt() << endl;
                cout << "    Glu: Idx=" << topEvent.getG() << " Pt=" << jetVectors[topEvent.getG()].Pt() << endl;
                if (topEvent.getPhotonSide()){
                    cout << "    Photon on leptonic decay side" << endl;
                } else {
                    cout << "    Photon on hadronic decay side" << endl;
                }
                cout << "    ----" << endl;
                cout << "    chi2="<<_chi2 << endl;
                cout << "    Tmass(Had)="<<_TopStarHad_mass << endl;
                cout << "    Tmass(Lep)="<<_TopStarLep_mass << endl;
                cout << "    Tmass(Lep)="<<_TopStar_mass << endl;
            }


        }
    }
    _Reco_angle_lepton_met = lepVector.Angle(METVector.Vect()); 
    if(phoVectors.size()>0){
        _Reco_angle_leadPhoton_met = phoVectors.at(0).Angle(METVector.Vect()); 
        _Reco_angle_leadPhoton_lepton = phoVectors.at(0).Angle(lepVector.Vect()); 
    }
    if(jetVectors.size()>0){
        _Reco_angle_leadJet_met = jetVectors.at(0).Angle(METVector.Vect()); 
    }
    if(bjetVectors.size()>0){
        _Reco_angle_leadBjet_met = bjetVectors.at(0).Angle(METVector.Vect()); 
    }
    ljetVectors.clear();
    bjetVectors.clear();
    ljetResVectors.clear();
    bjetResVectors.clear();
    
    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/HowToPDF
    //https://hypernews.cern.ch/HyperNews/CMS/get/generators/5234.html 
    //if (isMC){ 
    if (isMC && !selector->isQCD){//FIXME for UL
	// Float_t LHE scale variation weights (w_var / w_nominal); 
	// [0] is mur=0.5 muf=0.5 ; 
	// [1] is mur=0.5 muf=1 ; 
	// [2] is mur=0.5 muf=2 ; 
	// [3] is mur=1 muf=0.5 ; 
	// [4] is mur=1 muf=1 ; 
	// [5] is mur=1 muf=2 ; 
	// [6] is mur=2 muf=0.5 ; 
	// [7] is mur=2 muf=1 ; 
	// [8] is mur=2 muf=2 
    // https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopSystematics
    std::vector<float>   _genScaleSystWeights;
	if (tree->nLHEScaleWeight_==9){
	    for (int i = 0; i < 9; i++){
	        if(i==2||i==6){continue;}
	        _genScaleSystWeights.push_back(tree->LHEScaleWeight_[i]);
	    }
        double nomWeight=tree->LHEScaleWeight_[4];
        if (nomWeight!=0){
            _q2weight_Up = *max_element(_genScaleSystWeights.begin(), _genScaleSystWeights.end())/nomWeight;
            _q2weight_Do = *min_element(_genScaleSystWeights.begin(), _genScaleSystWeights.end())/nomWeight;
        }
	}
	if (tree->nLHEScaleWeight_==44){
	    _genScaleSystWeights.push_back(tree->LHEScaleWeight_[0]);
	    _genScaleSystWeights.push_back(tree->LHEScaleWeight_[5]);
	    _genScaleSystWeights.push_back(tree->LHEScaleWeight_[15]);
	    _genScaleSystWeights.push_back(tree->LHEScaleWeight_[24]);
	    _genScaleSystWeights.push_back(tree->LHEScaleWeight_[34]);
	    _genScaleSystWeights.push_back(tree->LHEScaleWeight_[39]);
	    _q2weight_Up = *max_element(_genScaleSystWeights.begin(), _genScaleSystWeights.end());
	    _q2weight_Do = *min_element(_genScaleSystWeights.begin(), _genScaleSystWeights.end());
	}

	double pdfMean = 0.;
    std::vector<float> _pdfSystWeight;
	for (int j=0; j < tree->nLHEPdfWeight_; j++ ){
	    _pdfSystWeight.push_back(tree->LHEPdfWeight_[j]);
        //std::cout<<tree->LHEPdfWeight_[j]<<std::endl;
	    pdfMean += tree->LHEPdfWeight_[j];
	}
	pdfMean = pdfMean/_pdfSystWeight.size();
	    
	double pdfVariance = 0.;
	for (int j=0; j < _pdfSystWeight.size(); j++){
	    pdfVariance += pow((_pdfSystWeight[j]-pdfMean),2.);
	}
        if (pdfMean==0) pdfMean=1;
    float _pdfuncer = 0.;
	_pdfuncer = sqrt(pdfVariance/_pdfSystWeight.size())/pdfMean;
	_pdfweight_Up = (1. + _pdfuncer);
	_pdfweight_Do = (1. - _pdfuncer);
	if (tree->nPSWeight_==4){
            if (tree->genWeight_ != 0){
                double scaleWeight=tree->PSWeight_[4];
                if (scaleWeight==0) scaleWeight=1.;
                _ISRweight_Up = tree->PSWeight_[2]/scaleWeight;
                _ISRweight_Do = tree->PSWeight_[0]/scaleWeight;

                _FSRweight_Up = tree->PSWeight_[3]/scaleWeight;
                _FSRweight_Do = tree->PSWeight_[1]/scaleWeight;
            }
        }

    }
}

// https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting
double makeNtuple::SFtop(double pt){
    return exp(0.0615 - 0.0005*pt);
}

double makeNtuple::topPtWeight(){
    double toppt=0.0;
    double antitoppt=0.0;
    double weight = 1.0;

    // TODO needs to be reimplemented with NANOAOD
    for(int mcInd=0; mcInd<tree->nGenPart_; ++mcInd){
    	if(tree->GenPart_pdgId_[mcInd]==6  && tree->GenPart_statusFlags_[mcInd]>>13&1) toppt = tree->GenPart_pt_[mcInd];
    	if(tree->GenPart_pdgId_[mcInd]==-6 && tree->GenPart_statusFlags_[mcInd]>>13&1) antitoppt = tree->GenPart_pt_[mcInd];
    }
    if(toppt > 0.001 && antitoppt > 0.001)
	weight = sqrt( SFtop(toppt) * SFtop(antitoppt) );
    
    //This has been changed, the new prescription is to not use the top pt reweighting, and the syst is using it
    return weight;
    
}

void makeNtuple::loadBtagEff(string sampleName, string year){
    //--------------------------
    //btag efficiency files
    //--------------------------
    std::map<std::string, string> btagFiles;
    string comBtag = "weight/BtagSF/btag_efficiencies_"; 
    btagFiles["2016PreVFP"]  = comBtag+"2016.root";
    btagFiles["2016PostVFP"] = comBtag+"2016.root";
    btagFiles["2017"]        = comBtag+"2017.root";
    btagFiles["2018"]        = comBtag+"2018.root";
    std::string fName = btagFiles[year]; 

    std::string effType = "Other";
    if (sampleType.find("TTGamma") != std::string::npos){
	effType = "Top";
    }
    if (sampleType.find("TTbar") != std::string::npos){
	effType = "Top";
    }
    std::string leffName = effType+"_l_efficiency";
    std::string ceffName = effType+"_c_efficiency";
    std::string beffName = effType+"_b_efficiency";

    TFile* inputFile = TFile::Open(fName.c_str(),"read");
    l_eff = (TH2D*) inputFile->Get(leffName.c_str());
    c_eff = (TH2D*) inputFile->Get(ceffName.c_str());
    b_eff = (TH2D*) inputFile->Get(beffName.c_str());
}				   

float makeNtuple::getBtagSF_1a(string sysType, BTagCalibrationReader reader, bool verbose){
    double weight = 1.0;
    double jetPt;
    double jetEta;
    double jetBtag;
    int jetFlavor;
    double SFb;
    double Eff;
    double pMC=1;
    double pData=1;
	
    string b_sysType = "central";
    string l_sysType = "central";
    if (sysType=="b_up"){
	b_sysType = "up";
    } else if (sysType=="b_down"){
	b_sysType = "down";
    } else if (sysType=="l_up"){
	l_sysType = "up";
    } else if (sysType=="l_down"){
	l_sysType = "down";
    }	
    if (verbose){
	cout << "Btagging Scale Factors"<<endl;
    }

    for(std::vector<int>::const_iterator jetInd = selector->Jets.begin(); jetInd != selector->Jets.end(); jetInd++){

	jetPt = tree->jetPt_[*jetInd];
	jetEta = fabs(tree->jetEta_[*jetInd]);
	jetFlavor = abs(tree->jetHadFlvr_[*jetInd]);
	jetBtag = tree->jetBtagDeepB_[*jetInd];

	if (jetFlavor == 5){
	    SFb = reader.eval_auto_bounds(b_sysType, BTagEntry::FLAV_B, jetEta, jetPt); 
	    int xbin = b_eff->GetXaxis()->FindBin(min(jetPt,799.));
	    int ybin = b_eff->GetYaxis()->FindBin(abs(jetEta));
	    Eff = b_eff->GetBinContent(xbin,ybin);
	}
	else if(jetFlavor == 4){
	    SFb = reader.eval_auto_bounds(b_sysType, BTagEntry::FLAV_C, jetEta, jetPt); 
	    int xbin = c_eff->GetXaxis()->FindBin(min(jetPt,799.));
	    int ybin = c_eff->GetYaxis()->FindBin(abs(jetEta));
	    Eff = c_eff->GetBinContent(xbin,ybin);
	}
	else {
	    SFb = reader.eval_auto_bounds(l_sysType, BTagEntry::FLAV_UDSG, jetEta, jetPt); 
	    int xbin = l_eff->GetXaxis()->FindBin(min(jetPt,799.));
	    int ybin = l_eff->GetYaxis()->FindBin(abs(jetEta));
	    Eff = l_eff->GetBinContent(xbin,ybin);
	}

	if (jetBtag>selector->btag_cut_DeepCSV){
	    pMC *= Eff;
	    pData *= Eff*SFb;
	} else {
	    pMC *= 1. - Eff;
	    pData *= 1. - (Eff*SFb);
	}
	if (verbose){
	    cout << "    jetPt="<<jetPt<<"  jetEta="<<jetEta<<"  jetFlavor="<<jetFlavor<<"  jetBtag="<<jetBtag<<"  Tagged="<<(jetBtag>selector->btag_cut_DeepCSV)<<"  Eff="<<Eff<<"  SF="<<SFb<<endl;
	    cout << "          --p(MC)="<<pMC<<"  --p(Data)="<<pData << endl;
	}
    }

    //    weight = pData/pMC;
    if (pMC==0){
	//      cout << "Inf weight" << endl;
	//	cout << pData << " / " << pMC << endl;
	weight = 0.;
    } else {
	weight = pData/pMC;
    }
    if (verbose){
	cout << "  FinalWeight="<<weight<<endl;
    }
    return weight;
}


vector<bool> makeNtuple::passPhoMediumID(int phoInd){
    Int_t bitMap = tree->phoVidWPBitmap_[phoInd];
    vector<bool> cuts = parsePhotonVIDCuts(bitMap, 2);
    return cuts;

}

vector<bool> makeNtuple::passPhoTightID(int phoInd){
    Int_t bitMap = tree->phoVidWPBitmap_[phoInd];
    vector<bool> cuts = parsePhotonVIDCuts(bitMap, 3);
    return cuts;

}

void makeNtuple::findPhotonCategory(int phoInd, EventTree* tree, bool* genuine, bool *misIDele, bool *hadronicphoton, bool *hadronicfake, bool *puPhoton, bool verbose){ // to use official phoGenMatch

    *genuine        = false;
    *misIDele       = false;
    *hadronicphoton = false;
    *hadronicfake   = false;
    *puPhoton       = false;
    
    int mcMatchInd = tree->phoGenPartIdx_[phoInd];

    if (verbose){cout << phoInd << "  " << mcMatchInd << "  " << tree->phoEt_[phoInd] << "  " << tree->phoEta_[phoInd] << "  " << tree->phoPhi_[phoInd] << endl;}

    // If no match, look deeper
    if (mcMatchInd== -1) {
    vector<int> genParticleCone_pid;
    vector<int> genParticleCone_idx;
    
    if (verbose){cout << "    NPartons="<<tree->nGenPart_ << endl;}
    for( int genIdx = 0; genIdx < tree->nGenPart_; genIdx++){

        if (verbose){cout << "    " << genIdx << " " << tree->GenPart_pdgId_[genIdx] << " " << tree->GenPart_pt_[genIdx] << " " << tree->GenPart_eta_[genIdx] << " " << tree->GenPart_phi_[genIdx] <<  " "  << dR(tree->GenPart_eta_[genIdx],tree->GenPart_phi_[genIdx],tree->phoEta_[phoInd],tree->phoPhi_[phoInd]) << endl;}
        // skip gen particles < 5 GeV
        if (tree->GenPart_pt_[genIdx]< 5) continue;

        // skip gen neutrinos
        vector<int> excludedPdgIds= {12, -12, 14, -14, 16, -16};
        int genPID = tree->GenPart_pdgId_[genIdx];
        if(std::find(excludedPdgIds.begin(),excludedPdgIds.end(),genPID) != excludedPdgIds.end()) continue;

        // find all gen particles within 0.3 of the reco photon
        double dRValue = dR(tree->GenPart_eta_[genIdx],tree->GenPart_phi_[genIdx],tree->phoEta_[phoInd],tree->phoPhi_[phoInd]);
        if (dRValue<0.3){
        genParticleCone_idx.push_back(genIdx);
        genParticleCone_pid.push_back(genPID);
        }
    }
    if (genParticleCone_pid.size()==0){
        *puPhoton = true;
        return;
    }
    
    // if a photon (22) and a pi_0 (111) are in the cone, it's a hadronic photon 
    if(std::find(genParticleCone_pid.begin(),genParticleCone_pid.end(),111) != genParticleCone_pid.end() && 
       std::find(genParticleCone_pid.begin(),genParticleCone_pid.end(),22) != genParticleCone_pid.end()) {
        *hadronicphoton = true;
        return;
    }

    *hadronicfake = true;
    return;
    }

    int mcMatchPDGID = tree->GenPart_pdgId_[mcMatchInd];

    Int_t parentIdx = mcMatchInd;
    int maxPDGID = 0;
    int motherPDGID = 0;
    while (parentIdx != -1){
    motherPDGID = std::abs(tree->GenPart_pdgId_[parentIdx]);
    maxPDGID = std::max(maxPDGID,motherPDGID);
    parentIdx = tree->GenPart_genPartIdxMother_[parentIdx];
    }

    bool parentagePass = maxPDGID < 37;
    // bool parentagePass = (fabs(tree->mcMomPID->at(mcMatchInd))<37 || tree->mcMomPID->at(mcMatchInd) == -999);

    if (mcMatchPDGID==22){
    if (parentagePass){ 
        *genuine = true;
    }
    else {
        *hadronicphoton = true;
    }
    }
    else if ( abs(mcMatchPDGID ) == 11 ) {
    *misIDele = true;
    } 
    else {
    *hadronicfake = true;
    }
}


#endif
int main(int ac, char** av){

 /*
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
  */
  makeNtuple(ac, av);

  return 0;
}
