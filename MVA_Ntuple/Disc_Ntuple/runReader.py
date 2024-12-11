import os
import sys
sys.dont_write_bytecode = True
import itertools
from optparse import OptionParser
from DiscInputs import SampDict 

#-----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2017",type='str',
                     help="Specifyi the year of the data taking" )
parser.add_option("-d", "--decay", dest="decay", default="Semilep",type='str',
                     help="Specify which decay moded of ttbar Semilep or Dilep? default is Semilep")
parser.add_option("-p", "--spin", dest="spin", default="Spin12",type='str',
                     help="Specify which signal spin Spin32 or Spin12? default is Spin12")
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
                     help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-s", "--sample", dest="sample", default="S1",type='str',
                             help="Specify which sample to run on" )
parser.add_option("-r", "--region", dest="region", default="ttyg_Enriched_SR_Resolved",type='str', 
                     help="which control selection and region"), 
parser.add_option("-z", "--systematic", dest="systematic", default="JetBase",type='str',
                     help="Specify which systematic to run on")
parser.add_option("-m", "--method", dest="method", default="BDTA",type='str', 
                     help="Which MVA method to be used")
(options, args) = parser.parse_args()
year    = options.year
decay   = options.decay
spin    = options.spin
channel = options.channel
sample  = options.sample
method  = options.method
region  = options.region
syst    = options.systematic

for s in SampDict[sample]: 
    #args = "-y %s -d %s -c %s -s %s --method %s -r %s --syst %s "%(year, decay, channel, s, method, region, syst)
    args = "-y %s -d %s -p %s -c %s -s %s -m %s -r %s -z %s "%(year, decay, spin, channel, s, method, region, syst)
    #os.system("python3 reader.py %s"%args)
    os.system("./runReadNtuple %s"%args)
    print(args)

