


TFile *f_trigSF_BCDEF   = new TFile("stack/muonSF/triggreSF_BCDEF.root");
TFile *f_trigSF_GH      = new TFile("stack/muonSF/triggreSF_GH.root");
TFile *f_idSF_BCDEF     = new TFile("stack/muonSF/idSF_BCDEF.root");
TFile *f_idSF_GH        = new TFile("stack/muonSF/idSF_GH.root");
TFile *f_trackSF_BCDEF  = new TFile("stack/muonSF/trackingSF_BCDEF.root");
TFile *f_trackSF_GH     = new TFile("stack/muonSF/trackingSF_GH.root");
TFile *f_isoSF_BCDEF        = new TFile("stack/muonSF/isoSF_BCDEF.root");
TFile *f_isoSF_GH       = new TFile("stack/muonSF/isoSF_GH.root");

TFile *f_ele_recoSF     = new TFile("stack/eleSF/ele_recoSF.root");
TFile *f_ele_veto_idSF  = new TFile("stack/eleSF/ele_veto_idSF.root");
TFile *f_ele_medium_idSF= new TFile("stack/eleSF/ele_medium_idSF.root");
TFile *f_ele_trigSF     = new TFile("stack/eleSF/ele_trigSF_Run2016All_v1.root");

TFile *f_fitDiag     = new TFile("fitDiagnostics_data.root");
//--------------------------------------------
//functions 
//--------------------------------------------
TH2F* get2DHisto(TFile *histFile, TString histPath, TString histName){
  TH2F* hist = (TH2F*)(histFile->Get(histPath+histName));
  return hist;
}
TH2F* decorate2DHist(TH2F* hist, TString myTit, TString xTit, TString yTit, TString zTit, int color, bool isFitDiag=false){
  hist->SetTitle(myTit);
  hist->SetTitleSize(0.1);
  hist->SetFillColor(color);
  //hist->GetXaxis()->SetTitle(xTit);
  //hist->GetYaxis()->SetTitle(yTit);
  hist->GetZaxis()->SetTitle(zTit);
  if(isFitDiag){
    //sys+stat
    hist->GetYaxis()->SetRangeUser(172, 202);
    hist->GetXaxis()->SetRangeUser(0, 30);
    hist->GetXaxis()->SetLabelSize(0.04);   
    hist->GetYaxis()->SetLabelSize(0.04);   
    //hist->SetMarkerSize(1.0);
    hist->SetMarkerSize(0.8);
    hist->GetXaxis()->LabelsOption("v");
    hist->GetZaxis()->SetLabelSize(0.03);
  }
  hist->GetYaxis()->SetTitleOffset(1.10);
  hist->GetXaxis()->SetTitleOffset(0.90);
  hist->GetYaxis()->SetTitleSize(0.05);   
  hist->GetXaxis()->SetTitleSize(0.05);
  hist->GetXaxis()->SetLabelSize(0.03);   
  hist->GetYaxis()->SetLabelSize(0.03);   
  //hist->GetXaxis()->SetTickLength(0.05); 
  hist->GetXaxis()->SetNdivisions(5); 
  //hist->SetMinimum(pMin);
  return hist;
}

void draw2DHist(TH2F * hist, TString outName, bool isDrawText=true, bool isFitDiag=false){
  gStyle->SetOptStat(0);
  if(isFitDiag) gStyle->SetPaintTextFormat("0.2f");
  else gStyle->SetPaintTextFormat("0.3f");
  gStyle->SetTextSize(0.01);
  TCanvas *c1 = new TCanvas();
  c1->cd();
  if(isFitDiag){
    gPad->SetBottomMargin(0.25);
    gPad->SetLeftMargin(0.15);
    gPad->SetRightMargin(0.07);
    gPad->SetTopMargin(0.055);
  }
  else{
    gPad->SetBottomMargin(0.10);
    gPad->SetLeftMargin(0.12);
    gPad->SetRightMargin(0.12);
  }
  //gStyle->SetPalette(55);
  if(isDrawText && isFitDiag)hist->Draw("colz text");
  else if(isDrawText )hist->Draw("colz text");
  else hist->Draw("colz");
  gPad->Update();
  if(isFitDiag){
    TPaletteAxis *palette = (TPaletteAxis*)hist->GetListOfFunctions()->FindObject("palette");
   palette->SetX1NDC(0.93);
   palette->SetX2NDC(0.95);
  }
  c1->SaveAs("2DHist/"+outName+".pdf");
}

void plot2DHist(){
  /* 
  TH2F* h_trigSF_BCDEF = get2DHisto(f_trigSF_BCDEF, "IsoMu24_OR_IsoTkMu24_PtEtaBins/", "abseta_pt_ratio");
  decorate2DHist(h_trigSF_BCDEF, "Muon trigger SF for era BCDEF", "", "", "",1);
  draw2DHist(h_trigSF_BCDEF, "mu_trigSF_BCDEF");
  
  TH2F* h_trigSF_GH = get2DHisto(f_trigSF_GH, "IsoMu24_OR_IsoTkMu24_PtEtaBins/", "abseta_pt_ratio");
  decorate2DHist(h_trigSF_GH, "Muon trigger SF for era GH", "", "", "",1);
  draw2DHist(h_trigSF_GH, "mu_trigSF_GH");

  TH2F* h_idSF_BCDEF = get2DHisto(f_idSF_BCDEF, "MC_NUM_MediumID2016_DEN_genTracks_PAR_pt_eta/", "abseta_pt_ratio");
  decorate2DHist(h_idSF_BCDEF, "Muon identification SF for era BCDEF", "", "", "",1);
  draw2DHist(h_idSF_BCDEF, "mu_idSF_BCDEF");

  TH2F* h_idSF_GH = get2DHisto(f_idSF_GH, "MC_NUM_MediumID2016_DEN_genTracks_PAR_pt_eta/", "abseta_pt_ratio");
  decorate2DHist(h_idSF_GH, "Muon identification SF for era GH", "", "", "",1);
  draw2DHist(h_idSF_GH, "mu_idSF_GH");
  
  TH2F* h_isoSF_BCDEF = get2DHisto(f_isoSF_BCDEF, "TightISO_MediumID_pt_eta/", "abseta_pt_ratio");
  decorate2DHist(h_isoSF_BCDEF, "Muon isolation SF for era BCDEF", "", "", "",1);
  draw2DHist(h_isoSF_BCDEF, "mu_isoSF_BCDEF");
  
  TH2F* h_isoSF_GH = get2DHisto(f_isoSF_GH, "TightISO_MediumID_pt_eta/", "abseta_pt_ratio");
  decorate2DHist(h_isoSF_GH, "Muon isolation SF for era GH", "", "", "",1);
  draw2DHist(h_isoSF_GH, "mu_isoSF_GH");

  TH2F* h_ele_recoSF = get2DHisto(f_ele_recoSF, "", "EGamma_SF2D");
  decorate2DHist(h_ele_recoSF, "Electron reconstruction SF for era GH", "", "", "",1);
  draw2DHist(h_ele_recoSF, "ele_recoSF", false);

  TH2F* h_ele_veto_idSF = get2DHisto(f_ele_veto_idSF, "", "EGamma_SF2D");
  decorate2DHist(h_ele_veto_idSF, "Electron veto ID SF for era GH", "", "", "",1);
  draw2DHist(h_ele_veto_idSF, "ele_veto_idSF");

  TH2F* h_ele_medium_idSF = get2DHisto(f_ele_medium_idSF, "", "EGamma_SF2D");
  decorate2DHist(h_ele_medium_idSF, "Electron veto ID SF for era GH", "", "", "",1);
  draw2DHist(h_ele_medium_idSF, "ele_medium_idSF");

  TH2F* h_ele_trigSF = get2DHisto(f_ele_trigSF, "", "Ele27_WPTight_Gsf");
  decorate2DHist(h_ele_trigSF, "Electron trigger SF for era GH", "", "", "",1);
  draw2DHist(h_ele_trigSF, "ele_trigSF", false);
  */
  TH2F* h_fitDiag = get2DHisto(f_fitDiag, "", "covariance_fit_s");
  //decorate2DHist(h_fitDiag, "Correlation matrix of systematics NPs", "", "", "",1,true);
  decorate2DHist(h_fitDiag, "Correlation matrix of a few fit parameters", "", "", "",1,true);
  draw2DHist(h_fitDiag, "fitDiag", true, true);

  //draw2DHist(f_trackSF_BCDEF, "", "ratio_eff_aeta_dr030e030_corr");
  //draw2DHist(f_trackSF_GH, "", "ratio_eff_aeta_dr030e030_corr");
}


