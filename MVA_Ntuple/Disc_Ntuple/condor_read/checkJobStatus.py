import os
import sys
import subprocess
import numpy as np
from ROOT import TFile
from termcolor import colored
import itertools
sys.dont_write_bytecode = True

#IMPORT MODULES FROM OTHER DIR
sys.path.insert(0, os.getcwd().replace("condor_read",""))
from DiscInputs import *

checkFile = False

condorLogDir = "tmpSub/log"
#condorLogDir = "tmpSub/log_resub"
#-----------------------------------------
#Function to compare two lists
#----------------------------------------
def returnNotMatches(a, b):
    return [[x for x in a if x not in b], [x for x in b if x not in a]]

#----------------------------------------
#Create jdl file to be resubmitted
#----------------------------------------
logDirResub = "log_resub"
os.system("mkdir -p tmpSub/%s"%logDirResub)
common_command = \
'Universe   = vanilla\n\
should_transfer_files = YES\n\
when_to_transfer_output = ON_EXIT\n\
Transfer_Input_Files = Disc_Ntuple.tar.gz, runReader2.sh\n\
x509userproxy        = /uscms/home/rverma/x509up_u56634\n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\n'%(logDirResub, logDirResub)
jdlFile = open("tmpSub/resubmitJobs.jdl",'w')
jdlFile.write('Executable =  runReader2.sh \n')
jdlFile.write(common_command)
#use_x509userproxy = true\n\

#----------------------------------------
# Search in stdout and stderr files 
#----------------------------------------
print(colored("----: Collecting major errors for ALL years :--------", "red"))
errors = []
errors.append("TNetXNGFile::Open")
#errors.append("TNetXNGFile::Close")
errors.append("permission")
errors.append("ERROR")
errors.append("truncated")
errors.append("zombie")
errors.append("nan")
errors.append("Error")
errors.append("FATAL")

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

localFile = open("tmpSub/localResubmitJobs.txt",'w')
resubJobs = 0
for year, decay, ch in itertools.product(Years, Decays, Channels):
    print("\n+++++++++++++++++++++++++++++++++++++++++++")
    print(colored("Running for: %s, %s, %s"%(year, decay, ch), 'green'))
    print("+++++++++++++++++++++++++++++++++++++++++++")
    #-----------------------------------------
    #Path of the output histrograms
    #----------------------------------------
    outDir="%s/Reader/%s/%s/%s/CombMass/BDTA"%(dirRead, year, decay, ch)

    #----------------------------------------
    #Get all submitted jobs
    #----------------------------------------
    submittedDict = {}
    submittedDict2 = {}
    #Create for Base, Signal region
    for s, r in itertools.product(Samples, Regions.keys()):
        rootFile = "%s_%s_Base.root"%(s, r)
        rootFile2 = "%s__%s__Base.root"%(s, r)
        submittedDict[rootFile] = s
        submittedDict2[rootFile] = rootFile2
        for sv in systVar: 
            if "JE" in sv:
                sv = sv.replace("_up", "Up")
                sv = sv.replace("_down", "Down")
            if "data_obs" not in s:
                rootFile  = "%s_%s_%s.root"%(s, r, sv)
                rootFile2 = "%s__%s__%s.root"%(s, r, sv)
                submittedDict[rootFile] = s
                submittedDict2[rootFile] = rootFile2
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
    corruptedList = []
    if checkFile:
        print(colored("(2): Checking corrupted files ... ", "red")) 
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
            f.Close()
        print("Finished but corrupted jobs: %s"%len(corruptedList))

    print(colored("----: Summary :----", "red"))
    totResubJobs = np.unique(unFinishedList[1]+corruptedList)
    resubJobs = resubJobs +  len(totResubJobs)
    #----------------------------------------
    #Create jdl files
    #----------------------------------------
    if len(unFinishedList) ==0 and len(corruptedList)==0:
        print("Noting to be resubmitted")
    else:
        for f in totResubJobs :
            fName = submittedDict2[f]
            fName_ = fName.split("__")
            samp = fName_[0]
            reg  = fName_[1]
            syst = fName_[2].replace(".root", "")
            jdlFile.write('Arguments  = %s %s %s %s %s %s %s \nQueue 1\n\n' %(year, decay, ch, reg, samp, syst, outDir))
            localFile.write('python reader.py -y %s -d %s -c %s -r %s -s %s --syst %s \n' %(year, decay, ch, reg, samp, syst))
    print(outDir)
jdlFile.close() 
localFile.close()
print("Total jobs to be resubmitted for all years = %s"%resubJobs)
