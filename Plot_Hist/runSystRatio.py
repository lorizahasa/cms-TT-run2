import os
import itertools
import json
from PlotInputs import *

def runCmd(cmd):
    print "\n\033[01;32m Excecuting: %s \033[00m"%cmd
    os.system(cmd)
#for year, channel, sample in itertools.product(Year, Channel, SamplesSyst): 
for year, channel in itertools.product(Year, Channel): 
    #args = "-y %s -c %s -s %s"%(year, channel, sample)
    args = "-y %s -c %s"%(year, channel)
    runCmd("python systRatioInc.py %s"%args)
