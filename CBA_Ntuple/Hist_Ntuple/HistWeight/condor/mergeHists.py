import os
import sys
import itertools
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("condor", ""))
from optparse import OptionParser
from HistInputs import *

#----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--isCheck","--isCheck", dest="isCheck",action="store_true",default=False, help="Merge for combined years and channels")
parser.add_option("--isSep","--isSep", dest="isSep",action="store_true",default=False, help="Merge for separate years and channels")
parser.add_option("--isComb","--isComb", dest="isComb",action="store_true",default=False, help="Merge for combined years and channels")
(options, args) = parser.parse_args()
isCheck = options.isCheck
isSep = options.isSep
isComb = options.isComb

if isCheck:
    Years  = [Years[0]]
    Decays = [Decays[0]]
    Channels = [Channels[0]]
    Samples  = [Samples[0]]
if isComb:
    Years  = Years_ 
    Channels = Channels_
if not isCheck and not isSep and not isComb:
    print("Add either --isCheck or --isSep or --isComb in the command line")
    exit()

def runCmd(cmd):
    print("\n\033[01;32m Excecuting: %s \033[00m"%cmd)
    os.system(cmd)

#-----------------------------------------
#Merge separate years and channels
#-----------------------------------------
if isSep:
    for y, d, c in itertools.product(Years, Decays, Channels):
        histDir  = "%s/Raw/%s/%s/%s"%(outHistDir, y, d, c)
        mergeDir = histDir.replace("Raw", "Merged")
        #if os.path.exists("/eos/uscms/%s"%mergeDir):
        runCmd("eos root://cmseos.fnal.gov rm -r %s"%mergeDir)
        runCmd("eos root://cmseos.fnal.gov mkdir -p %s"%mergeDir)
        #Merge for each sample
        for s in Samples:
            haddOut = "root://cmseos.fnal.gov/%s/%s.root"%(mergeDir, s)
            haddIn  = "`xrdfs root://cmseos.fnal.gov ls -u %s | grep \'/%s.*root\'`"%(histDir,s)
            runCmd("hadd -f -v 0  %s %s"%(haddOut, haddIn))
        #Merge for all sample
        haddOut = "root://cmseos.fnal.gov/%s/AllInc.root"%(mergeDir)
        haddIn  = "`xrdfs root://cmseos.fnal.gov ls -u %s | grep \'.*root\'`"%(mergeDir)
        runCmd("hadd -f -v 0  %s %s"%(haddOut, haddIn))
        print(runCmd(("eos root://cmseos.fnal.gov find --size %s")%mergeDir))

#-----------------------------------------
#Merge combining years and channels
#-----------------------------------------
if isComb:
    for year, d, ch in itertools.product(Years_, Decays, Channels_): 
        hists = []
        for y in year.split("__"):
            for c in ch.split("__"):
                iSubDir = "%s/Merged/%s/%s/%s/AllInc.root"%(outHistDir, y, d, c)
                iFullDir = "root://cmseosmgm01.fnal.gov:1094/%s"%iSubDir
                hists.append(iFullDir)
        haddIn = ' '.join(str(h) for h in hists)
        mergeDir = "%s/Merged/%s/%s/%s"%(outHistDir, year, d, ch)
        runCmd("eos root://cmseos.fnal.gov mkdir -p %s"%mergeDir)
        haddOut = "root://cmseos.fnal.gov/%s/AllInc.root"%(mergeDir)
        runCmd("eos root://cmseos.fnal.gov rm -r %s"%mergeDir)
        runCmd("eos root://cmseos.fnal.gov mkdir -p %s"%mergeDir)
        runCmd("hadd -f -v 0 %s %s"%(haddOut, haddIn))
        print(runCmd(("eos root://cmseos.fnal.gov find --size %s")%mergeDir))
