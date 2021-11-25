import ROOT
#-----------------------------------------------------------------
condorHistDir = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/MVA_Ntuple/Disc_Ntuple"
#-----------------------------------------------------------------
#Years 	      =	["2016", "2017", "2018"]
Years 	      =	["2016"]
#Channels 	  =	["Mu", "Ele"]
Channels 	  =	["Mu"]
Decays 	      =	["Semilep"]
Mass          = ["800", "1600"]

Systematics   =	[]
Systematics.append("Weight_pu")
Systematics.append("Weight_mu")
Systematics.append("Weight_pho")
Systematics.append("Weight_ele")
Systematics.append("Weight_btag_b")
Systematics.append("Weight_btag_l")
Systematics.append("Weight_prefire")
Systematics.append("Weight_q2")
Systematics.append("Weight_pdf")
Systematics.append("Weight_isr")
Systematics.append("Weight_fsr")
Systematics.append("Weight_jes")
Systematics.append("Weight_jer")
Systematics   =	[]

SystLevels = []
SystLevels.append("Up")
SystLevels.append("Down")

Regions = {}
isTTYG = True 
#--------------------------------
#tt+gamma+gluon control regions
#--------------------------------
if isTTYG:
    Regions['ttyg_Enriched_CR']         = "((Jet_size>=5 && FatJet_size==0) || (Jet_size>=2 && FatJet_size==1)) && Jet_b_size >=1 && Photon_size==1 && Photon_et < 75"
    Regions['ttyg_Enriched_CR_Resolved']= "Jet_size >=5 && Jet_b_size >=1 && Photon_size==1 && Photon_et < 75 && FatJet_size ==0"
    Regions['ttyg_Enriched_CR_Boosted'] = "Jet_size >=2 && Jet_b_size >=1 && Photon_size==1 && Photon_et < 75 && FatJet_size >=1"

    #--------------------------------
    #signal regions
    #--------------------------------
    Regions['ttyg_Enriched_SR']         = "((Jet_size>=5 && FatJet_size==0) || (Jet_size>=2 && FatJet_size==1)) && Jet_b_size >=1 && Photon_size==1 && Photon_et > 100"
    Regions['ttyg_Enriched_SR_Resolved']= "Jet_size >=5 && Jet_b_size >=1 && Photon_size==1 && Photon_et > 100 && FatJet_size ==0"
    Regions['ttyg_Enriched_SR_Boosted'] = "Jet_size >=2 && Jet_b_size >=1 && Photon_size==1 && Photon_et > 100 && FatJet_size >=1"



#https://github.com/ViniciusMikuni/ttbb-analysis/blob/5d48e5e03bdd0ca162d3dd058f4ee02ef33a8460/python/MVA_cfg.py
batchs = 64
layoutString = "Layout=RELU|64,RELU|64,RELU|64,SOFTSIGN"
training0 =  "LearningRate=1e-3,Momentum=0.0,Repetitions=1,ConvergenceSteps=20,BatchSize=256,TestRepetitions=10,Regularization=L2,Multithreading=True,DropConfig=0.1,DropRepetitions=1"
#training1 = "LearningRate=1e-2,Momentum=0.0,Repetitions=1,ConvergenceSteps=10,BatchSize=256,TestRepetitions=7,Regularization=L2,Multithreading=True"

trainingStrategyString  = "TrainingStrategy="
trainingStrategyString += training0
#trainingStrategyString += training0 + "|" + training1

nnOptions = "!H:V:ErrorStrategy=CROSSENTROPY:VarTransform=None:WeightInitialization=XAVIERUNIFORM"
nnOptions += ":" + layoutString + ":" +  trainingStrategyString + ":Architecture=CPU"

methodList = {"BDTP":[ROOT.TMVA.Types.kBDT,":".join(["!H","!V","NTrees=850","MaxDepth=5","BoostType=Grad","Shrinkage=0.01","UseBaggedBoost","BaggedSampleFraction=0.50","SeparationType=GiniIndex","nCuts=50"])],
              "BDTCW":[ROOT.TMVA.Types.kBDT,":".join(["!H","!V","NTrees=500","MaxDepth=8","BoostType=Grad","Shrinkage=0.01","UseBaggedBoost","BaggedSampleFraction=0.50","SeparationType=GiniIndex","nCuts=50"])],
              #"BDTFish":[ROOT.TMVA.Types.kBDT,":".join(["!H","!V","NTrees=500","MaxDepth=4","BoostType=Grad","Shrinkage=0.01","UseFisherCuts","MinLinCorrForFisher=0.5","UseBaggedBoost","BaggedSampleFraction=0.50","SeparationType=GiniIndex","nCuts=50"])],
              "LH":[ROOT.TMVA.Types.kLikelihood,"H:!V:TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmoothBkg[1]=10:NSmooth=1:NAvEvtPerBin=50"],
              #"Cuts":[ROOT.TMVA.Types.kCuts,"H:!V:PopSize=500:Steps=50"],
              "MLP": [ROOT.TMVA.Types.kMLP, "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator"],
              "SVM": [ROOT.TMVA.Types.kSVM,"VarTransform=Norm"],
              "BDTA": [ROOT.TMVA.Types.kBDT, "!H:!V:NTrees=850:MaxDepth=6:BoostType=AdaBoost:AdaBoostBeta=0.05:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=30"],
              "DNN": [ROOT.TMVA.Types.kDNN, nnOptions],
              #"PyDNN":[ROOT.TMVA.Types.kPyKeras,":".join(["H","V","NumEpochs=700","TriesEarlyStopping=20","BatchSize="+str(batchs)])],
              "SVM" : [ROOT.TMVA.Types.kSVM, "VarTransform=Norm"],
              #"Fish" : [ROOT.TMVA.Types.kFisher, "H:!V:Fisher:VarTransform=None:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" ],
              #"FishG" : [ROOT.TMVA.Types.kFisher, "H:!V:Fisher:VarTransform=Gauss:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:Boost_Num=20:Boost_Transform=log:Boost_Type=AdaBoost:Boost_AdaBoostBeta=0.2:!Boost_DetailedMonitoring" ],

              "PDEFoam": [ROOT.TMVA.Types.kPDEFoam, "!H:!V::SigBgSeparate=F:MaxDepth=4:UseYesNoCell=T:DTLogic=MisClassificationError:FillFoamWithOrigWeights=F:TailCut=0:nActiveCells=500:nBin=20:Nmin=400:Compress=T"],
              "LH":[ROOT.TMVA.Types.kLikelihood,"H:!V:TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmoothBkg[1]=10:NSmooth=1:NAvEvtPerBin=50:VarTransform=Decorrelate"],
              #"PyGTB": [ROOT.TMVA.Types.kPyGTB,"!V:NEstimators=850:NJobs=4"],
              #"PyAda": [ROOT.TMVA.Types.kPyAdaBoost,"!V:NEstimators=1000"],
              #"PyForest": [ROOT.TMVA.Types.kPyRandomForest, "!V:VarTransform=None:NEstimators=850:Criterion=gini:MaxFeatures=auto:MaxDepth=4:MinSamplesLeaf=1:MinWeightFractionLeaf=0:Bootstrap=kTRUE"]
              }



