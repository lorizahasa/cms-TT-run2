import os
import sys
import itertools
import collections
from PlotInputs import *
sys.path.insert(0, os.getcwd().replace('Plot_Hist', 'Hist_Ntuple'))
from HistInfo import allHistList
from HistInputs import Regions
from optparse import OptionParser
import numpy as np

#-----------------------------------------
#INPUT command-line arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--isCat","--isCat", dest="isCat",action="store_true",default=False,
                     help="do photon categorization" )
parser.add_option("--isMerge","--isMerge", dest="isMerge",action="store_true",default=False,
                     help="do photon categorization" )
(options, args) = parser.parse_args()
isCat           = options.isCat
isMerge         = options.isMerge

os.system("mkdir -p tex")
merge = []
if isCat:
    merge.append("Cat")
else:
    merge.append("")
texFile = open("tex/preFitPlot%s.tex"%merge[0], "w")
if isMerge:
    merge = ["", "Cat"]
    texFile = open("tex/preFitPlotMerge.tex", "w")

#texFile.write("\documentclass{article}\n")
#texFile.write("\usepackage{graphicx}\n")
#texFile.write("\usepackage{subfigure}\n")
#texFile.write("\\begin{document}\n")
allPlotPath = []
allPlotName = []
for plot in allHistList:
    print "================================="
    print "Making plot for: ", plot
    print "================================="
    for d, c in itertools.product(Decay, Channel):
        for r in Regions.keys():
            for m in merge:
                for y in Year:
                    args1 = "-y %s -d %s -c %s --hist %s -r %s "%(y, d, c, plot, r)
                    if "Mu" in c and "Ele" in plot:
                        continue
                    if "Ele" in c and "Mu" in plot:
                        continue
                    if "Resolved" in r and "FatJet" in plot:
                        continue
                    if "tt_Enriched" in r and "Photon" in plot: 
                        continue
                    if "tt_Enriched" in r and "Reco_mass_T" in plot:
                        continue
                    if "tty_Enriched" in r and "Reco_mass_T" in plot:
                        continue
                    plotDir  = "%s/Plot_Hist/%s/%s/%s/%s"%(condorHistDir, y, d, c, r)
                    plotName  = "%s_%s_%s"%(plot, y, c)
                    if not isMerge:
                        print m
                        os.system("python preFitPlots%s.py %s"%(m, args1))
                    plotPath = "%s/%s%s.pdf"%(plotDir, plotName, m)
                    allPlotPath.append(plotPath)
                    allPlotName.append(plot)

showPerFig = 3
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
        texFile.write("\includegraphics[width=0.32\linewidth]{%s}\n"%(plotPath))
    plotNames = [item for item, count in collections.Counter(perFigName).items()]
    figCap = ', '.join(plotNames)
    #texFile.write("\caption{Distribution of $%s$}\n"%(figCap.replace("_", "\_")))
    isTable = True
    for n in np.arange(showPerPage):
        perFigName.append(allPlotName[showPerFig*page + n])
        plotPath = allPlotPath[showPerFig*page + n]
        tablePath = plotPath.replace("pdf", "tex")
        if "Mu" in tablePath and "Ele" in tablePath:
            isTable = False
        if "Resolved" in tablePath and "FatJet" in tablePath:
            isTable = False
        if "tt_Enriched" in tablePath and "Photon" in tablePath: 
            isTable = False
        if "tt_Enriched" in tablePath and "Reco_mass_T" in tablePath:
            isTable = False
        if "tty_Enriched" in tablePath and "Reco_mass_T" in tablePath:
            isTable = False
        if isTable:
            tableFile = open(tablePath)
            for line in tableFile:
                texFile.write(line)
    texFile.write("\n")
    texFile.write("\end{figure}\n")
#texFile.write("\end{document}")

