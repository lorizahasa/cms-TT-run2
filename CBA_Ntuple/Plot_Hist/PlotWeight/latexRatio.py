import os
import sys
sys.dont_write_bytecode = True
import numpy as np
from PlotInputs import dirPlot, dirTwiki 

#fName = "effPlot"
#fName = "ratioWeight"
fName = "overlayWeight"
txtFile = open("%s/%s.txt"%(dirPlot, fName), "r")
texFile = open("%s/%s.tex"%(dirPlot, fName), "w")
os.system("mkdir -p %s"%dirTwiki)
twikiFile = open("%s/%s.log"%(dirTwiki, fName), "w")

allPlotPath = []
allPlotName = []

for line in txtFile:
    allPlotPath.append(line)
    allPlotName.append(line.split("/")[-1])

showPerFig = 9
widthFor   = 3
#figWidth = (1-0.05)/showPerFig#5% margin
isComb =False
if isComb:
    showPerFig = 12
    widthFor   = 3
figWidth = round((1-0.05)/widthFor, 2)#5% margin
if len(allPlotPath) < showPerFig:
    showPerFig = len(allPlotPath)
nPage = len(allPlotPath)/showPerFig
remainder = len(allPlotPath)%showPerFig
if remainder != 0:
    nPage = nPage +1
for page in np.arange(int(nPage)):
    texFile.write("\\begin{figure}\n")
    texFile.write("\centering\n")
    perFigName = []
    showPerPage = showPerFig
    if remainder != 0:
        if page == int(nPage -1):
            showPerPage = remainder
    for n in np.arange(int(showPerPage)):
        perFigName.append(allPlotName[showPerFig*page + n])
        plotPath = allPlotPath[showPerFig*page + n]
        texFile.write("\includegraphics[width=%s\linewidth]{%s}\n"%(figWidth, plotPath.strip()))
    figCap = ', '.join(perFigName)
    texFile.write("\caption{Distribution of $%s$}\n"%(figCap.replace("_", "\_")))
    texFile.write("\end{figure}\n")
    texFile.write("\n")
twikiFile.write("%s/%s.pdf\n"%(dirPlot, fName))
print(texFile)
print(twikiFile)
txtFile.close()
texFile.close()
twikiFile.close()
