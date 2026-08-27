#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
import ctypes
import ROOT
import CombineHarvester.CombineTools.plotting as plot
import argparse
from array import array
import os
import sys
sys.path.insert(0, os.getcwd().replace("condor", ""))
sys.path.insert(0, os.getcwd().replace("Fit_Disc/condor", "Disc_Ntuple"))
sys.path.insert(0, os.getcwd().replace("MVA_Ntuple/Fit_Disc/condor", "CBA_Ntuple/Plot_Hist"))
import json
import itertools
from PlotCMSLumi import *
from PlotTDRStyle import *
from PlotFunc import *
from array import array
from FitInputs import *
from optparse import OptionParser
from DiscInputs import methodDict
# import CombineHarvester.CombineTools.maketable as maketable
import ctypes
from math import isfinite

parser = argparse.ArgumentParser()
parser.add_argument(
    '--output', '-o', default='limit', help="""Name of the output
    plot without file extension""")
parser.add_argument(
    '--show', default='exp')
    #'--show', default='exp,obs')
# parser.add_argument(
#     '--debug-output', '-d', help="""If specified, write the
#     TGraphs into this output ROOT file""")
parser.add_argument(
    '--x-title', default='m_{T} (GeV)', help="""Title for the x-axis""")
parser.add_argument(
    '--y-title', default=None, help="""Title for the y-axis""")
parser.add_argument(
    #'--limit-on', default='#sigma_{t*#bar{t*}} B(t* #rightarrow t#gamma)B(#bar{t*} #rightarrow #bar{t}g) [pb]', help="""Shortcut for setting the y-axis label""")
    '--limit-on', default='#sigma(pp #rightarrow T#bar{T} #rightarrow Tg#bar{T}#gamma) [pb]', help="""Shortcut for setting the y-axis label""")
parser.add_argument(
    '--cms-sub', default='Internal', help="""Text below the CMS logo""")
parser.add_argument(
    '--scenario-label', default='sssss', help="""Scenario name to be drawn in top
    left of plot""")
parser.add_argument(
    '--title-right', default='', help="""Right header text above the frame""")
parser.add_argument(
    '--title-left', default='', help="""Left header text above the frame""")
parser.add_argument(
    '--logy', action='store_true', default=True, help="""Draw y-axis in log scale""")
parser.add_argument(
    '--logx', action='store_true', help="""Draw x-axis in log scale""")
parser.add_argument(
    '--ratio-to', default=None)
parser.add_argument(
    '--pad-style', default=None, help="""Extra style options for the pad, e.g. Grid=(1,1)""")
parser.add_argument(
    '--auto-style', nargs='?', const='', default=None, help="""Take line colors and styles from a pre-defined list""")
parser.add_argument('--table_vals', help='Amount of values to be written in a table for different masses', default=10)
parser.add_argument("--isCheck",action="store_true",default=False, help="Check for minimum inputs")
parser.add_argument("--isSep",action="store_true",default=False, help="Merge for separate years and channels")
args = parser.parse_args()

regionList = list(rDict.keys())
if args.isCheck:
    Year  = [Year[0]]
    Decay = [Decay[0]]
    Spin = [Spin[0]]
    Channel = [Channel[0]]
    regionList  = [regionList[0]]
if not args.isCheck and not args.isSep:
    print("Add either --isCheck or --isSep in the command line")
    exit()

def getRegLabel(region):
    reg = "Resolved"
    if 'Boosted' in region:
        reg = "Boosted"
    if 'Resolved' in region:
        reg = "Resolved"
    if 'Resolved' in region and "Boosted" in region:
        reg = "Resolved + Boosted"
    return reg

def DrawAxisHists(pads, axis_hists, def_pad=None):
    for i, pad in enumerate(pads):
        pad.cd()
        axis_hists[i].Draw('AXIS')
        axis_hists[i].Draw('AXIGSAME')
    if def_pad is not None:
        def_pad.cd()

def pretty_spin(spin_str):
    s = str(spin_str)
    if '32' in s: return 'Spin-3/2 T'
    if '12' in s: return 'Spin-1/2 T'
    return s

def _graph_points(gr): 
    xs, ys = [], []
    n = gr.GetN()
    x = ctypes.c_double(); y = ctypes.c_double()
    for i in range(n):
        gr.GetPoint(i, x, y)
        xs.append(float(x.value)); ys.append(float(y.value))
    # ensure sorted by x (ROOT graphs aren?~@~Yt guaranteed sorted)
    order = sorted(range(n), key=lambda i: xs[i])
    xs = [xs[i] for i in order]; ys = [ys[i] for i in order]
    return xs, ys 
def _interp_linear(xs, ys, xq):
    # piecewise-linear interpolation; returns None if xq is out of range
    if xq < xs[0] or xq > xs[-1]:
        return None
    # binary search for segment
    lo, hi = 0, len(xs)-1
    while hi - lo > 1:
        mid = (lo + hi)//2
        if xs[mid] <= xq: lo = mid
        else: hi = mid
    x0, x1 = xs[lo], xs[hi]
    y0, y1 = ys[lo], ys[hi]
    if x1 == x0:  # degenerate
        return y0 if isfinite(y0) else None
    t = (xq - x0) / (x1 - x0)
    return y0 + t*(y1 - y0)
def find_intersections(exp_graph, th_graph):
    ex, ey = _graph_points(exp_graph)
    tx, ty = _graph_points(th_graph)

    # scan across the expected-graph segments; look for sign changes of f = (exp - theory)
    xs_cross, ys_cross = [], []
    for i in range(len(ex)-1):
        x0, x1 = ex[i], ex[i+1]
        # interpolate theory at the segment endpoints
        th0 = _interp_linear(tx, ty, x0)
        th1 = _interp_linear(tx, ty, x1)
        if th0 is None or th1 is None:
            continue
        f0 = ey[i]   - th0
        f1 = ey[i+1] - th1
        if f0 == 0:     # exact hit at endpoint
            xs_cross.append(x0); ys_cross.append(ey[i]); 
        if f1 == 0:
            xs_cross.append(x1); ys_cross.append(ey[i+1])
        # sign change => one crossing in (x0, x1)
        if f0 * f1 < 0:
            # linear solve: f(x) = f0 + (f1-f0)*t = 0
            t = f0 / (f0 - f1)
            xc = x0 + t*(x1 - x0)
            yc = ey[i] + t*(ey[i+1] - ey[i])  # or interpolate theory; both equal at crossing
            xs_cross.append(xc); ys_cross.append(yc)
    # de-duplicate near-identical endpoints
    out = []
    for xc, yc in zip(xs_cross, ys_cross):
        if not out or abs(xc - out[-1][0]) > 1e-9:
            out.append((xc, yc))
    return out

# --- after you have graph_sets_this_combo (unscaled limits) and xss (theory pb by mass) ---

def graph_divide_by_theory(exp_graph, xss_dict):
    # returns a new TGraph of (exp(pb)/theory(pb)) vs mass
    xs, ys = _graph_points(exp_graph)  # you already have this helper
    out = ROOT.TGraph()
    j = 0
    for x, y in zip(xs, ys):
        # robust theory lookup (keys can be "1000.0" vs 1000)
        th = None
        if x in xss_dict:
            th = xss_dict[x]
        elif int(x) in xss_dict:
            th = xss_dict[int(x)]
        else:
            # nearest mass match
            km, th = min(((mk, xv) for mk, xv in xss_dict.items()),
                         key=lambda t: abs(float(t[0]) - x))
        if th and th > 0:
            out.SetPoint(j, x, y / th)
            j += 1
    return out

def find_horizontal_intersections(gr, y0=1.0):
    xs, ys = _graph_points(gr)
    hits = []
    for i in range(len(xs)-1):
        f0 = ys[i]   - y0
        f1 = ys[i+1] - y0
        if f0 == 0:
            hits.append((xs[i], y0))
        if f1 == 0:
            hits.append((xs[i+1], y0))
        if f0 * f1 < 0:  # sign change
            t  = f0 / (f0 - f1)
            xc = xs[i] + t*(xs[i+1] - xs[i])
            hits.append((xc, y0))
    return hits
#----------------------------------------
#Path of the I/O histrograms/plots
#----------------------------------------
fPath = open("%s/plotLimit.txt"%dirFit, 'w')
hName = 'Disc'
#dirFit2 ="/uscms/home/lhasa/nobackup/TTPrime/CMSSW_14_0_0/src/cms-TT-run2/MVA_Ntuple/Fit_Disc/output/Fit_Disc/FitMain"
#hName = 'Reco_mass_T'
for decay, region, spin, channel, year in itertools.product(Decay, regionList, Spin, Channel, Year):
    limits = "tex/allLimits.json"
    gDict = {}
    limDict={}
    ydsc = "%s/%s/%s/%s"%(year, decay, spin, channel)
    #ydsc = "%s/%s/%s/%s"%(year, decay, spin, channel)
    path = "%s/%s"%(dirFit, ydsc) 
    outPath = "%s/%s/%s"%(path, region, hName)
    os.system('mkdir -p %s'%outPath)
    jsonRaw = "%s/limits.json"%outPath
    jsonScaled = "%s/scaled_limits.json"%outPath

    args.title_right = getLumiLabel(year)
    args.title_left  = getChLabel(decay, channel)
    args.cms_sub     = getRegLabel(region) 

    allFiles = "%s/*/BDTA/%s/%s/higgsCombine_TT_run2.AsymptoticLimits.mH*.root"%(path, region, hName) 
    os.system("combineTool.py -M CollectLimits %s -o %s"%(allFiles, jsonRaw))
    with open(jsonRaw) as old_limit:
        new_limit = json.load(old_limit)
        
        #if '2500.0' in new_limit:
         #   del new_limit['2500.0']
        #if '1700.0' in new_limit:
         #   del new_limit['1700.0']
        #if '1600.0' in new_limit:
         #   del new_limit['1600.0']
        #if '2750.0' in new_limit:
        #    del new_limit['2750.0']
        if args.isCheck:
            print("OLD: ", new_limit)
        for mass in list(xss.keys()):
            for limit in new_limit[mass]:
                pass
                #new_limit[mass][limit] = xss[mass]*new_limit[mass][limit]
    with open (jsonScaled, 'w') as newLimitFile:
        if args.isCheck:
            print("\nNEW: ", new_limit)
        json.dump(new_limit, newLimitFile)

    ## Boilerplate
    ROOT.PyConfig.IgnoreCommandLineOptions = True
    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    plot.ModTDRStyle()
    ROOT.gStyle.SetNdivisions(510, 'XYZ') # probably looks better

    #canv = ROOT.TCanvas(args.output, args.output)
    canv = ROOT.TCanvas()

    if args.ratio_to is not None:
        pads = plot.TwoPadSplit(0.30, 0.01, 0.01)
    else:
        pads = plot.OnePad()

    # Set the style options of the pads
    for padx in pads:
        # Use tick marks on oppsite axis edges
        plot.Set(padx, Tickx=1, Ticky=1, Logx=args.logx)
        if args.pad_style is not None:
            settings = {x.split('=')[0]: eval(x.split('=')[1]) for x in args.pad_style.split(',')}
            print('Applying style options to the TPad(s):')
            print(settings)
            plot.Set(padx, **settings)

    graphs = []
    graph_sets = []

    legend = plot.PositionedLegend(0.45, 0.10, 3, 0.015)
    plot.Set(legend, NColumns=2)
   
    legend.SetHeader(pretty_spin(spin), "L")

    axis = None
    green = ROOT.TColor.GetColor("#607641")  # green
    gold  = ROOT.TColor.GetColor("#F5BB54")  # gold

    defcols = [
        green, ROOT.kRed, ROOT.kBlue, ROOT.kBlack, gold,
        ROOT.kOrange+10, ROOT.kCyan+3, ROOT.kMagenta+2, ROOT.kViolet-5, ROOT.kGray
        ]

    deflines = [1, 2, 3]

    if args.auto_style is not None:
        icol = {x: 0 for x in args.auto_style.split(',')}
        icol['default'] = 0
        iline = {}
        iline['default'] = 1
        for i, x in enumerate(args.auto_style.split(',')):
            iline[x] = i+1

    # Process each input argument
    #print args.input
    #for src in args.input:
    print(jsonScaled)
    for src in [jsonScaled]: 
        splitsrc = src.split(':')
        file = splitsrc[0]
        # limit.json => Draw as full obs + exp limit band
        if len(splitsrc) == 1:
            graph_sets.append(plot.StandardLimitsFromJSONFile(file, args.show.split(',')))
            if axis is None:
                #tmp_ = ctypes.c_double()
                axis = plot.CreateAxisHists(len(pads), list(graph_sets[-1].values())[0], True)
                DrawAxisHists(pads, axis, pads[0])
            plot.StyleLimitBand(graph_sets[-1])
            # robustly handle possible key names
            for key, col in [
                ('exp1', green),  # 1σ band
                ('exp2', gold)    # 2σ band
                ]:
                if key in graph_sets[-1]:
                    g = graph_sets[-1][key]
                    # solid fill with your color
                    if hasattr(g, 'SetFillColor'):
                        g.SetFillColor(col)
                    if hasattr(g, 'SetLineColor'):
                        g.SetLineColor(col)
                    if hasattr(g, 'SetMarkerColor'):
                        g.SetMarkerColor(col)
            plot.DrawLimitBand(pads[0], graph_sets[-1], legend=legend)
            for key in ('exp0', 'exp'):
                if key in graph_sets[-1]:
                    graph_sets[-1][key].SetLineColor(ROOT.kBlack)  # or green/gold if you prefer
                    graph_sets[-1][key].SetLineWidth(2)
                    graph_sets[-1][key].SetLineStyle(2)

            #plot.DrawLimitBand(pads[0], graph_sets[-1], legend=legend)
            pads[0].RedrawAxis()
            pads[0].RedrawAxis('g')
            pads[0].GetFrame().Draw()

        # limit.json:X => Draw a single graph for entry X in the json file 
        # 'limit.json:X:Title="Blah",LineColor=4,...' =>
        # as before but also apply style options to TGraph
        elif len(splitsrc) >= 2:
            settings = {}
            settings['Title'] = src
            if args.auto_style is not None:
                nm = 'default'
                for x in icol.keys():
                    if x in splitsrc[1]:
                        nm = x
                i = icol[nm]  # take the next default color...
                j = iline[nm]  # take the next default line style...
                settings['LineColor'] = defcols[i]
                settings['MarkerColor'] = defcols[i]
                settings['LineStyle'] = j
                icol[nm] = (i+1) if (i+1) < len(defcols) else 0
            graphs.append(plot.LimitTGraphFromJSONFile(file, splitsrc[1]))
            if len(splitsrc) >= 3:
                settings.update({x.split('=')[0]: eval(x.split('=')[1]) for x in splitsrc[2].split(',')})
            plot.Set(graphs[-1], **settings)
            if axis is None:
                axis = plot.CreateAxisHists(len(pads), graphs[-1], True)
                DrawAxisHists(pads, axis, pads[0])
            graphs[-1].Draw('PLSAME')
            legend.AddEntry(graphs[-1], '', 'PL')


    #axis[0].GetYaxis().SetTitle('95%% CL limit on %s' % args.limit_on)
    axis[0].GetYaxis().SetTitle('%s' % args.limit_on)
    if args.y_title is not None:
        axis[0].GetYaxis().SetTitle(args.y_title)
    axis[0].GetXaxis().SetTitle(args.x_title)
    axis[0].GetXaxis().SetLabelOffset(axis[0].GetXaxis().GetLabelOffset()*2)

    if args.logy:
        #axis[0].SetMinimum(0.01)  # we'll fix this later
        pads[0].SetLogy(True)
        # axis[0].GetYaxis().SetMoreLogLabels()
        axis[0].GetYaxis().SetRangeUser(0.0001, 1)
        # axis[0].SetNdivisions(50005, "X")

    y_min, y_max = (plot.GetPadYMin(pads[0]), plot.GetPadYMax(pads[0]))
    #plot.FixBothRanges(pads[0], y_min if args.logy else 0, 0.05 if args.logy else 0, y_max, 0.25)

    ratio_graph_sets = []
    ratio_graphs = []

    if args.ratio_to is not None:
        pads[1].cd()
        plot.SetupTwoPadSplitAsRatio(pads, axis[0], axis[1], 'Ratio_{}', True, 0.1, 2.4)
        axis[1].SetNdivisions(506, 'Y')
        splitsrc = args.ratio_to.split(':')
        ref = plot.LimitTGraphFromJSONFile(splitsrc[0], splitsrc[1])
        for gr_set in graph_sets:
            ratio_set = {}
            for key in gr_set:
                ratio_set[key] = plot.GraphDivide(gr_set[key], ref)
            ratio_graph_sets.append(ratio_set)
            plot.DrawLimitBand(pads[1], ratio_graph_sets[-1])
            pads[1].RedrawAxis()
            pads[1].RedrawAxis('g')
            pads[1].GetFrame().Draw()
        for gr in graphs:
            ratio_graphs.append(plot.GraphDivide(gr, ref))
            ratio_graphs[-1].Draw('LP')
        ry_min, ry_max = (plot.GetPadYMin(pads[1]), plot.GetPadYMax(pads[1]))
        plot.FixBothRanges(pads[1], ry_min, 0.1, ry_max, 0.1)


    pads[0].cd()
    if legend.GetNRows() == 1:
        legend.SetY1(legend.GetY2() - 0.5*(legend.GetY2()-legend.GetY1()))
    legend.Draw()

    # line = ROOT.TLine()
    # line.SetLineColor(ROOT.kBlue)
    # line.SetLineWidth(2)
    # plot.DrawHorizontalLine(pads[0], line, 1)

    box = ROOT.TPave(pads[0].GetLeftMargin(), 0.81, 1-pads[0].GetRightMargin(), 1-pads[0].GetTopMargin(), 1, 'NDC')
    box.Draw()

    legend.Draw()

    plot.DrawCMSLogo(pads[0], 'CMS, Prelim.', args.cms_sub, 10.5, 0.2, 0.035, 1.2, '', 0.8)
    #plot.DrawCMSLogo(pads[0], 'CMS, Prelim.', args.cms_sub, 10, 0.2, 0.02, 0.9, '', 1.0)
    plot.DrawTitle(pads[0], args.title_right, 3)
    plot.DrawTitle(pads[0], args.title_left, 1)

    drawTheory = True
    if drawTheory:
        x, y = array( 'd' ), array( 'd' )
        for key in list(xss.keys()):
            x.append(float(key))
        for val in xss.values():
            y.append(val)
        print(x)
        print(y)
        gTheory = ROOT.TGraph(len(x), x, y)
        #gTheory.Draw("ALPsame")
        gTheory.SetLineColor(2)
        gTheory.SetLineWidth(3)
        gTheory.SetMarkerStyle(15);
        gTheory.SetMarkerColor(2);
        gTheory.Draw("Lsame")
        legend.AddEntry(gTheory, "Theory xss", "LP")
        legend.Draw() 
    exp_key = 'exp0' if ('exp0' in graph_sets[-1]) else ('exp' if ('exp' in graph_sets[-1]) else None)
    if exp_key is not None:
        crossings = find_intersections(graph_sets[-1][exp_key], gTheory)
        # 1) make r_model(m) = limit_old(m) / sigma_theory(m)
        #gr_ratio = graph_divide_by_theory(graph_sets[-1][exp_key], xss)

        # 2) find intersections with r=1
       # crossings = find_horizontal_intersections(gr_ratio, y0=1.0)
        if crossings:
            print(f"[{year}/{decay}/{spin}/{channel}/{region}]:")
            for (xm, ym) in crossings:
                print(f"  m ≈ {xm:.0f} GeV, σ ≈ {ym:.3g} pb")
            #for (xm, _) in crossings:
            # optional: also print σ_theory and limit at that mass
              #  th = xss.get(xm, xss.get(int(xm), None))
               # print(f"  m ≈ {xm:.0f} GeV  (σ_theory≈{th:.3g} pb)")   
            else:
                print(f"[{year}/{decay}/{spin}/{channel}/{region}] No intersections in overlap range.")
    else:
        print(f"[{year}/{decay}/{spin}/{channel}/{region}] No expected graph ('exp0' or 'exp').")

    pdf = "%s/plotLimit.pdf"%(outPath)
    canv.SaveAs(pdf)
    fPath.write("%s\n"%pdf)
    #canv.Print('.png')
    # maketable.TablefromJson(args.table_vals, args.file, "TablefromJson.txt")
print(fPath)
