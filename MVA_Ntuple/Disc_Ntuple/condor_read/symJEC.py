import ROOT
import os
import sys
import math
import itertools
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("condor_read", ""))
from DiscInputs import *

input_dirs = dirRead

def symmetrize_histograms(input_filename, output_filename):
    # Open the input and output ROOT files
    input_file = ROOT.TFile.Open(input_filename, "READ")
    output_file = ROOT.TFile.Open(output_filename, "RECREATE")

    # Loop over top-level directories in the input file
    for key in input_file.GetListOfKeys():
        if key.GetClassName() != 'TDirectoryFile':
            continue  # Skip non-directory objects
        top_level_dir = key.ReadObj()
        top_level_dir_name = top_level_dir.GetName()
        print(f"Processing top-level directory: {top_level_dir_name}")

        # Create the same directory in the output file
        output_file.mkdir(top_level_dir_name)

        # Loop over subdirectories
        for subkey in top_level_dir.GetListOfKeys():
            if subkey.GetClassName() != 'TDirectoryFile':
                continue
            sub_dir = subkey.ReadObj()
            sub_dir_name = sub_dir.GetName()
            print(f"  Processing sub-directory: {sub_dir_name}")

            # Create corresponding subdirectory in the output file
            output_file.cd(top_level_dir_name)
            ROOT.gDirectory.mkdir(sub_dir_name)

            # Get the nominal histograms from the "JetBase" directory
            jetbase_dir = sub_dir.Get("JetBase")
            if not jetbase_dir:
                print(f"JetBase directory not found in {top_level_dir_name}/{sub_dir_name}")
                continue

            nominal_hists = {
                "Disc": jetbase_dir.Get("Disc"),
                "Reco_mass_T": jetbase_dir.Get("Reco_mass_T"),
            }

            for hist_name, nominal_hist in nominal_hists.items():
                if not nominal_hist:
                    print(f"Histogram '{hist_name}' not found in JetBase in {top_level_dir_name}/{sub_dir_name}")
                    continue

                # Prepare dictionaries to hold Up and Down histograms
                up_histograms = {}
                down_histograms = {}

                # Loop over systematic variation directories
                for sub_subkey in sub_dir.GetListOfKeys():
                    if sub_subkey.GetClassName() != 'TDirectoryFile':
                        continue
                    sub_sub_dir = sub_subkey.ReadObj()
                    sub_sub_dir_name = sub_sub_dir.GetName()

                    # Check for directories starting with "JEC_"
                    if sub_sub_dir_name.startswith("JE"):
                        #print(f" Symmetrizing JEC directory: {sub_sub_dir_name}")
                        hist = sub_sub_dir.Get(hist_name)
                        if not hist:
                            continue
                        # Determine if it's Up or Down variation
                        if sub_sub_dir_name.endswith("Up"):
                            syst_name = sub_sub_dir_name[:-2]
                            up_histograms[syst_name] = hist
                        elif sub_sub_dir_name.endswith("Down"):
                            syst_name = sub_sub_dir_name[:-4]
                            down_histograms[syst_name] = hist

                    if not sub_sub_dir_name.startswith("JE") and sub_sub_dir_name != "JetBase":
                        print(f"  Copying non-JEC sub-sub-directory: {sub_sub_dir_name}")
                        output_file.cd(f"{top_level_dir_name}/{sub_dir_name}")
                        output_dir = ROOT.gDirectory.GetDirectory(sub_sub_dir_name) or ROOT.gDirectory.mkdir(sub_sub_dir_name)
                        output_file.cd(f"{top_level_dir_name}/{sub_dir_name}/{sub_sub_dir_name}")
                        for obj_key in sub_sub_dir.GetListOfKeys():
                            obj = obj_key.ReadObj()
                            obj.Write()

                # Symmetrize histograms for each systematic variation
                for syst_name in up_histograms.keys():
                    if syst_name not in down_histograms:
                        print(f" Missing Down histogram for {syst_name} in {top_level_dir_name}/{sub_dir_name}")
                        continue
                    up_hist = up_histograms[syst_name]
                    down_hist = down_histograms[syst_name]

                    # Clone histograms for symmetrization
                    up_hist_sym = up_hist.Clone(hist_name)
                    down_hist_sym = down_hist.Clone(hist_name)

                    # Perform symmetrization bin by bin
                    nbins = nominal_hist.GetNbinsX()
                    for i in range(1, nbins + 1):
                        N_i = nominal_hist.GetBinContent(i)
                        U_i = up_hist.GetBinContent(i)
                        D_i = down_hist.GetBinContent(i)
                        E_U = up_hist.GetBinError(i)
                        E_D = down_hist.GetBinError(i)

                        # Avoid division by zero
                        if N_i != 0:
                            deltaU_i = (U_i - N_i) / N_i
                            deltaD_i = (D_i - N_i) / N_i
                            avg_delta = (abs(deltaU_i) + abs(deltaD_i)) / 2.0
                            deltaU_i_new = avg_delta
                            deltaD_i_new = -avg_delta
                            U_i_new = N_i * (1 + deltaU_i_new)
                            D_i_new = N_i * (1 + deltaD_i_new)
                        else:
                            U_i_new = N_i
                            D_i_new = N_i

                        # Set the new bin contents and errors
                        up_hist_sym.SetBinContent(i, U_i_new)
                        down_hist_sym.SetBinContent(i, D_i_new)
                        up_hist_sym.SetBinError(i, E_U)
                        down_hist_sym.SetBinError(i, E_D)

                    # Write the symmetrized histograms to the output file
                    output_file.cd(f"{top_level_dir_name}/{sub_dir_name}")
                    up_dir_name = syst_name + "Up"
                    down_dir_name = syst_name + "Down"

                    up_dir = ROOT.gDirectory.GetDirectory(up_dir_name) or ROOT.gDirectory.mkdir(up_dir_name)
                    down_dir = ROOT.gDirectory.GetDirectory(down_dir_name) or ROOT.gDirectory.mkdir(down_dir_name)

                    up_dir.cd()
                    up_hist_sym.Write(hist_name, ROOT.TObject.kOverwrite)
                    down_dir.cd()
                    down_hist_sym.Write(hist_name, ROOT.TObject.kOverwrite)

            # Copy the nominal histograms from JetBase
            output_file.cd(f"{top_level_dir_name}/{sub_dir_name}")
            jetbase_output_dir =ROOT.gDirectory.GetDirectory("JetBase") or ROOT.gDirectory.mkdir("JetBase")
            jetbase_output_dir.cd()
            for hist_key in jetbase_dir.GetListOfKeys():
                hist = hist_key.ReadObj()
                hist.Write()

    # Close the ROOT files
    input_file.Close()
    output_file.Close()


for year, decay, channel in itertools.product(Years, Decays, Channels):
    input_dir = f"{input_dirs}/Rebin/{year}/{decay}/{channel}/CombMass/BDTA"
    output_dir = input_dir.replace("Rebin", "AdjustForMain")

    # Create the output directory if it doesn't exist
    os.system(f"eos root://cmseos.fnal.gov mkdir -p {output_dir}")

    input_file_path = f"root://cmseos.fnal.gov/{input_dir}/AllInc.root"
    output_file_path = f"/eos/uscms/{output_dir}/AllInc.root"

    # Process the file
    print(f"Processing: {input_file_path}")
    symmetrize_histograms(input_file_path, output_file_path)
    print(f"Output written to: {output_file_path}")

