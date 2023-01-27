import os
import sys
sys.dont_write_bytecode = True
from optparse import OptionParser
from HistInputs import Samples 

#-----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016PreVFP",type='str',
                     help="Specifyi the year of the data taking" )
parser.add_option("-d", "--decay", dest="decay", default="Semilep",type='str',
                     help="Specify which decay moded of ttbar Semilep or Dilep? default is Semilep")
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
                     help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-r", "--region", dest="region", default="MisID_Enriched_a2j_e0b_e1y",type='str',
                     help="Specify which region to run on" )
parser.add_option("--syst", "--systematic", dest="systematic", default="Base",type='str',
                     help="Specify which systematic to run on")
(options, args) = parser.parse_args()
year = options.year
decay = options.decay
channel = options.channel
region = options.region
syst = options.systematic

for sample in Samples: 
    if "data_obs" in sample and "Base" not in syst:
        continue
    if "MisID_" in region:
        args = "-y %s -d %s -c %s -s %s -r %s --syst %s --allHists --isCat"%(year, decay, channel, sample, region, syst)
    else:
        args = "-y %s -d %s -c %s -s %s -r %s --syst %s --allHists"%(year, decay, channel, sample, region, syst)
    os.system("python3 makeHists.py %s"%args)
