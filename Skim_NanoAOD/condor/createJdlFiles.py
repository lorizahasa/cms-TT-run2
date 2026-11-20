import os
import sys
import itertools
from pathlib import Path
import tarfile
sys.dont_write_bytecode = True

#IMPORT MODULES FROM OTHER DIR
sys.path.insert(0, os.getcwd().replace("condor",""))
sys.path.insert(0, os.getcwd().replace("condor","sample"))
from SkimInputs import *
from JobsNano_cff import Samples_2016Pre, Samples_2016Post,  Samples_2017, Samples_2018 

if os.path.exists("tmpSub"):
    os.system("rm -r tmpSub")
    print("Deleted dir: tmpSub")
os.system("mkdir -p tmpSub/log")
print("Created dir: tmpSub")
condorLogDir = "log"
tarFile = "tmpSub/Skim_NanoAOD.tar.gz"
# Package only production inputs, never local ROOT outputs or archived studies.
skim_dir = Path(__file__).resolve().parents[1]
with tarfile.open(tarFile, "w:gz") as archive:
    def production_member(member):
        if "__pycache__" in Path(member.name).parts or member.name.endswith(".pyc"):
            return None
        return member
    for name in ("makeSkim", "makeSkim.C", "Makefile", "SkimInputs.py",
                 "interface/SkimBranchConfig.h", "sample"):
        archive.add(str(skim_dir / name), arcname="Skim_NanoAOD/" + name,
                    filter=production_member)
os.system("cp runMakeSkims.sh tmpSub/")
common_command = \
'Universe   = vanilla\n\
should_transfer_files = YES\n\
when_to_transfer_output = ON_EXIT\n\
Transfer_Input_Files = Skim_NanoAOD.tar.gz, runMakeSkims.sh\n\
x509userproxy        = /uscms/home/lhasa/x509up_u54210\n\
request_memory= 9216 \n\
request_cpus= 4 \n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\n'%(condorLogDir, condorLogDir)
#use_x509userproxy = true\n\

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
    if os.path.exists("/eos/uscms/%s"%outDir):
        print("Deleted out dir: %s"%outDir)
        #os.system("eos root://cmseos.fnal.gov rm -r %s"%outDir) 
    os.system("eos root://cmseos.fnal.gov mkdir -p %s"%outDir) 
    print("Created out dir: %s"%outDir)
    jdlFile.write("X=$(step)+1\n")
    
    for sampleName, nJobEvt in samples.items():
        nJob = nJobEvt[0]
        args =  'Arguments  = %s %s $INT(X) %i %s\n' %(year, sampleName, nJob, outDir)
        args += "Queue %i\n\n"%nJob
        jdlFile.write(args)
    
    subFile.write("condor_submit %s\n"%jdlName)
	#print "condor_submit jdl/%s"%jdlFile
    jdlFile.close() 
subFile.close()
