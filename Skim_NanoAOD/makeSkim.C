// Production NanoAOD skim: RDataFrame and the nominal Table 9 trigger ORs.
#include <ROOT/RDataFrame.hxx>
#include "interface/SkimBranchConfig.h"
#include <TBranch.h>
#include <TFile.h>
#include <TH1D.h>
#include <TH1F.h>
#include <TLeaf.h>
#include <TTree.h>

#include <algorithm>
#include <chrono>
#include <cmath>
#include <filesystem>
#include <functional>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <memory>
#include <regex>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
#include <unistd.h>

namespace {
using Strings = std::vector<std::string>;
using Node = ROOT::RDF::RNode;
using Count = ROOT::RDF::RResultPtr<ULong64_t>;
namespace fs = std::filesystem;

struct Options {
    std::string year, split, output;
    Strings inputs;
    unsigned threads = 4;
    int job = 0, jobs = 0;
    bool mc = true, remote = false;
};

int positiveInt(const std::string& text) {
    if (text.empty() || text.find_first_not_of("0123456789") != std::string::npos)
        throw std::runtime_error("Expected a positive integer, got: " + text);
    const auto value = std::stoll(text);
    if (value < 1 || value > std::numeric_limits<int>::max())
        throw std::runtime_error("Integer is out of range: " + text);
    return static_cast<int>(value);
}

Options parse(int argc, char** argv) {
    Options o;
    int i = 1, explicitMC = -1;
    while (i < argc && std::string(argv[i]).rfind("--", 0) == 0) {
        const std::string arg = argv[i++];
        if (arg == "--threads" && i < argc) o.threads = positiveInt(argv[i++]);
        else if (arg == "--data" || arg == "--mc") {
            if (explicitMC != -1) throw std::runtime_error("Specify --data or --mc only once");
            explicitMC = arg == "--mc";
        } else throw std::runtime_error("Unknown or incomplete option: " + arg);
    }
    if (argc - i < 5)
        throw std::runtime_error("Usage: makeSkim [--threads N] [--data|--mc] "
                                 "YEAR JOBofTOTAL OUTPUT.root local|xrootd INPUT.root [...]");
    o.year = argv[i++]; o.split = argv[i++]; o.output = argv[i++];
    if (o.year != "2016Pre" && o.year != "2016Post" && o.year != "2017" && o.year != "2018")
        throw std::runtime_error("Unsupported era: " + o.year);
    std::smatch match;
    if (!std::regex_match(o.split, match, std::regex("([0-9]+)of([0-9]+)")))
        throw std::runtime_error("Job must have the form 1of2");
    o.job = positiveInt(match[1]); o.jobs = positiveInt(match[2]);
    const std::string mode = argv[i++];
    if (mode != "local" && mode != "xrootd")
        throw std::runtime_error("Input mode must be local or xrootd");
    o.remote = mode == "xrootd";
    if (o.output.size() < 5 || o.output.substr(o.output.size()-5) != ".root")
        throw std::runtime_error("Output must end in .root");
    o.mc = explicitMC == -1 ? o.output.find("Data") == std::string::npos : explicitMC == 1;
    o.output.insert(o.output.size()-5, "_" + o.split);
    // Check duplicates over the whole supplied sample, before splitting jobs.
    std::set<std::string> identities;
    for (; i < argc; ++i) {
        std::string file = argv[i];
        if (file.empty()) throw std::runtime_error("Input filename is empty");
        const auto store = file.find("/store/");
        const auto key = store != std::string::npos ? file.substr(store) :
            file.find("://") == std::string::npos ? fs::weakly_canonical(file).string() : file;
        if (!identities.insert(key).second) throw std::runtime_error("Duplicate input: " + file);
        if (o.remote && file.rfind("root://", 0) != 0)
            file = std::string("root://cmsxrootd.fnal.gov/") + (file.front() == '/' ? "" : "/") + file;
        o.inputs.push_back(file);
    }
    if (o.job > o.jobs || static_cast<std::size_t>(o.jobs) > o.inputs.size())
        throw std::runtime_error("Require 1 <= job <= total jobs <= input file count");
    // Same contiguous split, including remainder assignment, as splitVector.
    const auto size = o.inputs.size() / o.jobs, remainder = o.inputs.size() % o.jobs;
    const auto start = (o.job-1)*size + std::min<std::size_t>(o.job-1, remainder);
    const auto count = size + (static_cast<std::size_t>(o.job-1) < remainder);
    o.inputs = Strings(o.inputs.begin()+start, o.inputs.begin()+start+count);
    if (!fs::is_directory(fs::absolute(o.output).parent_path()))
        throw std::runtime_error("Output directory does not exist");
    if (fs::exists(o.output)) throw std::runtime_error("Refusing to overwrite: " + o.output);
    return o;
}

struct Triggers { Strings mu, ele; };
Triggers triggers(const std::string& year) {
    return {SkimBranchConfig::muonTriggers(year), SkimBranchConfig::electronTriggers(year)};
}

std::string logicalOR(const Strings& columns) {
    std::string expression = "false";
    for (const auto& c : columns) expression += " || (" + c + ")";
    return "(" + expression + ")";
}
Strings branchPatterns(bool mc, const std::string& year) {
    return SkimBranchConfig::branches(mc, year);
}

bool matches(const std::string& name, const Strings& columns) {
    return std::find(columns.begin(), columns.end(), name) != columns.end();
}

struct Inputs {
    Strings columns;
    std::map<std::string, std::string> schema;
    Long64_t events = 0, genCount = 0;
    double genSumw = 0.;
};

Inputs inspect(const Options& o) {
    Inputs result;
    const auto patterns = branchPatterns(o.mc, o.year);
    for (const auto& path : o.inputs) {
        std::unique_ptr<TFile> f(TFile::Open(path.c_str(), "READ"));
        if (!f || f->IsZombie() || f->TestBit(TFile::kRecovered))
            throw std::runtime_error("Invalid or unreadable input: " + path);
        auto* events = dynamic_cast<TTree*>(f->Get("Events"));
        if (!events) throw std::runtime_error("Missing Events tree: " + path);
        Strings required = {"run", "luminosityBlock", "event", "nTrigObj", "nMuon", "nElectron", "nJet",
                            "nPhoton", "Flag_goodVertices", "Flag_globalSuperTightHalo2016Filter",
                            "Flag_HBHENoiseFilter", "Flag_HBHENoiseIsoFilter",
                            "Flag_EcalDeadCellTriggerPrimitiveFilter", "Flag_BadPFMuonFilter", "Flag_eeBadScFilter"};
        if (o.mc) required.push_back("Generator_weight");
        if (o.year != "2016Pre" && o.year != "2016Post") required.push_back("Flag_ecalBadCalibFilter");
        for (const auto& name : required)
            if (!events->GetBranch(name.c_str())) throw std::runtime_error("Missing required branch " + name + " in " + path);
        std::map<std::string, std::string> schema;
        Strings columns;
        std::set<std::string> added;
        // Snapshot needs an array's count column before the array itself.
        std::function<void(TBranch*)> add = [&](TBranch* branch) {
            const std::string name = branch->GetName();
            if (!added.insert(name).second) return;
            std::string signature = branch->GetClassName();
            for (auto* object : *branch->GetListOfLeaves()) {
                auto* leaf = static_cast<TLeaf*>(object);
                auto* count = leaf->GetLeafCount();
                if (count) add(count->GetBranch());
                signature += "|" + std::string(leaf->GetName()) + ":" + leaf->GetTypeName() + ":" +
                    std::to_string(leaf->GetLenStatic()) + ":" + (count ? count->GetName() : "");
            }
            columns.push_back(name);
            schema[name] = signature;
        };
        for (auto* object : *events->GetListOfBranches()) {
            auto* branch = static_cast<TBranch*>(object);
            if (matches(branch->GetName(), patterns)) add(branch);
        }
        if (result.schema.empty()) { result.schema = schema; result.columns = columns; }
        else if (result.schema != schema)
            throw std::runtime_error("Selected branch schema differs between assigned inputs: " + path);
        for (const auto& flag : {"passTrigMu", "passTrigEle", "passTrigMuTable9", "passTrigEleTable9"})
            if (events->GetBranch(flag)) throw std::runtime_error("Input is already a skim (contains " + std::string(flag) + ")");
        result.events += events->GetEntries();
        if (o.mc) {
            auto* runs = dynamic_cast<TTree*>(f->Get("Runs"));
            if (!runs || !runs->GetBranch("genEventCount") || !runs->GetBranch("genEventSumw"))
                throw std::runtime_error("Missing Runs generator metadata: " + path);
            Long64_t count = 0;
            Double_t sumw = 0.;
            runs->SetBranchStatus("*", 0);
            runs->SetBranchStatus("genEventCount", 1); runs->SetBranchStatus("genEventSumw", 1);
            if (runs->SetBranchAddress("genEventCount", &count) < 0 ||
                runs->SetBranchAddress("genEventSumw", &sumw) < 0)
                throw std::runtime_error("Unexpected Runs metadata type: " + path);
            for (Long64_t row = 0; row < runs->GetEntries(); ++row) {
                if (runs->GetEntry(row) <= 0 || count < 0 || !std::isfinite(sumw))
                    throw std::runtime_error("Unreadable or invalid Runs metadata: " + path);
                result.genCount += count; result.genSumw += sumw;
            }
        }
        std::cout << "Validated " << path << " (" << events->GetEntries() << " entries)" << std::endl;
    }
    // A split job's signed sum may be zero. Validate the full-sample sum downstream.
    if (o.mc && (result.genCount <= 0 || !std::isfinite(result.genSumw)))
        throw std::runtime_error("Invalid assigned-job generator totals");
    return result;
}

void writeCounts(const char* name, const char* title, const std::vector<double>& counts,
                 const Strings& labels, double low, double high) {
    TH1F h(name, title, counts.size(), low, high);
    double entries = 0.;
    double stats[4] = {};
    for (std::size_t i = 0; i < counts.size(); ++i) {
        h.SetBinContent(i+1, counts[i]);
        if (i < labels.size() && !labels[i].empty()) h.GetXaxis()->SetBinLabel(i+1, labels[i].c_str());
        entries += counts[i];
        const double x = h.GetBinCenter(i+1);
        stats[0] += counts[i]; stats[1] += counts[i];
        stats[2] += counts[i]*x; stats[3] += counts[i]*x*x;
    }
    h.PutStats(stats); h.SetEntries(entries); h.Write();
}

void restoreEmptySchema(TFile& output, const Options& options, const Inputs& input) {
    // ROOT 6.30 creates Snapshot branches on the first accepted event. With no
    // accepted events, copy only the schema; never scan or fill an extra event.
    std::unique_ptr<TFile> source(TFile::Open(options.inputs.front().c_str(), "READ"));
    if (!source || source->IsZombie() || source->TestBit(TFile::kRecovered))
        throw std::runtime_error("Cannot reopen input to preserve the empty output schema");
    auto* original = dynamic_cast<TTree*>(source->Get("Events"));
    if (!original) throw std::runtime_error("Missing Events schema for empty output");
    original->SetBranchStatus("*", 0);
    for (const auto& name : input.columns)
        if (original->GetBranch(name.c_str())) original->SetBranchStatus(name.c_str(), 1);
    output.Delete("Events;*");
    output.cd();
    std::unique_ptr<TTree> empty(original->CloneTree(0));
    if (!empty) throw std::runtime_error("Cannot clone the empty Events schema");
    Int_t flags[2] = {};
    const Strings names = {"passTrigMuTable9", "passTrigEleTable9"};
    for (std::size_t i = 0; i < names.size(); ++i)
        empty->Branch(names[i].c_str(), &flags[i], (names[i]+"/I").c_str());
    empty->Write("Events", TObject::kOverwrite);
    empty->ResetBranchAddresses();
}

void run(const Options& o, const std::string& temporary) {
    const auto start = std::chrono::steady_clock::now();
    const auto ts = triggers(o.year);
    auto input = inspect(o);
    const auto prepared = std::chrono::steady_clock::now();
    if (o.threads > 1) ROOT::EnableImplicitMT(o.threads);
    ROOT::RDataFrame df("Events", o.inputs);
    Node node(df);
    std::set<std::string> triggerColumns(ts.mu.begin(), ts.mu.end());
    triggerColumns.insert(ts.ele.begin(), ts.ele.end());
    for (const auto& t : triggerColumns) {
        if (!input.schema.count(t)) {
            std::cerr << "WARNING: missing HLT branch " << t << "; its decision is false" << std::endl;
            node = node.Define(t, [] { return false; });
        }
    }
    auto total = node.Count();
    const Strings multiplicities = {"nTrigObj", "nMuon", "nElectron", "nJet", "nPhoton"};
    std::vector<Count> rejected;
    for (const auto& m : multiplicities) rejected.push_back(node.Filter(m + " > 50").Count());
    node = node.Filter("nTrigObj <= 50 && nMuon <= 50 && nElectron <= 50 && nJet <= 50 && nPhoton <= 50",
                       "Legacy multiplicity veto");
    auto afterMultiplicity = node.Count();
    // Keep explicit integer flags for the nominal channel-specific Table 9 ORs.
    node = node.Define("passTrigMuTable9", "int(" + logicalOR(ts.mu) + ")")
               .Define("passTrigEleTable9", "int(" + logicalOR(ts.ele) + ")");
    std::string filters = "Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && "
                          "Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && "
                          "Flag_BadPFMuonFilter && Flag_eeBadScFilter";
    if (o.year == "2017" || o.year == "2018") filters += " && Flag_ecalBadCalibFilter";
    auto filtered = node.Filter(filters, "Event filters");
    auto afterFilters = filtered.Count();
    auto selected = filtered.Filter("passTrigMuTable9 || passTrigEleTable9", "Table 9 trigger OR");
    auto saved = selected.Count();
    for (const auto& name : {"passTrigMuTable9", "passTrigEleTable9"})
        input.columns.push_back(name);
    ROOT::RDF::RSnapshotOptions snapshotOptions;
    // All counts are already booked. An immediate Snapshot runs them together
    // and avoids ROOT 6.30's false lazy-Snapshot warning after MT cleanup.
    snapshotOptions.fLazy = false;
    // Match the original file's compression setting 207 (LZMA, level 7).
    snapshotOptions.fCompressionAlgorithm = ROOT::kLZMA;
    snapshotOptions.fCompressionLevel = 7;
    std::cout << "Processing " << input.events << " events using " << o.threads << " thread(s)" << std::endl;
    auto snapshot = selected.Snapshot("Events", temporary, input.columns, snapshotOptions);
    snapshot.GetValue(); // Already ready; no additional event loop.
    if (*total != static_cast<ULong64_t>(input.events)) throw std::runtime_error("Input entry count mismatch");
    if (df.GetNRuns() != 1) throw std::runtime_error("Internal error: more than one RDF event loop");
    {
        std::unique_ptr<TFile> f(TFile::Open(temporary.c_str(), "UPDATE"));
        if (!f || f->IsZombie()) throw std::runtime_error("Cannot update snapshot output");
        auto* tree = dynamic_cast<TTree*>(f->Get("Events"));
        if (*saved == 0 && (!tree || tree->GetListOfBranches()->GetEntries() == 0)) {
            restoreEmptySchema(*f, o, input);
            tree = dynamic_cast<TTree*>(f->Get("Events"));
        }
        if (!tree || tree->GetEntries() != static_cast<Long64_t>(*saved))
            throw std::runtime_error("Snapshot saved-entry count mismatch");
        writeCounts("hEvents", "Cutflow", {0., double(*total), double(*afterFilters), double(*saved), 0.},
                    {"", "NanoAOD", "Filters", "MuonOREleTrig", ""}, -1.5, 3.5);
        TH1D sumw("hGenEventSumw", "Generator-weight sum before skimming", 1, .5, 1.5);
        sumw.SetDirectory(nullptr);
        sumw.GetXaxis()->SetBinLabel(1, "genEventSumw"); sumw.SetBinContent(1, input.genSumw); sumw.Write();
        TH1D count("hGenEventCount", "Generated-event count before skimming", 1, .5, 1.5);
        count.SetDirectory(nullptr);
        count.GetXaxis()->SetBinLabel(1, "genEventCount"); count.SetBinContent(1, input.genCount); count.Write();
        f->Close();
        if (f->TestBit(TFile::kWriteError)) throw std::runtime_error("ROOT output write failed");
    }
    if (fs::exists(o.output)) throw std::runtime_error("Output appeared while processing; refusing to replace it");
    fs::rename(temporary, o.output);
    const auto end = std::chrono::steady_clock::now();
    std::cout << "Input events = " << *total << "\nAfter multiplicity veto = " << *afterMultiplicity
              << "\nAfter filters = " << *afterFilters << "\nnEvents_Skim = " << *saved
              << "\nBad Events = " << *total-*afterMultiplicity << std::endl;
    for (std::size_t i = 0; i < multiplicities.size(); ++i)
        std::cout << "  " << multiplicities[i] << " > 50: " << *rejected[i] << std::endl;
    std::cout << std::setprecision(15) << "genEventCount = " << input.genCount << "\ngenEventSumw = " << input.genSumw
              << "\nRDF event loops = " << df.GetNRuns()
              << "\nInput preparation seconds = " << std::chrono::duration<double>(prepared-start).count()
              << "\nProcessing/writing seconds = " << std::chrono::duration<double>(end-prepared).count()
              << "\nOutput = " << o.output << std::endl;
}
} // namespace

int main(int argc, char** argv) {
    if (argc == 2 && std::string(argv[1]) == "--help") {
        std::cout << "Usage: makeSkim [--threads N] [--data|--mc] YEAR JOBofTOTAL OUTPUT.root local|xrootd INPUT.root [...]\n"
                  << "Defaults: four threads; MC unless output name contains Data. Output gains _JOBofTOTAL.\n";
        return 0;
    }
    std::string temporary;
    try {
        const auto options = parse(argc, argv);
        const auto candidate = options.output + ".partial." + std::to_string(getpid()) + ".root";
        if (fs::exists(candidate)) throw std::runtime_error("Temporary output already exists: " + candidate);
        temporary = candidate;
        run(options, temporary);
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ERROR: " << error.what() << std::endl;
        if (!temporary.empty()) {
            std::error_code ignored;
            fs::remove(temporary, ignored);
        }
        return 1;
    }
}
