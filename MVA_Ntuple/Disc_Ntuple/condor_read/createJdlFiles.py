import os
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("condor_read", ""))
import itertools
from DiscInputs import *

tmpDir = "tmpSub"
condorLogDir = "log"
os.system("mkdir -p %s/%s"%(tmpDir, condorLogDir))
tarFile = "%s/Disc_Ntuple.tar.gz"%tmpDir
exDir = '../../Disc_Ntuple'
ex = '--exclude=%s/discs --exclude=%s/condor_read --exclude=%s/condor_class --exclude=%s/output'%(exDir, exDir, exDir, exDir)
os.system("tar %s -zcvf %s ../../Disc_Ntuple "%(ex, tarFile))
os.system("cp runReader*.sh %s"%tmpDir)
common_command = \
'Universe   = vanilla\n\
should_transfer_files = YES\n\
when_to_transfer_output = ON_EXIT\n\
Transfer_Input_Files = Disc_Ntuple.tar.gz, runReader.sh\n\
x509userproxy = /uscms/home/lhasa/x509up_u54210\n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\n'%(condorLogDir, condorLogDir)


#----------------------------------------
#Create jdl files
#----------------------------------------
subFile = open('%s/condorSubmit.sh'%tmpDir,'w')

for year, decay, spin, channel in itertools.product(Years, Decays, Spin, Channels):
    outDir  = "%s/"
    dirRead_ = "%s/Reader/%s/%s/%s/%s"%(dirRead, year, decay, spin, channel)
    #print("Deleting %s"%dirRead_)
    #os.system("eos root://cmseos.fnal.gov rm -r %s"%dirRead_)
    #os.system("eos root://eoscms.cern.ch/ rm -r %s"%dirRead_)
    os.system("eos root://cmseos.fnal.gov mkdir -p %s"%dirRead_)
    #os.system("eos root://eoscms.cern.ch/ mkdir -p %s"%dirRead_)
    print("Created  %s"%dirRead_)
    jdlName = 'submitJobs_%s%s%s%s.jdl'%(year, decay, spin, channel)
    jdlFile = open('%s/%s'%(tmpDir, jdlName),'w')
    jdlFile.write('Executable =  runReader.sh \n')
    jdlFile.write(common_command)
    #Create for Base
    for method, r, samp in itertools.product(methodDict.keys(), Regions.keys(), SampDict.keys()):
        args =  'Arguments  = %s %s %s %s %s %s %s JetBase %s\n' %(year, decay, spin, channel, samp, method, r, dirRead)
        args += 'Queue 1\n\n'
        jdlFile.write(args)
        for sv in systVar_by_year[year]: 
            if "data_obs" in SampDict[samp]:
                continue
            args =  'Arguments  = %s %s %s %s %s %s %s %s %s\n' %(year, decay, spin ,channel, samp, method, r, sv, dirRead)
            args += 'Queue 1\n\n'
            jdlFile.write(args)
            subFile.write("condor_submit %s\n"%jdlName)
    jdlFile.close() 
subFile.close()
