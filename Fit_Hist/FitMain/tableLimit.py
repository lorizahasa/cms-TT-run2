import itertools
from FitInputs import *
import json

#-----------------------------------------
# Get dySF from the JSON file
#-----------------------------------------
path = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/Fit_Hist/FitMain/forMain/"
def getLimit(jsonData, exp, m):
    paramDict   = jsonData["%s.0"%m]
    lim = 1.0
    for key, val in paramDict.iteritems():
        if exp==key:
            lim= val
    return lim

def roundMe(value, place):
    upStr = '{:.%sf}'%place
    upVal = round(value, place)
    final = upStr.format(upVal)
    return final

#Put SF in reformated dicts
lepDicts = {}
for c in Channel:
    lepDict = {}
    for m in Mass:
        sfList = []
        for y, decay in itertools.product(Year, Decay): 
            print "%s, %s, %s"%(c, m, y)
            limits = []
            for h in histList:
                for r in regionList:
                    limitJSON = "%s/%s/Semilep/%s/%s/%s/mH%s/limits.json"%(path, y, c, r, h, m)
                    with open (limitJSON) as jsonFile:
                        jsonData = json.load(jsonFile)
                        lim      = getLimit(jsonData,"exp0", m)
                        limits.append(lim*xss[m]*100)
            sfList.append(limits)
        lepDict[m] = sfList
    lepDicts[c] = lepDict
    #print lepDict


#print lepDicts
#make table from reformated dicts
#---------------------
#    Regions Years
#    ----------------
# mu
#    ----------------
#---------------------
nCol = 2 + len(Year)
col = ""
for i in range(nCol):
    col += "l"
table ="\\begin{table}"
table += "\\cmsTable{\n"
table += "\\centering\n"
table += "\\begin{tabular}{%s}\n"%col
table += "\\hline\n"
tHead = "Channel & Mass" 
for y in Year:
    tHead += "& %s"%y.replace("_", "+")
tHead += "\\\\\n"
table += tHead
table += "\\hline\n"
row = ""
#print Samples.keys()
#for ch in lepDicts.keys():
print lepDicts
for ch in Channel: 
    row ="\\multirow{%s}{*}{%s}"%(len(regionList), ch.replace("_", "+"))
    chDict = lepDicts[ch]
    print ch
    #for l in chDict.keys():
    for l in Mass: 
        #row += "& %s"%formatCRString(Regions[l]).replace("#", "\\")
        row += "& %s"%l.replace("_", "\\_")
        for sfs in chDict[l]:
            newList = []
            for sf in sfs:
                valNom = roundMe(sf, 2) # 0 = down, 1 = up, 2 = down
                #perUp  = roundMe(abs(100*sf[2]/sf[1]),1)
                #perDown  = roundMe(abs(100*sf[0]/sf[1]),1)
                #row += "& $%s^{+%s%s}_{-%s%s}$"%(valNom, perUp,"\\%", perDown, "\\%")
                #perUp  = roundMe(sf,2)
                #perDown  = roundMe(abs(sf[0]),2)
                #newList.append("$%s^{+%s}_{-%s}$"%(valNom, perUp, perDown))
                newList.append(valNom)
            row += "& %s"%newList
        row += "\\\\\n"
    table += "%s\\hline\n"%row
table += "\\end{tabular}\n"
table += "}"
cap = "from: %s, using distribution: %s"%(regionList, histList)
table += "\\caption{95%s CL median limit$\\times$ 100 %s}\n"%("\\%", cap.replace("_", "\\_")) 
table += "\\end{table}"
print table
tableFile = open("tex/tableLimitByVar.tex", "w")
tableFile.write(table.replace("'",""))
