import os
import sys
sys.path.insert(0, os.getcwd().replace("condor", ""))
import itertools
from HistInputs import *

if os.path.exists("tmpSub"):
	os.system("rm -r tmpSub")
else:
    os.makedirs("tmpSub/log")
condorLogDir = "log"
tarFile = "tmpSub/HistSF.tar.gz"
if os.path.exists("../hists"):
    os.system("rm -r ../hists")
os.system("tar -zcvf %s ../../HistSF --exclude condor"%tarFile)
os.system("cp runMakeHists.sh tmpSub/")
common_command = \
'Universe   = vanilla\n\
should_transfer_files = YES\n\
when_to_transfer_output = ON_EXIT\n\
Transfer_Input_Files = HistSF.tar.gz, runMakeHists.sh\n\
use_x509userproxy = true\n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\
Log    = %s/log_$(cluster)_$(process).condor\n\n'%(condorLogDir, condorLogDir, condorLogDir)

#----------------------------------------
#Create jdl files
#----------------------------------------
subFile = open('tmpSub/condorSubmit.sh','w')
for year, decay, channel in itertools.product(Years, Decays, Channels):
    condorOutDir = "%s/%s/%s/%s"%(condorHistDir, year, decay, channel)
    os.system("eos root://cmseos.fnal.gov mkdir -p %s"%condorOutDir)
    jdlName = 'submitJobs_%s%s%s.jdl'%(year, decay, channel)
    jdlFile = open('tmpSub/%s'%jdlName,'w')
    jdlFile.write('Executable =  runMakeHists.sh \n')
    jdlFile.write(common_command)
    #Create for Base, Syst, Control region
    for sample, syst, level in itertools.product(Samples, Systematics, SystLevels):
        run_command =  \
		'arguments  = %s %s %s %s %s %s \n\
queue 1\n\n' %(year, decay, channel, sample, syst, level)
        if syst in ["Weight_lumi", "1"] and level in ["up", "down"]:
            continue
        jdlFile.write(run_command)
	#print "condor_submit jdl/%s"%jdlFile
    subFile.write("condor_submit %s\n"%jdlName)
    jdlFile.close() 
subFile.close()
