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
      scp /Users/marzouk/mnt/nagoya/ubiquitin_saltbridge/2-doublemutation_A11S24/dual/prodrun/rep${i}/{prodrun.part0002.trr,prodrun.part0002.gro} /Users/marzouk/Desktop/marzouk/github_repos/RESTFEP_analysis/double_sub_mutation/dual/prodrun/rep${i}/
      scp /Users/marzouk/mnt/nagoya/ubiquitin_saltbridge/2-doublemutation_A11S24/refab/prodrun/rep${i}/{prodrun.part0002.trr,prodrun.part0002.gro}   /Users/marzouk/Desktop/marzouk/github_repos/RESTFEP_analysis/double_sub_mutation/ref/prodrun/rep${i}/
      #scp /Users/marzouk/mnt/nagoya/ubiquitin_saltbridge/2-doublemutation_A11S24/refb/prodrun/rep${i}/deltae.part0002.xvg  /Users/marzouk/Desktop/marzouk/analysis_doublemutationeffect_RESTFEP/refb/prodrun/rep${i}/
     
      done

exit 0
