from ROOT import TFile

_fileIn = TFile.Open("root://cmseos.fnal.gov//store/user/rverma/Output/cms-TT-run2/tytg/Hist_Ntuple/2016/Semilep/Mu/Merged/AllInc_old.root","read")
_fileOut = TFile("testNew.root","recreate")

#dict of histograms, with region as key
hists = {'SR':['TopStar_mass']}

systematicsToNormalize = ['Q2Up','Q2Down','PdfUp','PdfDown']

NominalYields = {}
processes = [k.GetName() for k in _fileIn.GetListOfKeys()]

for p in processes:
    NominalYields[p] = {}
    for r in hists:
        NominalYields[p][r] = {}
        for h in hists[r]:
            #_h = _fileIn.Get(f'{p}/Base/{r}/{h}')
            _h = _fileIn.Get("%s/Base/%s/%s"%(p, r, h))
            NominalYields[p][r][h] = _h.Integral()

for p in processes:
    _fileOut.mkdir(p)
    #systList = [k.GetName() for k in _fileIn.Get(f'{p}').GetListOfKeys()]
    systList = [k.GetName() for k in _fileIn.Get("%s"%p).GetListOfKeys()]
    for s in systList:
        #_fileOut.mkdir(f'{p}/{s}')
        _fileOut.mkdir("%s/%s"%(p, s))
        for r in hists:
            #_fileOut.mkdir(f'{p}/{s}/{r}')
            _fileOut.mkdir("%s/%s/%s"%(p, s, r))
            for h in hists[r]:
                #hName = f'{p}/{s}/{r}/{h}'
                hName = "%s/%s/%s/%s"%(p, s, r, h) 
                _hIn = _fileIn.Get(hName)
                if s in systematicsToNormalize:
                    _hIn.Scale(NominalYields[p][r][h]/_hIn.Integral())
                #_fileOut.cd(f'{p}/{s}/{r}/')
                _fileOut.cd("%s/%s/%s/"%(p, s, r))
                _hIn.Write()
_fileOut.Close()
