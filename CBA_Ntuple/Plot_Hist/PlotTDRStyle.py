import ROOT as R

def tdrGrid( gridOn):
  tdrStyle.SetPadGridX(gridOn)
  tdrStyle.SetPadGridY(gridOn)

#fixOverlay: Redraws the axis
def fixOverlay(): gPad.RedrawAxis()

def setTDRStyle():
  tdrStyle =  R.TStyle("tdrStyle","Style for P-TDR")

   #for the canvas:
  tdrStyle.SetCanvasBorderMode(0)
  tdrStyle.SetCanvasColor(R.kWhite)
  tdrStyle.SetCanvasDefH(600) #Height of canvas
  tdrStyle.SetCanvasDefW(600) #Width of canvas
  tdrStyle.SetCanvasDefX(0)   #POsition on screen
  tdrStyle.SetCanvasDefY(0)


  tdrStyle.SetPadBorderMode(0)
  #tdrStyle.SetPadBorderSize(Width_t size = 1)
  tdrStyle.SetPadColor(R.kWhite)
  tdrStyle.SetPadGridX(False)
  tdrStyle.SetPadGridY(False)
  tdrStyle.SetGridColor(0)
  tdrStyle.SetGridStyle(3)
  tdrStyle.SetGridWidth(1)

#For the frame:
  tdrStyle.SetFrameBorderMode(0)
  tdrStyle.SetFrameBorderSize(1)
  tdrStyle.SetFrameFillColor(0)
  tdrStyle.SetFrameFillStyle(0)
  tdrStyle.SetFrameLineColor(1)
  tdrStyle.SetFrameLineStyle(1)
  tdrStyle.SetFrameLineWidth(1)
  
#For the histo:
  #tdrStyle.SetHistFillColor(1)
  #tdrStyle.SetHistFillStyle(0)
  tdrStyle.SetHistLineColor(1)
  tdrStyle.SetHistLineStyle(0)
  tdrStyle.SetHistLineWidth(1)
  #tdrStyle.SetLegoInnerR(Float_t rad = 0.5)
  #tdrStyle.SetNumberContours(Int_t number = 20)

  tdrStyle.SetEndErrorSize(2)
  #tdrStyle.SetErrorMarker(20)
  #tdrStyle.SetErrorX(0.)
  
  tdrStyle.SetMarkerStyle(20)
  
#For the fit/function:
  tdrStyle.SetOptFit(1)
  tdrStyle.SetFitFormat("5.4g")
  tdrStyle.SetFuncColor(2)
  tdrStyle.SetFuncStyle(1)
  tdrStyle.SetFuncWidth(1)

#For the date:
  tdrStyle.SetOptDate(0)
  # tdrStyle.SetDateX(Float_t x = 0.01)
  # tdrStyle.SetDateY(Float_t y = 0.01)

# For the statistics box:
  tdrStyle.SetOptFile(0)
  tdrStyle.SetOptStat(0) # To display the mean and RMS:   SetOptStat("mr")
  tdrStyle.SetStatColor(R.kWhite)
  tdrStyle.SetStatFont(42)
  tdrStyle.SetStatFontSize(0.025)
  tdrStyle.SetStatTextColor(1)
  tdrStyle.SetStatFormat("6.4g")
  tdrStyle.SetStatBorderSize(1)
  tdrStyle.SetStatH(0.1)
  tdrStyle.SetStatW(0.15)
  # tdrStyle.SetStatStyle(Style_t style = 1001)
  # tdrStyle.SetStatX(Float_t x = 0)
  # tdrStyle.SetStatY(Float_t y = 0)

# Margins:
  tdrStyle.SetPadTopMargin(0.05)
  tdrStyle.SetPadBottomMargin(0.13)
  tdrStyle.SetPadLeftMargin(0.16)
  tdrStyle.SetPadRightMargin(0.02)

# For the Global title:

  tdrStyle.SetOptTitle(0)
  tdrStyle.SetTitleFont(42)
  tdrStyle.SetTitleColor(1)
  tdrStyle.SetTitleTextColor(1)
  tdrStyle.SetTitleFillColor(10)
  tdrStyle.SetTitleFontSize(0.05)
  # tdrStyle.SetTitleH(0) # Set the height of the title box
  # tdrStyle.SetTitleW(0) # Set the width of the title box
  # tdrStyle.SetTitleX(0) # Set the position of the title box
  # tdrStyle.SetTitleY(0.985) # Set the position of the title box
  # tdrStyle.SetTitleStyle(Style_t style = 1001)
  # tdrStyle.SetTitleBorderSize(2)

# For the axis titles:

  tdrStyle.SetTitleColor(1, "XYZ")
  tdrStyle.SetTitleFont(42, "XYZ")
  tdrStyle.SetTitleSize(0.06, "XYZ")
  # tdrStyle.SetTitleXSize(Float_t size = 0.02) # Another way to set the size?
  # tdrStyle.SetTitleYSize(Float_t size = 0.02)
  tdrStyle.SetTitleXOffset(0.9)
  tdrStyle.SetTitleYOffset(1.25)
  # tdrStyle.SetTitleOffset(1.1, "Y") # Another way to set the Offset

# For the axis labels:

  tdrStyle.SetLabelColor(1, "XYZ")
  tdrStyle.SetLabelFont(42, "XYZ")
  tdrStyle.SetLabelOffset(0.007, "XYZ")
  tdrStyle.SetLabelSize(0.05, "XYZ")

# For the axis:

  tdrStyle.SetAxisColor(1, "XYZ")
  tdrStyle.SetStripDecimals(True)
  tdrStyle.SetTickLength(0.03, "XYZ")
  tdrStyle.SetNdivisions(510, "XYZ")
  tdrStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
  tdrStyle.SetPadTickY(1)

# Change for log plots:
  tdrStyle.SetOptLogx(0)
  tdrStyle.SetOptLogy(0)
  tdrStyle.SetOptLogz(0)

# Postscript options:
  tdrStyle.SetPaperSize(20.,20.)
  # tdrStyle.SetLineScalePS(Float_t scale = 3)
  # tdrStyle.SetLineStyleString(Int_t i, const char* text)
  # tdrStyle.SetHeaderPS(const char* header)
  # tdrStyle.SetTitlePS(const char* pstitle)

  # tdrStyle.SetBarOffset(Float_t baroff = 0.5)
  # tdrStyle.SetBarWidth(Float_t barwidth = 0.5)
  # tdrStyle.SetPaintTextFormat(const char* format = "g")
  # tdrStyle.SetPalette(Int_t ncolors = 0, Int_t* colors = 0)
  # tdrStyle.SetTimeOffset(Double_t toffset)
  # tdrStyle.SetHistMinimumZero(kTRUE)

  tdrStyle.SetHatchesLineWidth(5)
  tdrStyle.SetHatchesSpacing(0.05)
  tdrStyle.cd()

#https://cms-analysis.github.io/CombineHarvester/plotting_8py_source.html
def ModTDRStyle(width=600, height=600, t=0.06, b=0.12, l=0.16, r=0.04):
  """Modified version of the tdrStyle
  
  Args:
      width (int): Canvas width in pixels
      height (int): Canvas height in pixels
      t (float): Pad top margin [0-1]
      b (float): Pad bottom margin [0-1]
      l (float): Pad left margin [0-1]
      r (float): Pad right margin [0-1]
  """
  setTDRStyle()
  
  # Set the default canvas width and height in pixels
  R.gStyle.SetCanvasDefW(width)
  R.gStyle.SetCanvasDefH(height)
  
  # Set the default margins. These are given as fractions of the pad height
  # for `Top` and `Bottom` and the pad width for `Left` and `Right`. But we
  # want to specify all of these as fractions of the shoRest length.
  def_w = float(R.gStyle.GetCanvasDefW())
  def_h = float(R.gStyle.GetCanvasDefH())
  
  scale_h = (def_w / def_h) if (def_h > def_w) else 1.
  scale_w = (def_h / def_w) if (def_w > def_h) else 1.
  
  def_min = def_h if (def_h < def_w) else def_w
  
  R.gStyle.SetPadTopMargin(t * scale_h)
  # default 0.05
  R.gStyle.SetPadBottomMargin(b * scale_h)
  # default 0.13
  R.gStyle.SetPadLeftMargin(l * scale_w)
  # default 0.16
  R.gStyle.SetPadRightMargin(r * scale_w)
  # default 0.02
  # But note the new CMS style sets these:
  # 0.08, 0.12, 0.12, 0.04
  
  # Set number of axis tick divisions
  R.gStyle.SetNdivisions(506, 'XYZ')  # default 510
  
  # Some marker propeRies not set in the default tdr style
  R.gStyle.SetMarkerColor(R.kBlack)
  R.gStyle.SetMarkerSize(1.0)
  
  R.gStyle.SetLabelOffset(0.007, 'YZ')
  # This is an adhoc adjustment to scale the x-axis label
  # offset when we stretch plot veRically
  # Will also need to increase if first x-axis label has more than one digit
  R.gStyle.SetLabelOffset(0.005 * (3. - 2. / scale_h), 'X')
  
  # In this next paR we do a slightly involved calculation to set the axis
  # title offsets, depending on the values of the TPad dimensions and
  # margins. This is to try and ensure that regardless of how these pad
  # values are set, the axis titles will be located towards the edges of the
  # canvas and not get pushed off the edge - which can often happen if a
  # fixed value is used.
  title_size = 0.05
  title_px = title_size * def_min
  label_size = 0.04
  R.gStyle.SetTitleSize(title_size, 'XYZ')
  R.gStyle.SetLabelSize(label_size, 'XYZ')
  
  R.gStyle.SetTitleXOffset(0.5 * scale_h *
                           (1.2 * (def_h * b * scale_h - 0.6 * title_px)) /
                           title_px)
  R.gStyle.SetTitleYOffset(0.5 * scale_w *
                           (1.2 * (def_w * l * scale_w - 0.6 * title_px)) /
                           title_px)
  
  # Draw ticks on the axes
  R.gStyle.SetPadTickX(1)
  R.gStyle.SetPadTickY(1)
  R.gStyle.SetTickLength(0.02, 'XYZ')
  
  R.gStyle.SetLegendBorderSize(0)
  R.gStyle.SetLegendFont(42)
  R.gStyle.SetLegendFillColor(0)
  R.gStyle.SetFillColor(0)
  
  R.gROOT.ForceStyle()
