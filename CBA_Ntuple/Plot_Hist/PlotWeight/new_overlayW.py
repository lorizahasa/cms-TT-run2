#!/usr/bin/env python3
import os, sys, math, json, itertools
sys.dont_write_bytecode = True

# --- your paths ---
sys.path.insert(0, os.getcwd().replace("PlotWeight", "")) 
sys.path.insert(0, os.getcwd().replace("Plot_Hist/PlotWeight", "Hist_Ntuple/HistWeight")) 
sys.path.insert(0, os.getcwd().replace("Plot_Hist/PlotWeight", "Plot_Hist")) 

from HistInputs import Corrs, Regions
from PlotFunc import *
from PlotInputs import *
from PlotCMSLumi import *
from PlotTDRStyle import *
from optparse import OptionParser
from PlotLabel import labelDict
from ROOT import TFile, TLegend, gPad, gROOT, TCanvas, TF1, TH1F

# ==============================
# Helpers
# ==============================
def sanitize_hist(h, tag="", replace_with=0.0):
    if not h:
        print(f"[sanitize_hist] Missing hist: {tag}")
        return None
    nb = h.GetNbinsX()
    for ib in range(0, nb+2): # include UF/OF
        c = h.GetBinContent(ib); e = h.GetBinError(ib)
        if (not math.isfinite(c)):
            print(f"[sanitize_hist] {tag}: bin {ib} content={c} → {replace_with}")
            h.SetBinContent(ib, replace_with); h.SetBinError(ib, 0.0)
        if (not math.isfinite(e)):
            print(f"[sanitize_hist] {tag}: bin {ib} error={e} → 0")
            h.SetBinError(ib, 0.0)
    return h

def prune_outliers_relative(h_var, h_ref, factor=50.0, abs_cap=1e9, tag=""):
    if (not h_var) or (not h_ref): return h_var
    nb = h_var.GetNbinsX(); eps = 1e-12
    for ib in range(0, nb+2):
        v = h_var.GetBinContent(ib); r = h_ref.GetBinContent(ib)
        kill = False
        if (r <= 0.0 and abs(v) > 0.0) or abs(v) > abs_cap or abs(v) > factor*(abs(r)+eps):
            kill = True
        if kill:
            print(f"[prune] {tag}: bin {ib} var={v:.3g}, ref={r:.3g} → 0")
            h_var.SetBinContent(ib, 0.0); h_var.SetBinError(ib, 0.0)
    return h_var

def prune_by_ratio(h_var, h_ref, rmax=4.0, rmin=0.1, min_ref=3.0, tag=""):
    if (not h_var) or (not h_ref): return h_var
    nb = h_var.GetNbinsX(); eps = 1e-12
    for ib in range(0, nb+2):
        v = h_var.GetBinContent(ib); r = h_ref.GetBinContent(ib)
        kill = False
        if r < min_ref:
            if abs(v) > rmax*max(1.0, abs(r)): kill = True
        else:
            ratio = v/(r+eps)
            if (not math.isfinite(ratio)) or (ratio > rmax) or (ratio < rmin): kill = True
        if kill:
            print(f"[prune-ratio] {tag}: bin {ib} v={v:.3g}, r={r:.3g} → 0")
            h_var.SetBinContent(ib, 0.0); h_var.SetBinError(ib, 0.0)
    return h_var

def full_integral(h):
    if not h: return float('nan')
    return h.Integral(0, h.GetNbinsX()+1)

def safe_divide(num, den, name="ratio"):
    out = num.Clone(name); out.Sumw2()
    nb = out.GetNbinsX()
    for ib in range(0, nb+2):
        d = den.GetBinContent(ib)
        if (d <= 0.0) or (not math.isfinite(d)):
            out.SetBinContent(ib, 0.0); out.SetBinError(ib, 0.0)
        else:
            n = num.GetBinContent(ib)
            out.SetBinContent(ib, n/d)
            out.SetBinError(ib, 0.0)
    return out

def ratio_or_dash(num, den):
    if (den is None) or (den == 0) or (not math.isfinite(den)) or (not math.isfinite(num)):
        return "—"
    return f"{round(num/den, 3)}"

def is_empty(h):
    return (not h) or (full_integral(h) == 0.0)

def has_bad_bins(h):
    if not h: return True
    nb = h.GetNbinsX()
    for ib in range(0, nb+2):
        if (not math.isfinite(h.GetBinContent(ib))) or (not math.isfinite(h.GetBinError(ib))):
            return True
    return False

def zero_like(h, name):
    z = h.Clone(name)
    z.Reset("ICE")   # zero contents & errors, keep binning
    if not z.GetSumw2N(): z.Sumw2()
    return z

# ==============================
# Style / pads
# ==============================
padGap = 0.0
iPeriod = 4
iPosX = 10
ModTDRStyle()
xPadRange  = [0.0,1.0]
rW = 0.25
yPadRange1 = [2*rW+padGap,1.0]
yPadRange2 = [rW+padGap,2*rW]
yPadRange3 = [0.0,rW]

#----------------------------------------
# CLI
#----------------------------------------
parser = OptionParser()
parser.add_option("--isCheck","--isCheck", dest="isCheck",action="store_true",default=False)
parser.add_option("--isSep","--isSep",     dest="isSep",  action="store_true",default=False)
parser.add_option("--isComb","--isComb",   dest="isComb", action="store_true",default=False)
(options, args) = parser.parse_args()
isCheck = options.isCheck
isSep   = options.isSep
isComb  = options.isComb

tuneSyst = {"Tune": ['Uncorr', 'Weight_tune', 'Weight_tuneUp', 'Weight_tuneDown']}
allCorrs = {**tuneSyst, **Corrs}
systKeys = list(allCorrs.keys())
outTxt = ""
if isCheck:
    Years    = [Years_[0]]
    Decays   = [Decays[0]]
    Channels = [Channels_[0]]
    systKeys = ["Weight_pdf"]
if isSep:  outTxt = "SepYears"
if isComb:
    outTxt   = "CombYears"
    Years    = Years_
    Channels = Channels_
if not isCheck and not isSep and not isComb:
    print("Add either --isCheck or --isSep or --isComb in the command line")
    sys.exit(0)

#-----------------------------------------
# I/O
#----------------------------------------
os.system("mkdir -p %s"%dirPlot)
fPath = open("%s/overlayWeight.txt"%dirPlot, 'w')

# Samples whose broken variations we drop (keep their Uncorr only)
block_samples = {"TTbar", "Others"}

for channel, decay, systKey, year in itertools.product(Channels, Decays, systKeys, Years):
    systs  = allCorrs[systKey]
    print(systs)
    if len(systs) < 2: continue

    hList = ["Reco_st"]
    for hName in hList:
        isData, isRatio, isLog = True, True, True
        print("----------------------------------------------")
        print("%s, %s, %s, %s, %s, %s"%(year, decay, channel, region, systs, hName))
        print("----------------------------------------------")

        if "tt_" in region and ("gamma" in hName or "Pho" in hName): continue 
        if ("ele" in systKey and "Mu" in channel):  continue
        if ("mu"  in systKey and "Ele" in channel): continue
        if "CR" in region:                          continue

        ydc = "%s/%s/%s"%(year, decay, channel)
        inHistDir  = "%s/%s"%(dirHist, ydc)
        outPlotDir = "%s/%s/%s"%(dirPlot, ydc, region)
        if not os.path.exists(outPlotDir): os.makedirs(outPlotDir)

        inFile = TFile("%s/AllInc.root"%(inHistDir), "read")
        gROOT.SetBatch(True)

        first = True
        for samp in sampBkg.keys():

            # Build paths
            if "Tune" in systKey:
                if "TTGamma" in samp:
                    hPathUncorr = "%s/%s/%s/%s"%("TTGamma",          region, systs[0], hName)
                    hPathCorr   = "%s/%s/%s/%s"%("TTGamma",          region, systs[0], hName)
                    hPathUp     = "%s/%s/%s/%s"%("TTGamma_TuneUp",   region, systs[0], hName)
                    hPathDown   = "%s/%s/%s/%s"%("TTGamma_TuneDown", region, systs[0], hName)
                else:
                    hPathUncorr = "%s/%s/%s/%s"%(samp, region, systs[0], hName)
                    hPathCorr   = "%s/%s/%s/%s"%(samp, region, systs[0], hName)
                    hPathUp     = "%s/%s/%s/%s"%(samp, region, systs[0], hName)
                    hPathDown   = "%s/%s/%s/%s"%(samp, region, systs[0], hName)
            else:
                hPathUncorr = "%s/%s/%s/%s"%(samp, region, systs[0], hName)
                hPathCorr   = "%s/%s/%s/%s"%(samp, region, systs[1], hName)
                hPathUp     = "%s/%s/%s/%s"%(samp, region, systs[2], hName)
                hPathDown   = "%s/%s/%s/%s"%(samp, region, systs[3], hName)
                if systs[1] == "Uncorr":  # central=uncorr
                    hPathCorr = hPathUncorr

            # Fetch
            hUncorr_  = inFile.Get(hPathUncorr)
            hCorr_    = inFile.Get(hPathCorr)
            hUp_      = inFile.Get(hPathUp)
            hDown_    = inFile.Get(hPathDown)

            # Decide if we drop variations for this sample (based on NaN/Inf)
            drop_vars = False
            if (samp in block_samples) and (has_bad_bins(hCorr_) or has_bad_bins(hUp_) or has_bad_bins(hDown_)):
                drop_vars = True
                print(f"[INFO] Dropping variations for {samp} (NaN/Inf found) — keeping Uncorr only.")

            # Sanitize nominal first (needed for zero_like clones)
            hUncorr_ = sanitize_hist(hUncorr_, f"{samp}:{hPathUncorr}")
            if not hUncorr_:
                print(f"[WARN] Skip {samp}: missing Uncorr.")
                continue
            if not hUncorr_.GetSumw2N(): hUncorr_.Sumw2()
            if drop_vars:
            # >>> The crucial change: clone Uncorr for base AND for Up/Down
                hCorr_ = hUncorr_.Clone(f"{samp}_Corr_baseUncorr");  hCorr_.Sumw2()
                hUp_   = hUncorr_.Clone(f"{samp}_Up_baseUncorr");    hUp_.Sumw2()
                hDown_ = hUncorr_.Clone(f"{samp}_Down_baseUncorr");  hDown_.Sumw2()
            else:
                # Otherwise sanitize variations normally
                 hCorr_ = sanitize_hist(hCorr_,   f"{samp}:{hPathCorr}");   hCorr_.Sumw2() if hCorr_ and not hCorr_.GetSumw2N() else None
                 hUp_   = sanitize_hist(hUp_,     f"{samp}:{hPathUp}");     hUp_.Sumw2()   if hUp_   and not hUp_.GetSumw2N()   else None
                 hDown_ = sanitize_hist(hDown_,   f"{samp}:{hPathDown}");   hDown_.Sumw2() if hDown_ and not hDown_.GetSumw2N() else None
            # Sumw2 & prune (variations always exist now)
            #if not hUncorr_.GetSumw2N(): hUncorr_.Sumw2()
            for h_ in (hCorr_, hUp_, hDown_):
                if h_ and not h_.GetSumw2N(): h_.Sumw2()

            # If we didn't drop, prune; if we did drop they're zeros already
            if not drop_vars:
                hCorr_ = prune_outliers_relative(hCorr_, hUncorr_, factor=50.0, abs_cap=1e9, tag=f"{samp}:Corr")
                hUp_   = prune_outliers_relative(hUp_,   hUncorr_, factor=50.0, abs_cap=1e9, tag=f"{samp}:Up")
                hDown_ = prune_outliers_relative(hDown_, hUncorr_, factor=50.0, abs_cap=1e9, tag=f"{samp}:Down")
                # Looser for Up, stricter for Down
                #hUp_   = prune_by_ratio(hUp_,   hUncorr_, rmax=10.0, rmin=0.01, min_ref=1.0, tag=f"{samp}:Up")
                #hDown_ = prune_by_ratio(hDown_, hUncorr_, rmax=5.0,  rmin=0.0,  min_ref=3.0, tag=f"{samp}:Down")

            # Accumulate
            if first:
                _ = getSystUnc(hUp_, hCorr_, hDown_, samp, True)
                hUncorr = hUncorr_.Clone("Bkgs_Uncorr"); hUncorr.Sumw2()
                hCorr   = hCorr_.Clone("Bkgs_Corr");     hCorr.Sumw2()
                hUp     = hUp_.Clone("Bkgs_CorrUp");     hUp.Sumw2()
                hDown   = hDown_.Clone("Bkgs_CorrDown"); hDown.Sumw2()
                first = False
            else:
                _ = getSystUnc(hUp_, hCorr_, hDown_, samp)
                hUncorr.Add(hUncorr_)
                hCorr.Add(hCorr_)
                hUp.Add(hUp_)
                hDown.Add(hDown_)

        #-----------------------------------------
        # Plot
        #-----------------------------------------
        def makePlot(hName, region, systs):
            canvas = TCanvas("Canvas", "Canvas", 600, 750)
            if isData and isRatio:
                canvas.Divide(1, 3)
                canvas.cd(1)
                gPad.SetRightMargin(0.03)
                gPad.SetPad(xPadRange[0],yPadRange1[0],xPadRange[1],yPadRange1[1])
                gPad.SetTopMargin(0.11)
                gPad.SetBottomMargin(padGap)
                gPad.SetLogy(True)
                gPad.RedrawAxis()
            else:
                canvas.cd()

            # Data
            hPathData = "%s/%s/%s/%s"%("data_obs", region, systs[0], hName)
            hData = inFile.Get(hPathData)
            hData = sanitize_hist(hData, f"data_obs:{hPathData}")
            if not hData:
                print("[WARN] Missing data histogram. Skipping plot.")
                return

            evtData   = full_integral(hData)
            evtUncorr = full_integral(hUncorr)
            evtCorr   = full_integral(hCorr)
            evtUp     = full_integral(hUp)
            evtDown   = full_integral(hDown)

            rData = ratio_or_dash(evtData, evtUncorr)
            rCorr = ratio_or_dash(evtCorr, evtUncorr)
            rUp   = ratio_or_dash(evtUp,   evtUncorr)
            rDown = ratio_or_dash(evtDown, evtUncorr)
            print("evtUncorr = %s, rCorr = %s, rUp = %s, rDown = %s"%(evtUncorr, rCorr, rUp, rDown))

            xTitle, yTitle = labelDict[hName], "Events / bin"
            decoHistSyst(hData,   xTitle, yTitle, colData);   hData.SetMarkerStyle(20)
            decoHistSyst(hUncorr, xTitle, yTitle, colUncorr)
            decoHistSyst(hCorr,   xTitle, yTitle, colCorr)
            decoHistSyst(hUp,     xTitle, yTitle, colUp)
            decoHistSyst(hDown,   xTitle, yTitle, colDown)

            hUncorr.Draw("HIST")
            if not is_empty(hCorr):  hCorr.Draw("hist same")
            if not is_empty(hUp):    hUp.Draw("hist same")
            if not is_empty(hDown):  hDown.Draw("hist same")
            hData.Draw("EPsame")

            lumi_13TeV = getLumiLabel(year)
            plotLegend = TLegend(0.45,0.60,0.80,0.88)
            decoLegend(plotLegend, 1, 0.045)
            plotLegend.AddEntry(hData, "Data", "PEL")
            plotLegend.AddEntry(hUncorr,"Bkgs_Uncorrected", "L")
            plotLegend.AddEntry(hUp,   "Bkgs_#color[2]{%s}(%s)"  %(systs[2].replace("Weight_",""), rUp),   "L")
            plotLegend.AddEntry(hCorr, "Bkgs_#color[2]{%s}(%s)"  %(systs[1].replace("Weight_",""), rCorr), "L")
            plotLegend.AddEntry(hDown, "Bkgs_#color[2]{%s}(%s)"  %(systs[3].replace("Weight_",""), rDown), "L")
            plotLegend.Draw()

            hUncorr.SetMaximum(20*max(hData.GetMaximum(), hUncorr.GetMaximum()))
            hUncorr.GetXaxis().SetTitle(xTitle); hUncorr.GetYaxis().SetTitle(yTitle)

            chName   = getChLabel(decay, channel)
            crName   = formatCRString(Regions[region])
            chCRName = "#splitline{#font[42]{%s}}{#font[42]{(%s)}}"%(chName, crName)
            extraText = "#splitline{Preliminary}{%s}"%chCRName
            CMS_lumi(lumi_13TeV, canvas, iPeriod, iPosX, extraText)

            if isData and isRatio:
                # Data/Bkgs
                canvas.cd(2)
                gPad.SetTopMargin(padGap); gPad.SetBottomMargin(padGap); gPad.SetRightMargin(0.03)
                gPad.SetPad(xPadRange[0],yPadRange2[0],xPadRange[1],yPadRange2[1]); gPad.RedrawAxis()

                hRatioUncorr = safe_divide(hData, hUncorr, "hRatioUnCorr")
                hRatioCorr   = safe_divide(hData, hCorr,   "hRatioCorr")
                hRatioUp     = safe_divide(hData, hUp,     "hRatioUp")
                hRatioDown   = safe_divide(hData, hDown,   "hRatioDown")

                rLabel = "#frac{Data}{Bkgs}"
                decoHistRatio(hRatioUncorr, xTitle, rLabel, colUncorr)
                decoHistRatio(hRatioCorr,   xTitle, rLabel, colCorr)
                decoHistRatio(hRatioUp,     xTitle, rLabel, colUp)
                decoHistRatio(hRatioDown,   xTitle, rLabel, colDown)

                try:
                    binCons = getContent(hRatioUncorr)+getContent(hRatioCorr)+getContent(hRatioUp)+getContent(hRatioDown)
                    yMin = min(binCons); yMax = max(binCons)
                    if (not math.isfinite(yMin)) or (not math.isfinite(yMax)) or (yMin==yMax):
                        yMin, yMax = 0.8, 1.2
                except Exception:
                    yMin, yMax = 0.8, 1.2
                hRatioUncorr.GetYaxis().SetRangeUser(yMin*(1-0.01), yMax*(1+0.01))
                hRatioUncorr.Draw("HIST")
                hRatioCorr.Draw("hist same")
                hRatioUp.Draw("hist same")
                hRatioDown.Draw("hist same")

                # Corr/Uncorr etc.
                canvas.cd(3)
                gPad.SetTopMargin(padGap); gPad.SetBottomMargin(0.25); gPad.SetRightMargin(0.03)
                gPad.SetPad(xPadRange[0],yPadRange3[0],xPadRange[1],yPadRange3[1]); gPad.RedrawAxis()

                hRatioCorr2  = safe_divide(hCorr,  hUncorr, "hRatioCorr2")
                hRatioUp2    = safe_divide(hUp,    hUncorr, "hRatioUp2")
                hRatioDown2  = safe_divide(hDown,  hUncorr, "hRatioDown2")

                rLabel = "#frac{Bkgs Corrected}{Bkgs Uncorrected}"
                decoHistRatio(hRatioCorr2, xTitle, rLabel, colCorr)
                decoHistRatio(hRatioUp2,   xTitle, rLabel, colUp)
                decoHistRatio(hRatioDown2, xTitle, rLabel, colDown)

                try:
                    binCons = getContent(hRatioCorr2)+getContent(hRatioUp2)+getContent(hRatioDown2)
                    yMin = min(binCons); yMax = max(binCons)
                    if (not math.isfinite(yMin)) or (not math.isfinite(yMax)) or (yMin==yMax):
                        yMin, yMax = 0.8, 1.2
                except Exception:
                    yMin, yMax = 0.8, 1.2
                hRatioCorr2.GetYaxis().SetRangeUser(yMin*(1-0.01), yMax*(1+0.01))
                hRatioCorr2.Draw("HIST")
                hRatioUp2.Draw("hist same")
                hRatioDown2.Draw("hist same")

                baseLine = TF1("baseLine","1", -100, 10000)
                baseLine.SetLineColor(colData)
                # baseLine.Draw("SAME")

            pdf = "%s/overlaySyst_%s_%s.pdf"%(outPlotDir, hName, systKey)
            canvas.SaveAs(pdf); fPath.write("%s\n"%pdf)

        makePlot(hName, region, systs)

print(fPath)

