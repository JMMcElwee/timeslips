for slip in $@
do
    for i in {0..20}
    do
	python TotalAnalysis.py -root smoothed_plots.root -slip $slip
    done
    python TotalAnalysis.py -root smoothed_plots.root -validate -slip $slip
done