
//////////////////////////
// Cross Sections Used  //
//////////////////////////
std::map<std::string, vector<double> > crossSections;
void initCrossSections(){
    //--------------------------
    // Signal samples
    //--------------------------
    //xss for spin 3/2: p p > t* t* > tytg
    //generated using MG_aMC_v2.7.3 with CMSSW_12_4_8 with slc7_amd64_gcc700
    //https://cms-project-generators.web.cern.ch/cms-project-generators/top32.tgz
    double br_tytg = 0.03*0.97*2;
    crossSections["SignalSpin32_M700"]   =  {br_tytg*4.686152e+00};
    crossSections["SignalSpin32_M800"]   =  {br_tytg*1.623764e+00};
    crossSections["SignalSpin32_M900"]   =  {br_tytg*6.192314e-01};
    crossSections["SignalSpin32_M1000"]  =  {br_tytg*2.573151e-01};
    crossSections["SignalSpin32_M1100"]  =  {br_tytg*1.133120e-01};
    crossSections["SignalSpin32_M1200"]  =  {br_tytg*5.251545e-02};
    crossSections["SignalSpin32_M1300"]  =  {br_tytg*2.527675e-02};
    crossSections["SignalSpin32_M1400"]  =  {br_tytg*1.262786e-02};
    crossSections["SignalSpin32_M1500"]  =  {br_tytg*6.498742e-03};
    crossSections["SignalSpin32_M1600"]  =  {br_tytg*3.424087e-03};
    crossSections["SignalSpin32_M1700"]  =  {br_tytg*1.846422e-03};
    crossSections["SignalSpin32_M1800"]  =  {br_tytg*1.009361e-03};
    crossSections["SignalSpin32_M1900"]  =  {br_tytg*5.607416e-04};
    crossSections["SignalSpin32_M2000"]  =  {br_tytg*3.155604e-04};
    crossSections["SignalSpin32_M2250"]  =  {br_tytg*7.825815e-05};
    crossSections["SignalSpin32_M2500"]  =  {br_tytg*2.051170e-05};
    crossSections["SignalSpin32_M2750"]  =  {br_tytg*5.602932e-06};
    crossSections["SignalSpin32_M3000"]  =  {br_tytg*1.585532e-06};

    //xss for spin 1/2: p p > t* t* > tytg
    crossSections["SignalSpin12_M700"]   =  {br_tytg*0.2659};
    crossSections["SignalSpin12_M800"]   =  {br_tytg*0.1147};
    crossSections["SignalSpin12_M900"]   =  {br_tytg*0.05318};
    crossSections["SignalSpin12_M1000"]  =  {br_tytg*0.02590};
    crossSections["SignalSpin12_M1100"]  =  {br_tytg*0.01322};
    crossSections["SignalSpin12_M1200"]  =  {br_tytg*0.006897};
    crossSections["SignalSpin12_M1300"]  =  {br_tytg*0.003732};
    crossSections["SignalSpin12_M1400"]  =  {br_tytg*0.002061};
    crossSections["SignalSpin12_M1500"]  =  {br_tytg*0.001165};
    crossSections["SignalSpin12_M1600"]  =  {br_tytg*0.0006675};
    crossSections["SignalSpin12_M1700"]  =  {br_tytg*0.0003911};
    crossSections["SignalSpin12_M1800"]  =  {br_tytg*0.0002329};
    crossSections["SignalSpin12_M1900"]  =  {br_tytg*0.0001404};
    crossSections["SignalSpin12_M2000"]  =  {br_tytg*0.00008614};
    crossSections["SignalSpin12_M2250"]  =  {br_tytg*0.00002748};
    crossSections["SignalSpin12_M2500"]  =  {br_tytg*0.000009695};
    crossSections["SignalSpin12_M2750"]  =  {br_tytg*0.000003746};
    crossSections["SignalSpin12_M3000"]  =  {br_tytg*0.000001535};

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
    //NLO/NNLO
    crossSections["TTbarPowheg"]              =  {831.76}; 
    crossSections["TTbarPowheg_Hadronic"]     =  {380.095};
    crossSections["TTbarPowheg_Semilept"]     =  {364.352};
    crossSections["TTbarPowheg_Dilepton"]     =  {87.315};

    //--------------------------
    // single t 
    //--------------------------
    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Single_top
    crossSections["ST_tW_channel"]      ={35.85}; //NNLO
    crossSections["ST_tbarW_channel"]   ={35.85}; //NNLO 
    crossSections["ST_t_channel"]       ={136.02};//NLO
    crossSections["ST_tbar_channel"]    ={80.95}; //NLO
    crossSections["ST_s_channel"]       ={3.36};  //NLO
    crossSections["TGJets"]             ={0.952};//NLO, 2.967*0.3208

    //--------------------------
    // Gamma+Jets
    //--------------------------
    // https://twiki.cern.ch/twiki/bin/viewauth/CMS/XsdbTutorialSep#Gamma_jets
    // LO/LO (kf = 1.0)
    crossSections["GJets_HT40To100"]  ={17420.};//{20790.};
    crossSections["GJets_HT100To200"] ={5391.};//{9238.}; 
    crossSections["GJets_HT200To400"] ={1168.};//{2305.}; 
    crossSections["GJets_HT400To600"] ={132.5};//{274.4}; 
    crossSections["GJets_HT600ToInf"] ={44.05};//{93.46}; 

    //--------------------------
    // DY+Jets
    //--------------------------
    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns
    crossSections["DYJetsM50"]         =  {6077.22}; 
    crossSections["DYJetsM10to50"]     =  {18610.};  
    
    //--------------------------
    // W + Jets samples
    //--------------------------
    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns//W_jets
    // Unused crossSections["WJetsInclusive"]    = {61526.7, 61526.7, 61526.7}; 
    crossSections["W1Jets"]            =  {11775.9345}; //9493.0;
    crossSections["W2Jets"]            =  { 3839.4345};  //3120.0;
    crossSections["W3Jets"]            =  { 1165.8108}; //942.3;
    crossSections["W4Jets"]            =  {  592.9176}; //524.2;

    //--------------------------
    //QCD mu
    //--------------------------
    //Product fo XS and filter eff from table at:
    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns//QCD
    crossSections["QCD_Pt15To20_Mu"]    = {3819570.0   };
    crossSections["QCD_Pt20To30_Mu"]    = {2960198.4   };
    crossSections["QCD_Pt30To50_Mu"]    = {1652471.46  };
    crossSections["QCD_Pt50To80_Mu"]    = { 437504.1   };
    crossSections["QCD_Pt80To120_Mu"]   = { 106033.6648};
    crossSections["QCD_Pt120To170_Mu"]  = {  25190.5151};
    crossSections["QCD_Pt170To300_Mu"]  = {   8654.4932};
    crossSections["QCD_Pt300To470_Mu"]  = {    797.3527};
    crossSections["QCD_Pt470To600_Mu"]  = {     79.0255};
    crossSections["QCD_Pt600To800_Mu"]  = {     25.0951};
    crossSections["QCD_Pt800To1000_Mu"] = {      4.7074};
    crossSections["QCD_Pt1000ToInf_Mu"] = {      1.6213};

    //--------------------------
    //QCD ele
    //--------------------------
    crossSections["QCD_Pt15To20_Ele"]   = {2302200.};
    crossSections["QCD_Pt20To30_Ele"]   = {5352960.};
    crossSections["QCD_Pt30To50_Ele"]   = {9928000.};
    crossSections["QCD_Pt50To80_Ele"]   = {2890800.};
    crossSections["QCD_Pt80To120_Ele"]  = { 350000.};
    crossSections["QCD_Pt120To170_Ele"] = {  62964.};
    crossSections["QCD_Pt170To300_Ele"] = {  18810.};
    crossSections["QCD_Pt300ToInf_Ele"] = {   1350.};

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

double getEvtWeight(string sampleType, double luminosity, double nEvents_MC){
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
    cout << "nEvents_NanoAOD = " << nEvents_MC << endl;
    
    return evtWeight;
}

