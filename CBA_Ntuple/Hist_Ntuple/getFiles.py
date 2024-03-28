import os
import sys
import subprocess
import itertools
sys.dont_write_bytecode = True
import json

#IMPORT MODULES FROM OTHER DIR
sys.path.insert(0, os.getcwd().replace("CBA_Ntuple/Hist_Ntuple","Ntuple_Skim"))
sys.path.insert(0, os.getcwd().replace("CBA_Ntuple/Hist_Ntuple","Skim_NanoAOD/sample"))
from NtupleInputs import * 
from JobsNano_cff import Samples_2016Pre, Samples_2016Post,  Samples_2017, Samples_2018 

ntupleFile = open('FilesNtuple_cff.py','w')
fileJSON = open('FilesNtuple_cff.json','w')
#for year in [2016]:
allJobs = 0
dicJson = {}
for year, decay, in itertools.product(Years, Decays): 
    for syst in SystJME[decay]:
        ntupleFile.write("\n#----------------------------------------------------\n")
        ntupleFile.write("#Year, Decay, Syst: %s, %s, %s\n"%(year, decay, syst))
        ntupleFile.write("#----------------------------------------------------\n")
        print("Year, Decay, Syst: %s, %s, %s"%(year, decay, syst))
        print("Sub\t  Done\t Diff\t Sample")
        missingJobs = {}
        sampleList = eval("Samples_%s"%year)
        for sampleName, fEvt in sampleList.items():
            if "Data" in sampleName and "_" in syst: continue
            #if not "M800" in sampleName: continue
            nJob = reducedJob(fEvt[0], sampleName)
            allJobs+=nJob
            extraArgs = "%s_Ntuple"%sampleName
            fileList = subprocess.Popen('eos root://eoscms.cern.ch/ ls %s/%s/%s/%s'%(outNtupleDir, year, decay, syst),shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf8').split('\n')
            #os.system('eos root://eoscms.cern.ch/ ls %s/%s/%s/%s/'%(outNtupleDir, year, decay, syst))
            fileList2 = []
            for file in fileList:
                if extraArgs in file:
                    fileList2.append(file)

            #fileList2.remove("")
            nFiles = len(fileList2)
            print("%i\t %i\t %i\t %s"%(nJob, nFiles, nJob-nFiles, sampleName))
            if nFiles is not nJob:
                missingJobs[sampleName] = nJob -nFiles
            lineLeft= '%s_%s__%s_FileList_%s'%(decay, syst, sampleName,year)
            ntupleFile.write("\n\n%s = %s"%(lineLeft, fileList2))
            dicJson[lineLeft] = fileList2
    print("Missing jobs:", missingJobs)
print("All jobs: ", allJobs)
ntupleFile.close()
json.dump(dicJson, fileJSON, indent=4)
