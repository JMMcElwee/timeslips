#!/bin/sh

# Awful help checking
if [[ "$@" == *" -h "* || "$@" == *" -h" || "$@" == "-h" ]]
then
    echo "Usage:"
    echo "./download_new_cosmicfiles.sh  destination  [startrun]  [endrun]"
    echo " --> destination : path to save files to"
    echo " --> startrun    : Lower run limit. Only run numbers above this downloaded."
    echo " --> endrun      : Upper run limit. Run numbers between startrun and endrun downloaded."
    return
    exit
fi 

# Read Arguments
totaldownloads=0
lastdownload=""
destination=$1
lower=$2
higher=$3
echo "=== Read Arguments ==="
echo "destination : $destination"
echo "startrun    : $lower"
echo "endrun      : $higher"

if [[ "$destination" == "" ]]
then
    echo "First argument should be valid destination!"
    return
    exit
fi

echo "=== Setting up ==="
# Changed the iRods path because the cluster is on Fire
#source /usr/local/t2k-software/setup-irods.sh
source /data/jmcelwee/T2K/timeSlips/setup-irods.sh
iinit

if [[ ! -e "$destination" ]]
then
    echo "Making $destination folder."
    mkdir $destination
fi

if [[ ! -e "$destination/dq-files/" ]]
then
    echo "Making $destination/dq-files/ folder."
    mkdir $destination/dq-files/
fi

echo "=== Download Search ==="
# Start loop over all folders
for file in $(ils /KEK-T2K/home/dataquality/data/tript/dq-tript-rdt/); 
do 	

    # Skip C- entries
    if [ $file == "C-" ];
    then 
	continue
    fi

    # Loop over all subfiles
    for rmmfile in $(ils $file);
    do
	# Skip bad entries    
	if [[ $rmmfile == *":"  || $rmmfile == "C-" ]]
	then
	    continue
	fi
	
	# Get run number
	baserun=$(basename $rmmfile)

	# Check limits
	if [[ "$lower" != ""  && "$lower" -gt "$baserun" ]]
        then
            continue
        fi
        if [[ "$higher" != ""  && "$higher" -lt "$baserun" ]]
        then
            continue
        fi
	
	# Loop over all files in the valid run
	for rootfile in $(ils $rmmfile);
	do
		    
	    if [[ $rootfile != *".root" ]];
	    then
		continue
	    fi
    
	    # Name DQ File
	    dqfile="$rmmfile/$rootfile"

	    # Check if we already have this dqfile
	    if [ ! -e $destination/dq-files/$rootfile ]
	    then
		echo "Downloading file $rmmfile/$rootfile"
		iget $dqfile $destination/dq-files/
		lastdownload=$baserun
	    fi
	    
	done
    done
done

echo "=== Complete! ==="
