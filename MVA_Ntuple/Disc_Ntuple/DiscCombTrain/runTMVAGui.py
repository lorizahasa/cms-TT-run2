from ROOT import gROOT, gSystem, TMVA
import os

gROOT.SetBatch(True)
gSystem.Load("libTMVAGui")
fName ="TMVA_Classification.root" 
TMVA.variables("dataset",fName)
TMVA.mvas("dataset",fName)
TMVA.mvas("dataset",fName, TMVA.kCompareType)
#TMVA.mvaeffs("dataset",fName)
TMVA.efficiencies("dataset",fName)
TMVA.correlations("dataset",fName)

