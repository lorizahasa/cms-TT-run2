import os
import sys
sys.path.insert(0, os.getcwd().replace("Fit_Hist/FitDYSF", "Hist_Ntuple/HistDYSF"))
import itertools
import json
from FitInputs import *
from HistInputs import Regions
from optparse import OptionParser
import numpy as np
import collections
parser = OptionParser()
parser.add_option("--hist", "--hist", dest="hName", default="Reco_mass_dilep",type='str', 
                     help="which histogram to be used for making datacard")
parser.add_option("--isFD","--isFD",dest="isFD", default=False, action="store_true",
		  help="run FitDiabnostics")
parser.add_option("--isImpact","--isImpact",dest="isImpact", default=False, action="store_true",
		  help="run impacts")
parser.add_option("--isComb","--isComb",dest="isComb", default=False, action="store_true",
		  help="run impacts")
(options, args) = parser.parse_args()
hName        = options.hName
isFD            = options.isFD
isImpact        = options.isImpact
isComb        = options.isComb

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
for y, d, c, r in itertools.product(Year, Decay, Channel, Regions): 
    args = "-y %s -d %s -c %s -r %s --hist %s "%(y, d, c, r, hName)
    print args
    plotDir  = "%s/Fit_Hist/FitDYSF/forDYSF/%s/%s/%s/%s/%s"%(condorHistDir, y, d, c, r, hName)
    if isFD:
        runCmd("python performFit.py %s --isT2W --isFD"%args)
    if isImpact:
        runCmd("python performFit.py %s --isT2W --isImpact"%args)
    plotPath = "%s/nuisImpact.pdf"%(plotDir)
    allPlotPath.append(plotPath)

if isComb:
    for y, d, r in itertools.product(Year, Decay, Regions): 
        args = "-y %s -d %s --isCombCh -r %s --hist %s "%(y, d, r, hName)
        print args
        plotDir  = "%s/Fit_Hist/FitDYSF/forDYSF/%s/%s/%s/%s/%s"%(condorHistDir, y, d, "Mu_Ele", r, hName)
        if isFD:
            runCmd("python performFit.py %s --isT2W --isFD"%args)
        if isImpact:
            runCmd("python performFit.py %s --isT2W --isImpact"%args)
        plotPath = "%s/nuisImpact.pdf"%(plotDir)
        allPlotPath.append(plotPath)

    for d, c, r in itertools.product(Decay, Channel, Regions): 
        args = "--isCombYear -d %s -c %s -r %s --hist %s "%(d, c, r, hName)
        print args
        plotDir  = "%s/Fit_Hist/FitDYSF/forDYSF/%s/%s/%s/%s/%s"%(condorHistDir, "2016_2017_2018", d, c, r, hName)
        if isFD:
            runCmd("python performFit.py %s --isT2W --isFD"%args)
        if isImpact:
            runCmd("python performFit.py %s --isT2W --isImpact"%args)
        plotPath = "%s/nuisImpact.pdf"%(plotDir)
        allPlotPath.append(plotPath)

    for d, r in itertools.product(Decay, Regions): 
        args = "--isCombChYear -d %s -r %s --hist %s "%(d, r, hName)
        print args
        plotDir  = "%s/Fit_Hist/FitDYSF/forDYSF/%s/%s/%s/%s/%s"%(condorHistDir, "2016_2017_2018", d, "Mu_Ele", r, hName)
        if isFD:
            runCmd("python performFit.py %s --isT2W --isFD"%args)
        if isImpact:
            runCmd("python performFit.py %s --isT2W --isImpact"%args)
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
    texFile.write("\caption{Distribution of $%s$}\n"%(plotPath.split("forDYSF")[1].replace("_", "\_")))
    for n in np.arange(showPerPage):
        plotPath = allPlotPath[showPerFig*page + n]
    texFile.write("\end{figure}\n")
    texFile.write("\n")
#texFile.write("\end{document}")
