import sys
sys.dont_write_bytecode = True
import pandas as pd
from collections import OrderedDict
from SamplesNano import getMC
from JobsNano_cff import Samples_2016Pre, Samples_2016Post,  Samples_2017, Samples_2018 

dicts = [Samples_2016Pre, Samples_2016Post, Samples_2017, Samples_2018]
for dict_ in dicts:
    print("\n------------------\n")
    dict_ = OrderedDict(sorted(dict_.items(), key=lambda t: t[0]))
    for k, v in dict_.items():
        if  "Data" in k: 
            print(k, v)

sampMC = getMC('2016Pre').keys()

mcPath = "./mcEvtTable.tex"
fMC = open(mcPath, "w")
dictData = {}
dictMC1 = {}
#Write half of the MC in half page
#for s in sampMC[0:len(sampMC)/2]: 
for s in sampMC:
    try:
        n16Pre  = Samples_2016Pre[s][1]
    except KeyError:
        n16Pre  = "---"
    try:
        n16Post  = Samples_2016Post[s][1]
    except KeyError:
        n16Post  = "---"
    try:
        n17  = Samples_2017[s][1]
    except KeyError:
        n17  = "---"
    try:
        n18  = Samples_2018[s][1]
    except KeyError:
        n18  = "---"
    dictMC1[s] = [n16Pre, n16Post, n17, n18] 
dictMC1 = OrderedDict(sorted(dictMC1.items(), key=lambda t: t[0]))
mcDF = pd.DataFrame.from_dict(dictMC1)
#fMC.write("\\begin{minipage}[c]{0.50\\textwidth}\n")
fMC.write("\\scalebox{.70}{\n")
fMC.write(mcDF.T.to_latex())
fMC.write("}")
#fMC.write("\\end{minipage}\n")

'''
dictMC2 = {}
#Write the second half in the rest page
for s in sampMC[len(sampMC)/2:len(sampMC)]: 
    try:
        n16Pre  = Samples_2016Pre[s][1]
    except KeyError:
        n16Pre  = "---"
    try:
        n16Post  = Samples_2016Post[s][1]
    except KeyError:
        n16Post  = "---"
    try:
        n17  = Samples_2017[s][1]
    except KeyError:
        n17  = "---"
    try:
        n18  = Samples_2018[s][1]
    except KeyError:
        n18  = "---"
    dictMC2[s] = [n16Pre, n16Post, n17, n18] 
dictMC2 = OrderedDict(sorted(dictMC2.items(), key=lambda t: t[0]))
mcDF = pd.DataFrame.from_dict(dictMC2)
fMC.write("\\begin{minipage}[c]{0.50\\textwidth}\n")
fMC.write("\\scalebox{.70}{\n")
fMC.write(mcDF.T.to_latex())
fMC.write("}")
fMC.write("\\end{minipage}\n")
'''

'''
with pd.option_context("max_colwidth", 1000):
    fMC.write("\\cmsTable{\n")
    fMC.write("\\begin{tabular}{p{0.10\\textwidth}p{0.30\\textwidth}p{0.30\\textwidth}p{0.30\\textwidth}}\n")
    fMC.write("\\hline\n")
    fMC.write("SFs & 2016 & 2017 & 2018 \\\\\n")
    fMC.write("\\hline\n")
    fMC.write(dfs.T.to_latex())
    fMC.write("\n}")
    print(dfs.to_latex())
f.close()
'''
print(mcPath)
