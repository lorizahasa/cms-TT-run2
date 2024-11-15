#-----------------------------------------------------------------
#outNtupleDir = "/store/user/rverma/Output/cms-TT-run2/Ntuple_Skim"
outNtupleDir = "/store/group/phys_b2g/lhasa/Output/cms-TT-run2/Ntuple_Skim"
#-----------------------------------------------------------------
#Years   =  ['2016Pre', '2016Post', '2017', '2018']
Years 	      =	["2017"]
#Decays 	      =	["Semilep", "Dilep"]
Decays 	      =	["Semilep"]

#https://twiki.cern.ch/twiki/bin/viewauth/CMS/JECUncertaintySources#Main_uncertainties_2018_Autumn18
JME     = ["JEC_Total", "JER"]
JME_dic = {}
JME_dic["2016Pre"] = ["JEC_Total", "JEC_Absolute","JEC_Absolute_2016","JEC_BBEC1", "JEC_BBEC1_2016","JEC_EC2","JEC_EC2_2016","JEC_HF","JEC_HF_2016","JEC_RelativeSample_2016","JEC_RelativeBal","JEC_FlavorQCD","JER"]
JME_dic["2016Post"] = JME_dic["2016Pre"]
JME_dic["2017"] =  ["JEC_Total", "JEC_Absolute","JEC_Absolute_2017","JEC_BBEC1", "JEC_BBEC1_2017","JEC_EC2","JEC_EC2_2017","JEC_HF","JEC_HF_2017","JEC_RelativeSample_2017","JEC_RelativeBal","JEC_FlavorQCD","JER"]
JME_dic["2018"]= ["JEC_Total", "JEC_Absolute","JEC_Absolute_2018","JEC_BBEC1", "JEC_BBEC1_2018","JEC_EC2","JEC_EC2_2018","JEC_HF","JEC_HF_2018","JEC_RelativeSample_2018","JEC_RelativeBal","JEC_FlavorQCD","JER"]

Levels  = ["up", "down"]

def get_syst_List(year, decay):
    syst_List = ["JetBase"]
    for level in Levels:
        if "Dilep" in decay:
            for jme in JME:
                syst_List.append("%s_%s"%(jme, level))
        if  "Semilep" in decay:
            for jme in JME_dic[year]:
                syst_List.append("%s_%s"%(jme, level))
    return  syst_List

#Reduce number of condor jobs w.r.t Skim by a factor of rData and rMC
def reducedJob(nJob, samp):
    rData   = 20
    rMC     = 5 
    if "Data" in samp:
        if nJob>rData:
            n = nJob/rData
        else:
            n = 1
    if not "Data" in samp:
        if nJob>rMC:
            n = nJob/rMC
        else:
            n = 1
    return int(n)
