import os
import sys
import json
import ROOT
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("MVA_Ntuple/Plot_Disc", "CBA_Ntuple/Plot_Hist")) 
sys.path.insert(0, os.getcwd().replace("Plot_Disc", "Disc_Ntuple"))
from DiscInputs import Regions
from VarInfo import GetVarInfo
from optparse import OptionParser
from collections import OrderedDict
import itertools
from PlotFunc import *
from PlotInputs import *
from PlotCMSLumi import *
from PlotTDRStyle import *
from ROOT import TFile, TLegend, gPad, gROOT, TCanvas, THStack, TF1, TH1F, TGraphAsymmErrors
import numpy as np

rList = list(Regions.keys())
padGap = 0.01
iPeriod = 4;
iPosX = 10;
ModTDRStyle()
xPadRange = [0.0,1.0]
yPadRange = [0.0,0.30-padGap, 0.30+padGap,1.0]

#----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--isCheck","--isCheck", dest="isCheck",action="store_true",default=False, help="Check for minimum inputs")
parser.add_option("--isSep","--isSep", dest="isSep",action="store_true",default=False, help="Merge for separate years and channels")
parser.add_option("--isComb","--isComb", dest="isComb",action="store_true",default=False, help="Merge for combined years and channels")
(options, args) = parser.parse_args()
isCheck = options.isCheck
isSep = options.isSep
isComb = options.isComb
outTxt = ""

if isCheck:
    isSep  = True
    isComb = False
    Years  = [Years[0]]
    Decays = [Decays[0]]
    Spin   = [Spin[0]]
    Channels = [Channels[0]]
    rList  = [rList[0]]
    Systematics   = [Systematics[0]]
    SampleSyst = [SampleSyst[0]]
if isSep: 
    isComb = False
    outTxt = "SepYears"
if isComb:
    isSep  = False
    outTxt = "CombYears"
    Years = Years_
    Channels = Channels_
if not isCheck and not isSep and not isComb:
    print("Add either --isCheck or --isSep or --isComb in the command line")
    exit()

#-----------------------------------------
#Path of the I/O histrograms/plots
#----------------------------------------
dir_ = "ForMain"
os.system("mkdir -p %s"%dirPlot)
fPath = open("%s/overlaySyst_%s_%s.txt"%(dirPlot, dir_, outTxt), 'w')

###############################################################################
# You can define the two samples to overlay here:
###############################################################################
samples_to_overlay = ["SignalSpin32_M800", "SignalSpin32_M3000"]  

def makePlotOverlay(inFile, hName, region, samples, syst, year, decay, spin, channel,
                    outPlotDir, isData=True, isRatio=True):
    """
    Create a single plot overlaying multiple samples (each with nominal, Up, Down).
    """
    # Prepare canvas
    canvas = TCanvas()
    if isData and isRatio:
        canvas.Divide(1, 2)
        # Top pad (main plot)
        canvas.cd(1)
        gPad.SetRightMargin(0.03)
        gPad.SetPad(xPadRange[0],yPadRange[2],xPadRange[1],yPadRange[3])
        gPad.SetTopMargin(0.09)
        gPad.SetBottomMargin(padGap)
        gPad.RedrawAxis()
    else:
        canvas.cd()

    # Prepare legend
    #plotLegend = TLegend(0.65, 0.40, 0.90, 0.88)
    plotLegend = TLegend(0.15, 0.32, 0.45, 0.62)
    decoLegend(plotLegend, 4, 0.035)

    # We will store the "base" histogram of the first sample
    # so we can set global axes and also do ratio divides easily
    # for each sample to its own base.
    first_base_hist = None
    maxY = 0.0

    # We can also store ratio hists to plot in the second pad:
    ratio_hists = []

    # Define different colors or styles for each sample
    # for clarity. Alternatively, you can cycle colors, etc.
    # For two samples, let's do simple: SampleA -> solid lines
    #                                    SampleB -> dashed lines
    # But you can also use distinct colors if you prefer.
    #color_list = [myRed, myBlue, myGreen+2, myOrange+1]  # pick some colors
    color_list = [ROOT.kRed+1,        # 0 – bright red
    ROOT.kBlue+1,       # 1 – strong blue
    ROOT.kGreen+2,      # 2 – vivid green
    ROOT.kMagenta+1,    # 3 – pink/magenta
    ROOT.kOrange+2,     # 4 – orange
    ROOT.kCyan+2,       # 5 – teal / light blue
    ROOT.kViolet+1,     # 6 – purple
    ROOT.kYellow+2      # 7 – golden yellow (use sparingly; thin lines only)
]
    line_styles = [1, 2, 4]  # 1 = solid, 2 = dashed, etc.

    for i, sample in enumerate(samples):
        # Build the paths
        hPathBase =  f"{sample}/{region}/JetBase/{hName}"
        hPathUp   =  f"{sample}/{region}/{syst}Up/{hName}"
        hPathDown =  f"{sample}/{region}/{syst}Down/{hName}"

        hBase = inFile.Get(hPathBase).Clone(f"Base_{sample}")
        hUp   = inFile.Get(hPathUp).Clone(f"{syst}Up_{sample}")
        hDown = inFile.Get(hPathDown).Clone(f"{syst}Down_{sample}")

        # Set style
        #hBase.SetLineColor(color_list[(2*i) % len(color_list)])
        #hUp.SetLineColor(color_list[(2*i+1) % len(color_list)])
        #hDown.SetLineColor(color_list[(2*i+1) % len(color_list)])
        base_color = color_list[i % len(color_list)]  # use a distinct color for each sample
        hBase.SetLineColor(base_color)
        hUp.SetLineColor(base_color+1)
        hDown.SetLineColor(base_color-1)
        # Optionally set line styles distinct for second sample, etc.
        hBase.SetLineStyle(1)
        hUp.SetLineStyle(2)
        hDown.SetLineStyle(4)

        # We draw in "same" mode if not the first sample
        drawopt = "HIST" if i == 0 else "HIST SAME"

        # For the first sample’s nominal, set axis range.
        if i == 0:
            hBase.Draw("HIST")
            first_base_hist = hBase
        else:
            hBase.Draw(drawopt)
        hUp.Draw("HIST SAME")
        hDown.Draw("HIST SAME")

        # Update maximum
        if hBase.GetMaximum() > maxY:
            maxY = hBase.GetMaximum()
        if hUp.GetMaximum() > maxY:
            maxY = hUp.GetMaximum()
        if hDown.GetMaximum() > maxY:
            maxY = hDown.GetMaximum()

        # Add to legend
        shortSample = sample.replace("SignalSpin32_", " ")
        plotLegend.AddEntry(hBase,  f"{shortSample} nom", "L")
        plotLegend.AddEntry(hUp,    f"{shortSample} up", "L")
        plotLegend.AddEntry(hDown,  f"{shortSample} down", "L")

        # For ratio plots, we store ratio hists if needed
        if isData and isRatio:
            ratioUp   = hUp.Clone(f"{hUp.GetName()}_ratio")
            ratioDown = hDown.Clone(f"{hDown.GetName()}_ratio")
            ratioBase = hBase.Clone(f"{hBase.GetName()}_base")

            # Divide each by the same sample's base
            ratioUp.Divide(hBase)
            ratioDown.Divide(hBase)
            ratioBase.Divide(hBase)  # This should be exactly 1

            # We'll keep them in a list, then draw them after
            ratio_hists.append((ratioBase, ratioUp, ratioDown, i)) 

    # Adjust main pad range
    if first_base_hist:
        first_base_hist.GetYaxis().SetRangeUser(0., 1.7 * maxY)
        first_base_hist.GetXaxis().SetTitle(hName)
        first_base_hist.GetYaxis().SetTitle("Events")

    plotLegend.Draw()

    # Put CMS-lumi, etc.
    lumi_13TeV = getLumiLabel(year)
    chName  = getChLabel(decay, channel)
    chName  = f"{chName}, #bf{{{region}}}"
    crName  = formatCRString(Regions[region])
    #systName =f"#bf{{syst}}"
    #chCRName = "#splitline{{#font[42]{%s}}}{#font[42]{(%s)}}" % (chName, crName)
    #extraText = f"#splitline{{Preliminary}}{{{chCRName}}}"
    extraText = "#splitline{Preliminary,#bf{%s}}{#font[42]{%s} (%s)}" % (syst, chName, crName)
    CMS_lumi(lumi_13TeV, canvas, iPeriod, iPosX, extraText)

    # Draw ratio pad if needed
    if isData and isRatio:
        canvas.cd(2)
        gPad.SetTopMargin(padGap)
        gPad.SetBottomMargin(0.30)
        gPad.SetRightMargin(0.03)
        gPad.SetPad(xPadRange[0], yPadRange[0], xPadRange[1], yPadRange[2])
        gPad.RedrawAxis()

        # Draw each sample's ratio hists
        firstRatioDrawn = False
        for (rBase, rUp, rDown, idx) in ratio_hists:
            # You can choose color/style to match the main pads
            # or define new ones. Let's match them.
            rBase.SetLineColor(color_list[(2*idx) % len(color_list)])
            rUp.SetLineColor(color_list[(2*idx+1) % len(color_list)])
            rDown.SetLineColor(color_list[(2*idx+1) % len(color_list)])
            rBase.SetLineStyle(line_styles[idx])
            rUp.SetLineStyle(line_styles[idx])
            rDown.SetLineStyle(line_styles[idx])

            # The nominal ratio = 1
            # We'll draw the Up ratio first if you prefer, or the base
            if not firstRatioDrawn:
                # We'll use the base ratio histogram to set axis labels
                decoHistRatio(rBase, hName, "Ratio", color_list[(2*idx) % len(color_list)])
                rBase.GetYaxis().SetRangeUser(0.8, 1.2)
                rBase.Draw("HIST")
                firstRatioDrawn = True
            else:
                rBase.Draw("HIST SAME")

            # Then draw Up/Down on same
            rUp.Draw("HIST SAME")
            rDown.Draw("HIST SAME")

        # Draw horizontal line at 1.0
        baseLine = TF1("baseLine","1", -1e9, 1e9)
        baseLine.SetLineColor(3)
        baseLine.Draw("SAME")

    # Finally save PDF
    pdf = f"{outPlotDir}/overlaySyst_{hName}_{region}_{syst}_overlay.pdf"
    canvas.SaveAs(pdf)
    return pdf

#==============================================================================
# Main loop: now we call makePlotOverlay with our two-sample list
#==============================================================================
for decay, region, spin, channel, year, samp in itertools.product(Decays, rList, Spin, Channels, Years, SampleSyst):

    hInfo = GetVarInfo(region, channel)
    hList = ["Disc"]  # or your variables of interest

    if isCheck:
        hList = ["Disc"]

    # Skip some unwanted combos (example logic from your code)
    if "tt_" in region and "gamma" in hList[0]: 
        continue
    if "CR" in region: 
        continue

    ydsc = f"{year}/{decay}/{spin}/{channel}"
    inHistDir  = f"{dirDisc}/{dir_}/{ydsc}/CombMass/BDTA"
    outPlotDir = f"{dirPlot}/{dir_}/{ydsc}/CombMass/BDTA"
    os.system("mkdir -p %s" % outPlotDir)
    
    inFile = TFile(f"{inHistDir}/AllInc.root", "read")

    gROOT.SetBatch(True)

    # Possibly refine which systematics to run over if isSep or isComb, etc.
    if isSep:
        Systematics = SystList_by_year[year]
    if isComb:
        split_year = year.split("__")
        syst_Comb = []
        for y in split_year:
            syst_Comb.append(SystList_by_year[y])    
        Systematics = list(np.unique(syst_Comb))            

    for hName in hList:
        for syst in Systematics:
            # Instead of calling a single sample, we now pass multiple samples:
            pdf_path = makePlotOverlay(inFile, hName, region,
                                       samples_to_overlay,  # <--- pass the list of samples
                                       syst, year, decay, spin, channel,
                                       outPlotDir,
                                       isData=True, isRatio=True)
            fPath.write(f"{pdf_path}\n")

fPath.close()

