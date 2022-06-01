import os
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("condor", ""))
import itertools
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

os.system("mkdir -p tmpSub/log")
logDir = "log"
tarFile = "tmpSub/Hist_Ntuple.tar.gz"
if os.path.exists("../hists"):
    os.system("rm -r ../hists")
tarDir ='../../../Hist_Ntuple'
exDir = '--exclude=%s/HistMain --exclude=%s/HistDYSF --exclude=%s/HistWeight --exclude=%s/HistMisIDSF/condor'%(tarDir, tarDir, tarDir, tarDir)
os.system("tar %s -zcvf %s %s"%(exDir, tarFile, tarDir))
os.system("cp runMakeHists.sh tmpSub/")
common_command = \
'Universe   = vanilla\n\
should_transfer_files = YES\n\
when_to_transfer_output = ON_EXIT\n\
Transfer_Input_Files = Hist_Ntuple.tar.gz, runMakeHists.sh\n\
use_x509userproxy = true\n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\
Log    = %s/log_$(cluster)_$(process).condor\n\n'%(logDir, logDir, logDir)

#----------------------------------------
#Create jdl files
#----------------------------------------
subFile = open('tmpSub/condorSubmit.sh','w')
for y, d, c in itertools.product(Years, Decays, Channels):
    outDir = "%s/Raw/%s/%s/%s"%(dirHist, y, d, c)
    os.system("eos root://cmseos.fnal.gov mkdir -p %s"%outDir)
    jdlName = 'submitJobs_%s%s%s.jdl'%(y, d, c)
    jdlFile = open('tmpSub/%s'%jdlName,'w')
    jdlFile.write('Executable =  runMakeHists.sh \n')
    jdlFile.write(common_command)
    for r in Regions.keys():
        args = 'Arguments  = %s %s %s %s Base %s \n'%(y, d, c, r, outDir)
        args += 'Queue 1\n\n' 
        jdlFile.write(args)
        for syst, var in itertools.product(Systematics, SystLevels):
            args = 'Arguments  = %s %s %s %s %s%s %s \n'%(y, d, c, r, syst, var, outDir)
            args += 'Queue 1\n\n'
            jdlFile.write(args)
    subFile.write("condor_submit %s\n"%jdlName)
    jdlFile.close() 
subFile.close()
