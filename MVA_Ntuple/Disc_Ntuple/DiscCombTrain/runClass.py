import os
from optparse import OptionParser
from DiscInputs import Regions

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
parser.add_option("--method", "--method", dest="method", default="BDTP",type='str', 
                     help="Which MVA method to be used")
parser.add_option("--level", "--level", dest="level", default="",type='str',
                     help="Specify up/down of systematic")
parser.add_option("--syst", "--systematic", dest="systematic", default="Base",type='str',
                     help="Specify which systematic to run on")
(options, args) = parser.parse_args()
year = options.year
decay = options.decay
channel = options.channel
method = options.method
level =options.level
syst = options.systematic

for r in Regions.keys():
    if level=="":
        args = "-y %s -d %s -c %s --method %s -r %s "%(year, decay, channel, method, r)
    else:
        args = "-y %s -d %s -c %s --method %s -r %s --syst %s --level %s "%(year, decay, channel, method, r, syst, level)
    print args
    os.system("python classification.py %s"%args)
