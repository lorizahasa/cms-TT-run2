
ROOT_I=-I`root-config --incdir`
ROOT_L=`root-config --libs`
CORR_A=`correction config --cflags --ldflags --rpath`
GCC=g++ -std=c++17

all:  src/JECvariation.o src/EventTree.o src/Selector.o src/EventPick.o makeNtuple

src/JECvariation.o: src/JECvariation.cpp interface/JECvariation.h
	${GCC} -o src/JECvariation.o -c ${CORR_A} ${ROOT_L} ${ROOT_I}  src/JECvariation.cpp

src/EventTree.o: src/EventTree.cpp interface/EventTree.h
	${GCC} -o src/EventTree.o -c ${ROOT_I} -D STANDALONE src/EventTree.cpp

src/Selector.o: src/EventTree.o src/Selector.cpp interface/Selector.h
	${GCC} -o src/Selector.o -c ${CORR_A} ${ROOT_L} ${ROOT_I} -D STANDALONE src/Selector.cpp

src/EventPick.o: src/Selector.o src/EventPick.cpp interface/EventPick.h
	${GCC} -o src/EventPick.o -c ${CORR_A} ${ROOT_I}  -D STANDALONE src/EventPick.cpp 

#/cvmfs/cms.cern.ch/slc7_amd64_gcc10/external/py3-correctionlib/2.1.0-bc1f1a24613552be911056d8eb959866/lib/python3.9/site-packages/correctionlib/
makeNtuple: src/Selector.o src/EventPick.o src/EventTree.o makeNtuple.C src/OverlapRemove.cpp interface/makeNtuple.h interface/ReaderLumiSF.h src/JECvariation.o src/TopEventCombinatorics.cpp interface/ReaderMuSF.h interface/ReaderEleSF.h interface/ReaderPhoSF.h
	${GCC} -o makeNtuple ${CORR_A} ${ROOT_L} ${ROOT_I} -D STANDALONE makeNtuple.C src/EventTree.o src/EventPick.o src/ParsePhotonID.cpp src/Selector.o src/OverlapRemove.cpp src/Utils.cc src/JECvariation.o src/METzCalculator.cpp src/TopEventCombinatorics.cpp 
clean:
	rm makeNtuple src/*.o 
