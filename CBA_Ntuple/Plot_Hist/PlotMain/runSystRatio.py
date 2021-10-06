
import os
import sys
import itertools
import collections
from PlotInputs import *
sys.path.insert(0, os.getcwd().replace('Plot_Hist', 'Hist_Ntuple'))
from HistInfo import allPlotList
import numpy as np

from optparse import OptionParser
parser =OptionParser()
parser.add_option("--ps", "--phaseSpace", dest="phaseSpace", default="Boosted_SR",type='str', 
                     help="which control selection and region")
(options, args) = parser.parse_args()
phaseSpace = options.phaseSpace

os.system("mkdir -p tex")
texFile = open("tex/preFitPlot_%s.tex"%phaseSpace, "w")
#texFile.write("\documentclass{article}\n")
#texFile.write("\usepackage{graphicx}\n")
#texFile.write("\usepackage{subfigure}\n")
#texFile.write("\\begin{document}\n")
allPlotPath = []
allPlotName = []
#for plot in allPlotList:
for plot in ["Reco_mass_T"]: 
    print "================================="
    print "Making plot for: ", plot
    print "================================="
    for s in SampleWeight:
        for d, c in itertools.product(Decay, Channel):
            for y in Year:
                args1 = "-y %s -d %s -c %s -s %s --plot %s --ps %s "%(y, d, c, s, plot, phaseSpace)
                if "Mu" in c and "Ele" in plot:
                    continue
                if "Ele" in c and "Mu" in plot:
                    continue
                if "Resolved" in phaseSpace and "FatJet" in plot:
                    continue
                os.system("python systRatio.py %s"%args1)
                plotDir  = "%s/Plot_Hist/%s/%s/%s/%s"%(condorHistDir, y, d, c, phaseSpace)
                plotName  = "SystRatio_%s_%s_%s_%s"%(plot, y, c, s)
                plotPath = "%s/%s.pdf"%(plotDir, plotName)
                allPlotPath.append(plotPath)
                allPlotName.append(plot)

showPerFig = 12
nPage = len(allPlotPath)/showPerFig
for page in np.arange(nPage):
    texFile.write("\\begin{figure}\n")
    texFile.write("\centering\n")
    perFigName = []
    for n in np.arange(showPerFig):
        #texFile.write("\subfigure[%s]{\includegraphics[width=0.45\linewidth]{%s/%s}}\n"%(plotLabel, plotPath, plotName))
        perFigName.append(allPlotName[showPerFig*page + n])
        plotPath = allPlotPath[showPerFig*page + n]
        texFile.write("\includegraphics[width=0.32\linewidth]{%s}\n"%(plotPath))
    plotNames = [item for item, count in collections.Counter(perFigName).items()]
    figCap = ', '.join(plotNames)
    texFile.write("\caption{Distribution of $%s$}\n"%(figCap.replace("_", "\_")))
    #texFile.write("\\vfil\n")
    texFile.write("\end{figure}\n")
    texFile.write("\n")
#texFile.write("\end{document}")

