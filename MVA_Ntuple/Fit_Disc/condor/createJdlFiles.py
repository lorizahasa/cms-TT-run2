import os
import sys
sys.path.insert(0, os.getcwd().replace("condor", ""))
sys.path.insert(0, os.getcwd().replace("Fit_Disc/condor", "Disc_Ntuple"))
from DiscInputs import methodDict
import itertools
from FitInputs import *

tmpDir = "tmpSub"
condorLogDir = "log"
os.system("mkdir -p %s/%s"%(tmpDir, condorLogDir))
tarFile = "tmpSub/Fit_Disc.tar.gz"
exDir = '../../Fit_Disc'
ex = '--exclude=%s/*output* --exclude=%s/condor'%(exDir, exDir)
os.system("tar %s -zcvf %s ../../Fit_Disc"%(ex, tarFile))
os.system("cp runPerformFit.sh %s"%tmpDir)
#os.system("cp /uscms_data/d3/rverma/codes/limitTools/CMSSW_14_1_0_pre4.tar.gz %s"%tmpDir)
os.system("cp /uscms_data/d3/lhasa/TTPrime/CombineTools/CMSSW_14_1_0_pre4.tar.gz %s"%tmpDir)
common_command = \
'Universe   = vanilla\n\
should_transfer_files = YES\n\
when_to_transfer_output = ON_EXIT\n\
Transfer_Input_Files = CMSSW_14_1_0_pre4.tar.gz, Fit_Disc.tar.gz, runPerformFit.sh\n\
use_x509userproxy = true\n\
request_memory= 4096 \n\
Output = %s/log_$(cluster)_$(process).stdout\n\
Error  = %s/log_$(cluster)_$(process).stderr\n\
Log    = %s/log_$(cluster)_$(process).condor\n\n'%(condorLogDir, condorLogDir, condorLogDir)

discDict = {}
discDict["Disc"] = methodDict.keys()
discDict["Reco_mass_T"] = methodDict.keys()
#for hist in histList:
#    discDict[hist] = ["BDTA"]

print(discDict)
#----------------------------------------
#Create jdl files
#----------------------------------------
os.system("mkdir -p /eos/uscms/%s"%condorOutDir)
subFile = open('%s/condorSubmit.sh'%tmpDir,'w')
for year, decay, spin, channel in itertools.product(Year, Decay, Spin, Channel):
    jdlName = 'submitJobs_%s%s%s%s.jdl'%(year, decay, spin, channel)
    jdlFile = open('tmpSub/%s'%jdlName,'w')
    jdlFile.write('Executable =  runPerformFit.sh \n')
    jdlFile.write(common_command)
    for mass, r, h in itertools.product(xss.keys(), list(rDict.keys()), discDict.keys()):
        for method in discDict[h]:
            run_command =  'arguments  = %s %s %s %s %s %s %s %s %s \nqueue 1\n' %(year, decay, spin, channel, int(float(mass)), method, r, h, condorOutDir)
            jdlFile.write(run_command)
    subFile.write("condor_submit %s\n"%jdlName)
    jdlFile.close() 
subFile.close()
