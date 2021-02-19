#include "../interface/TopEventCombinatorics.h"
#include "TLorentzVector.h"
#include <iostream>

double TopEventCombinatorics::topChiSq(TLorentzVector j1, double sigma_j1,
				       TLorentzVector j2, double sigma_j2,
				       TLorentzVector bh, double sigma_bh,
				       TLorentzVector bl, double sigma_bl,
				       double nu_pz_hypo){

    met.SetPz(nu_pz_hypo);

    //double sigma2_tHad = sigma_j1*sigma_j1 + sigma_j2*sigma_j2 + sigma_bh*sigma_bh;
    //double sigma2_WHad = sigma_j1*sigma_j1 + sigma_j2*sigma_j2;
    //double sigma2_tLep = sigma_bl*sigma_bl + pow(met.Pt()*METRes,2) + pow(lepton.Pt()*leptonRes,2);
    double sigma2_tHad = 34.0*34.0; 
    double sigma2_WHad = 24.0*24.0;
    double sigma2_tLep = 30.0*30.0;

    if (!useResolutions){
	sigma2_tHad = 1.;
	sigma2_WHad = 1.;
	sigma2_tLep = 1.;
    }
    double c = pow( (bh + j1 + j2).M() - mTop,2)/sigma2_tHad + pow( (j1 + j2).M() - mW,2)/sigma2_WHad + pow( (bl + lepton + met).M() - mTop,2)/sigma2_tLep;
    return c;

}

double TopEventCombinatorics::topChiSq_tgtg(TLorentzVector j1, double sigma_j1,
				       TLorentzVector j2, double sigma_j2,
				       TLorentzVector j3, double sigma_j3,
				       TLorentzVector j4, double sigma_j4,
				       TLorentzVector bh, double sigma_bh,
				       TLorentzVector bl, double sigma_bl,
				       double nu_pz_hypo){
    met.SetPz(nu_pz_hypo);
    double _met_px = met.Px();
    double _met_py = met.Py();
    double new_met_E = sqrt(_met_px*_met_px + _met_py*_met_py + nu_pz_hypo*nu_pz_hypo);
    met.SetE(new_met_E);

    //https://arxiv.org/pdf/1711.10949.pdf
    double sigma2_tHad = 34.0*34.0; 
    double sigma2_WHad = 24.0*24.0;
    double sigma2_tLep = 30.0*30.0;
    double sigma2_tstar = 233.0*233.0;
    double term1 = pow( (j1 + j2).M() - mW,2)/sigma2_WHad;
    double term2 = pow( (bh + j1 + j2).M() - mTop,2)/sigma2_tHad;
    //std::cout<<met.E()<<"\t"<<met.Px()<<"\t"<<met.Py()<<"\t"<<met.Pz()<<"\t"<<met.M()<<std::endl;
    double term3 = pow( (bl + lepton + met).M() - mTop,2)/sigma2_tLep;
    double term4 = pow( (bh + j1 + j2 + j3).M() - (bl + lepton + met + j4).M(),2)/sigma2_tstar;
    //double term4 = pow( (bh + j1 + j2 + j3).M() - 800, 2)/sigma2_tstar;
    //double term5 = pow( (bl + lepton + met + j4).M() - 800,2)/sigma2_tstar;
    double c = term1 + term2  + term2  + term4 ;
    //double c = term1 + term2  + term2  + term4 + term5 ;
    return c;

}
double TopEventCombinatorics::topChiSq_tytg(TLorentzVector j1, 
				       TLorentzVector j2, 
				       TLorentzVector j3, 
				       TLorentzVector pho, 
				       TLorentzVector bh, 
				       TLorentzVector bl, 
				       double nu_pz_hypo){
    met.SetPz(nu_pz_hypo);
    double _met_px = met.Px();
    double _met_py = met.Py();
    double new_met_E = sqrt(_met_px*_met_px + _met_py*_met_py + nu_pz_hypo*nu_pz_hypo);
    met.SetE(new_met_E);
    //https://arxiv.org/pdf/1711.10949.pdf
    double sigma2_tHad = 34.0*34.0; 
    double sigma2_WHad = 24.0*24.0;
    double sigma2_tLep = 30.0*30.0;
    double sigma2_tstar = 233.0*233.0;
    double term1 = pow( (j1 + j2).M() - mW,2)/sigma2_WHad;
    double term2 = pow( (bh + j1 + j2).M() - mTop,2)/sigma2_tHad;
    double term3 = pow( (bl + lepton + met).M() - mTop,2)/sigma2_tLep;
    double term4 = pow( (bh + j1 + j2 + j3).M() - (bl + lepton + met + pho).M(),2)/sigma2_tstar;
    double c = term1 + term2  + term2  + term4 ;
    return c;

}
int TopEventCombinatorics::Calculate(){

    goodCombo = false;

    if (jets.size() < 4){
	return -1;
    }

    bJetsList.clear();
    nu_pz_List.clear();

    if (nBjetSize==-1){
	for (unsigned int i =0; i < jets.size(); i++) bJetsList.push_back(i);
    } else {
	for (unsigned int i =0; i < jets.size(); i++){
	    if (btag[i] > btagThresh) bJetsList.push_back(i);
	}
	if (bJetsList.size() < nBjetSize){
	    for (unsigned int i =0; i < jets.size(); i++){
		if (std::find(bJetsList.begin(), bJetsList.end(), i) == bJetsList.end()){
		    bJetsList.push_back(i);
		}
		if (bJetsList.size()==nBjetSize) break;
	    }
	}
    }

    double _nu_pz_1 = metZ.Calculate();
    double _nu_pz_2 = metZ.getOther();
    nu_pz_List.push_back(_nu_pz_1);
    if (_nu_pz_1!=_nu_pz_2) nu_pz_List.push_back(_nu_pz_2);

    chi2 = 9.e9;
    double comboChi2 = 9.e9;

    for (const auto& i_bhad : bJetsList){
	for (const auto& i_blep : bJetsList){
	    if (i_bhad==i_blep) continue;
	    for (unsigned int i_j1=0; i_j1<jets.size(); i_j1++){
		if (i_bhad==i_j1 || i_blep==i_j1) continue; //skip if i_j1 is already used as a bjet
		for (unsigned int i_j2=i_j1+1; i_j2<jets.size(); i_j2++){
		    if (i_bhad==i_j2 || i_blep==i_j2) continue; //skip if i_j2 is already used as a bjet

		    //loop over nu_pz solutions
		    for (const auto& test_nu_pz: nu_pz_List){

			double comboChi2 = topChiSq(jets.at(i_j1), jetsRes.at(i_j1),
						    jets.at(i_j2), jetsRes.at(i_j2),
						    jets.at(i_bhad), jetsRes.at(i_bhad),
						    jets.at(i_blep), jetsRes.at(i_blep),
						    test_nu_pz);
			if (comboChi2 < chi2){
			    chi2 = comboChi2;
			    blep_idx = i_blep;
			    bhad_idx = i_bhad;
			    j1_idx = i_j1;
			    j2_idx = i_j2;
			    nu_pz = test_nu_pz;
			    goodCombo = true;
			}
		    }
		}
	    }
	}
    }

    return 0;
}

int TopEventCombinatorics::Calculate_tgtg(){

    goodCombo_tgtg = false;

    if (jets.size() < 4){
	return -1;
    }

    bJetsList.clear();
    nu_pz_List.clear();

    if (nBjetSize==-1){
	for (unsigned int i =0; i < jets.size(); i++) bJetsList.push_back(i);
    } else {
	for (unsigned int i =0; i < jets.size(); i++){
        //std::cout<<"btag[i]"<<btag[i]<<", btagThresh = "<<btagThresh<<std::endl;
	    if (btag[i] > btagThresh) bJetsList.push_back(i);
	}
	if (bJetsList.size() < nBjetSize){
	    for (unsigned int i =0; i < jets.size(); i++){
		if (std::find(bJetsList.begin(), bJetsList.end(), i) == bJetsList.end()){
		    bJetsList.push_back(i);
		}
		if (bJetsList.size()==nBjetSize) break;
	    }
	}
    }

    double _nu_pz_1 = metZ.Calculate();
    double _nu_pz_2 = metZ.getOther();
    nu_pz_List.push_back(_nu_pz_1);
    if (_nu_pz_1!=_nu_pz_2) nu_pz_List.push_back(_nu_pz_2);
    chi2_tgtg = 9.e9;
    double comboChi2 = 9.e9;
    //chi2_tgtg = 500.0;
    //double comboChi2 = 500.0;

    //std::cout<<"nJets = "<<jets.size()<<std::endl;
    //std::cout<<"nBJets = "<<bJetsList.size()<<std::endl;
    for (const auto& i_bhad : bJetsList){
	for (const auto& i_blep : bJetsList){
	    if (i_bhad==i_blep) continue;
	    for (unsigned int i_j1=0; i_j1<jets.size(); i_j1++){
		if (i_bhad==i_j1 || i_blep==i_j1) continue; //skip if i_j1 is already used as a bjet
		for (unsigned int i_j2=i_j1+1; i_j2<jets.size(); i_j2++){
		    if (i_bhad==i_j2 || i_blep==i_j2) continue; //skip if i_j2 is already used as a bjet
		for (unsigned int i_j3=0; i_j3<jets.size(); i_j3++){
		    if (i_bhad==i_j3 || i_blep==i_j3 || i_j3==i_j1 || i_j3==i_j2) continue; 
		for (unsigned int i_j4=0; i_j4<jets.size(); i_j4++){
		    if (i_bhad==i_j4 || i_blep==i_j4 || i_j4==i_j1 || i_j4==i_j2 || i_j4==i_j3) continue; 
		    //loop over nu_pz solutions
		    for (const auto& test_nu_pz: nu_pz_List){

			double comboChi2 = topChiSq_tgtg(jets.at(i_j1), jetsRes.at(i_j1),
						    jets.at(i_j2), jetsRes.at(i_j2),
						    jets.at(i_j3), jetsRes.at(i_j3),
						    jets.at(i_j4), jetsRes.at(i_j4),
						    jets.at(i_bhad), jetsRes.at(i_bhad),
						    jets.at(i_blep), jetsRes.at(i_blep),
						    test_nu_pz);
            //std::cout<<i_bhad<<"\t"<<i_blep<<"\t"<<i_j1<<"\t"<<i_j2<<"\t"<<i_j3<<"\t"<<i_j4<<"\t"<<comboChi2<<std::endl;
			if (comboChi2 < chi2_tgtg){
			    chi2_tgtg = comboChi2;
			    blep_idx = i_blep;
			    bhad_idx = i_bhad;
			    j1_idx = i_j1;
			    j2_idx = i_j2;
			    j3_idx = i_j3;
			    j4_idx = i_j4;
			    nu_pz = test_nu_pz;
			    goodCombo_tgtg = true;
			}
		    }
		}
	    }
        }
        }
	}
    }

    return 0;
}
int TopEventCombinatorics::Calculate_tytg(){

    goodCombo_tytg = false;

    if (jets.size() < 4){
	return -1;
    }

    bJetsList.clear();
    nu_pz_List.clear();

    if (nBjetSize==-1){
	for (unsigned int i =0; i < jets.size(); i++) bJetsList.push_back(i);
    } else {
	for (unsigned int i =0; i < jets.size(); i++){
        //std::cout<<"btag[i]"<<btag[i]<<", btagThresh = "<<btagThresh<<std::endl;
	    if (btag[i] > btagThresh) bJetsList.push_back(i);
	}
	if (bJetsList.size() < nBjetSize){
	    for (unsigned int i =0; i < jets.size(); i++){
		if (std::find(bJetsList.begin(), bJetsList.end(), i) == bJetsList.end()){
		    bJetsList.push_back(i);
		}
		if (bJetsList.size()==nBjetSize) break;
	    }
	}
    }

    double _nu_pz_1 = metZ.Calculate();
    double _nu_pz_2 = metZ.getOther();
    nu_pz_List.push_back(_nu_pz_1);
    if (_nu_pz_1!=_nu_pz_2) nu_pz_List.push_back(_nu_pz_2);
    chi2_tytg = 9.e9;
    double comboChi2 = 9.e9;
    //chi2_tgtg = 500.0;
    //double comboChi2 = 500.0;

    //std::cout<<"nJets = "<<jets.size()<<std::endl;
    //std::cout<<"nBJets = "<<bJetsList.size()<<std::endl;
    for (unsigned int i_pho=0; i_pho<photons.size(); i_pho++){
    for (const auto& i_bhad : bJetsList){
	for (const auto& i_blep : bJetsList){
	    if (i_bhad==i_blep) continue;
	    for (unsigned int i_j1=0; i_j1<jets.size(); i_j1++){
		if (i_bhad==i_j1 || i_blep==i_j1) continue; //skip if i_j1 is already used as a bjet
		for (unsigned int i_j2=i_j1+1; i_j2<jets.size(); i_j2++){
		    if (i_bhad==i_j2 || i_blep==i_j2) continue; //skip if i_j2 is already used as a bjet
		for (unsigned int i_j3=0; i_j3<jets.size(); i_j3++){
		    if (i_bhad==i_j3 || i_blep==i_j3 || i_j3==i_j1 || i_j3==i_j2) continue; 
		    //loop over nu_pz solutions
		    for (const auto& test_nu_pz: nu_pz_List){

			double comboChi2 = topChiSq_tytg(jets.at(i_j1), 
						    jets.at(i_j2), 
						    jets.at(i_j3), 
						    photons.at(i_pho), 
						    jets.at(i_bhad), 
						    jets.at(i_blep), 
						    test_nu_pz);
            //std::cout<<i_bhad<<"\t"<<i_blep<<"\t"<<i_j1<<"\t"<<i_j2<<"\t"<<i_j3<<"\t"<<i_j4<<"\t"<<comboChi2<<std::endl;
			if (comboChi2 < chi2_tgtg){
			    chi2_tgtg = comboChi2;
			    blep_idx = i_blep;
			    bhad_idx = i_bhad;
			    j1_idx = i_j1;
			    j2_idx = i_j2;
			    j3_idx = i_j3;
                pho_idx = i_pho;
			    nu_pz = test_nu_pz;
                photonIsLeptonSide=true;
			    goodCombo_tytg = true;
			}
			comboChi2 = topChiSq_tytg(jets.at(i_j1), 
						    jets.at(i_j2), 
						    photons.at(i_pho), 
						    jets.at(i_j3), 
						    jets.at(i_bhad), 
						    jets.at(i_blep), 
						    test_nu_pz);
            //std::cout<<i_bhad<<"\t"<<i_blep<<"\t"<<i_j1<<"\t"<<i_j2<<"\t"<<i_j3<<"\t"<<i_j4<<"\t"<<comboChi2<<std::endl;
			if (comboChi2 < chi2_tgtg){
			    chi2_tgtg = comboChi2;
			    blep_idx = i_blep;
			    bhad_idx = i_bhad;
			    j1_idx = i_j1;
			    j2_idx = i_j2;
			    j3_idx = i_j3;
                pho_idx = i_pho;
			    nu_pz = test_nu_pz;
                photonIsLeptonSide=false;
			    goodCombo_tytg = true;
			}
		    }
		}
	    }
        }
        }
	}
    }

    return 0;
}
