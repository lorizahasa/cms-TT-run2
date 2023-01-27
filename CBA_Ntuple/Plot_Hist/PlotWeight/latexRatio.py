import os
import sys
sys.dont_write_bytecode = True
import numpy as np
from PlotInputs import dirPlot, dirTwiki 

fName = "ratioWeight"
txtFile = open("%s/%s.txt"%(dirPlot, fName), "r")
texFile = open("%s/%s.tex"%(dirPlot, fName), "w")
os.system("mkdir -p %s"%dirTwiki)
twikiFile = open("%s/%s.log"%(dirTwiki, fName), "w")

allPlotPath = []
allPlotName = []

for line in txtFile:
    allPlotPath.append(line)
    allPlotName.append(line.split("/")[-1])

showPerFig = 4
figWidth = (1-0.05)/showPerFig#5% margin
nPage = len(allPlotPath)/showPerFig
for page in np.arange(int(nPage)):
    texFile.write("\\begin{figure}\n")
    texFile.write("\centering\n")
    perFigName = []
    for n in np.arange(int(showPerFig)):
        perFigName.append(allPlotName[showPerFig*page + n])
        plotPath = allPlotPath[showPerFig*page + n]
        texFile.write("\includegraphics[width=%s\linewidth]{%s}\n"%(figWidth, plotPath.strip()))
    figCap = ', '.join(perFigName)
    texFile.write("\caption{Distribution of $%s$}\n"%(figCap.replace("_", "\_")))
    texFile.write("\end{figure}\n")
    texFile.write("\n")
twikiFile.write("%s/%s.pdf\n"%(dirPlot, fName))
print(texFile)
#print(twikiFile)
txtFile.close()
texFile.close()
twikiFile.close()
