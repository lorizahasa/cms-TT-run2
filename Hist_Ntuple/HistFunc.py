from SampleInfo import *
from ROOT import TChain, TH1F, gROOT, gDirectory
import sys
gROOT.SetBatch(True)
#----------------------------------------------------------
#Get jet multiplicity cuts in a different control regions
#----------------------------------------------------------
#Jet selection naming: a3j_e2b = atleast 3 jet, out of which 2 are b jets: nJet >= 3, nBJet ==2
def getJetMultiCut(controlRegion="Boosted_SR"):
    if not len(controlRegion.split("_"))==2: 
        print "Please provide control region in Boosted_SR format" 
        sys.exit()
        nJet, nBJets, nJetSel, nBJetSel, allJetSel = 4, 2, "Jet_size>=4", "Jet_b_size>=2", "Jet_size>=4 && Jet_b_size>=2"
    if "Boosted" in controlRegion:
        nJet, nBJets, nJetSel, nBJetSel, allJetSel = 2, 1, "Jet_size>=2", "Jet_b_size>=1", "Jet_size>=2 && Jet_b_size>=1"
    if "Resolved" in controlRegion:
        nJet, nBJets, nJetSel, nBJetSel, allJetSel = 5, 1, "Jet_size>=5", "Jet_b_size>=1", "Jet_size>=5 && Jet_b_size>=1"
    print "nJet: %s, nBJets: %s, nJetSel: %s, nBJetSel: %s, allJetSel: %s"%(nJet, nBJets, nJetSel, nBJetSel, allJetSel)
    return nJet, nBJets, nJetSel, nBJetSel, allJetSel

#----------------------------------------------------------
#NICE WAY TO PRINT STRINGS
#----------------------------------------------------------
def toPrint(string, value):
    length = (len(string)+len(str(value))+2)
    line = "-"*length
    print ""
    print "* "+ line +                    " *"
    print "| "+ " "*length +              " |"
    print "| "+ string+ ": "+ str(value)+ " |"
    print "| "+ " "*length +              " |"
    print "* "+ line +                    " *"
