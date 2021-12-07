import os
import sys
import itertools
import json
from FitInputs import *
from optparse import OptionParser
import numpy as np
import collections
parser = OptionParser()
parser.add_option("--isFD","--isFD",dest="isFD", default=False, action="store_true",
		  help="run FitDiabnostics")
parser.add_option("--isImpact","--isImpact",dest="isImpact", default=False, action="store_true",
		  help="run impacts")
parser.add_option("--isLimit","--isLimit",dest="isLimit", default=False, action="store_true",
		  help="run impacts")
(options, args) = parser.parse_args()
isFD            = options.isFD
isImpact        = options.isImpact
isLimit        = options.isLimit

if not os.path.exists("./RateParams.json"):
    with open("RateParams.json", "w") as f:
        data = {}
        json.dump(data, f)

def runCmd(cmd):
    print "\n\033[01;32m Excecuting: %s \033[00m"%cmd
    os.system(cmd)

os.system("mkdir -p tex")
texFile = open("tex/performFit.tex", "w")
allPlotPath = []
for y, d, c, r, h, m in itertools.product(Year, Decay, Channel, regionList, histList, Mass): 
    args = "-y %s -d %s -c %s -r %s --hist %s -m %s "%(y, d, c, r, h, m)
    print args
    plotDir  = "%s/Fit_Hist/FitMain/forMain/%s/%s/%s/%s/%s/mH%s"%(condorHistDir, y, d, c, r, h,m)
    if isFD:
        runCmd("python performFit.py %s --isT2W --isFD"%args)
    if isImpact:
        runCmd("python performFit.py %s --isT2W --isImpact"%args)
    if isLimit:
        runCmd("python performFit.py %s --isT2W --isLimit"%args)
    plotPath = "%s/nuisImpact.pdf"%(plotDir)
    allPlotPath.append(plotPath)

showPerFig = 1
figWidth = 1.0
nPage = len(allPlotPath)/showPerFig
remainder = len(allPlotPath)%showPerFig
if remainder != 0:
    nPage = nPage +1
for page in np.arange(nPage):
    texFile.write("\\begin{figure}\n")
    texFile.write("\centering\n")
    perFigName = []
    showPerPage = showPerFig
    if remainder != 0:
        if page == nPage -1:
            showPerPage = remainder
    #Plots
    for n in np.arange(showPerPage):
        plotPath = allPlotPath[showPerFig*page + n]
        texFile.write("\includegraphics[width=%s\linewidth]{%s}\n"%(figWidth, plotPath))
    texFile.write("\caption{Distribution of $%s$}\n"%(plotPath.split("forMain")[1].replace("_", "\_")))
    for n in np.arange(showPerPage):
        plotPath = allPlotPath[showPerFig*page + n]
    texFile.write("\end{figure}\n")
    texFile.write("\n")
#texFile.write("\end{document}")
