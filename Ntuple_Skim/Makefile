all: src/FactorizedJetCorrector.o src/JetCorrectorParameters.o src/SimpleJetCorrector.o src/JetCorrectionUncertainty.o src/JECvariation.o src/JetResolutionObject.o src/JetResolution.o src/Selector.o src/EventTree.o src/EventPick.o makeNtuple #makeCutflows 

src/FactorizedJetCorrector.o: src/FactorizedJetCorrector.cpp interface/FactorizedJetCorrector.h interface/JetCorrectorParameters.h interface/SimpleJetCorrector.h src/Utilities.cc
	g++ -o src/FactorizedJetCorrector.o -c `root-config --libs` -I`root-config --incdir` -std=c++17 src/FactorizedJetCorrector.cpp

src/JetCorrectorParameters.o: src/JetCorrectorParameters.cpp interface/JetCorrectorParameters.h 
	g++ -o src/JetCorrectorParameters.o -c `root-config --libs` -I`root-config --incdir` -std=c++17 src/JetCorrectorParameters.cpp

src/SimpleJetCorrector.o: src/JetCorrectorParameters.cpp interface/JetCorrectorParameters.h interface/SimpleJetCorrector.h
	g++ -o src/SimpleJetCorrector.o -c `root-config --libs` -I`root-config --incdir` -std=c++17 src/SimpleJetCorrector.cpp 

src/JetCorrectionUncertainty.o: src/JetCorrectionUncertainty.cpp interface/JetCorrectionUncertainty.h src/SimpleJetCorrectionUncertainty.cpp interface/SimpleJetCorrectionUncertainty.h
	g++ -o src/JetCorrectionUncertainty.o -c `root-config --libs` -I`root-config --incdir` -std=c++17 src/JetCorrectionUncertainty.cpp 
	g++ -o src/SimpleJetCorrectionUncertainty.o -c `root-config --libs` -I`root-config --incdir` -std=c++17 src/SimpleJetCorrectionUncertainty.cpp 

src/JECvariation.o: src/FactorizedJetCorrector.o src/JetCorrectorParameters.o src/SimpleJetCorrector.o src/JetCorrectionUncertainty.o src/JECvariation.cpp
	g++ -o src/JECvariation.o -c `root-config --libs` -I`root-config --incdir` -std=c++17 src/JECvariation.cpp

src/JetResolutionObject.o: src/JetResolutionObject.cc interface/JetResolutionObject.h
	g++ -o src/JetResolutionObject.o -c `root-config --libs` -I`root-config --incdir` -std=c++17 -D STANDALONE src/JetResolutionObject.cc 

src/JetResolution.o: interface/JetResolution.h src/JetResolution.cc
	g++ -o src/JetResolution.o -c `root-config --libs` -I`root-config --incdir` -std=c++17 -D STANDALONE src/JetResolution.cc 

src/EventTree.o: src/EventTree.cpp interface/EventTree.h
	g++ -o src/EventTree.o -c -I`root-config --incdir` -std=c++17 -D STANDALONE src/EventTree.cpp

src/BTagCalibrationStandalone.o: src/BTagCalibrationStandalone.cpp interface/BTagCalibrationStandalone.h
	g++ -o src/BTagCalibrationStandalone.o -c -I`root-config --incdir` -std=c++17 -D STANDALONE src/BTagCalibrationStandalone.cpp

src/Selector.o: src/EventTree.o src/Selector.cpp interface/Selector.h
	g++ -o src/Selector.o -c -I `root-config --incdir` -std=c++17 -D STANDALONE src/Selector.cpp
#	g++ -o src/Selector.o -c -I `root-config --incdir` -std=c++17 -D STANDALONE src/ParsePhotonID.cpp src/Utils.cc src/JetResolution.cc src/JetResolutionObject.cc  src/Selector.cpp

src/EventPick.o: src/Selector.o src/EventPick.cpp interface/EventPick.h
	g++ -o src/EventPick.o -c -I `root-config --incdir` -std=c++17 -D STANDALONE src/EventPick.cpp 

makeNtuple: src/Selector.o src/EventPick.o src/EventTree.o makeNtuple.C src/OverlapRemove.cpp interface/makeNtuple.h interface/ReaderPileupSF.h src/BTagCalibrationStandalone.o interface/ReaderLumiSF.h src/JECvariation.o src/TopEventCombinatorics.cpp interface/ReaderMuSF.h interface/ReaderEleSF.h interface/ReaderPhoSF.h interface/ReaderTopSF.h 
	g++ -o makeNtuple `root-config --libs` -I`root-config --incdir` -std=c++17 -D STANDALONE makeNtuple.C src/EventTree.o src/EventPick.o src/ParsePhotonID.cpp src/Selector.o src/OverlapRemove.cpp src/BTagCalibrationStandalone.o src/Utils.cc src/FactorizedJetCorrector.o src/JetCorrectorParameters.o src/SimpleJetCorrector.o src/JetCorrectionUncertainty.o src/SimpleJetCorrectionUncertainty.o src/JECvariation.o src/JetResolution.cc src/JetResolutionObject.cc src/METzCalculator.cpp src/TopEventCombinatorics.cpp 

clean:
	rm makeNtuple src/*.o 
