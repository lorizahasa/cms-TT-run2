import os
import sys
import itertools
import collections
from PlotInputs import *
sys.path.insert(0, os.getcwd().replace('Plot_Hist/PlotMain', 'Hist_Ntuple/HistMain'))
sys.path.insert(0, os.getcwd().replace("Plot_Disc/PlotCombTrain", "Disc_Ntuple/DiscCombTrain"))
from DiscInputs import methodList
from optparse import OptionParser
import numpy as np

#-----------------------------------------------------------------
condorHistDir  = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/MVA_Ntuple" 
#-----------------------------------------------------------------
#-----------------------------------------
#INPUT command-line arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--isMerge","--isMerge", dest="isMerge",action="store_true",default=False,
                     help="merge plots from inclusive and photon categories" )
parser.add_option("--isTable","--isTable", dest="isTable",action="store_true",default=False,
                     help="make table for each plot" )
parser.add_option("--isRun2","--isRun2", dest="isRun2",action="store_true",default=False,
                     help="plot/table for full Run2" )
parser.add_option("--isMake","--isMake", dest="isMake",action="store_true",default=False,
                     help="plot/table for full Run2" )
parser.add_option("--forRebin","--forRebin", dest="forRebin",action="store_true",default=False,
                     help="plot/table for full Run2" )
parser.add_option("--forMain","--forMain", dest="forMain",action="store_true",default=False,
                     help="plot/table for full Run2" )
(options, args) = parser.parse_args()
isMerge         = options.isMerge
isTable         = options.isTable
isRun2          = options.isRun2
isMake          = options.isMake
forRebin          = options.forRebin
forMain          = options.forMain

merge = [""]
if forRebin:
    merge = ["Rebin"]
if forMain:
    merge = ["forMain"]
if forRebin and forMain:
    merge = ["Rebin", "forMain"]

ext = merge[0]
Year_ = Year

if isRun2:
    Year_ = ["Run2"]
    ext += "Run2"
    if isMerge:
        ext += "Merged"

if isMerge:
    merge = ["", "Cat"]
    ext += "Merged"
os.system("mkdir -p tex")
texFile = open("tex/plotBySample%s.tex"%ext, "w")

#texFile.write("\documentclass{article}\n")
#texFile.write("\usepackage{graphicx}\n")
#texFile.write("\usepackage{subfigure}\n")
#texFile.write("\\begin{document}\n")
allPlotPath = []
allPlotName = []

discDict = {}
discDict["Disc"] = methodList.keys()
for hist in histList:
    discDict[hist] = ["MLP"]

for d, c, r, y in itertools.product(Decay, Channel, regionList, Year_):
    for m in Mass:
        for h in discDict.keys(): 
            for method in discDict[h]:
                print "================================="
                print "Making plot for: ", m, method, h
                print "================================="
                args1 = "-y %s -d %s -c %s  --mass  %s --method %s --hist %s -r %s "%(y, d, c, m, method, h, r)
                if "Mu" in c and "Ele" in h:
                    continue
                if "Ele" in c and "Mu" in h:
                    continue
                if "Resolved" in r and "FatJet" in h:
                    continue
                if "tt_Enriched" in r and "Photon" in h: 
                    continue
                if "tt_Enriched" in r and "Reco_mass_T" in h:
                    continue
                if "tt_Enriched" in r and "Reco_mass_lgamma" in h:
                    continue
                if "tty_Enriched" in r and "Reco_mass_T" in h:
                    continue
                plotDir  = "%s/Plot_Disc/PlotCombTrain/%s/%s/%s/%s/%s/%s"%(condorHistDir, y, d, c, m, method, r)
                if isMake: 
                    os.system("python plotDisc.py %s"%(args1))
                plotPath = "%s/%s.pdf"%(plotDir, h)
                allPlotPath.append(plotPath)
                allPlotName.append(h)

showPerFig = 3
figWidth = 0.32
if not isTable:
    showPerFig = 12
if isRun2:
    if not isTable:
        figWidth=0.24
        showPerFig = 24
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
        if showPerPage==2:
            figWidth = 0.45
        if showPerPage==1:
            figWidth = 0.95
        texFile.write("\includegraphics[width=%s\linewidth]{%s}\n"%(figWidth, plotPath))
    plotNames = [item for item, count in collections.Counter(perFigName).items()]
    figCap = ', '.join(plotNames)
    #texFile.write("\caption{Distribution of $%s$}\n"%(figCap.replace("_", "\_")))
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
        if "tt_Enriched" in tablePath and "Reco_mass_lgamma" in plot:
            isTable = False
        if "tty_Enriched" in tablePath and "Reco_mass_T" in tablePath:
            isTable = False
        if isTable:
            tableFile = open(tablePath)
            for line in tableFile:
                texFile.write(line)
    texFile.write("\end{figure}\n")
    texFile.write("\n")
#texFile.write("\end{document}")

