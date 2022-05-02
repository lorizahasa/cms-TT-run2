
//////////////////////////
// Cross Sections Used  //
//////////////////////////
std::map<std::string, vector<double> > crossSections;
void initCrossSections(){
    //--------------------------
    // Signal samples
    //--------------------------
    double bTyTg = 0.03*0.97*2;
    crossSections["Signal_M700"]   =  {bTyTg*4.92};    
    crossSections["Signal_M800"]   =  {bTyTg*1.68};    
    crossSections["Signal_M900"]   =  {bTyTg*0.636};   
    crossSections["Signal_M1000"]  =  {bTyTg*0.262};   
    crossSections["Signal_M1100"]  =  {bTyTg*0.116};   
    crossSections["Signal_M1200"]  =  {bTyTg*0.0537};  
    crossSections["Signal_M1300"]  =  {bTyTg*0.0261};  
    crossSections["Signal_M1400"]  =  {bTyTg*0.0131};  
    crossSections["Signal_M1500"]  =  {bTyTg*0.00677}; 
    crossSections["Signal_M1600"]  =  {bTyTg*0.00359}; 

    //--------------------------
    // tty samples
    //--------------------------
    double kf = 1.4852;
    crossSections["TTGamma_Dilepton"]    =  {1.495*kf};
    crossSections["TTGamma_SingleLept"]  =  {5.056*kf};
    crossSections["TTGamma_Hadronic"]    =  {4.149*kf};

    crossSections["TTGamma_Dilepton_Pt100"]    =  {0.0341*kf};
    crossSections["TTGamma_SingleLept_Pt100"]  =  {0.1309*kf};
    crossSections["TTGamma_Hadronic_Pt100"]    =  {0.1249*kf};

    crossSections["TTGamma_Dilepton_Pt200"]    =  {0.00679*kf}; 
    crossSections["TTGamma_SingleLept_Pt200"]  =  {0.02685*kf}; 
    crossSections["TTGamma_Hadronic_Pt200"]    =  {0.02687*kf}; 

    //Need to check Dilep and SingleLep xss
    crossSections["TTGamma_Dilepton_TuneUp"]    = {1.495*kf};
    crossSections["TTGamma_Dilepton_TuneDown"]  = {1.495*kf};
    crossSections["TTGamma_SingleLept_TuneUp"]  = {5.056*kf};
    crossSections["TTGamma_SingleLept_TuneDown"]= {5.056*kf};

    //--------------------------
    // tt samples
    //--------------------------
    //ttbar NNLO (http://inspirehep.net/search?p=find+eprint+1112.5675)
    crossSections["TTbarPowheg"]              =  {831.76}; 
    crossSections["TTbarPowheg_Hadronic"]     =  {380.095};
    crossSections["TTbarPowheg_Semilept"]     =  {364.352};
    crossSections["TTbarPowheg_Dilepton"]     =  { 87.315};

    //--------------------------
    // single t 
    //--------------------------
    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns//TT_X
    crossSections["ST_s_channel"]       =  {3.68064};
    crossSections["ST_t_channel"]       =  {136.02}; 
    crossSections["ST_tbarW_channel"]   =  { 35.85}; 
    crossSections["ST_tW_channel"]      =  { 35.85}; 
    crossSections["ST_tbar_channel"]    =  { 80.95}; 
    crossSections["TGJets"]             =  {2.967};

    //--------------------------
    // y+jets
    //--------------------------
    // GJets cross sections taken from AN2016_471_v6 (SUSY photon + MET analysis)
    crossSections["GJets_HT40To100"]  = {20790.};
    crossSections["GJets_HT100To200"] = {9238.}; 
    crossSections["GJets_HT200To400"] = {2305.}; 
    crossSections["GJets_HT400To600"] = {274.4}; 
    crossSections["GJets_HT600ToInf"] = {93.46}; 

    //--------------------------
    // DY+jets
    //--------------------------
    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns
    crossSections["DYjetsM50"]         =  {6077.22}; 
    crossSections["DYjetsM10to50"]     =  {18610.};  
    
    //--------------------------
    // W + jets samples
    //--------------------------
    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns//W_jets
    // Unused crossSections["WjetsInclusive"]    = {61526.7, 61526.7, 61526.7}; 
    crossSections["W1jets"]            =  {11775.9345}; //9493.0;
    crossSections["W2jets"]            =  { 3839.4345};  //3120.0;
    crossSections["W3jets"]            =  { 1165.8108}; //942.3;
    crossSections["W4jets"]            =  {  592.9176}; //524.2;

    //--------------------------
    //QCD mu
    //--------------------------
    //Product fo XS and filter eff from table at:
    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns//QCD
    crossSections["QCD_Pt20to30_Mu"]    = {2960198.4   };
    crossSections["QCD_Pt30to50_Mu"]    = {1652471.46  };
    crossSections["QCD_Pt50to80_Mu"]    = { 437504.1   };
    crossSections["QCD_Pt80to120_Mu"]   = { 106033.6648};
    crossSections["QCD_Pt120to170_Mu"]  = {  25190.5151};
    crossSections["QCD_Pt170to300_Mu"]  = {   8654.4932};
    crossSections["QCD_Pt300to470_Mu"]  = {    797.3527};
    crossSections["QCD_Pt470to600_Mu"]  = {     79.0255};
    crossSections["QCD_Pt600to800_Mu"]  = {     25.0951};
    crossSections["QCD_Pt800to1000_Mu"] = {      4.7074};
    crossSections["QCD_Pt1000toInf_Mu"] = {      1.6213};

    //--------------------------
    //QCD ele
    //--------------------------
    crossSections["QCD_Pt20to30_Ele"]   = {5352960.};
    crossSections["QCD_Pt30to50_Ele"]   = {9928000.};
    crossSections["QCD_Pt50to80_Ele"]   = {2890800.};
    crossSections["QCD_Pt80to120_Ele"]  = { 350000.};
    crossSections["QCD_Pt120to170_Ele"] = {  62964.};
    crossSections["QCD_Pt170to300_Ele"] = {  18810.};
    crossSections["QCD_Pt300toInf_Ele"] = {   1350.};

    //--------------------------
    // W/Z + y
    //--------------------------
    crossSections["WGamma"]    = {489.};
    crossSections["ZGamma"]    = {98.3};//double check 

    //--------------------------
    // VV 
    //--------------------------
    crossSections["WW"]                = {75.8 };
    crossSections["WZ"]                = {27.6 };
    crossSections["ZZ"]                = {12.14};

    //--------------------------
    // ttV 
    //--------------------------
    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns
    crossSections["TTZtoQQ"]               =  {0.5297}; 
    crossSections["TTWtoQQ"]               =  {0.4062}; 
    crossSections["TTWtoLNu"]              =  {0.2043}; 
    crossSections["TTZtoLL"]               =  {0.2728}; 

    return;
}

double getEvtWeight(string sampleType, int year, double luminosity, double nEvents_MC){
    double evtWeight = -1.;
    if( sampleType.substr(0,4)=="Data") {evtWeight = 1.;}
    else if( sampleType=="Test") {evtWeight = 1.;}
    else if( sampleType=="TestAll") {evtWeight = 1.;}
    else if( sampleType=="TestFull") {evtWeight = 1.;}
    else {
	//	initCrossSections();
	if (crossSections.find(sampleType) != crossSections.end()) {
	    evtWeight = crossSections[sampleType][0] * luminosity / nEvents_MC;
	}
	else {
	    cout << "-------------------------------------------------" << endl;
	    cout << "-------------------------------------------------" << endl;
	    cout << "-- Unable to find event weight for this sample --" << endl;
	    cout << "-- Sample will be saved with a weight of -1    --" << endl;
	    cout << "-------------------------------------------------" << endl;
	    cout << "-------------------------------------------------" << endl;
	}
    }
    cout << "Using event weight " << evtWeight << endl;
    cout << "XS = " << evtWeight/luminosity*nEvents_MC << endl;
    cout << "lumi = " << luminosity << endl;
    cout << "nEvents_MC = " << nEvents_MC << endl;
    
    return evtWeight;
}

