export USERBASE=`pwd`
source /afs/cern.ch/sw/lcg/contrib/gcc/4.6/x86_64-slc6-gcc46-opt/setup.sh 
export QTHOME=/afs/cern.ch/sw/lcg/external/qt/4.8.4/x86_64-slc6-gcc46-opt/
export G4BASE=/afs/cern.ch/sw/lcg/external/geant4
export DAWNHOME=/afs/cern.ch/sw/lcg/external/dawn/3_88a/x86_64-slc5-gcc43-opt/
export G4DAWNFILE_DEST_DIR=/afs/cern.ch/work/a/amagnan/DawnFiles/
export HEPMC_DIR=/afs/cern.ch/sw/lcg/external/HepMC/2.06.08/x86_64-slc6-gcc46-opt/
export FASTJET_INSTALL=/afs/cern.ch/sw/lcg/external/fastjet/3.0.3/x86_64-slc6-gcc46-opt/
cd $G4BASE/9.6.p02/x86_64-slc6-gcc46-opt/share/Geant4-9.6.2/geant4make/
source geant4make.sh
cd - &> /dev/null
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$XERCESCROOT/lib:$HEPMC_DIR/lib:$USERBASE/userlib/lib:$USERBASE/analysis/lib:$FASTJET_INSTALL/lib
#source /afs/cern.ch/sw/lcg/contrib/gcc/4.6/x86_64-slc6/setup.sh
cd /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.18/x86_64-slc6-gcc46-opt/root/
source bin/thisroot.sh
cd - &> /dev/null
export PATH=$DAWNHOME/bin:$PATH:$FASTJET_INSTALL/bin
