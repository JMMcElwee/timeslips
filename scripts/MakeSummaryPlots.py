from ROOT import *
import sys
from array import array
import time
from SearchRoutines import *
import argparse


if __name__=="__main__":

    # Parse Inputs
    searchdescrip = "Code to search for timeslips in cosmic datafiles"
    parser = argparse.ArgumentParser(description=searchdescrip)
    parser.add_argument('-root', help='root file')
    args = parser.parse_args()


    if (not args.root):
        print "Need ROOT file input (-root)"
        sys.exit()

    rootfile   = args.root

    # Get Input ROOT File
    infile = TFile(rootfile,"READ")

    # Initialise
    allgraphs_cs_p0d  = []
    allgraphs_cs_smrd = []
    allgraphs_cs_ecal = []
      
    for i in xrange(0,12):
        plot = infile.Get("Cosmic_ECalRMM"+str(i) + "_UNSMOOTHED")
        allgraphs_cs_ecal.append(plot)

    for i in xrange(0,6):
        plot = infile.Get("Cosmic_P0DRMM"+str(i) + "_UNSMOOTHED")
        allgraphs_cs_p0d.append(plot)
        
    for i in xrange(0,4):
        plot = infile.Get("Cosmic_SMRDRMM"+str(i) + "_UNSMOOTHED")
        allgraphs_cs_smrd.append(plot)

    # Make the MCM to CTM Searcher
    graph_mcm_to_ctm = infile.Get("MCMtoCTM_Finder" + "_UNSMOOTHED")

    # Make the MCM to CTM Searcher
    graph_mcm_to_ctm = infile.Get("MCMtoCTM_Finder" + "_UNSMOOTHED")
    graph_cs_ecal = infile.Get("Cosmic_All_ECalRMMS" + "_UNSMOOTHED")
    graph_cs_smrd = infile.Get("Cosmic_All_SMRDRMMS" + "_UNSMOOTHED")
    graph_cs_p0d = infile.Get("Cosmic_All_P0DRMMS" + "_UNSMOOTHED")

    # Read input timeslips
    timeslips = GetSlipsFromFile("", "")

    
    # ____________________________________________
    # Make summary document
    c1 = TCanvas("c1","c1",800,600)
    c1.cd()

    allslips    = GetSlipGraph(timeslips,"ALLSLIPS")
    mcmctmslips = GetSlipGraph(timeslips,"MCMtoCTM")
    mcmscmslips = GetSlipGraph(timeslips,"ALLSCMS")
    scmrmmslips = GetSlipGraph(timeslips,"ALLRMMS")
    allslips.Draw("APL")
    if mcmctmslips: mcmctmslips.Draw("SAME PL")
    if mcmscmslips: mcmscmslips.Draw("SAME PL")
    if scmrmmslips: scmrmmslips.Draw("SAME PL")
    gPad.BuildLegend(0.1,0.6,0.6,0.9)
    c1.Update()
    c1.Print("summary_document.pdf(")
    
    # ECal
    allecalslips = GetSlipGraph(timeslips,"ALLECal")
    if allecalslips:
        ecalscmslips = GetSlipGraph(timeslips, "MCMtoECal")
        ecalrmmslips = []
        for i in range(12):
            ecalrmmslips.append(GetSlipGraph(timeslips, "ECalRMM" + str(i)))

        allecalslips.Draw("APL")
        if mcmctmslips: mcmctmslips.Draw("SAME PL")
        for slip in ecalrmmslips:
            slip.Draw("SAME PL")

        gPad.BuildLegend(0.1,0.6,0.6,0.9)
        c1.Update()
        c1.Print("summary_document.pdf")
    
    # P0D
    allp0dslips = GetSlipGraph(timeslips,"ALLP0D")
    if allp0dslips:
        p0dscmslips = GetSlipGraph(timeslips, "MCMtoP0D")
        p0drmmslips = []
        for i in range(6):
            p0drmmslips.append(GetSlipGraph(timeslips, "P0DRMM" + str(i)))

        allp0dslips.Draw("APL")
        if mcmctmslips: mcmctmslips.Draw("SAME PL")
        for slip in p0drmmslips:
            slip.Draw("SAME PL")

        gPad.BuildLegend(0.1,0.6,0.6,0.9)
        c1.Update()
        c1.Print("summary_document.pdf")

    # SMRD
    allsmrdslips = GetSlipGraph(timeslips,"ALLP0D")
    if allsmrdslips:
        smrdscmslips = GetSlipGraph(timeslips, "MCMtoP0D")
        smrdrmmslips = []
        for i in range(4):
            smrdrmmslips.append(GetSlipGraph(timeslips, "P0DRMM" + str(i)))

        allsmrdslips.Draw("APL")
        if mcmctmslips: mcmctmslips.Draw("SAME PL")
        for slip in smrdrmmslips:
            slip.Draw("SAME PL")

        gPad.BuildLegend(0.1,0.6,0.6,0.9)
        c1.Update()
        c1.Print("summary_document.pdf")

    # Make correction plots
    allplots = [graph_mcm_to_ctm, graph_cs_ecal, graph_cs_p0d, graph_cs_smrd]
    allplots += allgraphs_cs_ecal + allgraphs_cs_p0d + allgraphs_cs_smrd
    for plot in allplots:

        plot_corrected = ApplyCorrections(plot.Clone(),timeslips)
        plot_corrected.SetLineColor(kRed)
        plot_corrected.SetMarkerColor(kRed)
        plot_corrected.Draw("APL")
        plot.Draw("SAME PL")
        gPad.Update()

        lowy  = min([plot.GetYaxis().GetXmin(),plot_corrected.GetYaxis().GetXmin()])
        highy = max([plot.GetYaxis().GetXmax(),plot_corrected.GetYaxis().GetXmax()]) 

        plot_corrected.GetYaxis().SetRangeUser(lowy - (highy-lowy)*0.05,highy + (highy-lowy)*0.05)
        plot_corrected.GetXaxis().SetTimeDisplay(1)
        plot_corrected.GetXaxis().SetTitle("Date")
        plot_corrected.GetYaxis().SetTitle("TRTCT")
        gStyle.SetOptTitle(1)
        gPad.SetGridy(1)

        leg = TLegend(0.8,0.9,0.99,0.99)
        leg.AddEntry(plot_corrected,"Corrected","l")
        leg.AddEntry(plot,"Original","l")
        leg.Draw("SAME")
        
        c1.Print("summary_document.pdf")
        
    # Close Summary
    c1.Print("summary_document.pdf)")
