#----------------------------------------
# Make covariance matrix
#----------------------------------------
import ROOT
from array import array
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-d", "--dirDC", dest="dirDC", default="",type='str',
                     help="dir of fitDiag.root file" )
parser.add_option(
    '--cms-sub', default='Internal', help="""Text below the CMS logo""")
parser.add_option(
    '--title-right', default='', help="""Right header text above the frame""")
parser.add_option(
    '--title-left', default='', help="""Left header text above the frame""")
(options, args) = parser.parse_args()
dirDC           = options.dirDC

myTit = "%s, %s, %s"%(options.title_left, options.title_right, options.cms_sub)

ROOT.gROOT.SetBatch(True)
Red    = [ 1.00, 0.00, 0.00, 0.87, 1.00, 0.51 ]
Green  = [ 1.00, 0.00, 0.81, 1.00, 0.20, 0.00 ]
Blue   = [ 1.00, 0.51, 1.00, 0.12, 0.00, 0.00 ]
Length = [ 0.00, 0.02, 0.34, 0.51, 0.64, 1.00 ]
lengthArray = array('d', Length)
redArray = array('d', Red)
greenArray = array('d', Green)
blueArray = array('d', Blue)

ROOT.TColor.CreateGradientColorTable(6,lengthArray,redArray,greenArray,blueArray,99)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaintTextFormat('5.1f');
canvas = ROOT.TCanvas()
canvas.Divide(2,1)
canvas.SetFillColor(10);
canvas.SetBorderMode(0);
canvas.SetBorderSize(0);
canvas.SetTickx();
canvas.SetTicky();
canvas.SetLeftMargin(0.15);
canvas.SetRightMargin(0.15);
canvas.SetTopMargin(0.15);
canvas.SetBottomMargin(0.15);
canvas.SetFrameFillColor(0);
canvas.SetFrameBorderMode(0);

showNPs = 30
f1 = ROOT.TFile.Open('%s/fitDiagnosticsTest.root'%(dirDC),'read')
def getPlot(name):
    h = f1.Get(name)
    h.SetTitle("#splitline{%s}{%s}"%(name, myTit))
    h.GetYaxis().SetLabelSize(0.02)
    h.GetXaxis().SetLabelSize(0.02)
    h.GetZaxis().SetLabelSize(0.02)
    h.SetMarkerSize(0.7)
    h.LabelsOption("v", "X")
    h.SetContour(99)
    bins = h.GetNbinsX()
    print(bins)
    h.GetXaxis().SetRangeUser(0, showNPs)
    h.GetYaxis().SetRangeUser(bins-showNPs, bins)
    pale = h.GetListOfFunctions().FindObject('palette')
    pale.SetX1NDC(0.02);
    pale.SetX2NDC(0.06);
    pale.SetY1NDC(0.1);
    pale.SetY2NDC(0.9);
    return h

hSig = getPlot("covariance_fit_s")
hBkg = getPlot("covariance_fit_b")
canvas.cd(1)
hSig.Draw('colz, Y+, TEXT0')
canvas.cd(2)
hBkg.Draw('colz, Y+, TEXT0')

#canvas.Modified();
#canvas.Update();
#ROOT.gApplication.Run()
canvas.SaveAs('%s/covarianceMatrix.pdf'%dirDC) 

