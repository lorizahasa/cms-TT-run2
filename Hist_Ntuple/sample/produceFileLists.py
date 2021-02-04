import os
import sys
import subprocess

#IMPORT MODULES FROM OTHER DIR
sys.path.insert(0, os.getcwd().replace("Hist_Ntuple/sample","Skim_NanoAOD/sample"))
from NanoAOD_Gen_SplitJobs_cff import Samples_2016, Samples_2017, Samples_2018
eosDir = "/store/user/rverma/Output/cms-TT-run2/Ntuple_Skim" 
#for year in [2016]:
skimFiles = open('Ntuple_Skim_FileLists_cff.py','w')
#for year in [2016,2017,2018]:
for year in [2016]:
    print  "------------: %s :-----------"%year 
    print  "Sub\t  Done\t Diff\t Sample"
    missingJobs = {}
    line = ""
    sampleList = eval("Samples_%i"%year)
    for sampleName, nJob in sampleList.items():
        line += "%s_%s"%(sampleName,year) 
        #line += sampleName
        #extraArgs = "%s_Ntuple_Skim*.root"%sampleName
        extraArgs = "%s_%s_Ntuple*.root"%(sampleName,year)
        filePath = '%s/%i/%s'%(eosDir, year, extraArgs)
        fileList = subprocess.Popen('eos root://cmseos.fnal.gov/ ls %s'%filePath ,shell=True,stdout=subprocess.PIPE).communicate()[0].split('\n')
        fileList.remove("")
        nFiles = len(fileList)
        allFiles = []
        for f in fileList:
            allFiles.append(str(f).split("/")[-1])
        line += " = "
        line += str(allFiles)
        line += '\n\n'
        print("%i\t %i\t %i\t %s"%(nJob, nFiles, nJob-nFiles, sampleName))
        if nFiles is not nJob:
            missingJobs[sampleName] = nJob -nFiles
    skimFiles.write(line.encode('ascii'))
    print "Missing jobs:", missingJobs
skimFiles.close()

