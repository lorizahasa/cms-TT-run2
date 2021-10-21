import os
import sys
import itertools
import collections
from FitInputs import *
from optparse import OptionParser
import numpy as np

#-----------------------------------------
#INPUT command-line arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--isMake","--isMake", dest="isMake",action="store_true",default=False,
                     help="plot/table for full Run2" )
parser.add_option("--byCR","--byCR",dest="byCR", default=False, action="store_true",
		  help="run FitDiabnostics")
parser.add_option("--byVar","--byVar",dest="byVar", default=False, action="store_true",
		  help="run FitDiabnostics")
(options, args) = parser.parse_args()
isMake          = options.isMake
byCR           = options.byCR
byVar           = options.byVar
texFile = open("tex/compareLimit.tex", "w")

if byVar:
    name = "byVar"
elif byCR:
    name = "byCR"
else:
    name = "by"
allPlotPath = []
for d, c in itertools.product(Decay, Channel):
    for y in Year:
        args1 = "-y %s -d %s -c %s "%(y, d, c)
        plotDir = "%s/Fit_Hist/FitMain/forMain/%s/Semilep/%s"%(condorHistDir, y, c)
        plotName  = "limit_%s.pdf"%name
        if isMake: 
            if byVar:
                os.system("python comparLimits.py --byVar %s"%(args1))
            elif byCR:
                os.system("python comparLimits.py --byCR %s"%(args1))
            else:
                os.system("python comparLimits.py  %s"%(args1))
        plotPath = "%s/%s"%(plotDir, plotName)
        allPlotPath.append(plotPath)
    
figWidth = 0.32
showPerFig = 12
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
        perFigName.append(allPlotPath[showPerFig*page + n])
        plotPath = allPlotPath[showPerFig*page + n]
        if showPerPage==2:
            figWidth = 0.45
        if showPerPage==1:
            figWidth = 0.95
        texFile.write("\includegraphics[width=%s\linewidth]{%s}\n"%(figWidth, plotPath))
    texFile.write("\\end{figure}\n")
    #texFile.write("\caption{Distribution of $%s$}\n"%(figCap.replace("_", "\_")))
#texFile.write("\end{document}")

