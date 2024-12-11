import os
from optparse import OptionParser
import CombineHarvester.CombineTools.ch as ch
from FitInputs import *

#-----------------------------------------
#INPUT command-line arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--years", dest="years", default="2016Pre",type='str',
                     help="Specify the years of the data taking" )
parser.add_option("-d", "--decayMode", dest="decayMode", default="Semilep",type='str',
                     help="Specify which decayMode moded of ttbar Semilep or Dilep? default is Semilep")
parser.add_option("-c", "--channels", dest="channels", default="Mu",type='str',
		  help="Specify which channels Mu or Ele? default is Mu" )
parser.add_option("-m", "--mass", dest="mass", default="800",type='str',
                     help="Specify the mass of charged Higgs")
parser.add_option("--method", "--method", dest="method", default="BDTA",type='str',
                     help="Specify MVA method") 
parser.add_option("-r", "--regions", dest="regions", default="ttyg_Enriched_SR_Resolved",type='str', 
                     help="which control selection and regions"), 
parser.add_option("--hist", "--hist", dest="hName", default="Reco_mass_T",type='str', 
                     help="which histogram to be used for making datacard")
parser.add_option("-p", "--spin", dest="spin", default="Spin32",type='str', 
                     help="Specify which signal spin Spin32 or Spin12? default Spin32")
parser.add_option("--isT2W","--isT2W",dest="isT2W", default=False, action="store_true",
		  help="create text2workspace datacards")
parser.add_option("--isFD","--isFD",dest="isFD", default=False, action="store_true",
		  help="run FitDiabnostics")
parser.add_option("--isImpact","--isImpact",dest="isImpact", default=False, action="store_true",
		  help="run impacts")
parser.add_option("--isLimit","--isLimit",dest="isLimit", default=False, action="store_true",
		  help="run impacts")
parser.add_option("--isGOF","--isGOF",dest="isGOF", default=False, action="store_true",
		  help="make plot of covariance matrix")
(options, args) = parser.parse_args()
years           = options.years
decayMode       = options.decayMode
channels        = options.channels
mass            = options.mass
method            = options.method
regions          = options.regions
hName           = options.hName
spin            = options.spin

isT2W 			= options.isT2W
isFD            = options.isFD
isImpact        = options.isImpact
isLimit         = options.isLimit
isGOF            = options.isGOF
#-----------------------------------------
#Various functions
#----------------------------------------
def runCmd(cmd):
    print("\n\033[01;32m Excecuting: \033[00m %s"%cmd)
    os.system(cmd)

#-----------------------------------------
#For separate datacards
#----------------------------------------
def getDataCard(year, decayMode, channel, region, hName):
    args = "-y %s -d %s -p %s -c %s -m %s -r %s --hist %s --method %s"%(year, decayMode, spin, channel, mass, region, hName, method)
    runCmd("python3 makeDataCard.py  %s "%args)
    inDirDC = "./output/Fit_Disc/FitMain/%s/%s/%s/%s/%s/%s/%s/%s"%(year, decayMode, spin, channel, mass, method, region, hName)
    name = "%s/Datacard_Alone.txt"%inDirDC
    return name
#-----------------------------------------
#For combination of datacards
#----------------------------------------
dcList = []
for y in years.split("__"):
    for ch in channels.split("__"):
        for r in regions.split("__"):
            pathDC = getDataCard(y, decayMode, ch, r, hName)
            dcList.append(pathDC)
combDCText = ' '.join(dcList)
dirDC = "./output/Fit_Disc/FitMain/%s/%s/%s/%s/%s/%s/%s/%s"%(years, decayMode, spin, channels, mass, method, regions, hName)
if not os.path.exists(dirDC):
    os.makedirs(dirDC)
pathDC  = "%s/Datacard.txt"%(dirDC)
pathT2W = "%s/Text2W.root"%(dirDC)
runCmd("combineCards.py %s > %s"%(combDCText, pathDC))
print(pathDC)

regLable = rDict[regions]
regShort = getRegion(regions)
lumiLabel = getLumiLabel(years)
chLabel  = getChLabel(decayMode, channels)
myTit = "--title-right \"%s\" --title-left \"%s\" --cms-sub \"%s\""%(lumiLabel, chLabel, regLable)

#----------------------------------------
# Text to workspace
#----------------------------------------
if isT2W:
        #runCmd("text2workspace.py %s -o %s --channel-masks"%(pathDC, pathT2W))
        runCmd("text2workspace.py %s -o %s"%(pathDC, pathT2W))
        print(pathT2W)


#----------------------------------------
#Fit diagnostics
#----------------------------------------
rMin = 0
rMax = 20
#paramList = ["r", "WGammaSF", "ZGammaSF"]
paramList = ["r"]
params    = ','.join([str(param) for param in paramList])
if isFD:
    runCmd("combine -M FitDiagnostics  %s --out %s --robustHesse 1  --redefineSignalPOIs %s -v2 --cminDefaultMinimizerStrategy 0 --rMin=%s --rMax=%s --plots --saveShapes --saveWithUncertainties --saveNormalizations %s"%(pathT2W, dirDC, params, rMin, rMax, toInject[regShort]))
    #runCmd("python3 script/diffNuisances.py --all %s/fitDiagnostics.root -g %s/diffNuisances.root"%(dirDC,dirDC))
    runCmd("python3 script/plotCM.py --dirDC %s %s"%(dirDC, myTit))


#----------------------------------------
#Impacts of Systematics
#----------------------------------------
if isImpact:
    runCmd("combineTool.py -M Impacts -d %s  -m 125 --robustFit 1 --cminDefaultMinimizerStrategy 0  --redefineSignalPOIs %s --setParameterRanges r=-10,10 --doInitialFit %s"%(pathT2W, params, toInject[regShort])) 
    runCmd("combineTool.py -M Impacts -d %s  -m 125 --robustFit 1 --cminDefaultMinimizerStrategy 0  --redefineSignalPOIs %s --setParameterRanges r=-10,10 --doFits  --parallel 10 %s "%(pathT2W, params, toInject[regShort]))
    runCmd("combineTool.py -M Impacts -d %s -m 125 -o %s/nuisImpact.json --redefineSignalPOIs %s "%(pathT2W, dirDC, params))
    runCmd("python3 script/plotImpacts.py --cms-label \"   Internal\" -i %s/nuisImpact.json -o %s/nuisImpact.pdf"%(dirDC, dirDC))
    runCmd("python3 script/plotImpacts.py --cms-label \"   Internal\" -i %s/nuisImpact.json -o %s/nuisImpact.pdf %s"%(dirDC, dirDC, myTit))

#----------------------------------------
# Goodness of Fit 
#----------------------------------------
if isGOF:
    runCmd("combine -d %s -M GoodnessOfFit --algo saturated "%pathT2W)
    runCmd("combine -d %s -M GoodnessOfFit --algo saturated  -t 100 -s -1"%pathT2W)
    runCmd("combineTool.py -M CollectGoodnessOfFit --input higgsCombineTest.GoodnessOfFit*.root -o %s/gof.json"%(dirDC))
    runCmd("python3 script/plotGof.py %s/gof.json -o %s/gof --mass 120.0 %s"%(dirDC, dirDC, myTit))

#----------------------------------------
# 95% CL Limits
#----------------------------------------
if isLimit:
    #https://github.com/cms-analysis/CombineHarvester/blob/master/docs/Limits.md
    #runCmd("combine --rAbsAcc 0.000001 %s -M AsymptoticLimits --mass %s --name _TT_run2"%(pathT2W, mass))
    runCmd("combineTool.py -d %s -M AsymptoticLimits --mass %s -n _TT_run2 --run blind --there --parallel 4 "%(pathT2W, mass))
    nameLimitOut = "higgsCombine_TT_run2.AsymptoticLimits.mH%s.root"%(mass)
    runCmd("combineTool.py -M CollectLimits %s/%s -o %s/limits.json"%(dirDC, nameLimitOut, dirDC))
    print(dirDC)


