from ROOT import *
import sys
from array import array
import time
from SearchRoutines import *
import argparse

#_______________________________________________
if __name__=="__main__":

    #_______________________________________________
    # Parse Inputs
    searchdescrip = "Code to search for timeslips in cosmic datafiles"
    parser = argparse.ArgumentParser(description=searchdescrip)
    parser.add_argument('-root', help='root file')
    parser.add_argument('-slip', help='slip type')
    parser.add_argument('-id', help='id tag')
    parser.add_argument('-input',help='input slips')
    parser.add_argument('-draw',help='Draw progress',action='store_true')
    parser.add_argument('-window',help='Change Windowlist')
    parser.add_argument('-skip',help='Skip Value')
    parser.add_argument('-validate',help='make validation plots', action='store_true')
    parser.add_argument('-smoothed',help='use smoothed plots', action='store_true')
    parser.add_argument('-nomcm',help='remove mcm slips', action='store_true')

    args = parser.parse_args()

    if (not args.root):
        print "Need ROOT file input (-root)"
        sys.exit()

    if (not args.slip):
        print "Need slip types (-slip)"
        sys.exit()

    rootfile   = args.root
    sliptype   = args.slip

    inputslips = ""
    if (args.input): inputslips = args.input

    tag = sliptype
    if (args.id): tag = "_" + args.id

    if (args.skip): skipval = (int(args.skip))

    #_______________________________________________
    # Parse Graph Choice
    default_windows = []
    for i in range(10):
        wind1 = abs(int(gRandom.Gaus(1,40)))
        wind2 = abs(int(gRandom.Gaus(2,40)))
        if wind1 < 3.0: wind1 = 3.0
        if wind2 < 1.0: wind2 = 1.0
        default_windows.append( [wind1] )
        default_windows.append( [wind1,wind2,wind1] )
    
    # MCMtoCTM Types
    if "MCMtoCTM" in sliptype: 
        # default_windows    = [[3],[3], [5],[5],[10], [10], [40], [40], [60], [60], [40], [40], [20], [20]]
        default_threshold  = 4.0
        cosmic_plot        = "MCMtoCTM_Finder"

    # MCMtoECal MCMtoP0D MCMtoSMRD Types
    elif "MCM" in sliptype:
        # default_windows    = [[5],[5],[10], [10], [20], [20], [40], [40], [60], [60], [40], [40], [20], [20]]
        default_threshold  = 4.0
        
        if "ECal" in sliptype: cosmic_plot   = "Cosmic_All_ECalRMMS"
        elif "P0D" in sliptype: cosmic_plot  = "Cosmic_All_P0DRMMS"
        elif "SMRD" in sliptype: cosmic_plot = "Cosmic_All_SMRDRMMS"
        else:
            print "Missing MCMto- Tag"
            sys.exit()

    # All other single RMM Types
    elif "RMM" in sliptype:
        # default_windows   = [[5],[5],[10], [10], [40], [40], [60], [60], [40], [40], [20], [20]]
        default_threshold = 2.0

        rmm = int(sliptype.replace("ECalRMM","").replace("P0DRMM","").replace("SMRDRMM",""))
        cosmic_plot = "Cosmic_" + sliptype

    #_______________________________________________
    # Use unsmoothed option
    if not args.smoothed:
        cosmic_plot += "_UNSMOOTHED"


    #_______________________________________________
    # Get Graph of interst
    infile = TFile(rootfile,"READ")
    search_plot = infile.Get(cosmic_plot)

    #_______________________________________________
    # Read input timeslips
    timeslipfile = "timeslips_" + sliptype + ".txt"
    timeslips = GetSlipsFromFile("", sliptype)

    if args.nomcm:
        timeslips = RemoveMCMSlips(timeslips)


    #_______________________________________________
    # Add overrides
    windowlist = default_windows
    if (args.window):
        templist = args.window.split(',')
        windowlist = []
        for wind in templist:
            windowlist.append(map(int,wind.split("/")))

    threshold = default_threshold

    #_______________________________________________
    # Main Search Algorithm
    if not args.validate:

        #_______________________________________________
        # 10ns slip search

        # Loop over each Window
        windcount = 0
        while windcount < len(windowlist):

            # Get Window
            wind = windowlist[windcount]
            nslipsbefore = len(timeslips)

            # Get Step Plot for given threshold
            cur_plot = search_plot.Clone()
            cur_plot = StepPlot(cur_plot, 4.0)


            # Run Slip Search
            print "Scanning for slips in", [search_plot.GetTitle()], "Window =", wind, "Type =", [sliptype], "Threshold =", [4.0]
            timeslips = SearchForSlips(cur_plot, threshold, wind, timeslips, sliptype)

            # Skim out slips that are dodgy
            timeslips = SkimSlips(timeslips,2.0)
            nslipsafter = len(timeslips)

            # Get start nslips
            if nslipsbefore < nslipsafter:
                print "Repeating slip search at this window"
            else:
                windcount += 1

            #  Save after each scan incase we quit
            SaveSlips(timeslips,timeslipfile,sliptype)

        #_______________________________________________
        # Save slips incase 5ns messes things up
        timeslips_10ns = timeslips
        corgr = ApplyCorrections(search_plot, timeslips)
        nvals, xvals, yvals = GetVals(corgr)
        rms_10ns = GetArrRMS(yvals,nvals)

        #_______________________________________________
        # 5ns slip search
        if threshold < 4:
            # Loop over each Window
            windcount = 0
            while windcount < len(windowlist):

                # Get Window
                wind = windowlist[windcount]
                nslipsbefore = len(timeslips)

                # Get Step Plot for given threshold
                cur_plot = search_plot.Clone()
                cur_plot = StepPlot(cur_plot, 2.0)

                # Run Slip Search
                print "Scanning for slips in", [search_plot.GetTitle()], "Window =", wind, "Type =", [sliptype], "Threshold =", [2.0]
                timeslips = SearchForSlips(cur_plot, threshold, wind, timeslips, sliptype)

                # Skim out slips that are dodgy
                timeslips = SkimSlips(timeslips,2.0)
                nslipsafter = len(timeslips)

                # Get start nslips
                if nslipsbefore < nslipsafter:
                    print "Repeating slip search at this window"
                else:
                    windcount += 1

                #  Save after each scan incase we quit
                SaveSlips(timeslips,timeslipfile,sliptype)

        #_______________________________________________
        # Compare RMS to see if 5ns screwed everything up
        timeslips_5ns = timeslips
        corgr = ApplyCorrections(search_plot, timeslips)
        nvals, xvals, yvals = GetVals(corgr)
        rms_5ns = GetArrRMS(yvals,nvals)

        print "RMS 10 vs 5 : ", rms_10ns, rms_5ns
        if rms_10ns > rms_5ns: SaveSlips(timeslips_5ns,timeslipfile,sliptype)
        else: SaveSlips(timeslips_10ns,timeslipfile,sliptype)

    #_______________________________________________
    else:
        print "Validating ", sliptype
        plot_corrected = ApplyCorrections(search_plot.Clone(),timeslips)
        plot_corrected.SetLineColor(kRed)
        plot_corrected.SetMarkerColor(kRed)
        search_plot.Draw("APL")
        plot_corrected.Draw("SAME PL")
        gPad.Update()

        nvals, xvals, yvals = GetVals(plot_corrected)
        medy = 0.0
        for i in range(nvals):
            medy += yvals[i] / float(nvals)

        lowy  = medy - 8
        highy = medy + 8

        search_plot.GetYaxis().SetRangeUser(lowy - (highy-lowy)*0.05,highy + (highy-lowy)*0.05)
        search_plot.GetXaxis().SetTimeDisplay(1)
        search_plot.GetXaxis().SetTitle("Date")
        search_plot.GetYaxis().SetTitle("TRTCT")
        search_plot.GetYaxis().SetNdivisions(505)
        gStyle.SetOptTitle(1)
        gPad.SetGridy(1)

        leg = TLegend(0.8,0.9,0.99,0.99)
        leg.AddEntry(plot_corrected,"Corrected","l")
        leg.AddEntry(search_plot,"Original","l")
        leg.Draw("SAME")

        if args.nomcm:
            gPad.SaveAs("validation/correction_valnomcm_" + sliptype + ".pdf")
            outfile = TFile("validation/correction_valnomcm_" + sliptype + ".root","RECREATE")
            search_plot.Write("Uncorrected")
            plot_corrected.Write("Corrected")
            outfile.Close()
        else:
            gPad.SaveAs("validation/correction_validation_" + sliptype + ".pdf")
            outfile = TFile("validation/correction_validation_" + sliptype + ".root","RECREATE")
            search_plot.Write("Uncorrected")
            plot_corrected.Write("Corrected")
            outfile.Close()
        
