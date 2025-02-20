import os
import sys
import itertools
sys.dont_write_bytecode = True
from optparse import OptionParser
from HistInputs import Samples, Regions

#-----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016Pre",type='str',
                     help="Specifyi the year of the data taking" )
parser.add_option("-d", "--decay", dest="decay", default="Semilep",type='str',
                     help="Specify which decay moded of ttbar Semilep or Dilep? default is Semilep")
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
                     help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-s", "--sample", dest="sample", default="Signal_M800",type='str',
                     help="Specify which sample to run on" )
parser.add_option("--syst", "--systematic", dest="systematic", default="Uncorr",type='str',
                     help="Specify which systematic to run on")
(options, args) = parser.parse_args()
year = options.year
decay = options.decay
channel = options.channel
sample = options.sample
syst = options.systematic

for s, r in itertools.product(Samples, Regions.keys()):
    if "data_obs" in s and "Uncorr" not in syst:
        continue
    args = "python3 makeHists.py -y %s -d %s -c %s -s %s -r %s --syst %s --allHists"%(year, decay, channel, s, r, syst)
    print(args)
    os.system(args)
