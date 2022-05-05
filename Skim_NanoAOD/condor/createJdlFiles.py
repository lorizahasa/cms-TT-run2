import os
import sys
import itertools
sys.dont_write_bytecode = True

#IMPORT MODULES FROM OTHER DIR
sys.path.insert(0, os.getcwd().replace("condor",""))
sys.path.insert(0, os.getcwd().replace("condor","sample"))
from SkimInputs import *
from JobsNano_cff import Samples_2016PreVFP, Samples_2016PostVFP,  Samples_2017, Samples_2018 

if not os.path.exists("tmpSub/log"):
    os.makedirs("tmpSub/log")
condorLogDir = "log"
tarFile = "tmpSub/Skim_NanoAOD.tar.gz"
if os.path.exists(tarFile):
	os.system("rm %s"%tarFile)
os.system("tar -zcvf %s ../../Skim_NanoAOD --exclude condor"%tarFile)
os.system("cp runMakeSkims.sh tmpSub/")
common_command = \
'Universe   = vanilla\n\
should_transfer_files = YES\n\
when_to_transfer_output = ON_EXIT\n\
Transfer_Input_Files = Skim_NanoAOD.tar.gz, runMakeSkims.sh\n\
use_x509userproxy = true\n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\
Log    = %s/log_$(cluster)_$(process).condor\n\n'%(condorLogDir, condorLogDir, condorLogDir)

#----------------------------------------
#Create jdl files
#----------------------------------------
subFile = open('tmpSub/condorSubmit.sh','w')
for year in Years: 
    samples = eval("Samples_%s"%year)
    jdlName = 'submitJobs_%s.jdl'%(year)
    jdlFile = open('tmpSub/%s'%jdlName,'w')
    jdlFile.write('Executable =  runMakeSkims.sh \n')
    jdlFile.write(common_command)
    outDir="%s/%s"%(outSkimDir, year)
    os.system("eos root://cmseos.fnal.gov mkdir -p %s"%outDir) 
    jdlFile.write("X=$(step)+1\n")
    
    for sampleName, nJobEvt in samples.items():
        nJob = nJobEvt[0]
        if nJob==1:
            run_command =  'Arguments  = %s %s %s \nQueue 1\n\n' %(year, sampleName, outDir)
        else:
            run_command =  'Arguments  = %s %s %s $INT(X) %i\nQueue %i\n\n' %(year, sampleName, outDir, nJob, nJob)
	jdlFile.write(run_command)
    
	#print "condor_submit jdl/%s"%jdlFile
    subFile.write("condor_submit %s\n"%jdlName)
    jdlFile.close() 
subFile.close()
