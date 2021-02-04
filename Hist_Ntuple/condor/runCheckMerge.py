import os
import itertools
from optparse import OptionParser
from HistInputs import *

#----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--isCheck","--isCheck", dest="checkStatus",action="store_true",default=False, help="Check the status of histograms produced by condor jobs" )
parser.add_option("--isMerge","--isMerge", dest="mergeHistos",action="store_true",default=False, help="merge histograms produced by condor jobs" )
(options, args) = parser.parse_args()
isCheck = options.checkStatus
isMerge = options.mergeHistos


def runCmd(cmd):
    print "\n\033[01;32m Excecuting: %s \033[00m"%cmd
    os.system(cmd)

if isCheck:
    for year, decay, channel in itertools.product(Year, Decay, Channel): 
        args = "-y %s -d %s -c %s"%(year, decay, channel)
        runCmd("python checkJobStatus.py  %s "%args)

if isMerge:
    for year, decay, channel in itertools.product(Year, Decay, Channel): 
        args = "-y %s -d %s -c %s"%(year, decay, channel)
        runCmd("python mergeOutputHists.py  %s "%args)

