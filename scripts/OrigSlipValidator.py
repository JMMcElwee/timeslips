#!/usr/bin/env python

from ROOT import  *
from array import array
from sys import argv

def main():


    c1 = TCanvas("c1","c1",1000,600)
    if len(argv) != 3:
        print "Not enough, or too many files passed by command line."
        return

    if '.root' in argv[1] and '.txt' in argv[2]:
        rootfile = TFile.Open(argv[1])
        textfile = argv[2]

    elif '.root' in argv[2] and '.txt' in argv[1]:
        rootfile = TFile.Open(argv[2])
        textfile = argv[1]

    else:
        print "Required root and text files have not been provided."
        return

    outfile = TFile(rootfile.GetName()[:-5] + "_corrected.root", "RECREATE")

    ECalRMMs = []
    P0DRMMS = []
    SMRDRMMs = []

    for rmm in range(12):
        offsets, times = track_slips(textfile, 2, rmm)
        print "ECAL RMM " + str(rmm)
        corrected_graph = apply_slips(rootfile, "ECal_RMM" + str(rmm) + "_MeanTime300_Constrained1_Smoothed3", times, offsets)
        gPad.SaveAs("corrected_final_ecalrmm" + str(rmm) + ".pdf")
        if corrected_graph:
            outfile.Append(corrected_graph)

    for rmm in range(6):
        offsets, times = track_slips(textfile, 0, rmm)
        print "POD RMM " + str(rmm)
        corrected_graph = apply_slips(rootfile, "P0D_RMM" + str(rmm) + "_MeanTime300_Constrained1_Smoothed3", times, offsets)
        gPad.SaveAs("corrected_final_p0drmm" + str(rmm) + ".pdf")
        if corrected_graph:
            outfile.Append(corrected_graph)

    for rmm in range(4):
        offsets, times = track_slips(textfile, 3, rmm)
        print "SMRD RMM " + str(rmm)
        corrected_graph = apply_slips(rootfile, "SMRD_RMM" + str(rmm) + "_MeanTime300_Constrained1_Smoothed3", times, offsets)
        gPad.SaveAs("corrected_final_smrdrmm" + str(rmm) + ".pdf")
        if corrected_graph:
            outfile.Append(corrected_graph)

    rootfile.Close()
    outfile.Write()
    outfile.Close()
    
    return

def track_slips(TextFile, Det, RMM):

    apply_offset = []
    apply_time = []

    TextFile = open(TextFile, 'r')

    for line in TextFile:
        time, offset, rmm, det = line.split()

        if int(rmm) == RMM and int(det) == Det:

            apply_time.append(int(time))
            if len(apply_offset):
                
                apply_offset.append((float(offset)/2.5) + apply_offset[-1])
            else:
                apply_offset.append(float(offset)/2.5)

    TextFile.close()

    return apply_offset, apply_time

def apply_slips(RootFile, TGraphName, CorrectionTime, CorrectionVal):
        
    if not CorrectionTime:
        print "No Correction Time"
        return
    print CorrectionTime, CorrectionVal
    
    tgraph = RootFile.Get(TGraphName)
    
    n = tgraph.GetN()
    x = tgraph.GetX()
    y = tgraph.GetY()

    x.SetSize(n)
    y.SetSize(n)

    x = list(x)
    y = list(y)

    itr = 0

    for i in range(n):
        if x[i] >= CorrectionTime[itr]:
            y[i] = y[i] + CorrectionVal[itr]
            if itr < len(CorrectionVal)-1:
                if not x[i] < CorrectionTime[itr+1]:
                    itr += 1
                    
    graph = TGraph(n,array('f',x),array('f',y))
    graph.SetName(TGraphName + "_SlipCorrected")
    
#    tgraph.Draw("APL")
    graph.SetLineColor(2)
    graph.Draw("APL");
    gPad.SetGridx(1)
    gPad.SetGridy(1)
    graph.GetXaxis().SetNdivisions(919)
    gPad.Update()
    
    
    return graph

if __name__ == '__main__':
    main()
