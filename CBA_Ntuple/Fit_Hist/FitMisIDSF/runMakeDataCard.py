import os
import itertools
import json
import sys
sys.path.insert(0, os.getcwd().replace("Fit_Hist/FitMisIDSF", "Hist_Ntuple/HistMisIDSF"))
from FitInputs import *
from HistInputs import Regions
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--hist", "--hist", dest="hName", default="Reco_mass_lgamma",type='str', 
                     help="which histogram to be used for making datacard")
(options, args) = parser.parse_args()
hName        = options.hName

def runCmd(cmd):
    print "\n\033[01;32m Excecuting: %s \033[00m"%cmd
    os.system(cmd)

for year, decay, channel, r in itertools.product(Year, Decay, Channel, Regions): 
    args = "-y %s -d %s -c %s -r %s --hist %s"%(year, decay, channel, r, hName)
    runCmd("python makeDataCard.py  %s "%args)
    print args
