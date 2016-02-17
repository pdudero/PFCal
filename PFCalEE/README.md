# PFCalEE

Geant4 simulation of a Si-base sampling calorimeter

See the README for the repo from which this one was forked for all other instructions:
https://github.com/pfs/PFCal/tree/fasttime_TB/PFCalEE

Changes are as follows:

## Setup the environment (SLC6)

source g4env4lpc.csh (csh)
source g4env4lpc.sh (sh)

## Compile

The GNUmakefile, source code and scripts have been changed so that PFCalEE -> PFCalTB. This is because
I was playing with both the master and testbeam ("fasttime_TB") branches and wanted the two
libraries to coexist. 


## Submit jobs

cd scripts
submitFTTBJobs@LPC.sh # which calls submitFastTimeTestBeamProd@LPC.py, edit as necessary first
