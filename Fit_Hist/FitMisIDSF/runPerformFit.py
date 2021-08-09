import os
import sys
sys.path.insert(0, os.getcwd().replace("Fit_Hist/FitMisIDSF", "Hist_Ntuple/HistMisIDSF"))
import itertools
import json
from FitInputs import *
from HistInputs import Regions
from optparse import OptionParser
import numpy as np
import collections
parser = OptionParser()
parser.add_option("--hist", "--hist", dest="hName", default="Reco_mass_lgamma",type='str', 
                     help="which histogram to be used for making datacard")
parser.add_option("--isT2W","--isT2W",dest="isT2W", default=False, action="store_true",
		  help="create text2workspace datacards")
parser.add_option("--isFD","--isFD",dest="isFD", default=False, action="store_true",
		  help="run FitDiabnostics")
parser.add_option("--isImpact","--isImpact",dest="isImpact", default=False, action="store_true",
		  help="run impacts")
(options, args) = parser.parse_args()
hName        = options.hName
isT2W 			= options.isT2W
isFD            = options.isFD
isImpact        = options.isImpact

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
allPlotName = []
for y, d, c, r in itertools.product(Year, Decay, Channel, Regions): 
    args = "-y %s -d %s -c %s -r %s --hist %s "%(y, d, c, r, hName)
    plotDir  = "%s/Fit_Hist/FitMisIDSF/forMisIDSF/%s/%s/%s/%s/%s"%(condorHistDir, y, d, c, r, hName)
    print args
    if isT2W:
        runCmd("python performFit.py %s --isT2W"%args)
    if isFD:
        runCmd("python performFit.py %s --isFD"%args)
    if isImpact:
        runCmd("python performFit.py %s --isImpact"%args)
    plotPath = "%s/nuisImpact.pdf"%(plotDir)
    allPlotPath.append(plotPath)
    allPlotName.append(hName)

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
        perFigName.append(allPlotName[showPerFig*page + n])
        plotPath = allPlotPath[showPerFig*page + n]
        texFile.write("\includegraphics[width=%s\linewidth]{%s}\n"%(figWidth, plotPath))
    texFile.write("\caption{Distribution of $%s$}\n"%(plotPath.split("forMisIDSF")[1].replace("_", "\_")))
    for n in np.arange(showPerPage):
        perFigName.append(allPlotName[showPerFig*page + n])
        plotPath = allPlotPath[showPerFig*page + n]
    texFile.write("\end{figure}\n")
    texFile.write("\n")
#texFile.write("\end{document}")
