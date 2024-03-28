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
#JMEs    = ["JEC_Total", "JEC_SubTotalPileUp", "JEC_SubTotalRelative", "JEC_SubTotalAbsolute", "JEC_FlavorQCD", "JEC_TimePtEta", "JER"]
JMEs = ["JEC_Absolute","JEC_Absolute_2017","JEC_BBEC1", "JEC_BBEC1_2017","JEC_EC2","JEC_EC2_2017","JEC_HF","JEC_HF_2017","JEC_RelativeSample_2017","JEC_RelativeBal","JEC_FlavorQCD","JER"]

Levels  = ["up", "down"]
runMC   = ["JetBase"]
runMCs  = ["JetBase"]
for level in Levels:
    for jme in JME:
        runMC.append("%s_%s"%(jme, level))
    for jme in JMEs:
        runMCs.append("%s_%s"%(jme, level))
SystJME = {}
SystJME["Semilep"] = runMCs 
SystJME["Dilep"]   = runMC

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
