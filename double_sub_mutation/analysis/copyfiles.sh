#!/bin/bash
if [ -z "$2" ]
then
   echo :Usage ./$( basename $0 ) first replica and last replica
   exit 1
fi

fr=$1 # first replica 
lr=$2  # last replica 

COMMAND=$(cd $(dirname $0) && pwd)

for i in   `seq ${fr} ${lr} ` ; do
      scp /Users/marzouk/mnt/nagoya/ubiquitin_saltbridge/1-doublemutation_A11S24/dual1/prodrun/rep${i}/deltae.part0002.xvg  /Users/marzouk/Desktop/marzouk/analysis_doublemutationeffect_RESTFEP/dual/prodrun/rep${i}/
      scp /Users/marzouk/mnt/nagoya/ubiquitin_saltbridge/1-doublemutation_A11S24/refa/prodrun/rep${i}/deltae.part0002.xvg  /Users/marzouk/Desktop/marzouk/analysis_doublemutationeffect_RESTFEP/refa/prodrun/rep${i}/
      scp /Users/marzouk/mnt/nagoya/ubiquitin_saltbridge/1-doublemutation_A11S24/refb/prodrun/rep${i}/deltae.part0002.xvg  /Users/marzouk/Desktop/marzouk/analysis_doublemutationeffect_RESTFEP/refb/prodrun/rep${i}/
     
      done

exit 0
