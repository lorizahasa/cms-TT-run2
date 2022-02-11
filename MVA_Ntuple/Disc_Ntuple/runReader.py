import os
import itertools
from optparse import OptionParser
from DiscInputs import Systematics, SystLevels

#-----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016",type='str',
                     help="Specifyi the year of the data taking" )
parser.add_option("-d", "--decay", dest="decay", default="Semilep",type='str',
                     help="Specify which decay moded of ttbar Semilep or Dilep? default is Semilep")
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
                     help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-s", "--sample", dest="sample", default="TT_tytg_M800",type='str',
                     help="Specify which sample to run on" )
parser.add_option("-r", "--region", dest="region", default="ttyg_Enriched_SR_Resolved",type='str', 
                     help="which control selection and region"), 
parser.add_option("--level", "--level", dest="level", default="",type='str',
                     help="Specify up/down of systematic")
parser.add_option("--syst", "--systematic", dest="systematic", default="Base",type='str',
                     help="Specify which systematic to run on")
parser.add_option("--method", "--method", dest="method", default="BDTP",type='str', 
                     help="Which MVA method to be used")
parser.add_option("--allSyst", "--allSyst", dest="allSyst", action="store_true", default=False, help="")
(options, args) = parser.parse_args()
year    = options.year
decay   = options.decay
channel = options.channel
method  = options.method
sample  = options.sample
region  = options.region
level   = options.level
syst    = options.systematic
allSyst = options.allSyst
#Run for allSyst for some MC samples
if allSyst:
    for syst, level in itertools.product(Systematics, SystLevels):
        args = "-y %s -d %s -c %s -s %s --method %s -r %s --syst %s --level %s "%(year, decay, channel, sample, method, region, syst, level)
        os.system("python reader.py %s"%args)
#Run for base
elif level=="":
    args = "-y %s -d %s -c %s -s %s --method %s -r %s "%(year, decay, channel, sample, method, region)
    os.system("python reader.py %s"%args)
#Run for sepSyst, for other MC samples
else:
    args = "-y %s -d %s -c %s -s %s --method %s -r %s --syst %s --level %s "%(year, decay, channel, sample, method, region, syst, level)
    os.system("python reader.py %s"%args)
