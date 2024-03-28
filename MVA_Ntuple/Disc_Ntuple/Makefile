all: src/NtupleTree.o  runReadNtuple 
runReadNtuple:   src/NtupleTree.o  ReadNtuple.C
	g++ -o runReadNtuple `root-config --cflags --glibs` -lTMVA -I `root-config --incdir` -std=c++17 src/NtupleTree.o  ReadNtuple.C 

src/NtupleTree.o: src/NtupleTree.cpp src/NtupleTree.h
	g++ -c `root-config --libs` -I `root-config --incdir` -std=c++17 src/NtupleTree.cpp -o src/NtupleTree.o

clean:
	rm src/*.o runReadNtuple 
