python TotalAnalysis.py -slip MCMtoCTM  -root smoothed_plots.root  $@ -validate

python TotalAnalysis.py -slip MCMtoECal  -root smoothed_plots.root  $@ -validate
python TotalAnalysis.py -slip MCMtoP0D  -root smoothed_plots.root  $@ -validate
python TotalAnalysis.py -slip MCMtoSMRD  -root smoothed_plots.root  $@ -validate

for i in {0..4}
do
    python TotalAnalysis.py -root smoothed_plots.root -slip ECalRMM${i}  $@ -validate
done

for i in {0..5}
do
    python TotalAnalysis.py -root smoothed_plots.root -slip P0DRMM${i}  $@ -validate
done

for i in {0..3}
do
    python TotalAnalysis.py -root smoothed_plots.root -slip SMRDRMM${i}  $@ -validate
done

