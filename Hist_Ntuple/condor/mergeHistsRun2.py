
#//////////////////////////////////////////////////
#                                                 #
# Merge histo files into a single root file       #
#                                                 #
#//////////////////////////////////////////////////
#https://uscms.org/uscms_at_work/computing/LPC/usingEOSAtLPC.shtml#listFilesOnEOS
import os
import sys
sys.path.insert(0, os.getcwd().replace("condor", ""))
from optparse import OptionParser
from HistInputs import *

#-----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
                     help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-d", "--decay", dest="ttbarDecayMode", default="Semilep",type='str',
                     help="Specify which decay moded of ttbar Semilep or Dilep? default is Semilep")
(options, args) = parser.parse_args()
channel = options.channel
decay   = options.ttbarDecayMode

#-----------------------------------------
#Merge histograms using hadd
#----------------------------------------
def runCmd(cmd):
    print "\n\033[01;32m Excecuting: %s \033[00m"%cmd
    os.system(cmd)

hists = []
for y in Years:
    iSubDir = "%s/%s/%s/Merged/AllInc.root"%(y, decay, channel)
    iFullDir = "root://cmseosmgm01.fnal.gov:1094/%s/%s"%(condorHistDir, iSubDir)
    hists.append(iFullDir)

combHists = ' '.join(str(h) for h in hists)
oHistSubDir = "Run2/%s/%s"%(decay, channel)
oHistFullDir = "%s/%s/Merged"%(condorHistDir, oHistSubDir)
haddIn  = combHists 
haddOut = "root://cmseos.fnal.gov/%s/AllInc.root"%(oHistFullDir)
runCmd("eos root://cmseos.fnal.gov rm -r %s"%oHistFullDir)
runCmd("eos root://cmseos.fnal.gov mkdir -p %s"%oHistFullDir)
runCmd("hadd -f %s %s"%(haddOut, haddIn))
print runCmd(("eos root://cmseos.fnal.gov find --size %s")%oHistFullDir)


