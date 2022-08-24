import os
import sys
import subprocess
import itertools
sys.dont_write_bytecode = True

#IMPORT MODULES FROM OTHER DIR
sys.path.insert(0, os.getcwd().replace("CBA_Ntuple/Hist_Ntuple","Ntuple_Skim"))
sys.path.insert(0, os.getcwd().replace("CBA_Ntuple/Hist_Ntuple","Skim_NanoAOD/sample"))
from NtupleInputs import * 
from JobsNano_cff import Samples_2016Pre, Samples_2016Post,  Samples_2017, Samples_2018 

ntupleFile = open('FilesNtuple_cff.py','w')
#for year in [2016]:
for year, decay, syst in itertools.product(Years, Decays, Systs): 
    ntupleFile.write("\n#----------------------------------------------------\n")
    ntupleFile.write("#Year, Decay, Syst: %s, %s, %s\n"%(year, decay, syst))
    ntupleFile.write("#----------------------------------------------------\n")
    print("Year, Decay, Syst: %s, %s, %s"%(year, decay, syst))
    print  "Sub\t  Done\t Diff\t Sample"
    missingJobs = {}
    sampleList = eval("Samples_%s"%year)
    allJobs = 0
    for sampleName, fEvt in sampleList.items():
        if "Data" in sampleName and "_" in syst: continue
        nJob = reducedJob(fEvt[0], sampleName)
        allJobs+=nJob
        extraArgs = "%s_Ntuple*.root"%sampleName
        fileList = subprocess.Popen('eos root://cmseos.fnal.gov/ ls %s/%s/%s/%s/%s'%(outNtupleDir, year, decay, syst, extraArgs),shell=True,stdout=subprocess.PIPE).communicate()[0].split('\n')
        fileList.remove("")
        nFiles = len(fileList)
        print("%i\t %i\t %i\t %s"%(nJob, nFiles, nJob-nFiles, sampleName))
        if nFiles is not nJob:
            missingJobs[sampleName] = nJob -nFiles
        lineLeft= '%s_%s__%s_FileList_%s'%(decay, syst, sampleName,year)
        ntupleFile.write("\n\n%s = %s"%(lineLeft, fileList))
    print "All jobs: ", allJobs 
    print "Missing jobs:", missingJobs
ntupleFile.close()

