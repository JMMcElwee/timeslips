#!/bin/sh

# Awful help checking
if [[ "$@" == *" -h "* || "$@" == *" -h" || "$@" == "-h" ]]
then
    echo "Usage:"
    echo "./extract_distributions.sh  location  "
    echo " --> location : path files are saved in"
    return
    exit
fi 

# Read Arguments
destination=$1
dqfiles="dq-files/"
outname=${destination//\//}
outname=${outname//\./}

echo "=== Read Arguments ==="
echo "File Source : $dqfiles"
echo "Out Name : $outname"

echo "=== Setting up ===";
#export CMTPATH=/usr/local/t2k-software/ND280v11r31
#export CMTROOT=/usr/local/t2k-software/CMT/v1r20p20081118
#source /usr/local/t2k-software/ND280v11r31/nd280/v*r*/cmt/setup.sh "";
#export CMTPATH=/home/jenkins/software/
#export CMTROOT==/home/jenkins/software/CMT/v1r20p20081118
#source /data/perry/t2k-software/ND280v11r31/nd280/v*r*/cmt/setup.sh "";
#source /data/osullivan/timeslips/setupcalibration.sh "";

#source /data/jmcelwee/T2K/timeSlips/setup.sh;

#alias tript="/home/stowell/nd280Rep/soffTasks/v1r39/Linux-x86_64/tript_timeslip_analysis.exe";
echo "=== Running Extractor ==="
cd $destination
#/home/stowell/nd280Rep/soffTasks/v1r39/Linux-x86_64/tript_timeslip_analysis.exe ./dq-tript-rdt_????????_????.root $dqfiles/dq-tript-rdt_????????_????.root -o ${outname}_timeslipscan.root
/sft/t2k-software/ND280v12r25/soffTasks/v1r53/Linux-x86_64/tript_timeslip_analysis.exe ./dq-tript-rdt_????????_????.root $dqfiles/dq-tript-rdt_????????_????.root -o ${outname}_timeslipscan.root
echo "=== Extraction Complete, Copying scripts ==="
cp -v ../../scripts/*.py ./
cp -v ../../scripts/*.sh ./
mkdir ./validation/
mkdir ./tables/
echo "=== Running second smoothing stage ==="
python PlotSmoother.py ${outname}_timeslipscan.root_cosmics_tript.root
echo "=== Smoothing complete. ==="
echo " 1. To process slips first run the MCM to CTM search"
echo " $ source search_mcm_slips.sh "
echo " 2. Then check validations "
echo " $ source search_mcm_slips.sh  -validate"
echo " 3. Then search for normal slips"
echo " $ source search_rmm_slips.sh "
echo " 4. Then validate"
echo " $ source search_rmm_slips.sh  -validate"
echo " 5. When slips are final and validations look good, run the upload script."
echo " $ source upload_all_slips.sh"
echo " 6. Finally make the RMM slip frequency plots"
echo " $ source plot_slip_frequency.sh"
