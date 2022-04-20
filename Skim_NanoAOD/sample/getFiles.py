import os
import sys
import subprocess
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
    if names=='':
        print ("PROBLEM: %s \n"%sample)
    return names

#Function to print the total events in nice format 
def getEvents(sample):
    std_output, std_error = subprocess.Popen("dasgoclient --query='summary dataset=%s'"%sample,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
    num = eval(std_output)[0]['nevents']
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    evtStr = '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
    unit = evtStr[-1]
    return "%s%s"%(round(float(evtStr.replace(unit, '')), 1), unit)


#Store the ouputs in two separate files
f1 = open("FilesNano_cff.sh", "w")
f2 = open("JobsNano_cff.py", "w")

allJobs = 0
#for year in ['2016PreVFP', '2016PostVFP', '2017', '2018']:
for year in Years: 
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
        nFiles = len(fileList.split(" "))
        nJob = 1
        if nFiles >= 5:
            nJob = int (nFiles/5)
        #evt = "NA" 
        evt = getEvents(sample)
        splitJobs[sampleName] = [nJob, evt]
        jobs += nJob
        print("%i\t %i\t %s\t %s"%(nFiles, nJob, evt, sampleName))
    f1.write(line.encode('ascii'))
    f2.write("Samples_%s = %s \n"%(str(year), str(splitJobs)))
    f2.write("AllJobs_%s = %s \n"%(str(year), str(jobs)))
    print '=================='
    print "AllJobs_%s = %i"%(year, jobs)
    print '=================='
    allJobs += jobs
f2.write("AllJobs_AllYears = %s \n"%str(allJobs))
 
