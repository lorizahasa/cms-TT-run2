from ROOT import TFile
import itertools
import math
import os
import sys

sys.path.insert(0, os.getcwd().replace("condor", ""))
from HistInfo import *
from HistInputs import *

#dict of histograms, with region as key
hName = ["Reco_mass_T", "Reco_st", "Reco_ht"]
#hName = allHistList 
hists = {}
for r in Regions.keys():
    hists[r] = hName

systToNorm = []
systToNorm.append("Weight_q2Up")
systToNorm.append("Weight_q2Down")
systToNorm.append("Weight_pdfUp")
systToNorm.append("Weight_pdfDown")
systToNorm.append("Weight_isrUp")
systToNorm.append("Weight_isrDown")
systToNorm.append("Weight_fsrUp")
systToNorm.append("Weight_fsrDown")

for year, decay, channel in itertools.product(Years, Decays, Channels): 
    fileDir1 = "root://cmseos.fnal.gov//store/user/rverma/Output/cms-TT-run2/Hist_Ntuple"
    fileDir2 = "%s/%s/%s/Merged"%(year, decay, channel)
    inFileName = "AllInc.root"
    outFileName = "AllInc_Norm.root"
    _fileIn  = TFile.Open("%s/%s/%s"%(fileDir1, fileDir2, inFileName),"read")
    _fileOut = TFile.Open("%s/%s/%s"%(fileDir1, fileDir2, outFileName),"recreate")
    print "Input file: ", _fileIn

    NominalYields = {}
    processes = [k.GetName() for k in _fileIn.GetListOfKeys()]
    for p in processes:
        NominalYields[p] = {}
        for r in hists:
            NominalYields[p][r] = {}
            for h in hists[r]:
                _h = _fileIn.Get("%s/%s/Base/%s"%(p, r, h))
                NominalYields[p][r][h] = _h.Integral()

    for p in processes:
        _fileOut.mkdir(p)
        for r in hists:
            _fileOut.mkdir("%s/%s"%(p, r))
            systList = [k.GetName() for k in _fileIn.Get("%s/%s"%(p,r)).GetListOfKeys()]
            for s in systList:
                _fileOut.mkdir("%s/%s/%s"%(p, r, s))
                for h in hists[r]:
                    hName_ = "%s/%s/%s/%s"%(p, r, s, h) 
                    _hIn = _fileIn.Get(hName_)
                    if _hIn.Integral()==0:
                        #print "Zero yield:  ", hName_, " : ", _hIn.Integral()
                        pass
                    elif math.isnan(_hIn.Integral()):
                        #print "NAN yield:  ", hName_, " : ", _hIn.Integral()
                        pass
                    else:
                        if s in systToNorm:
                            _hIn.Scale(NominalYields[p][r][h]/_hIn.Integral())
                    _fileOut.cd("%s/%s/%s/"%(p, r, s))
                    _hIn.Write()
    _fileOut.Close()
    print "Normalised file: ", _fileOut 
