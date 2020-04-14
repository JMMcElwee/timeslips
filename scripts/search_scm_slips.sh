help(){
    echo -e "\e[32;1m[HELP]\e[37m ----- search_scm_slips.sh ----- \e[0m"
    echo -e "\e[32;1m[HELP]\e[0m Syntax:  source search_scm_slips.sh [-d detector] [-v]"
    echo -e "\e[32;1m[HELP]\e[0m Args:"
    echo -e "\e[32;1m[HELP]\e[0m [-d]     Requires a specific sub-detector."
    echo -e "\e[32;1m[HELP]\e[0m [-v]     Use this flag to validate slips."
    echo -e "\e[32;1m[HELP]\e[0m If no args given all sub-detectors will be run."
}


ecal(){
    python TotalAnalysis.py -slip MCMtoECal  -root smoothed_plots.root  $VALID 
}

p0d(){
    python TotalAnalysis.py -slip MCMtoP0D   -root smoothed_plots.root  $VALID
}

smrd(){
    python TotalAnalysis.py -slip MCMtoSMRD  -root smoothed_plots.root  $VALID
}


# Set default values
DET="ALL"
VALID=""

while getopts ":hvd:" opts; do
    case $opts in
        h)
            help
            OPTIND=1
            return;;
        d)
            DET=${OPTARG^^}
            echo -e "\e[34;1m[INFO]\e[0m Sub-detector selected: $DET."
            ;;
        v)
            VALID="-validate"
            echo -e "\e[34;1m[INFO]\e[0m Validating slips."
            ;;
        \?)
            echo -e "\e[33;1m[ERROR]\e[0m Unknown variable... just going to ignore it."
            ;;
        :)
            echo -e "\e[31;1m[ERROR]\e[0m -$OPTARG requires an argument. Try -h for help."
            OPTIND=1
            return;;
    esac
done

OPTIND=1

case $DET in 
    ECAL)
	ecal
	;;
    P0D)
	p0d
	;;
    SMRD)
	smrd
	;;
    ALL)
	ecal
	p0d
	smrd
	;;
    *)
	echo -e "\e[31;1m[ERROR]\e[0m Invalid detector supplied."
	return;;
esac
