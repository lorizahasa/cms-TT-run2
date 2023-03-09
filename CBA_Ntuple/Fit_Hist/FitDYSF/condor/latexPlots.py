import os
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("condor", ""))
import numpy as np
from FitInputs import dirFit_, dirTwiki 


fName = "FitDYSF_nuisImpact"
txtFile = open("%s/%s.txt"%(dirFit_, fName), 'r')
texFile = open("%s/%s.tex"%(dirFit_, fName), 'w')
os.system("mkdir -p %s"%dirTwiki)
twikiFile = open("%s/%s.log"%(dirTwiki, fName), "w")

allPlotPath = []
allPlotName = []

for line in txtFile:
    allPlotPath.append(line)
    plotName = line.split("/")[11:15]
    allPlotName.append(' '.join(plotName))

showPerFig = 4
widthFor   = 4
#figWidth = (1-0.05)/showPerFig#5% margin
figWidth = round((1-0.05)/widthFor, 2)#5% margin
nPage = len(allPlotPath)/showPerFig
for page in np.arange(int(nPage)):
    texFile.write("\\begin{figure}\n")
    texFile.write("\centering\n")
    perFigName = []
    for n in np.arange(int(showPerFig)):
        perFigName.append(allPlotName[showPerFig*page + n])
        plotPath = allPlotPath[showPerFig*page + n]
        texFile.write("\includegraphics[width=%s\linewidth]{%s}\n"%(figWidth, plotPath.strip()))
    figCap = '\\\\\\hspace{\\textwidth}, '.join(perFigName)
    #figCap = figCap.replace("\\", "")
    figCap = figCap.replace("_", "\\_")
    texFile.write("\caption{Distributions:  %s}\n"%figCap)
    texFile.write("\end{figure}\n")
    texFile.write("\n")
twikiFile.write("%s/%s.pdf\n"%(dirFit_, fName))
print(texFile)
txtFile.close()
texFile.close()
twikiFile.close()
#os.system("tex2pdf %s.tex"%fName)
