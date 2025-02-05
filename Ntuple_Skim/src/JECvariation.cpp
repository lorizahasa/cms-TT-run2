#include"../interface/JECvariation.h"
#include<iostream>


JECvariation::JECvariation(){
}

JECvariation::~JECvariation(){
}

void JECvariation::applyJEC(EventTree* tree, correction::CompoundCorrection::Ref jesRefSF, correction::Correction::Ref jesRefUnc, string systVar){

	TLorentzVector tMET;
	tMET.SetPtEtaPhiM(tree->MET_pt_,0.0,tree->MET_phi_,0.0);

	for(int jetInd = 0; jetInd < tree->nJet_ ; ++jetInd){
		if(tree->jetPt_[jetInd] < 10) continue;
		if(fabs(tree->jetEta_[jetInd]) > 5.2) continue;
        //correction = SF
        double rawPt = tree->jetPt_[jetInd] * (1.-tree->jetRawFactor_[jetInd]);
        auto corr = jesRefSF->evaluate({tree->jetArea_[jetInd], tree->jetEta_[jetInd], rawPt, tree->rho_});
        //std::cout<<"Corr = "<< corr <<std::endl;
		TLorentzVector tjet;
		tjet.SetPtEtaPhiM(tree->jetPt_[jetInd], tree->jetEta_[jetInd], tree->jetPhi_[jetInd], 0.0);
		tMET+=tjet;
        //Uncertanity
        auto unc=jesRefUnc->evaluate({tree->jetEta_[jetInd], tree->jetPt_[jetInd]});
        //std::cout<<"Unc = " << unc <<std::endl;
		if(systVar=="down"){ 
            corr-=unc;
           // std::cout<<"Corr down = "<< corr <<std::endl;
        }
		if(systVar=="up"){
            corr+=unc;
           // std::cout<<" Corr up = "<< corr <<std::endl;
        }
        double jes = (1.-tree->jetRawFactor_[jetInd]) * corr;
		
		tree->jetPt_[jetInd] = tree->jetPt_[jetInd] * jes; 
        tree->jetmuEF_[jetInd] = jes; //ad-hoc way of storing jes in other var for cross-check
		tjet.SetPtEtaPhiM(tree->jetPt_[jetInd], tree->jetEta_[jetInd], tree->jetPhi_[jetInd], 0.0);		       
		tMET-=tjet;
	}
	tree->MET_pt_ = tMET.Pt();
	tree->MET_phi_ = tMET.Phi();

}

