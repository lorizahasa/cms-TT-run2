#ifndef UTIL_H
#define UTIL_H 

#include<TMath.h>
#include <string>
#include <iostream>
#include <sstream>

double dR(double eta1, double phi1, double eta2, double phi2);
bool checkStr(std::string sentence, std::string wordToFind);
std::string getElementByIndex(const std::string& inputString, int index);

#endif
