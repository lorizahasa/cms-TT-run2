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

dictData = {}

sampMC = list(getMC('2016Pre').keys())
outF = open("./mcEvtTable.tex", "w")
halfSamp = int(len(sampMC)/2)

S1 = sampMC[0:halfSamp]
S2 = sampMC[halfSamp:len(sampMC)]
for samp in [S1, S2]:
    dictMC = {}
    for s in samp:
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
        dictMC[s] = [n16Pre, n16Post, n17, n18] 
    dictMC = OrderedDict(sorted(dictMC.items(), key=lambda t: t[0]))
    mcDF = pd.DataFrame.from_dict(dictMC)
    outF.write("\\begin{minipage}[c]{0.50\\textwidth}\n")
    outF.write("\\scalebox{.70}{\n")
    outF.write(mcDF.T.to_latex())
    outF.write("}")
    outF.write("\\end{minipage}\n")


'''
with pd.option_context("max_colwidth", 1000):
    outF.write("\\cmsTable{\n")
    outF.write("\\begin{tabular}{p{0.10\\textwidth}p{0.30\\textwidth}p{0.30\\textwidth}p{0.30\\textwidth}}\n")
    outF.write("\\hline\n")
    outF.write("SFs & 2016 & 2017 & 2018 \\\\\n")
    outF.write("\\hline\n")
    outF.write(dfs.T.to_latex())
    outF.write("\n}")
    print(dfs.to_latex())
f.close()
'''
print(outF)
