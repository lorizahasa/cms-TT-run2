#include <boost/property_tree/json_parser.hpp>
#include <boost/property_tree/ptree.hpp>
#include <iostream>

using namespace std;
class LumiMask
{
 public:
    LumiMask(string &filename){
        boost::property_tree::read_json(filename, loadedJSON);
    }
    bool isValidLumi(unsigned int &run, unsigned int &lumi);
 private:
    boost::property_tree::ptree loadedJSON;
};

bool LumiMask::isValidLumi(unsigned int &run, unsigned int &lumi){
    bool validLumi = false;
    std::string run_ = std::to_string(run);
    try{
        for (boost::property_tree::ptree::value_type &row : loadedJSON.get_child(run_)){
            vector<int>lumis;
            for (boost::property_tree::ptree::value_type &cell : row.second){
                lumis.push_back(cell.second.get_value<int>());
            }
            if (lumi >= lumis.at(0) && lumi <= lumis.at(1)) validLumi = true;
        }
    } catch (const std::exception& e) {
        //cout<<e.what()<<", this Run does not exist in the golden JSON"<<endl;
        validLumi = false;
    }
    return validLumi;
}

