import os
import sys
sys.path.insert(0, os.getcwd().replace("condor", ""))
import itertools
from FitInputs import *

if os.path.exists("tmpSub"):
	os.system("rm -r tmpSub")
else:
    os.makedirs("tmpSub/log")
condorLogDir = "log"
tarFile = "tmpSub/FitMain.tar.gz"
if os.path.exists("../output"):
    os.system("rm -r ../output")
os.system("tar -zcvf %s ../../FitMain --exclude condor"%tarFile)
os.system("cp runPerformFit.sh tmpSub/")
os.system("cp /uscms_data/d3/rverma/codes/CMSSW_10_2_13.tar.gz tmpSub/")
common_command = \
'Universe   = vanilla\n\
should_transfer_files = YES\n\
when_to_transfer_output = ON_EXIT\n\
Transfer_Input_Files = CMSSW_10_2_13.tar.gz, FitMain.tar.gz, runPerformFit.sh\n\
use_x509userproxy = true\n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\
Log    = %s/log_$(cluster)_$(process).condor\n\n'%(condorLogDir, condorLogDir, condorLogDir)

#----------------------------------------
#Create jdl files
#----------------------------------------
subFile = open('tmpSub/condorSubmit.sh','w')
for year, decay, channel in itertools.product(Year, Decay, Channel):
    condorOutDir = "%s/%s/%s/%s"%(condorHistDir, year, decay, channel)
    os.system("eos root://cmseos.fnal.gov mkdir -p %s"%condorOutDir)
    jdlName = 'submitJobs_%s%s%s.jdl'%(year, decay, channel)
    jdlFile = open('tmpSub/%s'%jdlName,'w')
    jdlFile.write('Executable =  runPerformFit.sh \n')
    jdlFile.write(common_command)
    for mass, h, r, comb in itertools.product(Mass, histList, regionList, combList):
        run_command =  'arguments  = %s %s %s %s %s %s --%s \nqueue 1\n' %(year, decay, channel, mass, h, r, comb)
        if comb == "isCombYear" and (year=="2017" or year=="2018"): continue
        if comb == "isCombCh" and channel=="Ele": continue
        if comb == "isCombChYear" and (year=="2017" or year=="2018" or channel =="Ele"): continue
        jdlFile.write(run_command)
    subFile.write("condor_submit %s\n"%jdlName)
    jdlFile.close() 
subFile.close()
