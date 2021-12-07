import os
import sys
sys.path.insert(0, os.getcwd().replace("condor", ""))
import itertools
from DiscInputs import *

if os.path.exists("tmpSub"):
	os.system("rm -r tmpSub")
else:
    os.makedirs("tmpSub/log")
condorLogDir = "log"
tarFile = "tmpSub/Disc_Ntuple.tar.gz"
if os.path.exists("../dataset"):
    os.system("rm -r ../dataset")
os.system("tar -zcvf %s ../../Disc_Ntuple --exclude condor"%tarFile)
os.system("cp runClassReader.sh tmpSub/")
common_command = \
'Universe   = vanilla\n\
should_transfer_files = YES\n\
when_to_transfer_output = ON_EXIT\n\
Transfer_Input_Files = Disc_Ntuple.tar.gz, runClassReader.sh\n\
use_x509userproxy = true\n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\
Log    = %s/log_$(cluster)_$(process).condor\n\n'%(condorLogDir, condorLogDir, condorLogDir)

#----------------------------------------
#Create jdl files
#----------------------------------------
subFile = open('tmpSub/condorSubmit.sh','w')
for year, decay, channel in itertools.product(Years, Decays, Channels):
    jdlName = 'submitJobs_%s%s%s.jdl'%(year, decay, channel)
    jdlFile = open('tmpSub/%s'%jdlName,'w')
    jdlFile.write('Executable =  runClassReader.sh \n')
    jdlFile.write(common_command)
    #Create for Base, Control region
    for mass, method in itertools.product(Mass, methodList.keys()):
        run_command =  \
		'arguments  = %s %s %s %s %s \n\
queue 1\n\n' %(year, decay, channel, mass, method)
        jdlFile.write(run_command)
        condorOutDir = "%s/%s/%s/%s/%s/%s"%(condorHistDir, year, decay, channel, mass, method)
        os.system("eos root://cmseos.fnal.gov mkdir -p %s"%condorOutDir)
    
    #Create for Syst, Control region
    for mass, method, syst, level in itertools.product(Mass, methodList.keys(), Systematics, SystLevels):
        run_command =  \
		'arguments  = %s %s %s %s %s %s %s \n\
queue 1\n\n' %(year, decay, channel, mass, method, syst, level)
        jdlFile.write(run_command)
	#print "condor_submit jdl/%s"%jdlFile
    subFile.write("condor_submit %s\n"%jdlName)
    jdlFile.close() 
subFile.close()
