
for i in {0..11}
do
    python TotalAnalysis.py -root smoothed_plots.root -slip ECalRMM${i}  $@ 
done

for i in {0..5}
do
    python TotalAnalysis.py -root smoothed_plots.root -slip P0DRMM${i}  $@ 
done

for i in {0..3}
do
    python TotalAnalysis.py -root smoothed_plots.root -slip SMRDRMM${i}  $@ 
done

