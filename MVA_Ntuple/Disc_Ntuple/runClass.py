import os
from optparse import OptionParser
from DiscInputs import Regions

#-----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2017",type='str',
                     help="Specifyi the year of the data taking" )
parser.add_option("-d", "--decay", dest="decay", default="Semilep",type='str',
                     help="Specify which decay moded of ttbar Semilep or Dilep? default is Semilep")
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
                     help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-r", "--region", dest="region", default="ttyg_Enriched_SR_Resolved",type='str', 
                     help="which control selection and region"), 
parser.add_option("--method", "--method", dest="method", default="BDTP",type='str', 
                     help="Which MVA method to be used")
parser.add_option("--level", "--level", dest="level", default="",type='str',
                     help="Specify up/down of systematic")
parser.add_option("--syst", "--systematic", dest="systematic", default="JetBase",type='str',
                     help="Specify which systematic to run on")
(options, args) = parser.parse_args()
year = options.year
decay = options.decay
channel = options.channel
method = options.method
region  = options.region
level =options.level
syst = options.systematic

if level=="":
    args = "-y %s -d %s -c %s --method %s -r %s "%(year, decay, channel, method, region)
else:
    args = "-y %s -d %s -c %s --method %s -r %s --syst %s --level %s "%(year, decay, channel, method, region, syst, level)
print(args)
os.system("python3 classification.py %s"%args)
