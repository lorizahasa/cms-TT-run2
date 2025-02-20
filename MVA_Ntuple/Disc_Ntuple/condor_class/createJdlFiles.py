import os
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("condor_class", ""))
import itertools
from DiscInputs import *

tmpDir = "tmpSub"
condorLogDir = "log"
os.system("mkdir -p %s/%s"%(tmpDir, condorLogDir))
tarFile = "%s/Disc_Ntuple.tar.gz"%tmpDir
exDir = '../../Disc_Ntuple'
ex = '--exclude=%s/discs --exclude=%s/condor_read --exclude=%s/condor_class'%(exDir, exDir, exDir)
os.system("tar %s -zcvf %s ../../Disc_Ntuple "%(ex, tarFile))
os.system("cp runClassification.sh %s"%tmpDir)
common_command = \
'Universe   = vanilla\n\
should_transfer_files = YES\n\
when_to_transfer_output = ON_EXIT\n\
Transfer_Input_Files = Disc_Ntuple.tar.gz, runClassification.sh\n\
use_x509userproxy = true\n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\
Log    = %s/log_$(cluster)_$(process).condor\n\n'%(condorLogDir, condorLogDir, condorLogDir)

#----------------------------------------
#Create jdl files
#----------------------------------------
os.system("mkdir -p /eos/uscms/%s"%dirClass)
subFile = open('%s/condorSubmit.sh'%tmpDir,'w')
for year, decay, spin, channel, in itertools.product(Years, Decays, Spin, Channels):
    jdlName = 'submitJobs_%s%s%s%s.jdl'%(year, decay,spin, channel)
    jdlFile = open('%s/%s'%(tmpDir, jdlName),'w')
    jdlFile.write('Executable =  runClassification.sh \n')
    jdlFile.write(common_command)
    #Create for Base, Control region
    for method, r in itertools.product(methodDict.keys(), Regions.keys()):
        run_command =  \
		'arguments  = %s %s %s %s %s %s %s\n\
queue 1\n\n' %(year, decay, spin, channel, method, r, dirClass)
        print(run_command)
        if "SR" in r:
            jdlFile.write(run_command)
    #Create for Syst, Control region
    for method, r, syst, level in itertools.product(methodDict.keys(), Regions.keys(), Systematics, SystLevels):
        run_command =  \
		'arguments  = %s %s %s %s %s %s %s %s %s\n\
queue 1\n\n' %(year, decay, spin,  channel, method, r, syst, level, dirClass)
        #jdlFile.write(run_command)
	#print("condor_submit jdl/%s"%jdlFile)
    subFile.write("condor_submit %s\n"%jdlName)
    jdlFile.close() 
subFile.close()
