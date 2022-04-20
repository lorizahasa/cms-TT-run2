import sys
sys.dont_write_bytecode = True
import pandas as pd
from JobsNano_cff import Samples_2016PreVFP, Samples_2016PostVFP,  Samples_2017, Samples_2018 

sampMC = []
for s in Samples_2017.keys():
    if "Data" in s: 
        continue
    sampMC.append(s)

mcPath = "./mcEvtTable.tex"
fMC = open(mcPath, "w")
dictData = {}
dictMC1 = {}
#Write half of the MC in half page
for s in sampMC[0:len(sampMC)/2]: 
    n16Pre  = Samples_2016PreVFP[s][1]
    n16Post = Samples_2016PostVFP[s][1]
    n17     = Samples_2017[s][1]
    n18     = Samples_2018[s][1]
    dictMC1[s] = [n16Pre, n16Post, n17, n18] 
mcDF = pd.DataFrame.from_dict(dictMC1)
fMC.write("\\begin{minipage}[c]{0.50\\textwidth}\n")
fMC.write("\\scalebox{.70}{\n")
fMC.write(mcDF.T.to_latex())
fMC.write("}")
fMC.write("\\end{minipage}\n")

dictMC2 = {}
#Write the second half in the rest page
for s in sampMC[len(sampMC)/2:len(sampMC)]: 
    n16Pre  = Samples_2016PreVFP[s][1]
    n16Post = Samples_2016PostVFP[s][1]
    n17     = Samples_2017[s][1]
    n18     = Samples_2018[s][1]
    dictMC2[s] = [n16Pre, n16Post, n17, n18] 
mcDF = pd.DataFrame.from_dict(dictMC2)
fMC.write("\\begin{minipage}[c]{0.50\\textwidth}\n")
fMC.write("\\scalebox{.70}{\n")
fMC.write(mcDF.T.to_latex())
fMC.write("}")
fMC.write("\\end{minipage}\n")

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
