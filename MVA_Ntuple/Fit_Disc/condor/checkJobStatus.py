import os
import sys
sys.path.insert(0, os.getcwd().replace("condor", ""))
from HistInputs import *
import itertools
from optparse import OptionParser

#----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016",type='str',
                     help="Specifyi the year of the data taking" )
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
                     help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-d", "--decay", dest="ttbarDecayMode", default="Semilep",type='str',
                     help="Specify which decay moded of ttbar Semilep or Dilep? default is Semilep")
(options, args) = parser.parse_args()
year = options.year
channel = options.channel
decay   = options.ttbarDecayMode


#-----------------------------------------
#Path of the output histrograms
#----------------------------------------
inHistSubDir = "%s/%s/%s"%(year, decay, channel)
#inHistFullDir = "/eos/uscms/%s/%s"%(condorHistDir, inHistSubDir)
inHistFullDir = "%s/%s"%(condorHistDir, inHistSubDir)
condorLogDir = "tmpSub/log"

#----------------------------------------
#Get all submitted jobs
#----------------------------------------
submittedDict = {}
#Create for Base
for sample, r in itertools.product(Samples, Regions.keys()):
    rootFile = "%s_%s_JetBase.root"%(sample, r)
    arguments = "%s %s %s %s %s"%(year, decay, channel, sample, r)
    submittedDict[rootFile] = arguments

#Create for Syst
for sample, syst, level, r in itertools.product(Samples, Systematics, SystLevels, Regions.keys()):
    rootFile = "%s_%s_%s_%s.root"%(sample, r, syst, level)
    arguments = "%s %s %s %s %s %s %s"%(year, decay, channel, sample, syst, level, r)
    if not sample in ["Data", "QCD_DD"]:
        submittedDict[rootFile] = arguments

print("Total submitted jobs: %s"%len(submittedDict.keys()))
for key, value in submittedDict.items():
    pass
    #print key
def returnNotMatches(a, b):
    return [[x for x in a if x not in b], [x for x in b if x not in a]]

#----------------------------------------
#Get all finished jobs
#----------------------------------------
finishedList = os.listdir(inHistFullDir)
print("Total finished jobs: %s"%len(finishedList))

#----------------------------------------
#Get all un-finished jobs
#----------------------------------------
print("Unfinished jobs: %s\n"%(len(submittedDict.keys()) - len(finishedList)))
unFinishedList = returnNotMatches(finishedList, submittedDict.keys())
for unFinished in unFinishedList[1]:
    print(submittedDict[unFinished])

#----------------------------------------
#Get finished but corrupted jobs
#----------------------------------------
corruptedList = []
for finished in finishedList:
    fullPath = "%s/%s"%(inHistFullDir, finished)
    sizeInBytes = os.path.getsize(fullPath)
    if sizeInBytes < 3000:
        corruptedList.append(finished)

print("\nFinished but corrupted jobs: %s"%len(corruptedList))
for corrupted in corruptedList:
    print(corrupted)

#----------------------------------------
# Check log fils as well
#----------------------------------------
grepName = "grep -rn nan %s -A 6 -B 2 "%condorLogDir
print("\n Nan/Inf is propgrated for the following jobs\n")
#os.system(grepName)

#----------------------------------------
#Create jdl file to be resubmitted
#----------------------------------------
condorLogDir = "tmpSub/log"
common_command = \
'Universe   = vanilla\n\
should_transfer_files = YES\n\
when_to_transfer_output = ON_EXIT\n\
Transfer_Input_Files = HistMain.tar.gz, runMakeHists.sh\n\
use_x509userproxy = true\n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\
Log    = %s/log_$(cluster)_$(process).condor\n\n'%(condorLogDir, condorLogDir, condorLogDir)


#----------------------------------------
#Create jdl files
#----------------------------------------
print(len(unFinishedList))
print(unFinishedList)
print(len(corruptedList))
if len(unFinishedList) ==0 and len(corruptedList)==0:
    print("Noting to be resubmitted")
else:
    jdlFileName = 'tmpSub/resubmitJobs_%s%s%s.jdl'%(year, decay, channel)
    jdlFile = open(jdlFileName,'w')
    jdlFile.write('Executable =  runMakeHists.sh \n')
    jdlFile.write(common_command)
    for unFinished in unFinishedList[1]:
        run_command =  \
		'arguments  = %s \n\
queue 1\n\n' %(submittedDict[unFinished])
        jdlFile.write(run_command)
    for corrupted in corruptedList:
        run_command =  \
		'arguments  = %s \n\
queue 1\n\n' %(submittedDict[corrupted])
        jdlFile.write(run_command)
    print("condor_submit %s"%jdlFileName)
    jdlFile.close()
print(inHistFullDir)
