import os
import sys
import itertools
sys.dont_write_bytecode = True

#IMPORT MODULES FROM OTHER DIR
sys.path.insert(0, os.getcwd().replace("condor",""))
sys.path.insert(0, os.getcwd().replace("Ntuple_Skim/condor","Skim_NanoAOD/sample"))
from NtupleInputs import *
from JobsNano_cff import Samples_2016Pre, Samples_2016Post,  Samples_2017, Samples_2018 

if os.path.exists("tmpSub"):
    os.system("rm -r tmpSub")
    print("Deleted dir: tmpSub")
os.system("mkdir -p tmpSub/log")
print("Created dir: tmpSub")
condorLogDir = "log"
tmpDir = "tmpSub"
tarFile = "%s/Ntuple_Skim.tar.gz"%tmpDir
if os.path.exists(tarFile):
	os.system("rm %s"%tarFile)
os.system("tar -zcvf %s ../../Ntuple_Skim --exclude condor"%tarFile)
os.system("cp runMakeNtuple.sh %s/"%tmpDir)
common_command = \
'Universe   = vanilla\n\
should_transfer_files = YES\n\
when_to_transfer_output = ON_EXIT\n\
Transfer_Input_Files = Ntuple_Skim.tar.gz, runMakeNtuple.sh\n\
use_x509userproxy = true\n\
request_memory= 9216 \n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\n'%(condorLogDir, condorLogDir)
#----------------------------------------
#Create jdl files
#----------------------------------------
subFile = open('%s/condorSubmit.sh'%tmpDir,'w')
nJobAll = 0
for year in Years:
    nJobYear = 0
    sampleList = eval("Samples_%s"%year)
    jdlName = 'submitJobs_%s.jdl'%(year)
    jdlFile = open('%s/%s'%(tmpDir, jdlName),'w')
    jdlFile.write('Executable =  runMakeNtuple.sh \n')
    jdlFile.write(common_command)
    for decay in Decays:
        for syst in get_syst_List(year, decay):
            outDir = "%s/%s/%s/%s"%(outNtupleDir, year, decay, syst)
            outDirPath = "/eos/cms/%s" % outDir
            check_cmd = "eos root://eoscms.cern.ch ls %s > /dev/null 2>&1" % outDirPath

            # Check if directory exists on EOS
            if os.system(check_cmd) == 0:  # if the ls command succeeds
                print("Deleted out dir: %s" % outDirPath)
                os.system("eos root://eoscms.cern.ch rm -r %s" % outDirPath)

            #if os.path.exists("/eos/cms/%s"%outDir):
            #    print("Deleted out dir: %s"%outDir)
            #    os.system("eos root://eoscms.cern.ch rm -r %s"%outDir) 
            #os.system("eos root://cmseos.fnal.gov mkdir -p %s"%outDir) 
            os.system("eos root://eoscms.cern.ch mkdir -p %s"%outDir)
            print("Created out dir: %s"%outDir)
            jdlFile.write("X=$(step)+1\n")
            for sampleName, fEvt in sampleList.items():
                if "Data" in sampleName and "_" in syst: continue
               # if "Data" in sampleName: continue
                if "Dilep" in decay and "Signal" in sampleName and "700" not in sampleName: continue
               # if not "Total" in syst: continue
               # if "Spin32" in sampleName: continue
               # if "Spin12" in sampleName and "M800" not in sampleName: continue
                nJob = reducedJob(fEvt[0], sampleName)
                args =  'Arguments  = %s %s %s %s $INT(X) %i %s\n' %(year, decay, syst, sampleName, nJob, outDir)
                args += "Queue %i\n\n"%nJob
                nJobYear += nJob
                nJobAll  += nJob
                jdlFile.write(args)
    #print "condor_submit jdl/%s"%jdlFile
    subFile.write("condor_submit %s\n"%jdlName)
    jdlFile.close() 
    print("All jobs for %s = %s"%(year, nJobYear))
subFile.close()
print("All jobs for all years = %s"%(nJobAll))
print("OutputDir: /eos/uscms/%s"%outNtupleDir)
