from ROOT import *
import sys
from array import array
import time
from SearchRoutines import *

vetos = []

#_______________________________________________
if __name__=="__main__":

    #_______________________________________________
    # Parameters
    res = 180           # Time window resolution in seconds
    smooth_count = 2   # Number of smoothing iterations (alternates between mean/median)
           
    #_______________________________________________               
    # Get CS Plots
    infile_cs = TFile(sys.argv[1],"READ")
    
    # Read graphs from file
    allgraphs_cs_p0d  = []
    allgraphs_cs_smrd = []
    allgraphs_cs_ecal = []

    for i in xrange(0,12):
        plot = infile_cs.Get("ECal_RMM"+str(i)+"_MeanTime60_Constrained1_Smoothed3")
        plot.SetTitle("Cosmic ECalRMM"+str(i))   

        allgraphs_cs_ecal.append(plot)

    for i in xrange(0,6):
        plot = infile_cs.Get("P0D_RMM"+str(i)+"_MeanTime60_Constrained1_Smoothed3")
        plot.SetTitle("Cosmic P0DRMM"+str(i))

        allgraphs_cs_p0d.append(plot)

    for i in xrange(0,4):
        plot = infile_cs.Get("SMRD_RMM"+str(i)+"_MeanTime60_Constrained1_Smoothed3")
        plot.SetTitle("Cosmic SMRDRMM"+str(i))

        allgraphs_cs_smrd.append(plot)

    #_______________________________________________
    # Make Window Mean Plots
    for rmmlist in [allgraphs_cs_ecal, allgraphs_cs_p0d, allgraphs_cs_smrd]:
        for rmm in range(len(rmmlist)):
            rmmlist[rmm] = MakeWindowMeanPlot(rmmlist[rmm], res, 1, vetos)

    #_______________________________________________
    # Make Combination Plots
    graph_cs_ecal = CombinePlots(allgraphs_cs_ecal, "Cosmic All ECalRMMS")
    graph_cs_ecal = MakeWindowMeanPlot(graph_cs_ecal,res*2,1,vetos)

    graph_cs_p0d  = CombinePlots(allgraphs_cs_p0d, "Cosmic All P0DRMMS")
    graph_cs_p0d  = MakeWindowMeanPlot(graph_cs_p0d,res*2,1,vetos)
    
    graph_cs_smrd = CombinePlots(allgraphs_cs_smrd, "Cosmic All SMRDRMMS")    
    graph_cs_smrd = MakeWindowMeanPlot(graph_cs_smrd,res*2,1,vetos)

    graph_mcm_to_ctm = CombinePlots([graph_cs_ecal,graph_cs_p0d,graph_cs_smrd],"MCMtoCTM Finder")
    graph_mcm_to_ctm = MakeWindowMeanPlot(graph_mcm_to_ctm, res*2,1,vetos)

    #_______________________________________________
    # Save plots before smoothing
    outFile = TFile(("smoothed_plots.root"),"RECREATE")

    for plot in [graph_cs_ecal, graph_cs_p0d, graph_cs_smrd, graph_mcm_to_ctm]:
        plot.Write(plot.GetTitle().replace(" ","_") + "_UNSMOOTHED")
    
    for plot in allgraphs_cs_ecal:
        plot.Write(plot.GetTitle().replace(" ","_") + "_UNSMOOTHED")

    for plot in allgraphs_cs_smrd:
        plot.Write(plot.GetTitle().replace(" ","_") + "_UNSMOOTHED")
        
    for plot in allgraphs_cs_p0d:
        plot.Write(plot.GetTitle().replace(" ","_") + "_UNSMOOTHED")

    #_______________________________________________
    # Smoothing Count
    for rmmlist in [allgraphs_cs_ecal, allgraphs_cs_p0d, allgraphs_cs_smrd]:
        for rmm in range(len(rmmlist)):
            print "Smoothing Plot :",rmmlist[rmm].GetTitle()
            for iteration in range(smooth_count):
                # if iteration % 2 != 0:
                rmmlist[rmm] = StepPlot(rmmlist[rmm], 4.0)
                rmmlist[rmm] = SmoothPlot(rmmlist[rmm], iteration)    

    print "Smoothing Combined Plots"
    graph_cs_ecal    = StepPlot(graph_cs_ecal, 4.0)
    graph_cs_p0d     = StepPlot(graph_cs_p0d, 4.0)
    graph_cs_smrd    = StepPlot(graph_cs_smrd, 4.0)
    graph_mcm_to_ctm = StepPlot(graph_mcm_to_ctm, 4.0)
    for iteration in range(smooth_count/2):
        graph_cs_ecal    = SmoothPlot(graph_cs_ecal, iteration)
        graph_cs_p0d     = SmoothPlot(graph_cs_p0d, iteration)
        graph_cs_smrd    = SmoothPlot(graph_cs_smrd, iteration)
        graph_mcm_to_ctm = SmoothPlot(graph_mcm_to_ctm, iteration)
    
    #_______________________________________________
    # Save plots
    
    for plot in [graph_cs_ecal, graph_cs_p0d, graph_cs_smrd, graph_mcm_to_ctm]:
        plot.Write(plot.GetTitle().replace(" ","_"))
    
    for plot in allgraphs_cs_ecal:
        plot.Write(plot.GetTitle().replace(" ","_"))

    for plot in allgraphs_cs_smrd:
        plot.Write(plot.GetTitle().replace(" ","_"))
        
    for plot in allgraphs_cs_p0d:
        plot.Write(plot.GetTitle().replace(" ","_"))
        
    outFile.Close()
    print "Saved all plots to : smoothed_plots.root"
        
        
    
        
        









    
    
    
    
