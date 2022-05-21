#-----------------------------------------------------------------
outNtupleDir = "/store/user/rverma/Output/cms-TT-run2/Ntuple_Skim"
#-----------------------------------------------------------------
Years   =  ['2016PreVFP', '2016PostVFP', '2017', '2018']
#Years 	      =	["2018"]
#Decays 	      =	["Semilep", "Dilep"]
Decays 	      =	["Semilep"]
Systs         = ["JetBase", "JECTotal_up", "JECTotal_down", "JER_up", "JER_down"]
#Systs         = ["JetBase"]
#Systs         = ["JECTotal_up"]

#Reduce number of condor jobs w.r.t Skim by a factor of rData and rMC
def reducedJob(nJob, samp):
    rData   = 20
    rMC     = 4 
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
    return n
