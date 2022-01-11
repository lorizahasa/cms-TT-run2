import os
import sys
sys.path.insert(0, os.getcwd().replace("condor", ""))
sys.path.insert(0, os.getcwd().replace("Fit_Disc/FitCombTrain/condor", "Disc_Ntuple/DiscCombTrain"))
from DiscInputs import methodDict
import itertools
from FitInputs import *

tmpDir = "tmpSub"
condorLogDir = "log"
os.system("mkdir -p %s/%s"%(tmpDir, condorLogDir))
tarFile = "tmpSub/FitCombTrain.tar.gz"
exDir = '../../FitCombTrain'
ex = '--exclude=%s/output --exclude=%s/condor'%(exDir, exDir)
os.system("tar %s -zcvf %s ../../FitCombTrain"%(ex, tarFile))
os.system("cp runPerformFit.sh %s"%tmpDir)
os.system("cp /uscms_data/d3/rverma/codes/limitTools/CMSSW_10_2_13.tar.gz %s"%tmpDir)
common_command = \
'Universe   = vanilla\n\
should_transfer_files = YES\n\
when_to_transfer_output = ON_EXIT\n\
Transfer_Input_Files = CMSSW_10_2_13.tar.gz, FitCombTrain.tar.gz, runPerformFit.sh\n\
use_x509userproxy = true\n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\
Log    = %s/log_$(cluster)_$(process).condor\n\n'%(condorLogDir, condorLogDir, condorLogDir)

discDict = {}
discDict["Disc"] = methodDict.keys()
for hist in histList:
    discDict[hist] = ["BDTA"]

print(discDict)
#----------------------------------------
#Create jdl files
#----------------------------------------
os.system("mkdir -p /eos/uscms/%s"%condorOutDir)
subFile = open('%s/condorSubmit.sh'%tmpDir,'w')
for year, decay, channel in itertools.product(Year, Decay, Channel):
    jdlName = 'submitJobs_%s%s%s.jdl'%(year, decay, channel)
    jdlFile = open('tmpSub/%s'%jdlName,'w')
    jdlFile.write('Executable =  runPerformFit.sh \n')
    jdlFile.write(common_command)
    for mass, r, h in itertools.product(Mass, regionList, discDict.keys()):
        for method in discDict[h]:
            run_command =  'arguments  = %s %s %s %s %s %s %s %s \nqueue 1\n' %(year, decay, channel, mass, method, r, h, condorOutDir)
            jdlFile.write(run_command)
    subFile.write("condor_submit %s\n"%jdlName)
    jdlFile.close() 
subFile.close()
