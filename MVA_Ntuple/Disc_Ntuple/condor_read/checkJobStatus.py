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
import json as js

checkFile = True
logDirResub = "log_resub"
condorLogDir = "tmpSub/log"
is_firstRun = True
if os.path.exists("tmpSub/%s"%logDirResub):
    condorLogDir = "tmpSub/%s"%logDirResub
    is_firstRun = False
#----------------------------------------
#Function to compare two lists
#----------------------------------------
def returnNotMatches(a, b):
    return [[x for x in a if x not in b], [x for x in b if x not in a]]

#----------------------------------------
#Create jdl file to be resubmitted
#----------------------------------------
common_command = \
'Universe   = vanilla\n\
should_transfer_files = YES\n\
when_to_transfer_output = ON_EXIT\n\
Transfer_Input_Files = Disc_Ntuple.tar.gz, runReaderResub.sh\n\
x509userproxy        = /uscms/home/lhasa/x509up_u54210\n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\n'%(logDirResub, logDirResub)
jdlFile = open("tmpSub/resubmitJobs.jdl",'w')
jdlFile.write('Executable =  runReaderResub.sh \n')
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

#----------------------------------------
#Get finished but corrupted jobs
#----------------------------------------
def checkFiles(outDir,finishedList, submittedDict2):
    corruptedList = []
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
        fName = submittedDict2[finished]
        fName_ = fName.split("__")
        samp = fName_[0]
        reg  = fName_[1]
        syst = fName_[2].replace(".root", "")
       # print(f.GetName())
        h = f.Get("%s/%s/%s/hEvents"%(samp,reg,syst))
        if h.Integral() == 0:
            print("Empty events: %s"%fROOT)
            corruptedList.append(finished)
            continue
        f.Close()
    if len(corruptedList)>0:
        print("Finished but corrupted jobs: %s"%len(corruptedList))
    return corruptedList

dicJson = {}
dicJson["jobs"] = []

if is_firstRun:
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
            #if "QCD" in s or "data_obs" in s:
               # s="%s%s"%(s,ch)
            rootFile = "%s_%s_JetBase.root"%(s, r)
            rootFile2 = "%s__%s__JetBase.root"%(s, r)
            submittedDict[rootFile] = s
            submittedDict2[rootFile] = rootFile2
            for sv in systVar_by_year[year]: 
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
       # print(finishedList)
       # print(submittedDict.keys())

        print(colored("(2): Checking corrupted files ... ", "red")) 
        corruptedList = checkFiles(outDir,finishedList,submittedDict2)
        #corruptedList = ["DYJets_ttyg_Enriched_SR_Resolved_JEC_AbsoluteDown.root"]
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
                if "JE" in syst:
                    syst=syst.replace("Up","_up").replace("Down","_down")
                jdlFile.write('Arguments  = %s %s %s %s %s %s %s \nQueue 1\n\n' %(year, decay, ch, reg, samp, syst, dirRead))
                dicJson["jobs"].append([year, decay, ch, reg, samp, syst, dirRead])
                localFile.write('python reader.py -y %s -d %s -c %s -r %s -s %s --syst %s \n' %(year, decay, ch, reg, samp, syst))
        print(dirRead)
    os.system("mkdir -p tmpSub/%s"%logDirResub)
    jsonFile = open("tmpSub/resubmitJobs.json",'w')
    jdlFile.close() 
    js.dump(dicJson, jsonFile, indent=4)
    localFile.close()
    print("Total jobs to be resubmitted for all years = %s"%resubJobs)
else:
    loadedFile = js.load(open("tmpSub/resubmitJobs.json","r"))
   # print(loadedFile["jobs"])

    newJson = open("tmpSub/resubmitJobs.json","w")
    newDJson ={}
    newDJson["jobs"]=[]
    #corrList = []
    subD2 ={}
    print(colored("(2): Checking corrupted files ... ", "red")) 
    for r in loadedFile["jobs"]:
        if "JE" in r[5] or "Weight" in r[5]:
            syst=r[5].replace("_up", "Up").replace("_down", "Down")
        fileName = "%s_%s_%s.root"%(r[4],r[3],syst)
        subD2[fileName]="%s__%s__%s.root"%(r[4],r[3],syst)
        resubList = []
        resubList.append(fileName)
        outDir="%s/Reader/%s/%s/%s/CombMass/BDTA"%(dirRead, r[0], r[1], r[2])
        corrList = checkFiles(outDir, resubList, subD2)
        if len(corrList)>0:
            newDJson["jobs"].append(r)
            jdlFile.write('Arguments  = %s %s %s %s %s %s %s \nQueue 1\n\n' %(r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
            print(corrList)
    js.dump(newDJson, newJson, indent=4)
    #jdlFile.close()
