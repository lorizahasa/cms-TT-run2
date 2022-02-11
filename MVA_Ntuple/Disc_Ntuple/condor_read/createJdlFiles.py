import os
import sys
sys.path.insert(0, os.getcwd().replace("condor_read", ""))
import itertools
from DiscInputs import *

tmpDir = "tmpSub"
condorLogDir = "log"
os.system("mkdir -p %s/%s"%(tmpDir, condorLogDir))
tarFile = "%s/Disc_Ntuple.tar.gz"%tmpDir
exDir = '../../Disc_Ntuple'
ex = '--exclude=%s/discs --exclude=%s/condor_read --exclude=%s/condor_class'%(exDir, exDir, exDir)
os.system("tar %s -zcvf %s ../../Disc_Ntuple "%(ex, tarFile))
os.system("cp runReader.sh %s"%tmpDir)
common_command = \
'Universe   = vanilla\n\
should_transfer_files = YES\n\
when_to_transfer_output = ON_EXIT\n\
Transfer_Input_Files = Disc_Ntuple.tar.gz, runReader.sh\n\
use_x509userproxy = true\n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\
Log    = %s/log_$(cluster)_$(process).condor\n\n'%(condorLogDir, condorLogDir, condorLogDir)

#----------------------------------------
#Create jdl files
#----------------------------------------
os.system("mkdir -p /eos/uscms/%s"%condorOutDir)
subFile = open('%s/condorSubmit.sh'%tmpDir,'w')

sepSyst = ["TTbar", "TTGamma", "WJets", "Others", "Data"]
allSyst = list(set(Samples) - set(sepSyst))
for year, decay, channel in itertools.product(Years, Decays, Channels):
    jdlName = 'submitJobs_%s%s%s.jdl'%(year, decay, channel)
    jdlFile = open('%s/%s'%(tmpDir, jdlName),'w')
    jdlFile.write('Executable =  runReader.sh \n')
    jdlFile.write(common_command)
    #Create for Base
    for sample, method, r in itertools.product(Samples, methodDict.keys(), Regions.keys()):
        run_command =  \
		'arguments  = %s %s %s %s %s %s %s\n\
queue 1\n\n' %(year, decay, channel, sample, method, r, condorOutDir)
        jdlFile.write(run_command)
    
    #Create for allSyst
    for sample, method, r in itertools.product(allSyst, methodDict.keys(), Regions.keys()):
        run_command =  \
		'arguments  = %s %s %s %s %s %s --allSyst  %s\n\
queue 1\n\n' %(year, decay, channel, sample, method, r, condorOutDir)
        jdlFile.write(run_command)

    #Create for sepSyst
    for sample, method, r, syst, level in itertools.product(sepSyst, methodDict.keys(), Regions.keys(), Systematics, SystLevels):
        run_command =  \
		'arguments  = %s %s %s %s %s %s %s %s %s\n\
queue 1\n\n' %(year, decay, channel, sample, method, r, syst, level, condorOutDir)
        if not sample in ["Data"]:
            jdlFile.write(run_command)
    subFile.write("condor_submit %s\n"%jdlName)
    jdlFile.close() 
subFile.close()
