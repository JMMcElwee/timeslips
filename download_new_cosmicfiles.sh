#!/bin/sh


# ADD A HELP FUNCTION                                                                           
help(){
    echo -e "----- download_new_cosmicfiles.sh -----"
    echo -e "\e[32;1m[HELP]\e[0m Syntax:  source download_new_cosmicfiles.sh <dir> <start> [end] "
    echo -e "\e[32;1m[HELP]\e[0m Args:"
    echo -e "\e[32;1m[HELP]\e[0m <dir>    Directory of time slip work."
    echo -e "\e[32;1m[HELP]\e[0m <start>  Lower run limit. Only run numbers above this downloaded."
    echo -e "\e[32;1m[HELP]\e[0m [end]    Upper run limit. Run numbers between start and end downloaded."
}

# Search for the correct flag, exit if not                                                      
while getopts ":h" option; do
    case $option in
	h)
            help
            OPTIND=0 # Probably bad practice                                                       
            return;;
	\?)
            echo -e "\e[31;1m[ERROR]\e[0m Invalid flag parsed."
            OPTIND=0 # Probably bad practice                                                       
            return;;
    esac
done



# READ ARGUMENTS AND CHECK THEY EXIST
LASTDOWN=""
DEST=$1
LOW=$2
HIGH=$3
echo -e "\e[34;1m[INFO]\e[0m Download destination: $DEST"
echo -e "\e[34;1m[INFO]\e[0m Start run:            $LOW"
echo -e "\e[34;1m[INFO]\e[0m End run:              $HIGH"

if [[ $DEST == "" ]]
then
    echo -e "\e[31;1m[Error]\e[0m First argument should be valid destination!"
    return
fi

if [[ $LOW == "" ]]
then 
    echo -e "\e[31;1m[Error]\e[0m Second argument should be the starting run number!!"
    return
fi


# SETUP IRODS
source $PWD/setup-irods.sh
iinit



# MAKING DESTINATION DIRECTORIES 
if [[ ! -e "$DEST" ]]
then
    echo -e "\e[34;1m[INFO]\e[0m Making directory" $DEST
    mkdir $DEST
fi

if [[ ! -e "$DEST/dq-files/" ]]
then
    echo -e "\e[34;1m[INFO]\e[0m Making directory" $DEST "/dq-files/"
    mkdir $DEST/dq-files/
fi




# START LOOPING OVER FILES TO DOWNLOAD IN IRODS
echo -e "\e[34;1m[INFO]\e[0m Starting data download."
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
	if [[ "$LOW" != ""  && "$LOW" -gt "$baserun" ]]
        then
            continue
        fi
        if [[ "$HIGH" != ""  && "$HIGH" -lt "$baserun" ]]
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
	    if [ ! -e $DEST/dq-files/$rootfile ]
	    then
		echo -e "\e[34;1m[INFO]\e[0m Downloading file $rmmfile/$rootfile"
		iget $dqfile $DEST/dq-files/
		LASTDOWN=$baserun
	    fi
	    
	done
    done
done

echo -e "\e[34;1m[INFO]\e[0m Download complete!"
