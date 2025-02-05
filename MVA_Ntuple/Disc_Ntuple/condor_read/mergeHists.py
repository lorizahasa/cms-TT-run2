import os
import sys
import itertools
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("condor_read", ""))
from optparse import OptionParser
from DiscInputs import *
import subprocess

#----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--isCheck","--isCheck", dest="isCheck",action="store_true",default=False, help="Merge for combined years and channels")
parser.add_option("--isSep","--isSep", dest="isSep",action="store_true",default=False, help="Merge for separate years and channels")
parser.add_option("--isComb","--isComb", dest="isMerge",action="store_true",default=False, help="Merge for combined years and channels")
(options, args) = parser.parse_args()
isCheck = options.isCheck
isSep = options.isSep
isComb = options.isMerge

if isCheck:
    isSep  = True
    isComb = False
    Years  = [Years[0]]
    Decays = [Decays[0]]
    Spin  = [Spin[0]]
    Channels = [Channels[0]]
    Samples  = [Samples[0]]
if isSep: 
    isComb = False
if isComb:
    isSep = False
    Years  = Years_ 
    Channels = Channels_
if not isCheck and not isSep and not isComb:
    print("Add either --isCheck or --isSep or --isComb in the command line")
    exit()

def runCmd(cmd):
    print("\n\033[01;32m Excecuting: %s \033[00m"%cmd)
    os.system(cmd)

print("In case of segmentation violation, cmsenv CMSSW_10_2_14")
#Merge separate years and channels

def list_root_files(directory):
    root_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".root"):
            root_files.append(os.path.join(directory, filename))
    return root_files

def hadd_files(input_files, output_file):
    # Chunk size for hadd
    chunk_size = 109  # Adjust as needed

    # Split input files into chunks
    file_chunks = [input_files[i:i+chunk_size] for i in range(0, len(input_files), chunk_size)]

    # List to store the names of merged files
    merged_files = []

    # Loop through chunks and merge
    for i, chunk in enumerate(file_chunks):
        merged_file_name = f"merged_{i}.root"
        merged_files.append(merged_file_name)
        
        # Perform hadd on the current chunk
        hadd_command = "hadd -f -v 0 %s %s"%(merged_file_name," ".join(chunk)) 
        #print(hadd_command)
        #subprocess.run(hadd_command, check=True)
        runCmd(hadd_command)
    # Finally, merge all the chunked merged files into a single output file
    #subprocess.run(["hadd -f ", output_file] + merged_files, check=True)
    runCmd("hadd -f -v 0 %s %s"%(output_file, " ".join(merged_files)))

    # Clean up: delete the chunked merged files
    for file in merged_files:
        runCmd("rm %s"%file)
        
#-----------------------------------------
if isSep:
    for y, d, p, c in itertools.product(Years, Decays, Spin,  Channels):
        histDir  = "%s/Reader/%s/%s/%s/%s/CombMass/BDTA"%(dirRead, y, d, p, c)
        mergeDir = histDir.replace("Reader", "Merged")
        #if os.path.exists("/eos/uscms/%s"%mergeDir):
        runCmd("eos root://cmseos.fnal.gov rm -r %s"%mergeDir)
        runCmd("eos root://cmseos.fnal.gov mkdir -p %s"%mergeDir)
        #Merge for all sample
        haddOut = "root://cmseos.fnal.gov/%s/AllInc.root"%(mergeDir)
       # haddIn  = "`xrdfs root://cmseos.fnal.gov ls -u %s | grep \'.*root\'`"%(histDir)
        haddIn_List = list_root_files("/eos/uscms/%s"%histDir)
        #print(haddIn_List)
        hadd_files(haddIn_List, haddOut)
       # runCmd("hadd -f -k %s %s"%(haddOut, haddIn))
        print(runCmd(("eos root://cmseos.fnal.gov find --size %s")%mergeDir))

#-----------------------------------------
#Merge combining years and channels
#-----------------------------------------
if isComb:
    for year, d, ch in itertools.product(Years_, Decays, Channels_): 
        hists = []
        for y in year.split("__"):
            for c in ch.split("__"):
                iSubDir = "%s/Merged/%s/%s/%s/CombMass/BDTA/AllInc.root"%(dirRead, y, d, c)
                iFullDir = "root://cmseosmgm01.fnal.gov:1094/%s"%iSubDir
                hists.append(iFullDir)
        haddIn = ' '.join(str(h) for h in hists)
        mergeDir = "%s/Merged/%s/%s/%s/CombMass/BDTA"%(dirRead, year, d, ch)
        runCmd("eos root://cmseos.fnal.gov mkdir -p %s"%mergeDir)
        haddOut = "root://cmseos.fnal.gov/%s/AllInc.root"%(mergeDir)
        runCmd("eos root://cmseos.fnal.gov rm -r %s"%mergeDir)
        runCmd("eos root://cmseos.fnal.gov mkdir -p %s"%mergeDir)
        runCmd("hadd -f -v 0 %s %s"%(haddOut, haddIn))
        print(runCmd(("eos root://cmseos.fnal.gov find --size %s")%mergeDir))
