# python ma5 runMadAnalysis.py
import Top32_UFO

set main.stacking_method = superimpose
#set main.graphic_render = root

import spin32_tgty_bWgbWg.lhe as        tgty_p27GeV
import spin32_tgty_bWgbWg_10GeV.lhe as  tgty_10GeV
import spin32_tgtg_bWgbWg.lhe as        tgtg_p27GeV
import spin32_tgtg_bWgbWg_10GeV.lhe as  tgtg_10GeV

# Histogram drawer (options: matplotlib or root)
#set main.normalize = auto
#set main.stacking_method = normalize2one 
#set selection[1].stacking_method = superimpose

#set tgty_p27GeV.type= tgty_p27GeV
#set tgty_10GeV.type = tgty_10GeV
#set tgtg_p27GeV.type= tgtg_p27GeV
#set tgtg_10GeV.type = tgtg_10GeV

set tgty_p27GeV.backcolor= none
set tgty_10GeV.backcolor = none
set tgtg_p27GeV.backcolor= none
set tgtg_10GeV.backcolor = none

set tgty_p27GeV.linecolor= red
set tgty_10GeV.linecolor = red+3
set tgtg_p27GeV.linecolor= blue
set tgtg_10GeV.linecolor = blue+3

#set tgty.weight = 1
#set tgtg.weight = 1
set tgty_p27GeV.weight = 1
set tgty_10GeV.weight = 1
set tgtg_p27GeV.weight = 1
set tgtg_10GeV.weight = 1

set tgty_p27GeV.xsection = 1
set tgty_10GeV.xsection = 1
set tgtg_p27GeV.xsection = 1
set tgtg_10GeV.xsection = 1

#set tgty.backstyle = hline
#set tgtg.backstyle = dline

# Global event variables
plot MET   40 0 1000 [logY]
plot THT   40 0 6000 [logY]
plot TET   40 0 6000 [logY]
#plot SQRTS 40 0 15000 [logY]
# PT and ETA distributions of all particles
plot  PT(tstar[1]) 40 0  2500 [logY interstate]
plot  PT(tstar~[1]) 40 0  2500 [logY interstate]
plot  PT(t[1]) 40 0  2500 [logY interstate]
plot  PT(t~[1]) 40 0  2500 [logY interstate]
plot  PT(g[1]) 40 0  2500 [logY]
plot  PT(g[2]) 40 0  2500 [logY]
plot  PT(a[1]) 40 0  2500 [logY]


plot ETA(tstar[1]) 40 -8 8 [logY interstate]
plot ETA(tstar~[1]) 40 -8 8 [logY interstate]
plot ETA(t[1]) 40 -8 8 [logY interstate]
plot ETA(t~[1]) 40 -8 8 [logY interstate]
plot ETA(g[1]) 40 -8 8 [logY]
plot ETA(g[2]) 40 -8 8 [logY]
plot ETA(a[1]) 40 -8 8 [logY]

define wdec = u d s c b u~ d~ s~ c~ b~ vl vl~ l+ l- ta+ ta-
plot  PT(wdec[1]) 40 0  2500 [logY]
plot  PT(wdec[2]) 40 0  2500 [logY]
plot  PT(wdec[3]) 40 0  2500 [logY]
plot  PT(wdec[4]) 40 0  2500 [logY]
plot  PT(wdec[5]) 40 0  2500 [logY]
plot  PT(wdec[6]) 40 0  2500 [logY]

plot ETA(wdec[1]) 40 -8 8 [logY]
plot ETA(wdec[2]) 40 -8 8 [logY]
plot ETA(wdec[3]) 40 -8 8 [logY]
plot ETA(wdec[4]) 40 -8 8 [logY]
plot ETA(wdec[5]) 40 -8 8 [logY]
plot ETA(wdec[6]) 40 -8 8 [logY]

plot PHI(wdec[1]) 40 -8 8 [logY]
plot PHI(wdec[2]) 40 -8 8 [logY]
plot PHI(wdec[3]) 40 -8 8 [logY]
plot PHI(wdec[4]) 40 -8 8 [logY]
plot PHI(wdec[5]) 40 -8 8 [logY]
plot PHI(wdec[6]) 40 -8 8 [logY]

plot DELTAR(tstar[1], tstar~[1]) 40 0 10 [allstate]
plot DELTAR(tstar[1], a[1]) 40 0 10 [allstate]
plot DELTAR(tstar~[1], a[1]) 40 0 10 [allstate]
plot DELTAR(tstar[1], g[1]) 40 0 10 [allstate]
plot DELTAR(tstar~[1], g[1]) 40 0 10 [allstate]
plot DELTAR(tstar[1], g[2]) 40 0 10 [allstate]
plot DELTAR(tstar~[1], g[2]) 40 0 10 [allstate]
plot DELTAR(t[1], t~[1]) 40 0 10 [allstate]
plot DELTAR(t[1], a[1]) 40 0 10 [allstate]
plot DELTAR(t[1], g[1]) 40 0 10 [allstate]
plot DELTAR(t[1], g[2]) 40 0 10 [allstate]
plot DELTAR(g[1], a[1]) 40 0 10 [allstate]
plot DELTAR(g[1], g[2]) 40 0 10 [allstate]

plot M(tstar[1])   200 950 1050 [logY allstate]
plot M(tstar~[1])   200 950 1050 [logY allstate]
plot M(t[1] g[1])   200 950 1050 [logY allstate]
plot M(t~[1] a[1])   200 950 1050 [logY allstate]
plot M(t~[1] g[2])   200 950 1050 [logY allstate]
plot M(t[1])   100 0 300 [logY allstate]
plot M(t~[1])   100 0 300 [logY allstate]
plot M(g[1])   100 -100 100 [logY allstate]
plot M(g[2])   100 -100 100 [logY allstate]
plot M(a[1])   100 -100 100 [logY allstate]
plot  M(t[1] t~[1]) 200 0  2400 [allstate]
plot  M(c s~ b) 40 100  250 [logY]
plot  M(mu- vm~  b~) 40 100  250 [logY]
plot  M(c s~ b g[1]) 200 950 1050 [logY]
plot  M(mu- vm~  b~ a[1]) 200 950 1050 [logY]
plot  M(mu- vm~  b~ g[2]) 200 950 1050 [logY]
submit out_spin32
exit
