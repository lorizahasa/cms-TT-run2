
import os
import sys
import itertools
from PlotInputs import *
sys.path.insert(0, os.getcwd().replace('Plot_Hist', 'Hist_Ntuple'))
from HistInfo import allPlotList

from optparse import OptionParser
parser =OptionParser()
parser.add_option("--cr", "--controlRegion", dest="controlRegion", default="",type='str', 
                     help="which control selection and region such as Tight, VeryTight, Tight0b, looseCR2e1, looseCRe2g1")
(options, args) = parser.parse_args()
CR = options.controlRegion

os.system("mkdir -p tex")
texFile = open("tex/preFitPlot.tex", "w")
#texFile.write("\documentclass{article}\n")
#texFile.write("\usepackage{graphicx}\n")
#texFile.write("\usepackage{subfigure}\n")
#texFile.write("\\begin{document}\n")

for plot in allPlotList:
    texFile.write("\\begin{figure}\n")
    texFile.write("\centering\n")
    for y in Year:
        for d, c in itertools.product(Decay, Channel):
            #args1 = "-y %s -d %s -c %s --cr %s --plot %s"%(y, d, c, CR, plot)
            args1 = "-y %s -d %s -c %s --plot %s"%(y, d, c, plot)
            print args1
            os.system("python preFitPlots.py %s"%args1)
            plotPath  = "%s/Plot_Hist/%s/%s/%s/SR"%(condorHistDir, y, d, c)
            plotLabel = "%s, %s channel"%(y, c)
            plotName  = "%s_%s_%s.pdf"%(plot, y, c)
            texFile.write("\subfigure[%s]{\includegraphics[width=0.45\linewidth]{%s/%s}}\n"%(plotLabel, plotPath, plotName))
        texFile.write("\\vfil\n")
    texFile.write("\caption{Distribution of $%s$}\n"%(plot.replace("_", "\_")))
    texFile.write("\end{figure}\n")

#texFile.write("\end{document}")

