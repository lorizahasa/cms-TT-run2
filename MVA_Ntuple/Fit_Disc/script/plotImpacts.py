#!/usr/bin/env python
import ROOT
import math
import json
import argparse
import CombineHarvester.CombineTools.plotting as plot
import CombineHarvester.CombineTools.combine.rounding as rounding
from decimal import Decimal

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.AddDirectory(0)

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='input json file')
parser.add_argument('--output', '-o', help='name of the output file to create')
parser.add_argument('--translate', '-t', help='JSON file for remapping of parameter names')
parser.add_argument('--units', default=None, help='Add units to the best-fit parameter value')
parser.add_argument('--per-page', type=int, default=60, help='Number of parameters to show per page')
parser.add_argument('--cms-label', default='Internal', help='Label next to the CMS logo')
parser.add_argument(
    '--cms-sub', default='Internal', help="""Text below the CMS logo""")
parser.add_argument(
    '--title-right', default='', help="""Right header text above the frame""")
parser.add_argument(
    '--title-left', default='', help="""Left header text above the frame""")
parser.add_argument('--transparent', action='store_true', help='Draw areas as hatched lines instead of solid')
parser.add_argument('--checkboxes', action='store_true', help='Draw an extra panel with filled checkboxes')
parser.add_argument('--blind', action='store_true', help='Do not print best fit signal strength')
parser.add_argument('--color-groups', default=None, help='Comma separated list of GROUP=COLOR')
parser.add_argument("--pullDef",  default=None, help="Choose the definition of the pull, see HiggsAnalysis/CombinedLimit/python/calculate_pulls.py for options")
parser.add_argument('--POI', default=None, help='Specify a POI to draw')
args = parser.parse_args()

myTit = "#splitline{%s, %s}{%s}"%(args.title_left, args.title_right, args.cms_sub)
if args.transparent:
    print('plotImpacts.py: --transparent is now always enabled, the option will be removed in a future update')

externalPullDef = False
if args.pullDef is not None:
    externalPullDef = True
    import HiggsAnalysis.CombinedLimit.calculate_pulls as CP


def Translate(name, ndict):
    return ndict[name] if name in ndict else name


def GetRounded(nom, e_hi, e_lo):
    if e_hi < 0.0:
        e_hi = 0.0
    if e_lo < 0.0:
        e_lo = 0.0
    rounded = rounding.PDGRoundAsym(nom, e_hi if e_hi != 0.0 else 1.0, e_lo if e_lo != 0.0 else 1.0)
    s_nom = rounding.downgradePrec(rounded[0],rounded[2])
    s_hi = rounding.downgradePrec(rounded[1][0][0],rounded[2]) if e_hi != 0.0 else '0'
    s_lo = rounding.downgradePrec(rounded[1][0][1],rounded[2]) if e_lo != 0.0 else '0'
    return (s_nom, s_hi, s_lo)

# Dictionary to translate parameter names
translate = {}
if args.translate is not None:
    with open(args.translate) as jsonfile:
        translate = json.load(jsonfile)

# Load the json output of combineTool.py -M Impacts
data = {}
with open(args.input) as jsonfile:
    data = json.load(jsonfile)

# Set the global plotting style
plot.ModTDRStyle(l=0.4, b=0.10, width=(900 if args.checkboxes else 700))

# We will assume the first POI is the one to plot
POIs = [ele['name'] for ele in data['POIs']]
POI = POIs[0]
if args.POI:
    POI = args.POI

for ele in data['POIs']:
    if ele['name'] == POI:
        POI_info = ele
        break

POI_fit = POI_info['fit']

# Sort parameters by largest absolute impact on this POI
data['params'].sort(key=lambda x: abs(x['impact_%s' % POI]), reverse=True)

if args.checkboxes:
    cboxes = data['checkboxes']

# Set the number of parameters per page (show) and the number of pages (n)
show = args.per_page
n = int(math.ceil(float(len(data['params'])) / float(show)))

colors = {
    'Gaussian': 1,
    'Poisson': 8,
    'AsymmetricGaussian': 9,
    'Unconstrained': 39,
    'Unrecognised': 2
}
color_hists = {}
color_group_hists = {}

if args.color_groups is not None:
    color_groups = {
        x.split('=')[0]: int(x.split('=')[1]) for x in args.color_groups.split(',')
    }

seen_types = set()

for name, col in colors.items():
    color_hists[name] = ROOT.TH1F()
    plot.Set(color_hists[name], FillColor=col, Title=name)

if args.color_groups is not None:
    for name, col in color_groups.iteritems():
        color_group_hists[name] = ROOT.TH1F()
        plot.Set(color_group_hists[name], FillColor=col, Title=name)

for page in range(n):
    canv = ROOT.TCanvas("nuisanceImpact", "nuisanceImpact", 1600, 1800)
    #canv = ROOT.TCanvas(args.output, args.output, 1600, 1800)
    n_params = len(data['params'][show * page:show * (page + 1)])
    pdata = data['params'][show * page:show * (page + 1)]
    print('>> Doing page %i, have %i parameters' % (page, n_params))

    boxes = []
    for i in range(n_params):
        y1 = ROOT.gStyle.GetPadBottomMargin()
        y2 = 1. - ROOT.gStyle.GetPadTopMargin()
        h = (y2 - y1) / float(n_params)
        y1 = y1 + float(i) * h
        y2 = y1 + h
        box = ROOT.TPaveText(0, y1, 1-0.08, y2, 'NDC') #rverma
        ##box = ROOT.TPaveText(0, y1, 1, y2, 'NDC')
        plot.Set(box, TextSize=0.015, BorderSize=0, FillColor=0, TextAlign=12, Margin=0.005)
        if i % 2 == 0:
            box.SetFillColor(18)
        box.AddText('%i' % (n_params - i + page * show))
        box.Draw()
        boxes.append(box)

    # Crate and style the pads
    if args.checkboxes:
        pads = plot.MultiRatioSplitColumns([0.54, 0.24], [0., 0.], [0., 0.])
        pads[2].SetGrid(1, 0)
    else:
        pads = plot.MultiRatioSplitColumns([0.7], [0.], [0.])
    pads[0].SetGrid(1, 0)
    pads[0].SetTickx(1)
    pads[1].SetGrid(1, 0)
    pads[1].SetTickx(1)

    h_pulls = ROOT.TH2F("pulls", "pulls", 6, -2.9, 2.9, n_params, 0, n_params)
    g_pulls = ROOT.TGraphAsymmErrors(n_params)
    g_impacts_hi = ROOT.TGraphAsymmErrors(n_params)
    g_impacts_lo = ROOT.TGraphAsymmErrors(n_params)
    g_check = ROOT.TGraphAsymmErrors()
    g_check_i = 0

    max_impact = 0.
    text_entries = []
    text_entries_3sigma = []
    redo_boxes = []
    for p in range(n_params):
        i = n_params - (p + 1)
        pre = pdata[p]['prefit']
        fit = pdata[p]['fit']
        r   = pdata[p]['r']
        impact_r = pdata[p]['impact_r']
        unc = (r[0]-r[1],r[2]-r[1])
        tp  = pdata[p]['type']
        seen_types.add(tp)
        if pdata[p]['type'] != 'Unconstrained':
            pre_err_hi = (pre[2] - pre[1])
            pre_err_lo = (pre[1] - pre[0])

            if externalPullDef:
                fit_err_hi = (fit[2] - fit[1])
                fit_err_lo = (fit[1] - fit[0])
                pull, pull_hi, pull_lo = CP.returnPullAsym(args.pullDef,fit[1],pre[1],fit_err_hi,pre_err_hi,fit_err_lo,pre_err_lo)
            else:
                pull = fit[1] - pre[1]
                pull = (pull/pre_err_hi) if pull >= 0 else (pull/pre_err_lo)
                pull_hi = fit[2] - pre[1]
                pull_hi = (pull_hi/pre_err_hi) if pull_hi >= 0 else (pull_hi/pre_err_lo)
                pull_hi = pull_hi - pull
                pull_lo = fit[0] - pre[1]
                pull_lo = (pull_lo/pre_err_hi) if pull_lo >= 0 else (pull_lo/pre_err_lo)
                pull_lo =  pull - pull_lo

            g_pulls.SetPoint(i, pull, float(i) + 0.5)
            nuisName = Translate(pdata[p]['name'],translate)
            #print('%s\t %f \t %f \t %f' % (nuisName, fit[0], fit[1], fit[2]))
            print('%20s\t %10f \t %10f \t %10f' % (nuisName, impact_r, max(unc), min(unc)))
            if(abs(pull) >2):
                if("prop" in nuisName):
                    chName = nuisName.split("_")[1].replace("bin", "")
                    binName = nuisName.split("_")[2].replace("bin", "")
                    #print('%s\t %s\t %s\t %f \t %f \t %f' % (nuisName, chName, binName, pull_lo, pull, pull_hi))
                else:
                    print("-----------------------------")
                    print('%s\t %f \t %f \t %f' % (nuisName, fit[0], fit[1], fit[2]))
                    print("-----------------------------")
            g_pulls.SetPointError( i, pull_lo, pull_hi, 0., 0.)
            #Put a text on points not shown in the graph
            if(abs(pull) >3):
                y1 = ROOT.gStyle.GetPadBottomMargin()
                y2 = 1. - ROOT.gStyle.GetPadTopMargin()
                x1 = ROOT.gStyle.GetPadLeftMargin()
                h = (y2 - y1) / float(n_params)
                y1 = y1 + ((float(i)+0.5) * h)
                x1 = x1 + (1 - pads[0].GetRightMargin() -x1)/2.
                s_nom, s_hi, s_lo = GetRounded(fit[1], fit[2] - fit[1], fit[1] - fit[0])
                s_nom_rounded ='%.1E' % Decimal(s_nom)
                s_hi_rounded = '%.1E' % Decimal(s_hi)
                s_lo_rounded = '%.1E' % Decimal(s_lo)
                text_entries_3sigma.append((x1, y1, '%s^{#plus%s}_{#minus%s}' % (s_nom_rounded, s_hi_rounded, s_lo_rounded)))
        else:
            # Hide this point
            g_pulls.SetPoint(i, 0., 9999.)
            y1 = ROOT.gStyle.GetPadBottomMargin()
            y2 = 1. - ROOT.gStyle.GetPadTopMargin()
            x1 = ROOT.gStyle.GetPadLeftMargin()
            h = (y2 - y1) / float(n_params)
            y1 = y1 + ((float(i)+0.5) * h)
            x1 = x1 + (1 - pads[0].GetRightMargin() -x1)/2.
            s_nom, s_hi, s_lo = GetRounded(fit[1], fit[2] - fit[1], fit[1] - fit[0])
            s_nom_rounded ='%.1E' % Decimal(s_nom)
            s_hi_rounded = '%.1E' % Decimal(s_hi)
            s_lo_rounded = '%.1E' % Decimal(s_lo)
            text_entries.append((x1, y1, '%s^{#plus%s}_{#minus%s}' % (s_nom_rounded, s_hi_rounded, s_lo_rounded)))
            redo_boxes.append(i)
        g_impacts_hi.SetPoint(i, 0, float(i) + 0.5)
        g_impacts_lo.SetPoint(i, 0, float(i) + 0.5)
        if args.checkboxes:
            pboxes = pdata[p]['checkboxes']
            for pbox in pboxes:
                cboxes.index(pbox)
                g_check.SetPoint(g_check_i, cboxes.index(pbox) + 0.5, float(i) + 0.5)
                g_check_i += 1
        imp = pdata[p][POI]
        g_impacts_hi.SetPointError(i, 0, imp[2] - imp[1], 0.5, 0.5)
        g_impacts_lo.SetPointError(i, imp[1] - imp[0], 0, 0.5, 0.5)
        max_impact = max(
            max_impact, abs(imp[1] - imp[0]), abs(imp[2] - imp[1]))
        col = colors.get(tp, 2)
        if args.color_groups is not None and len(pdata[p]['groups']) == 1:
            col = color_groups.get(pdata[p]['groups'][0], 1)
        h_pulls.GetYaxis().SetBinLabel(
            i + 1, ('#color[%i]{%s}'% (col, Translate(pdata[p]['name'], translate))))

    # Style and draw the pulls histo
    if externalPullDef:
        plot.Set(h_pulls.GetXaxis(), TitleSize=0.04, LabelSize=0.03, Title=CP.returnTitle(args.pullDef))
    else:
        plot.Set(h_pulls.GetXaxis(), TitleSize=0.04, LabelSize=0.03, Title='(#hat{#theta}-#theta_{0})/#Delta#theta')

    plot.Set(h_pulls.GetYaxis(), LabelSize=0.021, TickLength=0.0)
    h_pulls.GetYaxis().LabelsOption('v')
    h_pulls.Draw()

    for i in redo_boxes:
        newbox = boxes[i].Clone()
        newbox.Clear()
        newbox.SetY1(newbox.GetY1()+0.005)
        newbox.SetY2(newbox.GetY2()-0.005)
        newbox.SetX1(ROOT.gStyle.GetPadLeftMargin()+0.001)
        newbox.SetX2(0.7-0.001)
        newbox.Draw()
        boxes.append(newbox)
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.SetTextSize(0.02)
    latex.SetTextAlign(22)
    for entry in text_entries:
        latex.DrawLatex(*entry)

    # Go to the other pad and draw the impacts histo
    pads[1].cd()
    ROOT.gPad.SetRightMargin(0.08)
    if max_impact == 0.: max_impact = 1E-6  # otherwise the plotting gets screwed up
    h_impacts = ROOT.TH2F(
        "impacts", "impacts", 6, -max_impact * 1.1, max_impact * 1.1, n_params, 0, n_params)
    plot.Set(h_impacts.GetXaxis(), LabelSize=0.03, TitleSize=0.04, Ndivisions=505, Title=
        '#Delta#hat{%s}' % (Translate(POI, translate)))
    plot.Set(h_impacts.GetYaxis(), LabelSize=0, TickLength=0.0)
    h_impacts.Draw()

    if args.checkboxes:
        pads[2].cd()
        h_checkboxes = ROOT.TH2F(
            "checkboxes", "checkboxes", len(cboxes), 0, len(cboxes), n_params, 0, n_params)
        for i, cbox in enumerate(cboxes):
            h_checkboxes.GetXaxis().SetBinLabel(i+1, Translate(cbox, translate))
        plot.Set(h_checkboxes.GetXaxis(), LabelSize=0.03, LabelOffset=0.002)
        h_checkboxes.GetXaxis().LabelsOption('v')
        plot.Set(h_checkboxes.GetYaxis(), LabelSize=0, TickLength=0.0)
        h_checkboxes.Draw()
        # g_check.SetFillColor(ROOT.kGreen)
        g_check.Draw('PSAME')

    # Back to the first pad to draw the pulls graph
    pads[0].cd()
    #prefit band from -1 to +1
    box_prefit = ROOT.TBox()
    box_prefit.SetLineColor(25)
    box_prefit.SetFillColor(25)
    box_prefit.DrawBox(-1, 0, +1, n_params)
    for entry in text_entries_3sigma:
        latex.DrawLatex(*entry)

    plot.Set(g_pulls, MarkerSize=1.5, LineWidth=2)
    g_pulls.Draw('PSAME')

    # And back to the second pad to draw the impacts graphs
    pads[1].cd()
    alpha = 0.7

    lo_color = {
        'default': 38,
        'hesse': ROOT.kOrange - 3,
        'robust': ROOT.kGreen + 1
    }
    hi_color = {
        'default': 46,
        'hesse': ROOT.kBlue,
        'robust': ROOT.kAzure - 5
    }
    method = 'default'
    if 'method' in data and data['method'] in lo_color:
        method = data['method']
    g_impacts_hi.SetFillColor(plot.CreateTransparentColor(hi_color[method], alpha))
    g_impacts_hi.Draw('2SAME')
    g_impacts_lo.SetFillColor(plot.CreateTransparentColor(lo_color[method], alpha))
    g_impacts_lo.Draw('2SAME')
    pads[1].RedrawAxis()

    legend = ROOT.TLegend(0.02, 0.02, 0.40, 0.06, '', 'NBNDC')
    legend.SetNColumns(3)
    legend.AddEntry(g_pulls, 'Pull', 'LP')
    legend.AddEntry(g_impacts_hi, '+1#sigma Impact', 'F')
    legend.AddEntry(g_impacts_lo, '-1#sigma Impact', 'F')
    legend.Draw()

    leg_width = pads[0].GetLeftMargin() - 0.01
    if args.color_groups is not None:
        legend2 = ROOT.TLegend(0.01, 0.94, leg_width, 0.99, '', 'NBNDC')
        legend2.SetNColumns(2)
        for name, h in color_group_hists.iteritems():
            legend2.AddEntry(h, Translate(name, translate), 'F')
        legend2.Draw()
    elif len(seen_types) > 1:
        legend2 = ROOT.TLegend(0.01, 0.94, leg_width, 0.99, '', 'NBNDC')
        legend2.SetNColumns(2)
        for name, h in color_hists.iteritems():
            if name == 'Unrecognised': continue
            legend2.AddEntry(h, name, 'F')
        legend2.Draw()

    plot.DrawCMSLogo(pads[0], 'CMS', args.cms_label, 0, 0.25, 0.00, 0.00)
    s_nom, s_hi, s_lo = GetRounded(POI_fit[1], POI_fit[2] - POI_fit[1], POI_fit[1] - POI_fit[0])
    latex2 = ROOT.TLatex()
    latex2.SetNDC()
    latex2.SetTextFont(42)
    latex2.SetTextSize(0.025)
    latex2.SetTextAlign(22)
    latex2.DrawLatex(0.15, 0.96, myTit)
    if not args.blind:
        s_nom_rounded ='%.1E' % Decimal(s_nom)
        s_hi_rounded = '%.1E' % Decimal(s_hi)
        s_lo_rounded = '%.1E' % Decimal(s_lo)
        plot.DrawTitle(pads[1], '#hat{%s} = %s^{#plus%s}_{#minus%s}%s' % (
            Translate(POI, translate), s_nom_rounded, s_hi_rounded, s_lo_rounded,
            '' if args.units is None else ' '+args.units), 3, 0.27)
    extra = ''
    if page == 0:
        extra = '('
    if page == n - 1:
        extra = ')'
    canv.Print('%s%s' %(args.output, extra))
