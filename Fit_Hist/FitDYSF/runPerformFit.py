import os
import sys
sys.path.insert(0, os.getcwd().replace("Fit_Hist/FitDYSF", "Hist_Ntuple/HistDYSF"))
import itertools
import json
from FitInputs import *
from HistInputs import Regions
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--hist", "--hist", dest="hName", default="Reco_mass_dilep",type='str', 
                     help="which histogram to be used for making datacard")
(options, args) = parser.parse_args()
hName        = options.hName

if not os.path.exists("./RateParams.json"):
    with open("RateParams.json", "w") as f:
        data = {}
        json.dump(data, f)

def runCmd(cmd):
    print "\n\033[01;32m Excecuting: %s \033[00m"%cmd
    os.system(cmd)

for year, decay, channel, r in itertools.product(Year, Decay, Channel, Regions): 
    args = "-y %s -d %s -c %s -r %s --hist %s "%(year, decay, channel, r, hName)
    print args
    #runCmd("python performFit.py %s --isT2W "%args)
    runCmd("python performFit.py %s --isT2W --isFD"%args)
