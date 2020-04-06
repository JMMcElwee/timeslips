#!/bin/sh


# ADD A HELP FUNCTION
help(){
    echo -e "----- extract_distributions.sh -----"
    echo -e "\e[32;1m[HELP]\e[0m Syntax:  source extract_distributions.sh <dir>  "
    echo -e "\e[32;1m[HELP]\e[0m Args:"
    echo -e "\e[32;1m[HELP]\e[0m <dir>    Directory of time slip work (same as before)."
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


# READ ARGUMENTS AND SET USEFUL VARIABLES
SCRIPTLOC=$PWD/scripts
DEST=$1
DQDIR="dq-files"
OUTFILE=${DEST//\//}

if [[ ! -e $DEST ]]
then
    echo -e "\e[31;1m[ERROR]\e[0m Please supply destination directory."
    return
fi

echo -e "\e[34;1m[INFO]\e[0m File Source: $PWD/$DEST/$DQDIR"
echo -e "\e[34;1m[INFO]\e[0m Out Name:" $OUTFILE"_timeslipscan.root"



# CHECK ND280SYS SET CORRECTLY
if [[ ! -z "$ND280SYS" ]] 
then 
    echo -e "\e[34;1m[INFO]\e[0m \$ND280SYS set to" $ND280SYS
    # Find the extraction script. Saves on hardcoding the position
    EXTRACTOR=$(find $ND280SYS/soffTasks -name "tript_timeslip_analysis.exe")
else
    echo -e "\e[31;1m[ERROR]\e[0m Please set \$ND280SYS to point at your ND280 build." 
    return;
fi



# RUNNING THE EXTRACTOR SCRIPT
cd $DEST
echo -e "\e[34;1m[INFO]\e[0m Moving to directory:" $DEST

echo -e "\e[34;1m[INFO]\e[0m Running the extractor."
$EXTRACTOR ./dq-tript-rdt_????????_????.root $DQDIR/dq-tript-rdt_????????_????.root -o ${OUTFILE//\./}_timeslipscan.root



# ADD SYM LINKS TO THE ANALYSIS SCRIPTS
echo -e "\e[34;1m[INFO]\e[0m Extraction complete. Linking analysis scripts."

# See if scripts exist
SCRIPTS=$PWD/search_mcm_slips.sh
if [[ -f "$SCRIPTS" ]]
then 
    echo -e "\e[34;1m[INFO]\e[0m Analysis scripts already exist."
else
    ln -s $SCRIPTLOC/* .
    echo -e "\e[34;1m[INFO]\e[0m Creating links to scripts."
fi

echo -e "\e[34;1m[INFO]\e[0m Making analysis directories."
VAL=validation
TAB=tables
if [[ ! -e $VAL ]]; then
    mkdir $VAL
fi
if [[ ! -e $TAB ]]; then
    mkdir $TAB
fi


# SECOND SMOOTHING STAGE
echo -e "\e[34;1m[INFO]\e[0m Running second smoothing stage (PlotSmoother.py).. making it smooooothier."
python PlotSmoother.py ${OUTFILE}_timeslipscan.root_cosmics_tript.root

echo -e "\e[34;1m[INFO]\e[0m Smoothing complete. Time to find some slips!"
