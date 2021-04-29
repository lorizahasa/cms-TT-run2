all: src/FactorizedJetCorrector.o src/JetCorrectorParameters.o src/SimpleJetCorrector.o src/JetCorrectionUncertainty.o src/JECvariation.o src/JetResolutionObject.o src/JetResolution.o src/Selector.o src/EventTree.o src/EventPick.o makeNtuple #makeCutflows 

src/FactorizedJetCorrector.o: src/FactorizedJetCorrector.cpp interface/FactorizedJetCorrector.h interface/JetCorrectorParameters.h interface/SimpleJetCorrector.h src/Utilities.cc
	g++ -c `root-config --libs` -I`root-config --incdir` -std=c++17 src/FactorizedJetCorrector.cpp

src/JetCorrectorParameters.o: src/JetCorrectorParameters.cpp interface/JetCorrectorParameters.h 
	g++ -c `root-config --libs` -I`root-config --incdir` -std=c++17 src/JetCorrectorParameters.cpp

src/SimpleJetCorrector.o: src/JetCorrectorParameters.cpp interface/JetCorrectorParameters.h interface/SimpleJetCorrector.h
	g++ -c `root-config --libs` -I`root-config --incdir` -std=c++17 src/SimpleJetCorrector.cpp 

src/JetCorrectionUncertainty.o: src/JetCorrectionUncertainty.cpp interface/JetCorrectionUncertainty.h src/SimpleJetCorrectionUncertainty.cpp interface/SimpleJetCorrectionUncertainty.h
	g++ -c `root-config --libs` -I`root-config --incdir` -std=c++17 src/JetCorrectionUncertainty.cpp src/SimpleJetCorrectionUncertainty.cpp 

src/JECvariation.o: src/FactorizedJetCorrector.o src/JetCorrectorParameters.o src/SimpleJetCorrector.o src/JetCorrectionUncertainty.o src/JECvariation.cpp
	g++ -c `root-config --libs` -I`root-config --incdir` -std=c++17 src/JECvariation.cpp

src/JetResolutionObject.o: src/JetResolutionObject.cc interface/JetResolutionObject.h
	g++ -c `root-config --libs` -I`root-config --incdir` -std=c++17 -D STANDALONE interface/JERUtilities.h src/JetResolutionObject.cc 

src/JetResolution.o: interface/JetResolution.h src/JetResolution.cc
	g++ -c `root-config --libs` -I`root-config --incdir` -std=c++17 -D STANDALONE src/JetResolution.cc 

src/EventTree.o: src/EventTree.cpp interface/EventTree.h
	g++ -c -I`root-config --incdir` -std=c++17 -D STANDALONE src/EventTree.cpp

src/BTagCalibrationStandalone.o: src/BTagCalibrationStandalone.cpp interface/BTagCalibrationStandalone.h
	g++ -c -I`root-config --incdir` -std=c++17 -D STANDALONE src/BTagCalibrationStandalone.cpp

makeNtuple: src/Selector.o src/EventPick.o src/EventTree.o makeNtuple.C src/OverlapRemove.cpp interface/makeNtuple.h src/ReaderPileupSF.cpp interface/ReaderPileupSF.h src/BTagCalibrationStandalone.o interface/ReaderLumiSF.h src/JECvariation.o src/TopEventCombinatorics.cpp interface/ReaderMuSF.h interface/ReaderEleSF.h interface/ReaderPhoSF.h 
	g++ -o makeNtuple `root-config --libs` -I`root-config --incdir` -std=c++17 -D STANDALONE makeNtuple.C src/EventTree.o src/EventPick.o src/ParsePhotonID.cpp src/Selector.o src/OverlapRemove.cpp src/ReaderPileupSF.cpp src/BTagCalibrationStandalone.o src/Utils.cc src/FactorizedJetCorrector.o src/JetCorrectorParameters.o src/SimpleJetCorrector.o src/JetCorrectionUncertainty.o src/SimpleJetCorrectionUncertainty.o src/JECvariation.o src/JetResolution.cc src/JetResolutionObject.cc src/METzCalculator.cpp src/TopEventCombinatorics.cpp 


src/Selector.o: src/EventTree.o src/Selector.cpp interface/Selector.h
	g++ -c -I `root-config --incdir` -std=c++17 -D STANDALONE src/ParsePhotonID.cpp src/Utils.cc src/JetResolution.cc src/JetResolutionObject.cc  src/Selector.cpp

src/EventPick.o: src/Selector.o src/EventPick.cpp interface/EventPick.h
	g++ -c -I `root-config --incdir` -std=c++17 -D STANDALONE src/EventPick.cpp 

src/Selector_gen.o: src/EventTree.o src/Selector_gen.cpp interface/Selector.h
	g++ -c -I`root-config --incdir` -std=c++17 -D STANDALONE src/Selector_gen.cpp

src/EventPick_gen.o: src/Selector_gen.o src/EventPick_gen.cpp interface/EventPick.h
	g++ -c -I `root-config --incdir` -std=c++17 -D STANDALONE src/EventPick_gen.cpp 

clean:
	rm *.o src/*.o 
