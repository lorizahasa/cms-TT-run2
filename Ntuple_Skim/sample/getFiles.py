import os
import sys
import subprocess
sys.dont_write_bytecode = True

#IMPORT MODULES FROM OTHER DIR
sys.path.insert(0, os.getcwd().replace("sample",""))
sys.path.insert(0, os.getcwd().replace("Ntuple_Skim/sample","Skim_NanoAOD"))
sys.path.insert(0, os.getcwd().replace("Ntuple_Skim/sample","Skim_NanoAOD/sample"))
from SkimInputs import outSkimDir
from NtupleInputs import Years
from JobsNano_cff import Samples_2016Pre, Samples_2016Post,  Samples_2017, Samples_2018 

skimFiles = open('FilesSkim_cff.sh','w')
#for year in [2016]:
for year in Years: 
    print  "------------: %s :-----------"%year 
    print  "Sub\t  Done\t Diff\t Sample"
    missingJobs = {}
    line = ""
    sampleList = eval("Samples_%s"%year)
    skimFiles.write("eosDirSkim=root://cmseos.fnal.gov/%s\n"%outSkimDir)
    allJobs = 0
    for sampleName, fEvt in sampleList.items():
        nJob = fEvt[0]
        allJobs+=nJob
        line += '%s_FileList_%s="'%(sampleName,year)
        extraArgs = "%s_Skim*.root"%sampleName
        fileList = subprocess.Popen('eos root://cmseos.fnal.gov/ ls %s/%s/%s'%(outSkimDir, year, extraArgs),shell=True,stdout=subprocess.PIPE).communicate()[0].split('\n')
        fileList.remove("")
        nFiles = len(fileList)
        joinList = ' '.join(["$eosDirSkim/%s/%s"%(year, str(y).split("/")[-1]) for y in fileList])
        line += joinList
        line += '"\n\n'
        print("%i\t %i\t %i\t %s"%(nJob, nFiles, nJob-nFiles, sampleName))
        if nFiles is not nJob:
            missingJobs[sampleName] = nJob -nFiles
    skimFiles.write(line.encode('ascii'))
    print "All jobs: ", allJobs 
    print "Missing jobs:", missingJobs
skimFiles.close()

