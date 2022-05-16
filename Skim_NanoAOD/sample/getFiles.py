import os
import sys
import subprocess
import numpy as np
sys.dont_write_bytecode = True
from SamplesNano import sampleDict 
sys.path.insert(0, os.getcwd().replace("sample",""))
from SkimInputs import *

#Function to fetch the name of all files in one string
def getFileList(sample, isDAS=True):
    if isDAS:
        std_output, std_error = subprocess.Popen("dasgoclient --query='file dataset=%s status=*'"%sample,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
    else:
        std_output, std_error = subprocess.Popen("xrdfs root://cmseos.fnal.gov/ ls -u %s | grep '.root'"%sample,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
    names = std_output.decode("ascii").replace('\n',' ')
    return names

#Function to print the total events in nice format 
def getEvents(sample):
    std_output, std_error = subprocess.Popen("dasgoclient --query='summary dataset=%s'"%sample,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
    num = eval(std_output)[0]['nevents']
    rawNum = num
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    evtStr = '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
    unit = evtStr[-1]
    formatStr = "%s%s"%(round(float(evtStr.replace(unit, '')), 1), unit)
    return [rawNum, formatStr] 


#Store the ouputs in two separate files
f1 = open("FilesNano_cff.sh", "w")
f2 = open("JobsNano_cff.py", "w")

allJobs = 0
for year in Years: 
#for year in ['2017']: 
    splitJobs = {}
    print '---------------------------------------'
    print  year 
    print  "nFiles\t  nJobs\t nEvents\t Samples"
    print '---------------------------------------'
    line = ""
    jobs = 0
    for sampleName, sample in sampleDict(year).items():
        line += '%s_FileList_%s="'%(sampleName,year)
        if '/store/user/' in sample:
            fileList = getFileList(sample, False)
            line += fileList
            line += '"\n\n'
        else:
            line += "xrootd "
            fileList = getFileList(sample, True)
            line += fileList 
            line += '"\n\n'
        if fileList=='':
            print ("PROBLEM: %s \n"%sample)
            continue
        nFiles = len(fileList.split(" "))
        evt     = getEvents(sample)[0]
        evtStr  = getEvents(sample)[1]
        evtPerJob = 5e6 #5 million
        nJob = int(np.ceil(evt/evtPerJob))
        if nFiles<nJob: 
            nJob = nFiles
        #evt = "NA" 
        splitJobs[sampleName] = [nJob, evtStr, evt, nFiles]
        jobs += nJob
        print("%i\t %i\t %s\t %s"%(nFiles, nJob, evtStr, sampleName))
    f1.write(line.encode('ascii'))
    f2.write("Samples_%s = %s \n"%(str(year), str(splitJobs)))
    f2.write("AllJobs_%s = %s \n"%(str(year), str(jobs)))
    print '=================='
    print "AllJobs_%s = %i"%(year, jobs)
    print '=================='
    allJobs += jobs
f2.write("AllJobs_AllYears = %s \n"%str(allJobs))
 
