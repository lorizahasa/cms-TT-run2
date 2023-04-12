import sys
sys.dont_write_bytecode = True
import pandas as pd
from collections import OrderedDict
from SamplesNano import getMC
from JobsNano_cff import Samples_2016Pre, Samples_2016Post,  Samples_2017, Samples_2018 
from getFiles import toM

def makeMC(isBkg=True):
    outF_ = "mcEvtTable_Sig.tex"
    samps = sampSig
    if isBkg:
        outF_ = "mcEvtTable_Bkg.tex"
        samps = sampBkg
    outF = open("/uscms_data/d3/rverma/docs/CMSSW_10_4_0/src/cms-TT-run2/AN-21-151/Tables/%s"%outF_, "w")
    halfSamp = int(len(samps)/2)
    S1 = samps[0:halfSamp]
    S2 = samps[halfSamp:len(samps)]
    for samp in [S1, S2]:
        dictMC = {}
        tot16Pre = []
        tot16Post= []
        tot17    = []
        tot18    = []
        for s in samp:
            try:
                n16Pre  = Samples_2016Pre[s][1]
                n16Pre_  = Samples_2016Pre[s][2]
            except KeyError:
                n16Pre  = "---"
                n16Pre_ = 0
            try:
                n16Post  = Samples_2016Post[s][1]
                n16Post_  = Samples_2016Post[s][2]
            except KeyError:
                n16Post  = "---"
                n16Post_ = 0
            try:
                n17  = Samples_2017[s][1]
                n17_  = Samples_2017[s][2]
            except KeyError:
                n17  = "---"
                n17_ = 0
            try:
                n18  = Samples_2018[s][1]
                n18_  = Samples_2018[s][2]
            except KeyError:
                n18  = "---"
                n18_ = 0
            tot16Pre.append(n16Pre_)
            tot16Post.append(n16Post_)
            tot17.append(n17_)
            tot18.append(n18_)
            if isBkg:
                dictMC[s] = [n16Pre, n16Post, n17, n18]
            else:
                m = s.split("_")[-1]
                dictMC[s] = [xss32[m], xss12[m], round(xss32[m]/xss12[m], 2), n16Pre, n16Post, n17, n18]
        dictMC = OrderedDict(sorted(dictMC.items(), key=lambda t: t[0]))
        if isBkg:
            dictMC["Total"] = [toM(sum(tot16Pre)), toM(sum(tot16Post)), toM(sum(tot17)), toM(sum(tot18))]
            sumY = toM(sum(tot16Pre) + sum(tot16Post) + sum(tot17) + sum(tot18))
        else:
            dictMC["Total"] = ["---", "---", "---", toM(sum(tot16Pre)), toM(sum(tot16Post)), toM(sum(tot17)), toM(sum(tot18))]
            sumY = toM(sum(tot16Pre) + sum(tot16Post) + sum(tot17) + sum(tot18))
        print("%s : %s"%(sumY, samp))
        mcDF = pd.DataFrame.from_dict(dictMC)
        outF.write("\\begin{minipage}[c]{0.60\\textwidth}\n")
        outF.write("\\scalebox{.60}{\n")
        outF.write(mcDF.T.to_latex())
        outF.write("}")
        outF.write("\\end{minipage}\n")
    print(outF)

xss12 = {}
xss32 = {}
xss12["M700"]   =  0.2659
xss12["M800"]   =  0.1147
xss12["M900"]   =  0.05318
xss12["M1000"]  =  0.02590
xss12["M1100"]  =  0.01322
xss12["M1200"]  =  0.006897
xss12["M1300"]  =  0.003732
xss12["M1400"]  =  0.002061
xss12["M1500"]  =  0.001165
xss12["M1600"]  =  0.0006675
xss12["M1700"]  =  0.0003911
xss12["M1800"]  =  0.0002329
xss12["M1900"]  =  0.0001404
xss12["M2000"]  =  0.00008614
xss12["M2250"]  =  0.00002748
xss12["M2500"]  =  0.000009695
xss12["M2750"]  =  0.000003746
xss12["M3000"]  =  0.000001535
    
xss32["M700"]   =  4.686152e+00 
xss32["M800"]   =  1.623764e+00 
xss32["M900"]   =  6.192314e-01 
xss32["M1000"]  =  2.573151e-01 
xss32["M1100"]  =  1.133120e-01 
xss32["M1200"]  =  5.251545e-02 
xss32["M1300"]  =  2.527675e-02 
xss32["M1400"]  =  1.262786e-02 
xss32["M1500"]  =  6.498742e-03 
xss32["M1600"]  =  3.424087e-03 
xss32["M1700"]  =  1.846422e-03 
xss32["M1800"]  =  1.009361e-03 
xss32["M1900"]  =  5.607416e-04 
xss32["M2000"]  =  3.155604e-04 
xss32["M2250"]  =  7.825815e-05 
xss32["M2500"]  =  2.051170e-05 
xss32["M2750"]  =  5.602932e-06 
xss32["M3000"]  =  1.585532e-06 

if __name__=="__main__":
    dicts = [Samples_2016Pre, Samples_2016Post, Samples_2017, Samples_2018]
    sumData = 0
    for dict_ in dicts:
        print("\n------------------\n")
        dict_ = OrderedDict(sorted(dict_.items(), key=lambda t: t[0]))
        for k, v in dict_.items():
            if  "Data" in k: 
                sumData = sumData + v[2]
                print(k, v)
    print("All data events = %s"%toM(sumData))
    sampMC = list(getMC('2016Pre').keys())
    sampBkg = []
    sampSig = []
    for s in sampMC:
        if "Signal" in s:
            sampSig.append(s)
        else:
            sampBkg.append(s)

    makeMC(True)
    makeMC(False)
