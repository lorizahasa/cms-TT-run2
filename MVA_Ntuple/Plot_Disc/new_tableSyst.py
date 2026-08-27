import os
import sys
from collections import OrderedDict

# --- inputs you already have ---
systPath = '/eos/uscms/store/user/lhasa/Output/cms-TT-run2/MVA_Ntuple/C/Plot_Disc/PlotMain'
sys.path.insert(0, systPath)
from PlotInputs import *                           # provides Years, SystList_by_year, etc.
from systRatioDisc_ForMain_SepYears import systDict

# ------------- helpers -------------
def tex_escape(s: str) -> str:
    return s.replace('_', r'\_')

def getRange(vals):
    """Return min--max % (with one decimal) of |1 - v| over vals."""
    newVals = [abs(1 - v) for v in vals]
    mn = min(newVals)
    mx = max(newVals)
    return f"{100*mn:.1f}--{100*mx:.1f}"

def safe_range(key: str) -> str:
    try:
        return getRange(systDict[key])
    except KeyError:
        return "--"

# strip trailing _<year> if present; return (base, year_tag or None)
def split_year_tag(sys_name: str):
    for y in Years:
        suf = "_" + y
        if sys_name.endswith(suf):
            return sys_name[:-len(suf)], y
    return sys_name, None

# ------------- collect unique BASE systematics (merge year-tagged names) -------------
base_sys_order = []
for y in Years:
    for s in Syst_w_JER[y]:
        base, _ = split_year_tag(s)
        if base not in base_sys_order:
            base_sys_order.append(base)

# ------------- build rows: for each BASE, fill one chunk per year -------------
sysRows = {}   # base -> list of "muR, eleR, muB, eleB" (len == len(Years))
sortKey = {}   # base -> max upper bound across all years

for base in base_sys_order:
    chunks = []
    max_for_sort = 0.0

    for year in Years:
        # prefer a year-tagged variant if it exists in that year; otherwise use the plain base if present
        if f"{base}_{year}" in SystList_by_year[year]:
            sys_key = f"{base}_{year}"
        elif base in SystList_by_year[year]:
            sys_key = base
        else:
            sys_key = None

        if sys_key is not None:
            muR  = safe_range(f"{year}_Mu_ttyg_Enriched_SR_Resolved_{sys_key}")
            eleR = safe_range(f"{year}_Ele_ttyg_Enriched_SR_Resolved_{sys_key}")
            muB  = safe_range(f"{year}_Mu_ttyg_Enriched_SR_Boosted_{sys_key}")
            eleB = safe_range(f"{year}_Ele_ttyg_Enriched_SR_Boosted_{sys_key}")
        else:
            muR = eleR = muB = eleB = "--"

        chunks.append(f"{muR}, {eleR}, {muB}, {eleB}")

        # update sort key using available numeric uppers
        for v in (muR, eleR, muB, eleB):
            if "--" in v:
                try:
                    hi = float(v.split("--")[1])
                    if hi > max_for_sort:
                        max_for_sort = hi
                except ValueError:
                    pass

    sysRows[base] = chunks
    sortKey[base] = max_for_sort

# ------------- labels (use BASE names now) -------------
label = {
    "Weight_pu": "PU",
    "Weight_mu": "$\\mu$",
    "Weight_pho": "$\\gamma$",
    "Weight_ele": "e",
    "Weight_btag_b": "b",
    "Weight_btag_l": "non-b",
    "Weight_prefire": "PF",
    "Weight_q2": "Q2",
    "Weight_pdf": "PDF",
    "Weight_isr": "ISR",
    "Weight_fsr": "FSR",
    "JEC_Total": "JES",
    "Weight_ttag": "t",
    "JER": "JER",                 # <-- base label for merged JER rows
}
def label_of(base: str) -> str:
    return tex_escape(label.get(base, base))

# ------------- build LaTeX table -------------
# Column format: first column for names, then 4 per year; vertical bars between years
col = "c|"
n_data_cols = 4 * len(Years)
for i in range(n_data_cols):
    col += "c"
    if (i % 4) == 3 and i != n_data_cols - 1:
        col += "|"

table  = "\\cmsTable{\n"                   # keep if you use the macro; otherwise remove the wrapper
table += "\\centering\n"
table += "\\begin{tabular}{%s}\n" % col
table += "\\hline\n"

# header line 1: years
tHead = "Systematic"
for y in Years:
    tHead += " & \\multicolumn{4}{c}{%s}" % y.replace("_", "+")
tHead += "\\\\\n"
table += tHead

# header line 2: channel labels per year
tHead = "Uncertainties"
for _ in Years:
    tHead += "& $\\mu_R$ & $e_R$ & $\\mu_B$ & $e_B$"
tHead += "\\\\\n"
table += tHead

# header line 3: units (%)
tHead = "on"
for _ in Years:
    tHead += "& (\\%) & (\\%) & (\\%) & (\\%)"
tHead += "\\\\\n"
table += tHead
table += "\\hline\n"

# rows (ascending; set reverse=True for descending)
for base in sorted(sysRows.keys(), key=lambda b: sortKey[b]):
    row = f" \\SF{{{label_of(base)}}}"
    for chunk in sysRows[base]:           # one chunk per year
        for val in chunk.split(','):
            row += f"& {val.strip()}"
    row += "\\\\\n"
    table += row

table += "\\hline\n"
table += "\\end{tabular}\n"
table += "}\n"

print(table)

# ------------- write out -------------
out_tex = f"{systPath}/systRatioDisc_ForMain_SepYears.tex"
with open(out_tex, "w") as tableFile:
    tableFile.write(table)
print(f"Wrote: {out_tex}")

