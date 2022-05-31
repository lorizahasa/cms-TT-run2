import os
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("condor", ""))
sys.path.insert(0, os.getcwd().replace("Fit_Hist/FitDYSF/condor", "Hist_Ntuple/HistDYSF"))

import itertools
from HistInputs import Regions
from FitInputs import *

tmpDir = "tmpSub"
condorLogDir = "log"
os.system("mkdir -p %s/%s"%(tmpDir, condorLogDir))
tarFile = "tmpSub/FitDYSF.tar.gz"
tarDir  = "../../FitDYSF"
ex = ' --exclude=%s/output --exclude=%s/condor'%(tarDir, tarDir)
os.system("tar %s -zcvf %s %s"%(ex, tarFile, tarDir))
os.system("cp runPerformFit.sh %s"%tmpDir)
os.system("cp /uscms_data/d3/rverma/codes/limitTools/CMSSW_10_2_13.tar.gz %s"%tmpDir)
common_command = \
'Universe   = vanilla\n\
should_transfer_files = YES\n\
when_to_transfer_output = ON_EXIT\n\
Transfer_Input_Files = CMSSW_10_2_13.tar.gz, FitDYSF.tar.gz, runPerformFit.sh\n\
use_x509userproxy = true\n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\
Log    = %s/log_$(cluster)_$(process).condor\n\n'%(condorLogDir, condorLogDir, condorLogDir)

os.system("eos root://cmseos.fnal.gov mkdir -p %s"%dirCBA)
#----------------------------------------
#Create jdl files
#----------------------------------------
jdlName = 'submitJobs.jdl'
jdlFile = open('tmpSub/%s'%jdlName,'w')
jdlFile.write('Executable =  runPerformFit.sh \n')
jdlFile.write(common_command)
for y, d, c, r in itertools.product(Year, Decay, Channel, Regions.keys()):
    run_command =  'arguments  = %s %s %s %s %s \nqueue 1\n' %(y, d, c, r, dirCBA)
    jdlFile.write(run_command)
jdlFile.close() 
