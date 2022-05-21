import sys
sys.dont_write_bytecode = True
import numpy as np
from PlotInputs import dirPlot 

txtFile = open("%s/ratioWeight.txt"%dirPlot, "r")
texFile = open("%s/ratioWeight.tex"%dirPlot, "w")
#texFile = open("./ratioWeight.tex", "w")
allPlotPath = []
allPlotName = []

for line in txtFile:
    allPlotPath.append(line)
    allPlotName.append(line.split("/")[-1])

showPerFig = 4
figWidth = (1-0.05)/showPerFig#5% margin
nPage = len(allPlotPath)/showPerFig
for page in np.arange(nPage):
    texFile.write("\\begin{figure}\n")
    texFile.write("\centering\n")
    perFigName = []
    for n in np.arange(showPerFig):
        perFigName.append(allPlotName[showPerFig*page + n])
        plotPath = allPlotPath[showPerFig*page + n]
        texFile.write("\includegraphics[width=%s\linewidth]{%s}\n"%(figWidth, plotPath.strip()))
    figCap = ', '.join(perFigName)
    texFile.write("\caption{Distribution of $%s$}\n"%(figCap.replace("_", "\_")))
    texFile.write("\end{figure}\n")
    texFile.write("\n")
print(texFile)
