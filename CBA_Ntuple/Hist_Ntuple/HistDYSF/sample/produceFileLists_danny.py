import subprocess
import itertools
import sys
import os
sys.path.insert(0, os.getcwd().replace("Hist_Ntuple/HistDYSF/sample","Ntuple_Skim/"))
sys.path.insert(0, os.getcwd().replace("Hist_Ntuple/HistDYSF/sample","Ntuple_Skim/sample"))
from Skim_NanoAOD_SplitJobs_cff_danny import Samples_2016, Samples_2017, Samples_2018
from NtupleInputs import *

newSamples = []
f1 = open('Ntuple_Skim_FileLists_cff_danny.py','w')
allJobs = 0

def returnNotMatches(a, b):
    return [[x for x in a if x not in b], [x for x in b if x not in a]]

for year, decay, syst in itertools.product(Years, Decays, Systs):
    print  "------------: %s, %s, %s :-----------"%(year, decay, syst) 
    print  "Sub\t  Done\t Diff\t Sample"
    missingJobs = {}
    jobsDictPerYear = {}
    nJobsPerYear = 0
    directory = "%s/%s/%s/%s"%(condorNtupleDir, year, decay, syst)
    year = int(year)
    fileList = subprocess.Popen('xrdfs root://cmseos.fnal.gov/ ls %s'%(directory),shell=True,stdout=subprocess.PIPE).communicate()[0].split('\n')
    allSamples = []
    for x in fileList:
        if len(x)>1:
            sample = x.split('/')[-1]
            sType = sample.split('_%i_Ntuple'%year)[0]
            allSamples.append(sType)
    allSamples.sort()
    newSamples = list(set(allSamples))
    sampleList = eval("Samples_%i"%year)
    for s in newSamples:
        filesPerSample = []
        line = '%s_FileList_%i'%(s, year)
        hasAny=False
        sType = '%s/%s_%i'%(directory, s,year)
        sType_ext = '%s/%s_ext'%(directory, s)
        for f in fileList:
            if f.startswith(sType) or f.startswith(sType_ext): 
                hasAny=True
                f = f.replace(directory, "")
                filesPerSample.append(f)
        fileDict = {}
        fileDict[line] = filesPerSample
        line += " = "
        line += str(filesPerSample)
        line += '\n\n'
        if hasAny:
            f1.write(line.encode('ascii'))
        nJobsPerSample = len(filesPerSample)
        nJobsPerYear+=nJobsPerSample
        allJobs += nJobsPerSample
        jobsDictPerYear[s] = nJobsPerSample

        #check missing jobs
        #print newSamples
        #print sampleList
        subJobs = sampleList[s.split("__")[1]]
        unFinished = 0
        if nJobsPerSample is not subJobs:
            unFinished = subJobs - nJobsPerSample
            missingJobs[s] = subJobs-nJobsPerSample
        print("%i\t %i\t %i\t %s"%(subJobs, nJobsPerSample, unFinished , s))
    print ("Year = %i, nJobs = %i"%(year, nJobsPerYear))
    print "Missing jobs:", missingJobs
    #print returnNotMatches(sampleList, newSamples)
    print len(returnNotMatches(sampleList, newSamples)[0])
print ("Total jobs for all years = %i"%allJobs)
f1.close()

