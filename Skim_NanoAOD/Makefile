CXX = g++
ROOT_CFLAGS := $(shell root-config --cflags)
ROOT_LIBS := $(shell root-config --libs)
CXXFLAGS ?= -O2 -Wall -Wextra

.PHONY: all clean
all: makeSkim

makeSkim: makeSkim.C interface/SkimBranchConfig.h
	$(CXX) $(ROOT_CFLAGS) $(CXXFLAGS) -std=c++17 $< -o $@ $(ROOT_LIBS)

clean:
	rm -f makeSkim
