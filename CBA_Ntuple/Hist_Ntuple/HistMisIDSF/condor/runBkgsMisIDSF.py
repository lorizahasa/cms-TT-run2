import os
import sys
sys.path.insert(0, os.getcwd().replace("condor",""))
import itertools
from optparse import OptionParser
from HistInputs import *

#----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--forMisIDSF","--forMisIDSF", dest="forMisIDSF",action="store_true",
        default=False, help="")
parser.add_option("--afterMisIDSF","--afterMisIDSF", dest="afterMisIDSF",action="store_true",
        default=False, help="")
(options, args) = parser.parse_args()

forMisIDSF = options.forMisIDSF
afterMisIDSF = options.afterMisIDSF

def runCmd(cmd):
    print "\n\033[01;32m Excecuting: %s \033[00m"%cmd
    os.system(cmd)

if forMisIDSF:
    for year, decay, channel, cr in itertools.product(Years, Decays, Channels, Regions.keys()): 
        args = "-y %s -d %s -c %s --cr %s"%(year, decay, channel, cr)
        runCmd("python bkgsForMisIDSF.py  %s "%args)

if afterMisIDSF:
    for year, decay, channel, cr in itertools.product(Years, Decays, Channels, Regions.keys()): 
        args = "-y %s -d %s -c %s --cr %s"%(year, decay, channel, cr)
        runCmd("python bkgsAfterMisIDSF.py  %s "%args)

