#!/bin/bash

#NEVT=100
NEVT=100000
NJOB=1

siThicknesses=(120 200 320)
#siThicknesses=(200 320)
#pbX0=(1 2)
pbX0=(0)

#muon runs
# for thick in ${siThicknesses[@]}; do 
#     for x0 in ${pbX0[@]}; do 
# 	python scripts/submitFastTimeTestBeamProd.py -q 8nh -n 50000 -e 150 --particle mu- -v ${thick}${x0} -o /store/cmst3/group/hgcal/TimingTB_H2_Jul2015/SIM; 
#     done 
# done

#electron runs
for thick in ${siThicknesses[@]}; do 
    for x0 in ${pbX0[@]}; do 
	echo "python scripts/submitFastTimeTestBeamProd@LPC.py -S -n $NEVT -N $NJOB -e 50 --particle e- -v ${thick}${x0}"
	python scripts/submitFastTimeTestBeamProd@LPC.py -S -n $NEVT -N $NJOB -e 50 --particle e- -v ${thick}${x0}
   done 
done

