import os
import itertools
import json
from FitInputs import *
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--hist", "--hist", dest="hName", default="Reco_mass_T",type='str', 
                     help="which histogram to be used for making datacard")
(options, args) = parser.parse_args()
hName        = options.hName

def runCmd(cmd):
    print "\n\033[01;32m Excecuting: %s \033[00m"%cmd
    os.system(cmd)

for year, decay, channel, mass, ps in itertools.product(Year, Decay, Channel, Mass, PhaseSpace): 
    args = "-y %s -d %s -c %s -m %s --ps %s --hist %s"%(year, decay, channel, mass, ps, hName)
    runCmd("python makeDataCard.py  %s "%args)
    print args
