import os
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("condor", ""))
import numpy as np
from FitInputs import dirFit, dirTwiki 

#fName = "compareLimit"
#fName = "plotLimit"
isLimit = False
isImpact = True
fName = "plotLimits"
if isImpact:
    fName = "FitDisc_nuisImpact"
txtFile = open("%s/%s.txt"%(dirFit, fName), "r")
texFile = open("%s/%s.tex"%(dirFit, fName), "w")
os.system("mkdir -p %s"%dirTwiki)
twikiFile = open("%s/%s.log"%(dirTwiki, fName), "w")

allPlotPath = []
allPlotName = []

for line in txtFile:
    allPlotPath.append(line)
    if isImpact:
        plotName = line.split("/")[11:15]
        allPlotName.append(' '.join(plotName))
    else:
        allPlotName.append(line.split("/")[-1])

showPerFig = 16
if isImpact:
    showPerFig = 4
widthFor   = 4
figWidth = round((1-0.05)/widthFor, 2)#5% margin
nPage = int(len(allPlotPath)/showPerFig)
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
    for n in np.arange(int(showPerPage)):
        perFigName.append(allPlotName[showPerFig*page + n])
        plotPath = allPlotPath[showPerFig*page + n]
        texFile.write("\includegraphics[width=%s\linewidth]{%s}\n"%(figWidth, plotPath.strip()))
    figCap = ', '.join(perFigName)
    texFile.write("\caption{Distribution of $%s$}\n"%(figCap.replace("_", "\_")))
    texFile.write("\end{figure}\n")
    texFile.write("\n")
twikiFile.write("%s/%s.pdf\n"%(dirFit, fName))
print(texFile)
txtFile.close()
texFile.close()
twikiFile.close()
#os.system("tex2pdf %s.tex"%fName)
