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
parser.add_option("--forRebin","--forRebin", dest="forRebin",action="store_true",
        default=False, help="")
parser.add_option("--forMain","--forMain", dest="forMain",action="store_true",
        default=False, help="")
parser.add_option("--afterMain","--afterMain", dest="afterMain",action="store_true",
        default=False, help="")
(options, args) = parser.parse_args()

forRebin = options.forRebin
forMain = options.forMain
afterMain = options.afterMain

def runCmd(cmd):
    print "\n\033[01;32m Excecuting: %s \033[00m"%cmd
    os.system(cmd)

if forRebin:
    for year, decay, channel, cr in itertools.product(Years, Decays, Channels, Regions.keys()):
        args = "-y %s -d %s -c %s --cr %s"%(year, decay, channel, cr)
        runCmd("python bkgsRebin.py  %s "%args)

if forMain:
    for year, decay, channel, cr in itertools.product(Years, Decays, Channels, Regions.keys()):
        args = "-y %s -d %s -c %s --cr %s"%(year, decay, channel, cr)
        runCmd("python bkgsForMain.py  %s "%args)

if afterMain:
    for year, decay, channel, cr in itertools.product(Years, Decays, Channels, Regions.keys()):
        args = "-y %s -d %s -c %s --cr %s"%(year, decay, channel, cr)
        runCmd("python bkgsAfterMain.py  %s "%args)

