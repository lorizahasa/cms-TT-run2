import os
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("condor", ""))
import itertools
from HistInputs import *

if os.path.exists("tmpSub"):
    os.system("rm -r tmpSub")
    print("Deleted dir: tmpSub")
os.system("mkdir -p tmpSub/log")
print("Created dir: tmpSub")
logDir = "log"
tarFile = "tmpSub/Hist_Ntuple.tar.gz"
if os.path.exists("../hists"):
    os.system("rm -r ../hists")
tarDir ='../../../Hist_Ntuple'
exDir = '--exclude=%s/HistDYSF --exclude=%s/HistMisIDSF --exclude=%s/HistMain --exclude=%s/HistWeight/condor'%(tarDir, tarDir, tarDir, tarDir)
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
for year, decay, channel in itertools.product(Years, Decays, Channels):
    outDir = "%s/Raw/%s/%s/%s"%(outHistDir, year, decay, channel)
    if os.path.exists("/eos/uscms/%s"%outDir):
        print("Deleted out dir: %s"%outDir)
        os.system("eos root://cmseos.fnal.gov rm -r %s"%outDir) 
    os.system("eos root://cmseos.fnal.gov mkdir -p %s"%outDir) 
    print("Created out dir: %s"%outDir)
    jdlName = 'submitJobs_%s%s%s.jdl'%(year, decay, channel)
    jdlFile = open('tmpSub/%s'%jdlName,'w')
    jdlFile.write('Executable =  runMakeHists.sh \n')
    jdlFile.write(common_command)
    for corr in Corrs.keys():
        for c in Corrs[corr]:
            if "Ele" in channel and "mu" in c: continue
            if "Mu" in channel and "ele" in c: continue
            if "Uncorr" in c and "Uncorr" not in corr: continue
            run_command =  \
		    'Arguments  = %s %s %s %s %s \n\
Queue 1\n\n' %(year, decay, channel, c, outDir)
            jdlFile.write(run_command)
	#print "condor_submit jdl/%s"%jdlFile
    subFile.write("condor_submit %s\n"%jdlName)
    jdlFile.close() 
subFile.close()
