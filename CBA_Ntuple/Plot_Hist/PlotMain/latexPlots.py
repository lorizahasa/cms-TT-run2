import os
import sys
sys.dont_write_bytecode = True
import numpy as np
from PlotInputs import dirPlot 
from optparse import OptionParser

#----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--isCheck","--isCheck", dest="isCheck",action="store_true",default=False, help="Merge for combined years and channels")
parser.add_option("--isSep","--isSep", dest="isSep",action="store_true",default=False, help="Merge for separate years and channels")
parser.add_option("--isComb","--isComb", dest="isMerge",action="store_true",default=False, help="Merge for combined years and channels")
parser.add_option("--isCat","--isCat", dest="isCat",action="store_true",default=False, help="Merge for separate years and channels")
(options, args) = parser.parse_args()
isCheck = options.isCheck
isSep = options.isSep
isCat = options.isCat
isComb = options.isMerge

byWhat = "Sample"
if isCat:
    byWhat = "Cat"

outTxt = "SepYears"
if isComb:
    outTxt = "CombYears"

fName = "%s/plotBy%s_%s"%(dirPlot, byWhat, outTxt)
txtFile = open("%s.txt"%fName, "r")
texFile = open("%s.tex"%fName, "w")
#texFile = open("./ratioWeight.tex", "w")
allPlotPath = []
allPlotName = []

for line in txtFile:
    allPlotPath.append(line)
    allPlotName.append(line.split("/")[-1])

showPerFig = 16
widthFor   = 4
#figWidth = (1-0.05)/showPerFig#5% margin
if isComb:
    showPerFig = 12
    widthFor   = 3
figWidth = round((1-0.05)/widthFor, 2)#5% margin
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
#os.system("tex2pdf %s.tex"%fName)
