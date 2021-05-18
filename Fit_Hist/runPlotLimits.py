import os
import json
import itertools
import collections
from FitInputs import *
import numpy as np
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--hist", "--hist", dest="hName", default="Reco_mass_T",type='str', 
                     help="which histogram to be used for making datacard")
(options, args) = parser.parse_args()
hName        = options.hName

scaleLimits =True
def runCmd(cmd):
    print "\n\033[01;32m Excecuting: %s \033[00m"%cmd
    os.system(cmd)

os.system("mkdir -p tex")
texFile = open("tex/limitPlot.tex", "w")
#texFile.write("\documentclass{article}\n")
#texFile.write("\usepackage{graphicx}\n")
#texFile.write("\usepackage{subfigure}\n")
#texFile.write("\\begin{document}\n")
allPlotPath = []
allPlotName = []
for ps in PhaseSpace:
    for decay, channel in itertools.product(Decay, Channel):
        for year in Year:
            dirDC = "%s/Fit_Hist/%s/%s/%s/%s/%s"%(condorHistDir, year, decay, channel, ps, hName)
            nameDC = "mH*/higgsCombine_TT_run2.AsymptoticLimits.mH*.root" 
            print hName
            runCmd("combineTool.py -M CollectLimits %s/%s -o %s/limits.json"%(dirDC, nameDC, dirDC))
            if scaleLimits:
                xss = {}
                xss["700.0"]   = 0.03*0.97*2*4.92
                xss["800.0"]   = 0.03*0.97*2*1.68
                xss["900.0"]   = 0.03*0.97*2*0.636
                xss["1000.0"]  = 0.03*0.97*2*0.262
                #xss["1100.0"]  = 0.03*0.97*2*0.116
                xss["1200.0"]  = 0.03*0.97*2*0.0537
                xss["1300.0"]  = 0.03*0.97*2*0.0261
                xss["1400.0"]  = 0.03*0.97*2*0.0131
                xss["1500.0"]  = 0.03*0.97*2*0.00677
                xss["1600.0"]  = 0.03*0.97*2*0.00359
                with open ("%s/limits.json"%dirDC) as old_limit:
                    new_limit = json.load(old_limit)
                    print "OLD: ", new_limit
                    for mass in xss.keys():
                        for limit in new_limit[mass]:
                            new_limit[mass][limit] = xss[mass]*new_limit[mass][limit] 
                with open ('%s/scaled_limits.json'%dirDC, 'w') as newLimitFile:
                    print "\nNEW: ", new_limit
                    json.dump(new_limit, newLimitFile)
            
            title_right = "35.9 fb^{-1} (13 TeV)"
            if "16" in year:
                title_right = "35.9 fb^{-1} (2016) (13 TeV)"
            if "17" in year:
                title_right = "41.5 fb^{-1} (2017) (13 TeV)"
            if "18" in year:
                title_right = "59.7 fb^{-1} (2018) (13 TeV)"
            title_left = "e + jets"
            if "Mu" in channel:
                title_left = "1 #mu, 1 #gamma, "
            else:
                title_left = "1 e, 1 #gamma, "
            if "Boosted" in ps:
                title_left += "#geq 1 AK8, #geq 2 AK4, #geq 1 b"
            if "Resolved" in ps:
                title_left += "0 AK8, #geq 5 AK4, #geq 1 b"
            out = "%s/limit_%s_%s_%s"%(dirDC, year, channel, ps)
            if scaleLimits:
                limitFile = "scaled_limits.json"
            else:
                limitFile = "limits.json"
            runCmd("python plotLimits.py --title-left \"%s\" --title-right \"%s\" %s/%s -o %s --logy --cms-sub \"%s\""%(title_left, title_right, dirDC, limitFile, out, ps))
            plotPath = "%s.pdf"%(out)
            allPlotPath.append(plotPath)
            allPlotName.append(hName)
            #print args

showPerFig = 12
print allPlotName
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
