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
from HistInputs import *
from optparse import OptionParser

#----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--isCheck","--isCheck", dest="isCheck",action="store_true",default=False, help="Merge for combined years and channels")
parser.add_option("--isSep","--isSep", dest="isSep",action="store_true",default=False, help="Merge for separate years and channels")
(options, args) = parser.parse_args()
isCheck = options.isCheck
isSep = options.isSep

if isSep:
    isCheck = False
if isCheck:
    isSep  = True
    isComb = False
    Years  = [Years[0]]
    Decays = [Decays[0]]
    Channels = [Channels[0]]
if not isCheck and not isSep:
    print("Add either --isCheck or --isSep in the command line")
    exit()

logDir = "tmpSub/log"
#logDir = "tmpSub/log_resub"
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
Transfer_Input_Files = Hist_Ntuple.tar.gz, runMakeHists.sh\n\
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
grepList = subprocess.Popen('grep -rn nan %s'%(logDir),shell=True,stdout=subprocess.PIPE).communicate()[0].split('\n')
grepList.remove("")
grepList2 = subprocess.Popen('grep -rn rror %s'%(logDir),shell=True,stdout=subprocess.PIPE).communicate()[0].split('\n')
grepList2.remove("")
errList = []
for err in grepList+grepList2:
    errList.append(err.split(":")[0])
argList = []
for err in np.unique(errList):
    if "std" not in err: continue
    search = "All arguements"
    out = err.replace("stderr", "stdout")
    arg = subprocess.Popen('grep -rn \"%s\" %s'%(search, out),shell=True,stdout=subprocess.PIPE).communicate()[0].split('\n')
    args = arg[0].split(" ")[2:]
    argList.append(args)
#print(argList)

resubJobs = 0
for year, decay, ch in itertools.product(Years, Decays, Channels):
    print("\n+++++++++++++++++++++++++++++++++++++++++++")
    print(colored("Running for: %s, %s, %s"%(year, decay, ch), 'green'))
    print("+++++++++++++++++++++++++++++++++++++++++++")
    #-----------------------------------------
    #Path of the output histrograms
    #----------------------------------------
    outDir="%s/Raw/%s/%s/%s"%(dirHist, year, decay, ch)

    #----------------------------------------
    #Get all submitted jobs
    #----------------------------------------
    submittedDict = {}
    for s, r in itertools.product(Samples, Regions.keys()):
        rootFile = "%s_%s_Base.root"%(s, r)
        submittedDict[rootFile] = s
        for syst, level in itertools.product(Systematics, SystLevels): 
            if "data_obs" not in s:
                rootFile = "%s_%s_%s_%s.root"%(s, r, syst, level)
                submittedDict[rootFile] = s
    print(colored("(1): Checking unfinished jobs ...", 'red'))
    print "Total submitted jobs: %s"%len(submittedDict.keys())

    #----------------------------------------
    #Get all finished jobs
    #----------------------------------------
    finishedList = subprocess.Popen('eos root://cmseos.fnal.gov/ ls %s'%(outDir),shell=True,stdout=subprocess.PIPE).communicate()[0].split('\n')
    finishedList.remove("")
    print "Total finished jobs: %s"%len(finishedList)

    #----------------------------------------
    #Get all un-finished jobs
    #----------------------------------------
    unFinJobs = len(submittedDict.keys()) - len(finishedList)
    print "Unfinished jobs: %s"%(unFinJobs)
    unFinishedList = returnNotMatches(finishedList, submittedDict.keys())   
    print unFinishedList
    resubJobs +=unFinJobs

    #----------------------------------------
    #Get finished but corrupted jobs
    #----------------------------------------
    print(colored("(2): Checking corrupted files ... ", "red")) 
    corruptedList = []
    '''
    for finished in finishedList:
        fROOT = "root://cmsxrootd.fnal.gov/%s/%s"%(outDir, finished)
        f = TFile.Open(fROOT, "READ")
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
    print "Finished but corrupted jobs: %s"%len(corruptedList)
    '''
    resubJobs += len(corruptedList)

    print(colored("(3): Checking nan/error ...", "red"))
    argListYear = []
    for arg in argList:
        if year==arg[0]:
            print(arg[1:-1])
            argListYear.append(arg)
    resubJobs += len(argListYear)
    print("Total jobs with nan errors = %s"%len(argListYear))

    #----------------------------------------
    #Create jdl files
    #----------------------------------------
    '''
    allResub = []
    if len(unFinishedList) ==0 and len(corruptedList)==0 and len(argListYear)==0:
        print "Noting to be resubmitted"
    else:
        for f in unFinishedList[1]+corruptedList:
            allResub.append("%s__%s__%s__%s__%s__%s__%s"%(year, decay, ch, samp, nJobs[0], nJobs[1], outDir))
        for arg in argListYear:
            allResub.append("%s__%s__%s__%s__%s__%s__%s"%(arg[0], arg[1], arg[2], arg[3], arg[4], arg[5], arg[6]))

    for resub in np.unique(allResub):
         r = resub.split("__")
         args = 'Arguments  = %s %s %s %s %s %s %s \nQueue 1\n\n' %(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
         jdlFile.write(args)
    print outDir 
    '''
jdlFile.close() 
print("Total jobs to be resubmitted for all years = %s"%resubJobs)
