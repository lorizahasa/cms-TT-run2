#include "interface/makeNtuple.h"
#define makeNtuple_cxx

int jecvar012_g = 1; // 0:down, 1:norm, 2:up
int jervar012_g = 1; // 0:down, 1:norm, 2:up
int phosmear012_g = 1; // 0:down, 1:norm, 2:up
int musmear012_g = 1; // 0:down, 1:norm, 2: up
int elesmear012_g = 1; // 0:down, 1:norm, 2: up
int phoscale012_g = 1;
int elescale012_g = 1;
bool dileptonsample;
bool qcdSample;
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
    bool saveCutflow=false;
    if (std::string(av[1])=="cutflow"){
	saveCutflow=true;
	for (int i = 1; i < ac-1; i++){
	    av[i] = av[i+1];
	}
	ac = ac-1;
    }

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
    dileptonsample = false;
    qcdSample = false;

    if (std::string(av[1])=="dilepton" || 
        std::string(av[1])=="dilept" ||
        std::string(av[1])=="dilep" ||
        std::string(av[1])=="Dilepton" || 
        std::string(av[1])=="Dilept" ||
        std::string(av[1])=="Dilep"){
  
        dileptonsample=true;
        for (int i = 1; i < ac-1; i++){
            av[i] = av[i+1];
	}
	ac = ac-1;
        cout << "---------------------------------------" << endl;
        cout << "Using Dilepton Control Region Selection" << endl;
        cout << "---------------------------------------" << endl;
    }

    if (std::string(av[1])=="qcd" || 
        std::string(av[1])=="qcdCR" ||
        std::string(av[1])=="QCDcr" ||
        std::string(av[1])=="QCD" ||
        std::string(av[1])=="QCDCR"){
  
        qcdSample=true;
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
    sampleType = av[2];
    systematicType = "";
    cout << sampleType << endl;

    isMC = true;
    if (sampleType.find("Data") != std::string::npos){
	isMC = false;
    }
    std::string year(av[1]);
    tree = new EventTree(ac-4, false, year, !isMC, av+4);
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
    
    std::string PUfilename; 
    std::string PUfilename_up;
    std::string PUfilename_down;
    if (year=="2016"){
	PUfilename      = "weight/PileupSF/Data_2016BCDGH_Pileup.root";
	PUfilename_up   = "weight/PileupSF/Data_2016BCDGH_Pileup_scaledUp.root";
	PUfilename_down = "weight/PileupSF/Data_2016BCDGH_Pileup_scaledDown.root";
    }
    if (year=="2017"){
	PUfilename      = "weight/PileupSF/Data_2017BCDEF_Pileup.root";
	PUfilename_up   = "weight/PileupSF/Data_2017BCDEF_Pileup_scaledUp.root";
	PUfilename_down = "weight/PileupSF/Data_2017BCDEF_Pileup_scaledDown.root";
    }
    if (year=="2018"){
	PUfilename      = "weight/PileupSF/Data_2018ABCD_Pileup.root";
	PUfilename_up   = "weight/PileupSF/Data_2018ABCD_Pileup_scaledUp.root";
	PUfilename_down = "weight/PileupSF/Data_2018ABCD_Pileup_scaledDown.root";
    }
    if (eventNum > -1) {
	string cut = "event=="+eventStr;
	cout << "Selecting only entries with " << cut << endl;
	tree->chain = (TChain*) tree->chain->CopyTree(cut.c_str());
    }

    selector = new Selector();
    evtPick = new EventPick("");
    selector->year = year;
    evtPick->year = year;
    selector->printEvent = eventNum;
    evtPick->printEvent = eventNum;
    evtPick->Njet_ge = 2;
    evtPick->NBjet_ge = 0;

    evtPick->applyMetFilter = true; 
    bool applyHemVeto=true; 
    //bool applyHemVeto=false; //test
    if (saveCutflow){
	selector->smearJetPt=false;
	evtPick->saveCutflows=true;
	evtPick->Njet_ge = 4;
	evtPick->NBjet_ge = 1;
    }

    if (eventNum > -1){
        //	selector->smearJetPt=false;
    }
    selector->looseJetID = false;
    selector->useDeepCSVbTag = true;
    if (isMC){
    	if (year=="2016") selector->init_JER("weight/JetSF/JER/Summer16_25nsV1");
    	if (year=="2017") selector->init_JER("weight/JetSF/JER/Fall17_V3");
    	if (year=="2018") selector->init_JER("weight/JetSF/JER/Autumn18_V7b");
    }
    if (year=="2016") selector->btag_cut_DeepCSV = 0.6321;
    if (year=="2017") selector->btag_cut_DeepCSV = 0.4941;
    if (year=="2018") selector->btag_cut_DeepCSV = 0.4184;
    
    if (year=="2016") selector->toptag_cut_DeepAK8 = 0.834;
    if (year=="2017") selector->toptag_cut_DeepAK8 = 0.725;
    if (year=="2018") selector->toptag_cut_DeepAK8 = 0.802;

    //	selector->jet_Pt_cut = 40.;
    BTagCalibration calib;
    if (!selector->useDeepCSVbTag){
	if (year=="2016") calib = BTagCalibration("csvv2", "weight/BtagSF/CSVv2_Moriond17_B_H.csv");
	if (year=="2017") calib = BTagCalibration("csvv2", "weight/BtagSF/CSVv2_94XSF_V2_B_F.csv");
	if (year=="2018") calib = BTagCalibration("csvv2", "weight/BtagSF/CSVv2_94XSF_V2_B_F.csv");
    } else {
	if (year=="2016"){ calib = BTagCalibration("deepcsv", "weight/BtagSF/DeepCSV_2016LegacySF_V1.csv");}
	if (year=="2017"){ calib = BTagCalibration("deepcsv", "weight/BtagSF/DeepCSV_94XSF_V3_B_F.csv");}
	if (year=="2018"){ calib = BTagCalibration("deepcsv", "weight/BtagSF/DeepCSV_102XSF_V1.csv");} //DeepCSV_102XSF_V1.csv
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

    if(dileptonsample)     {evtPick->Nmu_eq=2; evtPick->Nele_eq=2;}
    if(qcdSample)       {selector->QCDselect = true; evtPick->QCDselect = true;}
    //    if( systematicType=="QCDcr")       {selector->QCDselect = true; evtPick->ZeroBExclusive=true; evtPick->QCDselect = true;}
    std::cout << "Dilepton Sample :" << dileptonsample << std::endl;
    std::cout << "JEC: " << jecvar012_g << "  JER: " << jervar012_g << " eleScale "<< elescale012_g << " phoScale" << phoscale012_g << "   ";
    std::cout << "  PhoSmear: " << phosmear012_g << "  muSmear: " << musmear012_g << "  eleSmear: " << elesmear012_g << std::endl;
    if (dileptonsample && saveCutflow){
	evtPick->Njet_ge = 2;
	evtPick->NBjet_ge = 0;
    }

    if (isSystematicRun){
	std::cout << "  Systematic Run : Dropping genMC variables from tree" << endl;
    }

    std::string outputDirectory(av[3]);
    std::string outputFileName;
    if (nJob==-1){
	outputFileName = outputDirectory + "/" + sampleType+"_"+year+"_Ntuple.root";
    } else {
	outputFileName = outputDirectory + "/" + sampleType+"_"+year+"_Ntuple_"+to_string(nJob)+"of"+to_string(totJob)+".root";
    }
    // char outputFileName[100];
    cout << av[3] << " " << sampleType << " " << systematicType << endl;
    if (systematicType!=""){
	outputFileName.replace(0,outputDirectory.size()+1, outputDirectory + "/"+systematicType + "_");
	//	outputFileName.replace(outputFileName.begin(),outputDirectory.size()+1, outputDirectory + "/"+systematicType + "_");
	//	outputFileName = outputDirectory + "/"+systematicType + "_" +sampleType+"_"+year+"_Ntuple.root";
    }

    if (dileptonsample){
	outputFileName.replace(0,outputDirectory.size()+1, outputDirectory + "/Dilep_");
    }
    if (qcdSample){
	outputFileName.replace(0,outputDirectory.size()+1, outputDirectory + "/QCDcr_");
    }
    if (saveCutflow) {
	//outputFileName.replace(outputFileName.find("Ntuple"),14, "Cutflow");
    }

    cout << av[3] << " " << sampleType << " " << systematicType << endl;
    cout << outputFileName << endl;
    TFile *outputFile = new TFile(outputFileName.c_str(),"recreate");
    outputTree = new TTree("AnalysisTree","AnalysisTree");
    //outputTree->SetAutoFlush(1000000000);
    //outputTree->SetAutoSave(10000000000);//Save to disk after 1000 GB

    if (saveCutflow) {
	evtPick->init_cutflow_files(outputFileName);
    }
    cout << "HERE" << endl;
    PUReweight* PUweighter = new PUReweight(ac-4, av+4, PUfilename);
    PUReweight* PUweighterUp = new PUReweight(ac-4, av+4, PUfilename_up);
    PUReweight* PUweighterDown = new PUReweight(ac-4, av+4, PUfilename_down);
    cout << "DONE" << endl;
    tree->GetEntry(0);
        
    std::cout << "isMC: " << isMC << endl;

    InitBranches();

    JECvariation* jecvar;
    if (isMC && jecvar012_g!=1) {
	cout << "Applying JEC uncertainty variations : " << JECsystLevel << endl;
	if (year=="2016") jecvar = new JECvariation("weight/JetSF/Summer16_07Aug2017_V11", isMC, JECsystLevel);
	if (year=="2017") jecvar = new JECvariation("weight/JetSF/Fall17_17Nov2017_V32", isMC, JECsystLevel);
	if (year=="2018") jecvar = new JECvariation("weight/JetSF/Autumn18_V19", isMC, JECsystLevel);
    }

    double luminosity = 1.;
    if (year=="2016") luminosity=35921.875595;
    if (year=="2017") luminosity=41529.548819;
    if (year=="2018") luminosity=59740.565202;

    double nMC_total = 0.;
    useGenWeightScaling = true;

    double nMC_thisFile = 0.;
    char** fileNames = av+4;
    for(int fileI=0; fileI<ac-4; fileI++){
	TFile *_file = TFile::Open(fileNames[fileI],"read");
	TH1D *hEvents = (TH1D*) _file->Get("hEvents");
	nMC_thisFile = (hEvents->GetBinContent(2)); //sum of gen weights
	if (nMC_thisFile==0) {useGenWeightScaling=false;} //if bin isn't filled, fall back to using positive - negative bins
	nMC_total += nMC_thisFile;
    }
    if (!useGenWeightScaling){
	for(int fileI=0; fileI<ac-4; fileI++){
	    TFile *_file = TFile::Open(fileNames[fileI],"read");
	    TH1D *hEvents = (TH1D*) _file->Get("hEvents");
	    nMC_total += (hEvents->GetBinContent(3) - hEvents->GetBinContent(1));  //positive weight - neg weight 
	}
    }
	
    if (nMC_total==0){
	nMC_total=1;
    }
    _lumiWeight = getEvtWeight(sampleType, std::stoi(year), luminosity, nMC_total);
    _PUweight       = 1.;
    _muEffWeight    = 1.;
    _muEffWeight_Do = 1.;
    _muEffWeight_Up = 1.;
    _eleEffWeight    = 1.;
    _eleEffWeight_Up = 1.;
    _eleEffWeight_Do = 1.;

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
    //    nEntr = 4000;
    if (year=="2016"){
	muSFa = new MuonSF("weight/MuEleGammaSF/mu2016/EfficienciesStudies_2016_legacy_rereco_rootfiles_RunBCDEF_SF_ID.root", "NUM_TightID_DEN_genTracks_eta_pt",
			   "weight/MuEleGammaSF/mu2016/EfficienciesStudies_2016_legacy_rereco_rootfiles_RunBCDEF_SF_ISO.root", "NUM_TightRelIso_DEN_TightIDandIPCut_eta_pt",
			   "weight/MuEleGammaSF/mu2016/EfficienciesStudies_2016_trigger_EfficienciesAndSF_RunBtoF.root", "Mu50_OR_TkMu50_PtEtaBins/abseta_pt_ratio");
	
	muSFb = new MuonSF("weight/MuEleGammaSF/mu2016/EfficienciesStudies_2016_legacy_rereco_rootfiles_RunGH_SF_ID.root", "NUM_TightID_DEN_genTracks_eta_pt",
			   "weight/MuEleGammaSF/mu2016/EfficienciesStudies_2016_legacy_rereco_rootfiles_RunGH_SF_ISO.root", "NUM_TightRelIso_DEN_TightIDandIPCut_eta_pt",
			   "weight/MuEleGammaSF/mu2016/EfficienciesStudies_2016_trigger_EfficienciesAndSF_RunGtoH.root", "Mu50_OR_TkMu50_PtEtaBins/abseta_pt_ratio");
	
	eleSF = new ElectronSF("weight/MuEleGammaSF/ele2016/2016LegacyReReco_ElectronTight_Fall17V2.root",
			       "weight/MuEleGammaSF/ele2016/EGM2D_BtoH_GT20GeV_RecoSF_Legacy2016.root",
			       "weight/MuEleGammaSF/ele2016/sf_ele_2016_trig_v5.root");
	
	phoSF = new PhotonSF("weight/MuEleGammaSF/pho2016/Fall17V2_2016_Medium_photons.root",
			     "weight/MuEleGammaSF/pho2016/ScalingFactors_80X_Summer16.root",
			     2016);
    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/L1ECALPrefiringWeightRecipe
	l1PrefireSF = new PrefireWeights("weight/MuEleGammaSF/prefire/L1prefiring_photonpt_2016BtoH.root", "L1prefiring_photonpt_2016BtoH",
					 "weight/MuEleGammaSF/prefire/L1prefiring_jetpt_2016BtoH.root", "L1prefiring_jetpt_2016BtoH");


    } else if (year=="2017") {
	
	muSFa = new MuonSF("weight/MuEleGammaSF/mu2017/RunBCDEF_SF_ID.root", "NUM_TightID_DEN_genTracks_pt_abseta",
			   "weight/MuEleGammaSF/mu2017/RunBCDEF_SF_ISO.root", "NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta",
			   "weight/MuEleGammaSF/mu2017/EfficienciesAndSF_RunBtoF_Nov17Nov2017.root", "Mu50_PtEtaBins/abseta_pt_ratio");
	
	eleSF = new ElectronSF("weight/MuEleGammaSF/ele2017/2017_ElectronTight.root",
			       "weight/MuEleGammaSF/ele2017/egammaEffi.txt_EGM2D_runBCDEF_passingRECO.root",
			       "weight/MuEleGammaSF/ele2017/sf_ele_2017_trig_v5.root");

	
	phoSF = new PhotonSF("weight/MuEleGammaSF/pho2017/2017_PhotonsMedium.root",
			     "weight/MuEleGammaSF/pho2017/PixelSeed_ScaleFactors_2017.root",
			     2017);
	
	
	l1PrefireSF = new PrefireWeights("weight/MuEleGammaSF/prefire/L1prefiring_photonpt_2017BtoF.root", "L1prefiring_photonpt_2017BtoF",
					"weight/MuEleGammaSF/prefire/L1prefiring_jetpt_2017BtoF.root", "L1prefiring_jetpt_2017BtoF");

    } else if (year=="2018") {

	muSFa = new MuonSF("weight/MuEleGammaSF/mu2018/EfficienciesStudies_2018_rootfiles_RunABCD_SF_ID.root",  "NUM_TightID_DEN_TrackerMuons_pt_abseta",
			   "weight/MuEleGammaSF/mu2018/EfficienciesStudies_2018_rootfiles_RunABCD_SF_ISO.root", "NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta",
			   "weight/MuEleGammaSF/mu2018/EfficienciesStudies_2018_trigger_EfficienciesAndSF_2018Data_BeforeMuonHLTUpdate.root", "Mu50_OR_OldMu100_OR_TkMu100_PtEtaBins/abseta_pt_ratio");
	
	muSFb = new MuonSF("weight/MuEleGammaSF/mu2018/EfficienciesStudies_2018_rootfiles_RunABCD_SF_ID.root",  "NUM_TightID_DEN_TrackerMuons_pt_abseta",
			   "weight/MuEleGammaSF/mu2018/EfficienciesStudies_2018_rootfiles_RunABCD_SF_ISO.root", "NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta",
			   "weight/MuEleGammaSF/mu2018/EfficienciesStudies_2018_trigger_EfficienciesAndSF_2018Data_AfterMuonHLTUpdate.root", "Mu50_OR_OldMu100_OR_TkMu100_PtEtaBins/abseta_pt_ratio");

	eleSF = new ElectronSF("weight/MuEleGammaSF/ele2018/2018_ElectronTight.root",
			       "weight/MuEleGammaSF/ele2018/egammaEffi.txt_EGM2D_updatedAll.root",
			       "weight/MuEleGammaSF/ele2018/sf_ele_2018_trig_v5.root");


	phoSF = new PhotonSF("weight/MuEleGammaSF/pho2018/2018_PhotonsMedium.root",
			     "weight/MuEleGammaSF/pho2018/HasPix_2018.root",
			     2018);

    }

    int dumpFreq = 1;
    if (nEntr >50)     { dumpFreq = 5; }
    if (nEntr >100)     { dumpFreq = 10; }
    if (nEntr >500)     { dumpFreq = 50; }
    if (nEntr >1000)    { dumpFreq = 100; }
    if (nEntr >5000)    { dumpFreq = 500; }
    if (nEntr >10000)   { dumpFreq = 1000; }
    if (nEntr >50000)   { dumpFreq = 5000; }
    if (nEntr >100000)  { dumpFreq = 10000; }
    if (nEntr >500000)  { dumpFreq = 50000; }
    if (nEntr >1000000) { dumpFreq = 100000; }
    if (nEntr >5000000) { dumpFreq = 500000; }
    if (nEntr >10000000){ dumpFreq = 1000000; }
    int count_overlap=0;
    int count_HEM=0;

    int entryStart;
    int entryStop;
    if (nJob==-1){
	entryStart = 0;
	entryStop=nEntr;
    }
    else {
	int evtPerJob = nEntr/totJob;
	entryStart = (nJob-1) * evtPerJob;
	entryStop = (nJob) * evtPerJob;
	if (nJob==totJob){
	    entryStop = nEntr;
	}
    }

    for(Long64_t entry=entryStart; entry<entryStop; entry++){
	if(entry%dumpFreq == 0){
	    std::cout << "processing entry " << entry << " out of " << nEntr << " : " 
		      << std::chrono::duration<double>(std::chrono::high_resolution_clock::now()-startClock).count()
		      << " seconds since last progress" << std::endl;
	    startClock = std::chrono::high_resolution_clock::now();			
	}
	//  cout << entry << endl;
	tree->GetEntry(entry);
	if( isMC && doOverlapInvert_TTG){
	    //if (!overlapRemovalTT(tree, tree->event_==eventNum)){	
	    if (!overlapRemoval(tree, 10., 5., 0.1, tree->event_==eventNum)){
		count_overlap++;			
		continue;
	    }
	}

	if( isMC && doOverlapRemoval_TT){
	    // if (overlapRemovalTT(tree, tree->event_==eventNum) != overlapRemoval(tree, 10., 5., 0.1, tree->event_==eventNum)){	
	    // 	cout << "ISSUE WITH OVERLAP REMOVAL" << endl;
	    // 	cout << "    " << tree->event_ << endl;
	    // }
	    if (!invertOverlap){
		//if (overlapRemovalTT(tree, tree->event_==eventNum)){	
		if (overlapRemoval(tree, 10., 5., 0.1, tree->event_==eventNum)){
		    count_overlap++;			
		    continue;
		}
	    } else {
		//if (!overlapRemovalTT(tree, tree->event_==eventNum)){	
		if (!overlapRemoval(tree, 10., 5., 0.1, tree->event_==eventNum)){
		    count_overlap++;			
		    continue;
		}
	    }
	}

	if( isMC && doOverlapRemoval_W){
	    //if (overlapRemovalWJets(tree, tree->event_==eventNum)){
	    if (overlapRemoval(tree, 15., 2.6, 0.05, tree->event_==eventNum)){
		count_overlap++;
		continue;
	    }
	}

	if( isMC && doOverlapInvert_WG){
	    //if (!overlapRemovalWJets(tree, tree->event_==eventNum)){	
	    if (!overlapRemoval(tree, 15., 2.6, 0.05, tree->event_==eventNum)){
		count_overlap++;			
		continue;
	    }
	}
	if( isMC && doOverlapRemoval_Z){
	    //if (overlapRemovalZJets(tree, tree->event_==eventNum)){
	    if (overlapRemoval(tree, 15., 2.6, 0.05, tree->event_==eventNum)){
		count_overlap++;
		continue;
	    }
	}
	if( isMC && doOverlapInvert_ZG){
	    //if (!overlapRemovalZJets(tree, tree->event_==eventNum)){
	    if (!overlapRemoval(tree, 15., 2.6, 0.05, tree->event_==eventNum)){
		count_overlap++;
		continue;
	    }
	}
	if( isMC && doOverlapRemoval_Tchannel){
	    //if (overlapRemoval_Tchannel(tree)){
	    if (overlapRemoval_2To3(tree, 10., 2.6, 0.05, tree->event_==eventNum)){
		count_overlap++;
		continue;
	    }
	}

	if( isMC && doOverlapInvert_TG){
	    //if (!overlapRemoval_Tchannel(tree)){
	    if (!overlapRemoval_2To3(tree, 10., 2.6, 0.05, tree->event_==eventNum)){
		count_overlap++;
		continue;
	    }
	}

	if( isMC && doOverlapInvert_GJ){
	    //if (!overlapRemoval_Tchannel(tree)){
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

	// //		Apply systematics shifts where needed
	if( isMC ){
	    if (jecvar012_g != 1){
		jecvar->applyJEC(tree, jecvar012_g); // 0:down, 1:norm, 2:up
	    }
	}

	//HEM test 
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

	selector->clear_vectors();

	evtPick->process_event(tree, selector, _PUweight);

        if (tree->event_==eventNum){
            cout << "EventSelection:" << endl;
            cout << "  PassPresel e " << evtPick->passPreselEle << endl;
            cout << "  PassPresel mu" << evtPick->passPreselMu<< endl;
            cout << "  PassPhoton e " << evtPick->passAllEle << endl;
            cout << "  PassPhoton mu" << evtPick->passAllMu << endl;
        }

	if ( evtPick->passPreselEle || evtPick->passPreselMu || saveAllEntries) {
	    if (saveCutflow && !(evtPick->passAllEle || evtPick->passAllMu) ) continue;
	    InitVariables();
	   // FillEvent(year);
	    FillEvent(year); //HEM test

	    if(isMC) {
		_PUweight    = PUweighter->getWeight(tree->nPUTrue_);
		_PUweight_Up = PUweighterUp->getWeight(tree->nPUTrue_);
		_PUweight_Do = PUweighterDown->getWeight(tree->nPUTrue_);

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
		    if (year=="2016"){
		        vector<double> muWeights_a    = muSFa->getMuSFs(tree->muPt_[muInd_],tree->muEta_[muInd_],1, 2016, tree->event_==eventNum);
		        vector<double> muWeights_b    = muSFb->getMuSFs(tree->muPt_[muInd_],tree->muEta_[muInd_],1, 2016, tree->event_==eventNum);
		        vector<double> muWeights_a_Do = muSFa->getMuSFs(tree->muPt_[muInd_],tree->muEta_[muInd_],0, 2016);
		        vector<double> muWeights_b_Do = muSFb->getMuSFs(tree->muPt_[muInd_],tree->muEta_[muInd_],0, 2016);
		        vector<double> muWeights_a_Up = muSFa->getMuSFs(tree->muPt_[muInd_],tree->muEta_[muInd_],2, 2016);
		        vector<double> muWeights_b_Up = muSFb->getMuSFs(tree->muPt_[muInd_],tree->muEta_[muInd_],2, 2016);
			    for (int _i=0; _i < muWeights_a.size(); _i++){
			        muWeights.push_back( muWeights_a.at(_i) * 19.695422959/35.921875595 + muWeights_b.at(_i) * 16.226452636/35.921875595);
			        muWeights_Do.push_back( muWeights_a_Do.at(_i) * 19.695422959/35.921875595 + muWeights_b_Do.at(_i) * 16.226452636/35.921875595);
			        muWeights_Up.push_back( muWeights_a_Up.at(_i) * 19.695422959/35.921875595 + muWeights_b_Up.at(_i) * 16.226452636/35.921875595);
			    }
		    }
		    if (year=="2017"){    
		        muWeights    = muSFa->getMuSFs(tree->muPt_[muInd_],tree->muEta_[muInd_],1, 2017, tree->event_==eventNum);
			    muWeights_Do = muSFa->getMuSFs(tree->muPt_[muInd_],tree->muEta_[muInd_],0, 2017);
			    muWeights_Up = muSFa->getMuSFs(tree->muPt_[muInd_],tree->muEta_[muInd_],2, 2017);
		    }
            if(year=="2018"){
                vector<double> muWeights_a    = muSFa->getMuSFs(tree->muPt_[muInd_],tree->muEta_[muInd_],1, 2018, tree->event_==eventNum);
                vector<double> muWeights_b    = muSFb->getMuSFs(tree->muPt_[muInd_],tree->muEta_[muInd_],1, 2018, tree->event_==eventNum);
                vector<double> muWeights_a_Do = muSFa->getMuSFs(tree->muPt_[muInd_],tree->muEta_[muInd_],0, 2018);
		        vector<double> muWeights_b_Do = muSFb->getMuSFs(tree->muPt_[muInd_],tree->muEta_[muInd_],0, 2018);
                vector<double> muWeights_a_Up = muSFa->getMuSFs(tree->muPt_[muInd_],tree->muEta_[muInd_],2, 2018);
		        vector<double> muWeights_b_Up = muSFb->getMuSFs(tree->muPt_[muInd_],tree->muEta_[muInd_],2, 2018);
                for (int _i=0; _i < muWeights_a.size(); _i++){
                    muWeights.push_back( muWeights_a.at(_i) * 8.950818835/59.740565202 + muWeights_b.at(_i) * 50.789746366/59.740565202);
                    muWeights_Do.push_back( muWeights_a_Do.at(_i) * 8.950818835/59.740565202 + muWeights_b_Do.at(_i) * 50.789746366/59.740565202);
                    muWeights_Up.push_back( muWeights_a_Up.at(_i) * 8.950818835/59.740565202 + muWeights_b_Up.at(_i) * 50.789746366/59.740565202);
			    }
		    }
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

		    _eleEffWeight    = 1.;
		    _eleEffWeight_Up = 1.;
		    _eleEffWeight_Do = 1.;
		}
		if (evtPick->passPreselEle) {
		    int eleInd_ = selector->Electrons.at(0);
		    _muEffWeight    = 1.;
		    _muEffWeight_Do = 1.;
		    _muEffWeight_Up = 1.;

		    
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
            //if(_eleEffWeight_Trig_Up >1.0)cout<<_eleEffWeight_Trig_Up<<endl;
		}
	    }

	    if (year=="2016" || year=="2017"){
		float prefireSF[3] = {1.,1.,1.};

		l1PrefireSF->getPrefireSF(tree, prefireSF);

		_prefireSF = prefireSF[1];
		_prefireSF_Do = prefireSF[0];
		_prefireSF_Up = prefireSF[2];
	    }
	    else{
		_prefireSF = 1;
		_prefireSF_Do = 1.;
		_prefireSF_Up = 1.;
	    }

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
	}
    }
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

    outputTree->Write();

    if (saveCutflow){
	std::cout << "e+jets cutflow" << std::endl;
	evtPick->print_cutflow_ele(evtPick->cutFlow_ele);

	std::cout << "mu+jets cutflow" << std::endl;
	evtPick->print_cutflow_mu(evtPick->cutFlow_mu);

	std::cout << "e+jets cutflow Weighted" << std::endl;
	evtPick->print_cutflow_ele(evtPick->cutFlowWeight_ele);

	std::cout << "mu+jets cutflow Weighted" << std::endl;
	evtPick->print_cutflow_mu(evtPick->cutFlowWeight_mu);

	evtPick->cutFlow_mu->Write();
	evtPick->cutFlow_ele->Write();
	evtPick->cutFlowWeight_mu->Write();
	evtPick->cutFlowWeight_ele->Write();
    }

    if (saveCutflow) {
	evtPick->close_cutflow_files();
    }
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


void makeNtuple::FillEvent(std::string year)
//void makeNtuple::FillEvent(std::string year, bool isHemVetoObj) //HEM test
{

    _run             = tree->run_;
    _event           = tree->event_;
    _lumis           = tree->lumis_;
    _isData	         = !isMC;
    _nVtx		 = tree->nVtx_;
    _nGoodVtx	 = tree->nGoodVtx_;
    // _isPVGood	 = tree->isPVGood_;
    // _rho		 = tree->rho_;
    if (useGenWeightScaling){
	_evtWeight       = _lumiWeight *  tree->genWeight_; 
    }else{
	_evtWeight       = _lumiWeight *  ((tree->genWeight_ >= 0) ? 1 : -1);  //event weight needs to be positive or negative depending on sign of genWeight (to account for mc@nlo negative weights)
    }

    if (_isData) {
	_evtWeight= 1.;
	//	_evtWeightAlt= 1.;
    }


    //MC HEM test
    if(isMC && _inHEMVeto){
        _evtWeight = _evtWeight*0.3518;
    }




    _genMET		     = tree->GenMET_pt_;
    _pfMET		     = tree->MET_pt_;
    _pfMETPhi    	     = tree->MET_phi_;
    
    _nPho		     = selector->Photons.size();
    _nLoosePho	             = selector->LoosePhotons.size();
    _nPhoNoID	             = selector->PhotonsNoID.size();
    _nEle		     = selector->Electrons.size();
    _nEleLoose               = selector->ElectronsLoose.size();
    _nMu		     = selector->Muons.size();
    _nMuLoose                = selector->MuonsLoose.size();
    
    _nJet            = selector->Jets.size();
    _nFatJet         = selector->FatJets.size();
    _nBJet           = selector->bJets.size();

    _nGenPart        = tree->nGenPart_;
    _nGenJet         = tree->nGenJet_;

    //TODO
    //        _pdfWeight       = tree->pdfWeight_;	
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
        _muPFRelIso.push_back(tree->muMiniPFRelIso_[muInd]);
        
        lepVector.SetPtEtaPhiM(tree->muPt_[muInd],
        		       tree->muEta_[muInd],
        		       tree->muPhi_[muInd],
        		       tree->muMass_[muInd]);
        lepCharge=tree->muCharge_[muInd];
        lt += tree->muPt_[muInd];
    }
    _ST = ht + lt + tree->MET_pt_;
	
    if (dileptonsample){
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
    }
	
    _passPresel_Ele  = evtPick->passPreselEle;
    _passPresel_Mu   = evtPick->passPreselMu;
    _passAll_Ele     = evtPick->passAllEle;
    _passAll_Mu      = evtPick->passAllMu;
    _nPhoBarrel=0.;
    _nPhoEndcap=0.;

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
        //	_phoSCEta.push_back(tree->phoEta_[phoInd]);
        
        _phoR9.push_back(tree->phoR9_[phoInd]);		
        _phoSIEIE.push_back(tree->phoSIEIE_[phoInd]);
        _phoHoverE.push_back(tree->phoHoverE_[phoInd]);
        _phoIsBarrel.push_back( abs(tree->phoEta_[phoInd])<1.47 );
        
        _phoPFRelIso.push_back( tree->phoPFRelIso_[phoInd]);
        _phoPFRelChIso.push_back( tree->phoPFRelChIso_[phoInd]);
        _phoPFChIso.push_back( tree->phoPFRelChIso_[phoInd] * tree->phoEt_[phoInd]);
        
        if (abs(tree->phoEta_[phoInd])<1.47){
            _nPhoBarrel++;
        }else{
            _nPhoEndcap++;
        } 
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
        
            _phoEffWeight_eVeto.push_back(phoWeights.at(2));
            _phoEffWeight_eVeto_Do.push_back(phoWeights_Do.at(2));
            _phoEffWeight_eVeto_Up.push_back(phoWeights_Up.at(2));
        }
        _phoMassLepGamma.push_back( (phoVector+lepVector).M() );
        int phoGenMatchInd = -1.;
        
        // TODO needs to be reimplemented with NANOAOD
        if (!tree->isData_){
            phoGenMatchInd = tree->phoGenPartIdx_[phoInd];
            if (evtPick->saveCutflows){
        	string run_lumi_event = to_string(tree->run_)+","+to_string(tree->lumis_)+","+to_string(tree->event_)+"\n";		
            }
        }
	_dRPhotonLepton.push_back(phoVector.DeltaR(lepVector));
	_MPhotonLepton.push_back((phoVector+lepVector).M());
	_AnglePhotonLepton.push_back(phoVector.Angle(lepVector.Vect())); 
    }
    
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
        //std::cout<<tree->fatJetPt_[fatJetInd]<<std::endl;
        _fatJetPt.push_back(          tree->fatJetPt_[fatJetInd]);
        _fatJetEta.push_back(         tree->fatJetEta_[fatJetInd]);
        _fatJetPhi.push_back(         tree->fatJetPhi_[fatJetInd]);
        _fatJetMass.push_back(        tree->fatJetMass_[fatJetInd]);
        _fatJetMassSoftDrop.push_back(tree->fatJetMassSoftDrop_[fatJetInd]);
        _fatJetBtagDeepB.push_back(   tree->fatJetBtagDeepB_[fatJetInd]);
        _fatJetDeepTagT.push_back(    tree->fatJetDeepTagT_[fatJetInd]);
        _fatJetDeepTagW.push_back(    tree->fatJetDeepTagW_[fatJetInd]);
        _fatJetDeepTagMDT.push_back(  tree->fatJetDeepTagMDT_[fatJetInd]);
        _fatJetDeepTagMDW.push_back(  tree->fatJetDeepTagMDW_[fatJetInd]);
        _fatJetEleIdx.push_back(      tree->fatJetEleIdx_[fatJetInd]);
        _fatJetMuIdx.push_back(       tree->fatJetMuIdx_[fatJetInd]);
        _fatJetGenJetAK8Idx.push_back(tree->fatJetGenJetAK8Idx_[fatJetInd]);
        _fatJetHadFlvr.push_back(     tree->fatJetHadFlvr_[fatJetInd]);
        _fatJetID.push_back(          tree->fatJetID_[fatJetInd]);
        fatJetVector.SetPtEtaPhiM(tree->fatJetPt_[fatJetInd], 
                tree->fatJetEta_[fatJetInd], 
                tree->fatJetPhi_[fatJetInd], 
                tree->fatJetMass_[fatJetInd]);
        fatJetVectors.push_back(fatJetVector);
    }
    for (int i_jet = 0; i_jet <_nJet; i_jet++){
        int jetInd = selector->Jets.at(i_jet);
        _jetPt.push_back(tree->jetPt_[jetInd]);
        _jetEta.push_back(tree->jetEta_[jetInd]);
        _jetPhi.push_back(tree->jetPhi_[jetInd]);
        _jetMass.push_back(tree->jetMass_[jetInd]);
        _jetCMVA.push_back(tree->jetBtagCMVA_[jetInd]);
        _jetCSVV2.push_back(tree->jetBtagCSVV2_[jetInd]);
        _jetDeepB.push_back(tree->jetBtagDeepB_[jetInd]);
        _jetDeepC.push_back(tree->jetBtagDeepC_[jetInd]);
        _jetGenJetIdx.push_back(tree->jetGenJetIdx_[jetInd]);
        double resolution = selector->jet_resolution.at(i_jet);
        _jetRes.push_back(resolution);
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
            _TopStarHad_mass = (bhad + Wj1 + Wj2 + hadDecay).M();
            _TopStarLep_mass = (blep + lepVector + METVector + lepDecay).M();
            _TopStar_mass = (_TopStarHad_mass + _TopStarLep_mass)/2.;
            _tgtg_mass = (bhad + Wj1 + Wj2 + hadDecay + blep + lepVector + METVector + lepDecay).M();


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
            _TopStarHad_mass = (topHad + hadDecay).M();
            _TopStarLep_mass = (blep + lepVector + METVector + lepDecay).M();
            _TopStar_mass = (_TopStarHad_mass + _TopStarLep_mass)/2.;
            _tgtg_mass = (topHad + hadDecay + blep + lepVector + METVector + lepDecay).M();
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
    ljetVectors.clear();
    bjetVectors.clear();
    ljetResVectors.clear();
    bjetResVectors.clear();
    
    
    if (isMC){
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

	_q2weight_Up = 1.;
	_q2weight_Do = 1.;

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
	for (int j=0; j < tree->nLHEPdfWeight_; j++ ){
	    _pdfSystWeight.push_back(tree->LHEPdfWeight_[j]);
	    pdfMean += tree->LHEPdfWeight_[j];
	}
	pdfMean = pdfMean/_pdfSystWeight.size();
	    
	double pdfVariance = 0.;
	for (int j=0; j < _pdfSystWeight.size(); j++){
	    pdfVariance += pow((_pdfSystWeight[j]-pdfMean),2.);
	}
        if (pdfMean==0) pdfMean=1;
	_pdfuncer = sqrt(pdfVariance/_pdfSystWeight.size())/pdfMean;
	_pdfweight_Up = (1. + _pdfuncer);
	_pdfweight_Do = (1. - _pdfuncer);

	_ISRweight_Up = 1.;
	_ISRweight_Do = 1.;

	_FSRweight_Up = 1.;
	_FSRweight_Do = 1.;
	
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
    /*
    for (int i_mc = 0; i_mc <_nGenPart; i_mc++){
	_genPt.push_back(tree->GenPart_pt_[i_mc]);
	_genPhi.push_back(tree->GenPart_phi_[i_mc]);
	_genEta.push_back(tree->GenPart_eta_[i_mc]);
	_genMass.push_back(tree->GenPart_mass_[i_mc]);
	_genStatus.push_back(tree->GenPart_status_[i_mc]);
	_genStatusFlag.push_back(tree->GenPart_statusFlags_[i_mc]);
	_genPDGID.push_back(tree->GenPart_pdgId_[i_mc]);
	_genMomIdx.push_back(tree->GenPart_genPartIdxMother_[i_mc]);
    }

    for (int i_genJet = 0; i_genJet < _nGenJet; i_genJet++){
	_genJetPt.push_back(tree->GenJet_pt_[i_genJet]);
	_genJetEta.push_back(tree->GenJet_eta_[i_genJet]);
	_genJetPhi.push_back(tree->GenJet_phi_[i_genJet]);
	_genJetMass.push_back(tree->GenJet_mass_[i_genJet]);
    }
    */
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
    std::string fName = "weight/BtagSF/btag_efficiencies_"+year+".root";
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
