VALID=""
for arg in "$@"
do 
    if [[ $arg == "-v" ]] 
    then 
	VALID="-validate"
	echo -e "\e[34;1m[INFO]\e[0m Validating slips."
    else
	echo -e "\e[33;1m[ERROR]\e[0m Unknown argument... just going to ignore it."
    fi
done

python TotalAnalysis.py -slip MCMtoCTM -root smoothed_plots.root $VALID
