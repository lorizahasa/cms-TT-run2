import os
import sys
sys.path.insert(0, os.getcwd().replace("condor_read",""))
import itertools
from optparse import OptionParser
from DiscInputs import *

#----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--isCheck","--isCheck", dest="checkStatus",action="store_true",default=False, help="Check the status of histograms produced by condor jobs" )
parser.add_option("--isMerge","--isMerge", dest="mergeHistos",action="store_true",default=False, help="merge histograms produced by condor jobs" )
parser.add_option("--isMain","--isMain", dest="rebinHistos",action="store_true",default=False, help="merge histograms produced by condor jobs" )
(options, args) = parser.parse_args()
isCheck = options.checkStatus
isMerge = options.mergeHistos
isMain = options.rebinHistos

def runCmd(cmd):
    print "\n\033[01;32m Excecuting: %s \033[00m"%cmd
    os.system(cmd)

if isCheck:
    for year, decay, channel in itertools.product(Years, Decays, Channels): 
        args = "-y %s -d %s -c %s"%(year, decay, channel)
        runCmd("python checkJobStatus.py  %s "%args)

if isMerge:
    for year, decay, channel, method in itertools.product(Years, Decays, Channels, methodDict.keys()): 
        args = "-y %s -d %s -c %s --method %s"%(year, decay, channel, method)
        runCmd("python mergeOutputHists.py  %s "%args)
    
    for decay, channel in itertools.product( Decays, Channels): 
        args = "-d %s -c %s"%(decay, channel)
        #runCmd("python mergeHistsRun2.py  %s "%args)
    
    for decay in Decays: 
        args = "-d %s -c Lep "%decay
        #runCmd("python mergeHistsRun2.py  %s "%args)
if isMain:
    for year, decay, channel, method in itertools.product(Years, Decays, Channels, methodDict.keys()): 
        args = "-y %s -d %s -c %s --method %s"%(year, decay, channel, method)
        runCmd("python discForMain.py  %s "%args)



