import os
import sys
sys.path.insert(0, os.getcwd().replace("category",""))
import itertools
from optparse import OptionParser
from HistInputs import *

#----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--forDYSF","--forDYSF", dest="forDYSF",action="store_true",
        default=False, help="")
parser.add_option("--afterDYSF","--afterDYSF", dest="afterDYSF",action="store_true",
        default=False, help="")
parser.add_option("--forMisIDSF","--forMisIDSF", dest="forMisIDSF",action="store_true",
        default=False, help="")
parser.add_option("--afterMisIDSF","--afterMisIDSF", dest="afterMisIDSF",action="store_true",
        default=False, help="")
(options, args) = parser.parse_args()

forDYSF = options.forDYSF
afterDYSF = options.afterDYSF
forMisIDSF = options.forMisIDSF
afterMisIDSF = options.afterMisIDSF

def runCmd(cmd):
    print "\n\033[01;32m Excecuting: %s \033[00m"%cmd
    os.system(cmd)

if forDYSF:
    for year, decay, channel, cr in itertools.product(Years, Decays, Channels, Regions.keys()): 
        args = "-y %s -d %s -c %s --cr %s"%(year, decay, channel, cr)
        runCmd("python catHist_forDYSF.py  %s "%args)

