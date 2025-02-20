import os
import sys
import subprocess
import itertools
import numpy as np
from ROOT import TFile
from termcolor import colored
sys.dont_write_bytecode = True
from optparse import OptionParser

#IMPORT MODULES FROM OTHER DIR
sys.path.insert(0, os.getcwd().replace("condor",""))
sys.path.insert(0, os.getcwd().replace("Ntuple_Skim/condor","Skim_NanoAOD/sample"))
from NtupleInputs import *
from JobsNano_cff import Samples_2016Pre, Samples_2016Post,  Samples_2017, Samples_2018 

#condorLogDir = "tmpSub/log"
condorLogDir = "tmpSub/log_resub"
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
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--isCheck","--isCheck", dest="isCheck",action="store_true",default=False, help="Check for minimum inputs")
(options, args) = parser.parse_args()
isCheck = options.isCheck

if isCheck:
    Years  = [Years[0]]
    Decays = [Decays[0]]

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
request_memory= 4096 \n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\
Log    = %s/log_$(cluster)_$(process).condor\n\n'%(logDirResub, logDirResub, logDirResub)
jdlFile = open("tmpSub/resubmitJobs.jdl",'w')
jdlFile.write('Executable =  runMakeNtuple.sh \n')
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
#errors.append("Error")
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

def get_directory_sizes_eos(directory):
    print("Executing get_directory_sizes_eos()")
    sizes = {}  # Dictionary to store file sizes
    command = f"eos root://eoscms.cern.ch ls -l {directory}"
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        output_lines = result.stdout.splitlines()
        #print (output_lines)
        for line in output_lines[0:]:  # Skip the first line (header)
            fields = line.split()
            size = int(fields[4])  # Fifth field is the size in bytes
            filename = fields[-1]  # Last field is the filename
            sizes[filename] = size
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    return sizes

def run_yd_syst(year, decay, syst):
    print("\n+++++++++++++++++++++++++++++++++++++++++++")
    print(colored("Running for: %s, %s, %s"%(year, decay, syst), 'green'))
    print("+++++++++++++++++++++++++++++++++++++++++++")
    #-----------------------------------------
    #Path of the output histrograms
    #----------------------------------------
    outDir="%s/%s/%s/%s"%(outNtupleDir, year, decay, syst)
    sizes_dict = get_directory_sizes_eos(outDir)
    #print(sizes_dict)
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
    #finishedList = subprocess.Popen('eos root://cmseos.fnal.gov/ ls %s'%(outDir),shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf8').split('\n')
    finishedList = subprocess.Popen('eos root://eoscms.cern.ch/ ls %s'%(outDir),shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf8').split('\n')
    finishedList.remove("")

    print("Total finished jobs: %s"%len(finishedList))
    
    #----------------------------------------
    #Get all un-finished jobs
    #----------------------------------------
    unFinJobs = len(submittedDict.keys()) - len(finishedList)
    print("Unfinished jobs: %s"%(unFinJobs))
    unFinishedList = returnNotMatches(finishedList, submittedDict.keys())   
    print(unFinishedList)
    global resubJobs
    resubJobs +=unFinJobs
    
    #----------------------------------------
    #Get finished but corrupted jobs
    #----------------------------------------
    print(colored("(2): Checking corrupted files ... ", "red")) 
    corruptedList = []
    nEvents = {}
    for finished in finishedList:
        try:
            if sizes_dict[finished]> 50000: 
                continue
        except:
            corruptedList.append(finished)
        print(finished)
        #fROOT = "root://cmseos.fnal.gov/%s/%s"%(outDir, finished)
        fROOT = "root://eoscms.cern.ch/%s/%s"%(outDir, finished) 
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
        h = f.Get("hAll_MuTrig")
        tree = f.Get("AnalysisTree")
        if not tree:
            print("No tree in: %s"%fROOT)
            corruptedList.append(finished)
            continue
        try:
            nEvents[finished] = [h.GetBinContent(1), tree.GetEntries()]
        except: 
            print(fROOT)
            corruptedList.append(finished)
            continue
    print("Finished but corrupted jobs: %s"%len(corruptedList))
    resubJobs += len(corruptedList)
   
    '''
    print(colored("(3): Checking same nEvents from NanoAOD and Skim ...", "red"))
    print("nDAS_Skim\t nDAS_Ntuple\t nNtuple\t %nDAS \tSample")
    for samp in sampleDict.keys():
        if "Data" in samp and "_" in syst: continue
        nSkim = sampleDict[samp][2]
        nNtuple = 0
        nSkim2  = 0
        for fileSkim in nEvents.keys():
            if samp == fileSkim.split("_Ntuple")[0]:
                nSkim2+=nEvents[fileSkim][0]
                nNtuple+=nEvents[fileSkim][1]
        dSkim = abs(nSkim - nSkim2)
        pDiff = "%s"%dSkim
        if(dSkim >10):
            pDiff = "%s ->"%dSkim
        print("%10s %15s, %10s, %10s, %10s%s\t %s"%(nSkim, nSkim2, pDiff, int(nNtuple), int(100*(nNtuple/nSkim)), '%', samp))
    '''

    #argListYear = []
    #for arg in argList:
    #    if year==arg[0]:
    #        print(arg[1:-1])
    #        argListYear.append(arg)
    #resubJobs += len(argListYear)
    #print("Total jobs with errors = %s"%len(argListYear))
       
    #----------------------------------------
    #Create jdl files
    #----------------------------------------
    allResub = []
    if len(unFinishedList) ==0 and len(corruptedList)==0: #and len(argListYear)==0:
        print("Nothing to be resubmitted")
    else:
        for f in unFinishedList[1]+corruptedList:
            samp = submittedDict[f]
            nJobs = getJobs(f)
            allResub.append("%s__%s__%s__%s__%s__%s__%s"%(year, decay, syst, samp, nJobs[0], nJobs[1], outDir))
        #for arg in argListYear:
        #    allResub.append("%s__%s__%s__%s__%s__%s__%s"%(arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], arg[6]))
    
    for resub in np.unique(allResub):
         r = resub.split("__")
         args = 'Arguments  = %s %s %s %s %s %s %s \nQueue 1\n\n' %(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
         jdlFile.write(args)
    print(outDir)

resubJobs = 0
for year, decay in itertools.product(Years, Decays):
    systs = get_syst_List(year, decay)
    if isCheck:
        systs = [systs[0]]
    for syst in systs:
        run_yd_syst(year, decay, syst)

jdlFile.close() 
print("Total jobs to be resubmitted for all years = %s"%resubJobs)
