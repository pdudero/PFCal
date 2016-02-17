#!/usr/bin/env python

import os,sys
import optparse
import commands
import math
import random
import time

seed=random.seed()
githash=commands.getstatusoutput('git log --pretty=format:\'%h\' -n 1')[1]
detectorModel=5

mydir='/uscms_data/d2/pdudero/PFCalTB/PFCalEE'

usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-t', '--git-tag'     ,    dest='gittag'             , help='git tag version'          , default=githash)
parser.add_option('-v', '--version'     ,    dest='version'            , help='detector version'         , default=3203,  type=int)
parser.add_option(      '--particle'    ,    dest='particle'           , help='particle type'            , default='e-')
parser.add_option('-N', '--njobs'       ,    dest='njobs'              , help='number of jobs'           , default=1,     type=int)
parser.add_option('-n', '--nevtsperjob' ,    dest='nevtsperjob'        , help='number of events per job' , default=1000,  type=int)
parser.add_option('-e', '--en'          ,    dest='energy'             , help='energy'                   , default=50,    type=float)
parser.add_option('-o', '--out'         ,    dest='out'                , help='output directory'         , default=os.getcwd() )
parser.add_option('-S', '--no-submit', action='store_true', dest='nosubmit', help='Do not submit batch job.')
(opt, args) = parser.parse_args()

print "nevents = ",opt.nevtsperjob
print "njobs = ",opt.njobs
    
#prepare output directory
timeTag=time.time()
#outDir='%s/%s/version_%d/model_%d/'%(opt.out,opt.gittag,opt.version,detectorModel)
outDir='%s'%opt.out
#if '/store/' in outDir:
#    os.system('cmsMkdir %s' % outDir)
#else:
#    os.system('mkdir -p %s' % outDir)
os.system('mkdir -p JOBS')

#wrapper to run the job
scriptFile = open('%s/JOBS/runJob_%s.sh'%(mydir,timeTag), 'w')
scriptFile.write('#!/bin/bash\n')
scriptFile.write('JOBNUM=$1\n')
scriptFile.write('shift\n')                         # the shift is necessary to consume the argument prior to sourcing any other scripts!
scriptFile.write('source ./g4env4lpc.sh\n')
scriptFile.write('OUTFILE=%s_version_%d_model_%d_TBSim_%s_%g_${JOBNUM}\n'%(opt.gittag,opt.version,detectorModel,opt.particle,opt.energy))
#scriptFile.write('cp %s/JOBS/g4steer_%s.mac ./\n'%(os.getcwd(),timeTag))
scriptFile.write('./PFCalTB g4steer_%s_${JOBNUM}.mac %d %d 0 | tee ${OUTFILE}.log\n'%(timeTag,opt.version,detectorModel))
scriptFile.write('mv PFcal.root ${OUTFILE}.root\n')
scriptFile.write('localdir=`pwd`\n')
scriptFile.write('echo "--Local directory is $localdir"\n')
scriptFile.write('ls -l\n')
    # if '/store/' in outDir:
    #     scriptFile.write('mv %s.root /eos/uscms/%s/\n' % (outFile,outDir) )
    #     scriptFile.write('mv %s.log /eos/uscms/%s/\n' % (outFile,outDir) )
        #    scriptFile.write('rm %s.*\n' % outFile)
#elif outDir!=os.getcwd():
#    scriptFile.write('mv %s.root %s/\n' % (outFile,outDir) )
#    scriptFile.write('mv %s.log %s/\n' % (outFile,outDir) )
#    scriptFile.write('rm %s.*\n' % outFile)
scriptFile.write('rm core.*\n')
scriptFile.write('rm g4steer_%s_${JOBNUM}.mac\n' %(timeTag))
scriptFile.write('echo "All done"\n')
scriptFile.close()
os.system('chmod u+rwx %s/JOBS/runJob_%s.sh'%(mydir,timeTag))
    
#write geant 4 macro
#
# NEED njobs mac files for njobs different random seeds
#
for j in xrange(0,opt.njobs):
    g4Macro = open('%s/JOBS/g4steer_%s_%d.mac' %(mydir,timeTag,j), 'w')
    g4Macro.write('/control/verbose 0\n')
    g4Macro.write('/control/saveHistory\n')
    g4Macro.write('/run/verbose 0\n')
    g4Macro.write('/event/verbose 0\n')
    g4Macro.write('/tracking/verbose 0\n')
    g4Macro.write('/N03/det/setField 0 T\n')
    g4Macro.write('/N03/det/setModel %d\n'%detectorModel)
    g4Macro.write('/random/setSeeds %d %d\n'%( random.uniform(0,100000), random.uniform(0,100000) ) )
    g4Macro.write('/generator/select particleGun\n')
    g4Macro.write('/gun/particle %s\n' % opt.particle )
    g4Macro.write('/gun/energy %f GeV\n' % opt.energy )
    g4Macro.write('/gun/direction 0.0 0.0 1.0\n')
    g4Macro.write('/run/beamOn %ld\n'%(opt.nevtsperjob))
    g4Macro.close()

# Condor jdl file
jdlFile = open('%s/JOBS/submitProd_%s.jdl'%(mydir,timeTag), 'w')
jdlFile.write('Executable = %s/JOBS/runJob_%s.sh\n'%(mydir,timeTag))
jdlFile.write('Universe = vanilla\n')
jdlFile.write('Requirements = FileSystemDomain=="fnal.gov" && Arch=="X86_64"\n')
jdlFile.write('Notification = ERROR\n')
jdlFile.write('Should_Transfer_Files = YES\n')
jdlFile.write('WhenToTransferOutput = ON_EXIT\n')
jdlFile.write('x509userproxy = $ENV(X509_USER_PROXY)\n')
for j in xrange(0,opt.njobs):
    jdlFile.write('Arguments = %d\n'%j)
    jdlFile.write('transfer_input_files = %s/g4env4lpc.sh,%s/JOBS/g4steer_%s_%d.mac,%s/bin/Linux-g++/PFCalTB,%s/tmp/Linux-g++/PFCalTB/libPFCalTB.so,%s/userlib/lib/libPFCalTBuserlib.so\n'%(mydir,mydir,timeTag,j,os.environ['G4WORKDIR'],os.environ['G4WORKDIR'],mydir))
    jdlFile.write('Error = pfcaltb_%s_%d.stderr\n'%(timeTag,j))
    jdlFile.write('Output = pfcaltb_%s_%d.stdout\n'%(timeTag,j))
    jdlFile.write('Queue\n')

jdlFile.close()
    
#submit
if opt.nosubmit : os.system('echo condor_submit %s/JOBS/submitProd_%s.jdl'%(mydir,timeTag))
else:             os.system('condor_submit %s/JOBS/submitProd_%s.jdl'%(mydir,timeTag))
