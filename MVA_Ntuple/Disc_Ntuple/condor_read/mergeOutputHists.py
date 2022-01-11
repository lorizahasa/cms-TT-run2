
#//////////////////////////////////////////////////
#                                                 #
# Merge histo files into a single root file       #
#                                                 #
#//////////////////////////////////////////////////
#https://uscms.org/uscms_at_work/computing/LPC/usingEOSAtLPC.shtml#listFilesOnEOS
import os
import sys
sys.path.insert(0, os.getcwd().replace("condor_read", ""))
from optparse import OptionParser
from DiscInputs import *

#-----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016",type='str',
                     help="Specifyi the year of the data taking" )
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
                     help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-d", "--decay", dest="decayMode", default="Semilep",type='str',
                     help="Specify which decay moded of ttbar Semilep or Dilep? default is Semilep")
parser.add_option("--method", "--method", dest="method", default="BDTG",type='str', 
                     help="Which MVA method to be used")
(options, args) = parser.parse_args()
year = options.year
channel = options.channel
decay   = options.decayMode
method = options.method

#-----------------------------------------
#Merge histograms using hadd
#----------------------------------------
def runCmd(cmd):
    print "\n\033[01;32m Excecuting: %s \033[00m"%cmd
    os.system(cmd)

#-----------------------------------------
#Path of the I/O histrograms
#----------------------------------------
inDir = "%s/Reader/%s/%s/%s/CombMass/%s"%(condorOutDir, year, decay, channel, method)
outDir = "%s/Merged"%inDir
runCmd("eos root://cmseos.fnal.gov rm -r %s"%outDir)
runCmd("eos root://cmseos.fnal.gov mkdir -p %s"%outDir)

for sample in Samples:
    haddOut = "root://cmseos.fnal.gov/%s/%s.root"%(outDir, sample)
    haddIn  = "`xrdfs root://cmseos.fnal.gov ls -u %s | grep \'%s_.*root\'`"%( inDir, sample)
    print haddIn
    runCmd("hadd -f %s %s"%(haddOut, haddIn))

#Merge all histograms
haddOut = "root://cmseos.fnal.gov/%s/AllInc.root"%(outDir)
haddIn  = "`xrdfs root://cmseos.fnal.gov ls -u %s | grep \'.*root\'`"%(outDir)
runCmd("hadd -f %s %s"%(haddOut, haddIn))
print "-------------------------------------"
print "OUTPUT DIR: ", outDir
print "-------------------------------------"
print runCmd(("eos root://cmseos.fnal.gov find --size %s")%outDir)


