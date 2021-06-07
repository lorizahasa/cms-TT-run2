import subprocess
import sys

directory = '/store/user/lpctop/TTGamma_FullRun2/BSM_Skims/'
newSamples = []
f1 = open('Skim_NanoAOD_FileLists_cff_danny.sh','w')
fPy = open('Skim_NanoAOD_FileLists_cff_danny.py','w')
f2 = open("Skim_NanoAOD_SplitJobs_cff_danny.py", "w")
allJobs = 0

for year in [2016,2017,2018]:
#for year in [2016]:
    jobsDictPerYear = {}
    nJobsPerYear = 0
    f1.write('eosDir="root://cmseos.fnal.gov/%s%i"'%(directory,year))
    fileList = subprocess.Popen('xrdfs root://cmseos.fnal.gov/ ls %s%i'%(directory, year),shell=True,stdout=subprocess.PIPE).communicate()[0].split('\n')
    allSamples = []
    for x in fileList:
        if len(x)>1:
            sample = x.split('/')[-1]
            sType = sample.split('_%i_skim'%year)[0]
            if 'ext' in sample:
                sType = sample.split('_ext')[0]
            if not sType in allSamples:
                allSamples.append(sType)

    allSamples.sort()
    unUsed = fileList[:]
    
    print allSamples
    #print(unUsed)
    for s in list(set(allSamples)):
        filesPerSample = []
        f1.write("\n")
        line = '%s_FileList_%i="'%(s, year)
        hasAny=False
        sType = '%s%i/%s_%i'%(directory, year, s,year)
        sType_ext = '%s%i/%s_ext'%(directory, year, s)
        for f in fileList:
            if f.startswith(sType) or f.startswith(sType_ext):
                #print(s,f)
                # if '%s_Pt'%s in f: continue
                # if '%s_Tune'%s in f: continue
                # if '%s_erd'%s in f: continue
                hasAny=True
                unUsed.remove(f)
                line += 'root://cmseos.fnal.gov/%s '%(f)
                filesPerSample.append(f)
        line = line[:-1] + '"\n'
        linePy = line
        line = line.replace("root://cmseos.fnal.gov/%s%i"%(directory,year), "${eosDir}")
        if hasAny:
            #print(line)
            f1.write(line.encode('ascii'))
            fPy.write(linePy.encode('ascii'))
        nJobsPerSample = len(filesPerSample)
        nJobsPerYear+=nJobsPerSample
        allJobs += nJobsPerSample
        jobsDictPerYear[s] = nJobsPerSample
    f2.write("Samples_%s = %s \n"%(str(year), str(jobsDictPerYear)))
    f2.write("AllJobs_%s = %s \n"%(str(year), str(nJobsPerYear)))
    print ("Year = %i, nJobs = %i"%(year, nJobsPerYear))
f2.write("AllJobs_AllYears = %s \n"%str(allJobs))
print ("Total jobs for all years = %i"%allJobs)
f2.close()
f1.close()

