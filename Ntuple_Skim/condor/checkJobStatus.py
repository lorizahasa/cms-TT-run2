import os
import sys
import subprocess
import itertools
import numpy as np
from ROOT import TFile
from termcolor import colored
sys.dont_write_bytecode = True

#IMPORT MODULES FROM OTHER DIR
sys.path.insert(0, os.getcwd().replace("condor",""))
sys.path.insert(0, os.getcwd().replace("Ntuple_Skim/condor","Skim_NanoAOD/sample"))
from NtupleInputs import *
from JobsNano_cff import Samples_2016Pre, Samples_2016Post,  Samples_2017, Samples_2018 

condorLogDir = "tmpSub/log"
#condorLogDir = "tmpSub/log_resub"
#-----------------------------------------
#Function to compare two lists
#----------------------------------------
def returnNotMatches(a, b):
    return [[x for x in a if x not in b], [x for x in b if x not in a]]

def getJobs(skim):
    a = skim.split("Ntuple_")
    b = a[-1].split(".root")
    c = b[0].split("of")
    return c

#----------------------------------------
#Create jdl file to be resubmitted
#----------------------------------------
logDirResub = "log_resub"
os.system("mkdir -p tmpSub/%s"%logDirResub)
common_command = \
'Universe   = vanilla\n\
should_transfer_files = YES\n\
when_to_transfer_output = ON_EXIT\n\
Transfer_Input_Files = Ntuple_Skim.tar.gz, runMakeNtuple.sh\n\
use_x509userproxy = true\n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\
Log    = %s/log_$(cluster)_$(process).condor\n\n'%(logDirResub, logDirResub, logDirResub)
jdlFile = open("tmpSub/resubmitJobs.jdl",'w')
jdlFile.write('Executable =  runMakeNtuple.sh \n')
jdlFile.write(common_command)
#use_x509userproxy = true\n\


#Search in the log files to see if xrdcp was not able to copy a file
print("Collecting error logs for all years ...")
grepList = subprocess.Popen('grep -rn floating %s'%(condorLogDir),shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf8').split('\n')
grepList.remove("")
grepList2 = subprocess.Popen('grep -rn truncated %s'%(condorLogDir),shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf8').split('\n')
grepList2.remove("")
errList = []
for err in grepList+grepList2:
    errList.append(err.split(":")[0])
argList = []
for err in np.unique(errList):
    if "std" not in err: continue
    search = "All arguements"
    out = err.replace("stderr", "stdout")
    arg = subprocess.Popen('grep -rn \"%s\" %s'%(search, out),shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf8').split('\n')
    args = arg[0].split(" ")[2:]
    argList.append(args)
#print(argList)

resubJobs = 0
for year, decay, syst in itertools.product(Years, Decays, Systs):
    print("\n+++++++++++++++++++++++++++++++++++++++++++")
    print(colored("Running for: %s, %s, %s"%(year, decay, syst), 'green'))
    print("+++++++++++++++++++++++++++++++++++++++++++")
    #-----------------------------------------
    #Path of the output histrograms
    #----------------------------------------
    outDir="%s/%s/%s/%s"%(outNtupleDir, year, decay, syst)

    #----------------------------------------
    #Get all submitted jobs
    #----------------------------------------
    submittedDict = {}
    #Create for Base, Signal region
    sampleDict = eval("Samples_%s"%year)
    for sampleName, fEvt in sampleDict.items():
        if "Data" in sampleName and "_" in syst: continue
        nJob = reducedJob(fEvt[0], sampleName) 
        for job in range(nJob):
            rootFile = "%s_Ntuple_%sof%s.root"%(sampleName, job+1, nJob)
            submittedDict[rootFile] = sampleName

    print(colored("(1): Checking unfinished jobs ...", 'red'))
    print("Total submitted jobs: %s"%len(submittedDict.keys()))

    #----------------------------------------
    #Get all finished jobs
    #----------------------------------------
    finishedList = subprocess.Popen('eos root://cmseos.fnal.gov/ ls %s'%(outDir),shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf8').split('\n')
    finishedList.remove("")
    print("Total finished jobs: %s"%len(finishedList))

    #----------------------------------------
    #Get all un-finished jobs
    #----------------------------------------
    unFinJobs = len(submittedDict.keys()) - len(finishedList)
    print("Unfinished jobs: %s"%(unFinJobs))
    unFinishedList = returnNotMatches(finishedList, submittedDict.keys())   
    print(unFinishedList)
    resubJobs +=unFinJobs

    #----------------------------------------
    #Get finished but corrupted jobs
    #----------------------------------------
    print(colored("(2): Checking corrupted files ... ", "red")) 
    corruptedList = []
    nEvents = {}
    for finished in finishedList:
        fROOT = "root://cmseos.fnal.gov/%s/%s"%(outDir, finished)
        #fROOT = "root://cmsxrootd.fnal.gov/%s/%s"%(outDir, finished)
        try:
            f = TFile.Open(fROOT, "READ")
        except:
            corruptedList.append(finished)
            continue
        if not f:
            print("Null pointer: %s"%fROOT)
            corruptedList.append(finished)
            continue
        if f.IsZombie():
            print("Zombie: %s"%fROOT)
            corruptedList.append(finished)
            continue
        if f.GetSize() < 3000:
            print("Empty file: %s"%fROOT)
            corruptedList.append(finished)
            continue
        #h = f.Get("hEvents")
        #nEvents[finished] = h.Integral()
        tree = f.Get("AnalysisTree")
        if not tree:
            print("No tree in: %s"%fROOT)
            corruptedList.append(finished)
            continue
        nEvents[finished] = tree.GetEntries() 
    print("Finished but corrupted jobs: %s"%len(corruptedList))
    resubJobs += len(corruptedList)

    print(colored("(3): Checking same nEvents from NanoAOD and Skim ...", "red"))
    print(" \tnSkim\t nNtuple\t %nSkim \tSample")
    for samp in sampleDict.keys():
        nSkim = sampleDict[samp][2]
        nNtuple = 0
        for fileSkim in nEvents.keys():
            if samp == fileSkim.split("_Ntuple")[0]:
                nNtuple+=nEvents[fileSkim]
        print("%10s %10s, %10s%s\t %s"%(nSkim, int(nNtuple), int(100*(nNtuple/nSkim)), '%', samp))

    print(colored("(4): Checking xrdcp errors ...", "red"))
    argListYear = []
    for arg in argList:
        if year==arg[0]:
            print(arg[1:-1])
            argListYear.append(arg)
    resubJobs += len(argListYear)
    print("Total jobs with xrdcp errors = %s"%len(argListYear))

    print(colored("(5): Checking Nan or Inf filled in jobs ... ", "red"))
    grepList3 = subprocess.Popen('grep -rn nan %s'%(condorLogDir),shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf8').split('\n')
    grepList3.remove("")
    print("Nan/Inf is propgrated for the following jobs:", grepList3)

    #----------------------------------------
    #Create jdl files
    #----------------------------------------
    allResub = []
    if len(unFinishedList) ==0 and len(corruptedList)==0 and len(argListYear)==0:
        print("Noting to be resubmitted")
    else:
        for f in unFinishedList[1]+corruptedList:
            samp = submittedDict[f]
            nJobs = getJobs(f)
            allResub.append("%s__%s__%s__%s__%s__%s__%s"%(year, decay, syst, samp, nJobs[0], nJobs[1], outDir))
        for arg in argListYear:
            allResub.append("%s__%s__%s__%s__%s__%s__%s"%(arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], arg[6]))

    for resub in np.unique(allResub):
         r = resub.split("__")
         args = 'Arguments  = %s %s %s %s %s %s %s \nQueue 1\n\n' %(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
         jdlFile.write(args)
    print(outDir)
jdlFile.close() 
print("Total jobs to be resubmitted for all years = %s"%resubJobs)
