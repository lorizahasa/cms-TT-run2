import os
import sys
import subprocess
import numpy as np
from ROOT import TFile
from termcolor import colored
sys.dont_write_bytecode = True

#IMPORT MODULES FROM OTHER DIR
sys.path.insert(0, os.getcwd().replace("condor",""))
sys.path.insert(0, os.getcwd().replace("condor","sample"))
from SkimInputs import *
from JobsNano_cff import Samples_2016Pre, Samples_2016Post,  Samples_2017, Samples_2018 

#condorLogDir = "tmpSub/log"
condorLogDir = "tmpSub/log_resub"
#-----------------------------------------
#Function to compare two lists
#----------------------------------------
def returnNotMatches(a, b):
    return [[x for x in a if x not in b], [x for x in b if x not in a]]

def getJobs(skim):
    a = skim.split("Skim_")
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
Transfer_Input_Files = Skim_NanoAOD.tar.gz, runMakeSkims.sh\n\
x509userproxy        = /uscms/home/rverma/x509up_u56634\n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\
Log    = %s/log_$(cluster)_$(process).condor\n\n'%(logDirResub, logDirResub, logDirResub)
jdlFile = open("tmpSub/resubmitJobs.jdl",'w')
jdlFile.write('Executable =  runMakeSkims.sh \n')
jdlFile.write(common_command)
#use_x509userproxy = true\n\
localFile = open("tmpSub/localResubmitJobs.txt",'w')


#----------------------------------------
# Search in stdout and stderr files 
#----------------------------------------
print(colored("----: Collecting major errors for ALL years :--------", "red"))
errors = []
errors.append("TNetXNGFile::Open")
#errors.append("TNetXNGFile::Close")
errors.append("permission")
errors.append("truncated")
errors.append("zombie")
errors.append("nan")

errList = []
for err in errors: 
    grepList = subprocess.Popen('grep -l %s %s/*.stderr'%(err, condorLogDir),shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf8').split('\n')
    grepList.remove("")
    errList = errList + grepList
    print(colored("%s for %s jobs = "%(err, len(grepList)), "red"), grepList)

argList = []
for err in np.unique(errList):
    search = "All arguements"
    out = err.replace("stderr", "stdout")
    arg = subprocess.Popen('grep -rn \"%s\" %s'%(search, out),shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf8').split('\n')
    args = arg[0].split(" ")[2:]
    argList.append(args)
#print(argList)

forLocal = []
resubJobs = 0
for year in Years:
    print("\n++++++++++++++++++++++++++++")
    print(colored("Running for: %s"%year, 'green'))
    print("++++++++++++++++++++++++++++")
    #-----------------------------------------
    #Path of the output histrograms
    #----------------------------------------
    outDir="%s/%s"%(outSkimDir, year)

    #----------------------------------------
    #Get all submitted jobs
    #----------------------------------------
    submittedDict = {}
    #Create for Base, Signal region
    sampleDict = eval("Samples_%s"%year)
    for sampleName in sampleDict.keys():
        nJob = sampleDict[sampleName][0]
        for job in range(nJob):
            rootFile = "%s_Skim_%sof%s.root"%(sampleName, job+1, nJob)
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
        except Exception:
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
        h = f.Get("hEvents")
        if not h:
            print("hEvents does not exist: %s"%fROOT)
            corruptedList.append(finished)
            continue
        nEvents[finished] = h.GetBinContent(2)
        f.Close()
    print("Finished but corrupted jobs: %s"%len(corruptedList))

    print(colored("(3): Checking same nEvents from NanoAOD and Skim ...", "red"))
    print("\tnDiff\t nNano\t nSkim\t Sample")
    for samp in sampleDict.keys():
        nNano = sampleDict[samp][2]
        nSkim = 0
        for fileSkim in nEvents.keys():
            if samp == fileSkim.split("_Skim")[0]:
                nSkim+=nEvents[fileSkim]
        print("%10s %10s, %10s\t %s"%(nNano-int(nSkim), nNano, int(nSkim), samp))

    #Print errors for each year
    print(colored("(4): Checking %s  "%errors, "red"))
    argListYear = []
    for arg in argList:
        if year==arg[0]:
            fName = "%s_Skim_%sof%s.root"%(arg[1], arg[2], arg[3])
            print(fName)
            argListYear.append(fName)
    print("Total jobs with these errors = %s"%len(argListYear))

    print(colored("----: Summary :----", "red"))
    totResubJobs = np.unique(unFinishedList[1]+corruptedList+argListYear)
    resubJobs = resubJobs + len(totResubJobs)
    #----------------------------------------
    #Create jdl files
    #----------------------------------------
    if len(unFinishedList) ==0 and len(corruptedList)==0 and len(argListYear)==0:
        print("Noting to be resubmitted")
    else:
        for f in totResubJobs :
            samp = submittedDict[f]
            nJobs = getJobs(f)
            n0 = nJobs[0]
            n1 = nJobs[1]
            args = 'Arguments  = %s %s %s %s %s \nQueue 1\n\n' %(year, samp, n0, n1, outDir)
            jdlFile.write(args)
            forLocal.append([year, n0, n1, samp, outDir])
    print(outDir)

for i, loc in enumerate(forLocal):
    year    = loc[0]
    n0      = loc[1]
    n1      = loc[2]
    samp    = loc[3]
    outDir  = loc[4]
    outFile = "%s_Skim_%sof%s.root"%(samp, n0, n1)
    outFile_ = "%s_Skim_%s_%sof%s.root"%(samp, year, n0, n1)
    cmd1 = "./makeSkim %s %sof%s %s_Skim_%s.root $%s_FileList_%s"%(year, n0, n1, samp, year, samp, year)
    cmd2 = "xrdcp -f  %s root://cmseos.fnal.gov/%s/%s"%(outFile_, outDir, outFile)
    cmd3 = "rm %s"%outFile_
    localFile.write("%s && %s && %s \n"%(cmd1, cmd2, cmd3))
jdlFile.close() 
localFile.close()
print("Total jobs to be resubmitted for all years = %s"%resubJobs)
