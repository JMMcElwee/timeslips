from ROOT import *
import sys
from array import array
import time
import os.path
from math import *
import numpy as np

#_______________________________________________
def GetVals(graph):
    nvals = graph.GetN()
    xvals = graph.GetX()
    yvals = graph.GetY()
    return nvals, xvals, yvals

#_______________________________________________
def arr(vals):
    return array('f',vals) # Hack because numpy is being awkward

#_______________________________________________
def MakeWindowMeanPlot(graph, timewindow=120, scale=1.0, vetos = []):
    print "Making window mean :", graph.GetTitle()

    # Get Graph Points
    nvals, xvals, yvals = GetVals(graph)

    # Correct all points back to median
    allyvals = []
    for i in range(nvals):
        allyvals.append(yvals[i])
    medyval = GetMedian(allyvals)

    # Get Average baseline
    avgbaseline = 0.0
    count = 0
    for i in range(nvals):
        if fabs(yvals[i]) < 2E4:
            avgbaseline += yvals[i]
            count += 1
    avgbaseline /= (count + 0.)


    # Get points within range
    stime = xvals[0]
    ctime = xvals[0]

    wvals = []
    tvals = []

    newxvals = []
    newyvals = []

    for i in range(nvals):
        ctime = xvals[i]

        if ((ctime - stime) > timewindow and
            len(wvals) > 0):
            wavg = GetAvg(wvals)
            tavg = GetAvg(tvals)

            stime = ctime
            wvals = []
            tvals = []

            if (fabs(wavg - avgbaseline) > 200): continue

            newxvals.append(tavg)
            newyvals.append(wavg * scale)

        tvals.append(xvals[i])
        wvals.append(yvals[i])

    # Create a new graph
    newgraph = TGraph(len(newxvals), arr(newxvals), arr(newyvals))
    newgraph.SetTitle(graph.GetTitle())
    newgraph.SetName(graph.GetName())
    del graph

    return newgraph

#_______________________________________________
# def GetAvg(vals):
#     if len(vals) == 0: return 0.0
#     return np.mean(vals)

def GetAvg(invals):

    vals = []
    for val in invals:
        if val == 0.0: continue
        vals.append(val)

    if (len(vals) == 0): return 0.0

    avg = 0.0
    for newval in vals:
        avg += newval

    avg /= (len(vals) + 0.)

    return avg
    
#_______________________________________________
def GetMedian(numbers):
    if (len(numbers) == 0): return 0.0
    return np.median(np.array(numbers))


#_______________________________________________
# def GetRMS(vals):
#     if len(vals) == 0: return 0.0
#     return np.std(np.array(vals))
def GetArrRMS(vals, nvals):
    vallist = []
    for i in range(nvals):
        vallist.append(vals[i])
    return GetRMS(vallist)

def GetRMS(invals):

    vals = []
    for val in invals:
        if val == 0.0: continue
        vals.append(val)


    if (len(vals) <= 2): return  0.0

    avg = 0.0
    for val in vals:
        avg += val
    avg /= len(vals)

    rms = 0.0
    for val in vals:
        # print val, avg, val-avg
        rms += (val - avg)*(val-avg)

    rms = sqrt(rms)/len(vals)
    if rms > 2: return 0.0

    return rms**2

#_______________________________________________
def CombinePlots(graphlist, title):

    # Load all points into one list
    vals = []
    firstbase = None
    for graph in graphlist:
        n, x, y = GetVals(graph)    

        # Correct each point to an average of 0.0
        avgy = 0.0
        for i in range(n):
            avgy += y[i]
        avgy /= float(n)

        # If no first baseline add one
        if not firstbase: firstbase = avgy

        # Append points to list
        for i in range(n):
            vals.append([x[i],y[i]-avgy+firstbase])

    # Sort list by x
    sorted(vals, key=lambda x: x[0])
    list.sort(vals)
    
    # Make combinations seperate lists again (bad python...)
    xvals = []
    yvals = []
    for pair in vals:
        xvals.append(pair[0])
        yvals.append(pair[1])

    # Make new graph
    newgraph = TGraph(len(xvals), arr(xvals), arr(yvals))
    newgraph.SetTitle(title)

    return newgraph

#_______________________________________________
def StepPlot(graph, threshold):


    # Get initial values
    nvals, xvals, yvals = GetVals(graph)

    f1 = TF1("f1","[0]")
    lowval = xvals[0]
    highval = xvals[ 30 ]
    graph.Fit("f1","Q","Q",lowval,highval)
    baseline = f1.GetParameter(0)

    truncxvals = []
    truncyvals = []
    for i in range(nvals):
        if fabs(yvals[i] - baseline) > threshold: continue
        if i < 30: continue
        truncxvals.append(xvals[i])
        truncyvals.append(yvals[i])

    truncgr = TGraph(len(truncxvals), arr(truncxvals), arr(truncyvals))
    truncgr.Fit("f1","Q")
    baseline = f1.GetParameter(0)



    # graph.Draw("APL")
    # f2 = TF1("f2","[0]" , lowval, xvals[nvals-1])
    # f2.SetParameter(0,baseline)
    # f2.Draw("SAME")
    # f3 = TF1("f3","[0]+2.0" , lowval, xvals[nvals-1])
    # f3.SetParameter(0,baseline)
    # f3.Draw("SAME")
    # f4 = TF1("f4","[0]+4.0" , lowval, xvals[nvals-1])
    # f4.SetParameter(0,baseline)
    # f4.Draw("SAME")

    # Make new truncated plot
    truncxvals = []
    truncyvals = []
    window = 3
    for i in xrange(1,graph.GetN()-2):   
        if (fabs(yvals[i] - baseline)     >0.15 and
            fabs(yvals[i] - baseline+threshold) >0.15 and
            fabs(yvals[i] - baseline+2.0*threshold) >0.15 and 
            fabs(yvals[i] - baseline+3.0*threshold) >0.15 and 
            fabs(yvals[i] - baseline+4.0*threshold) >0.15 and
            fabs(yvals[i] - baseline-threshold) >0.15 and
            fabs(yvals[i] - baseline-2.0*threshold) >0.15 and 
            fabs(yvals[i] - baseline-3.0*threshold) >0.15 and 
            fabs(yvals[i] - baseline-4.0*threshold) >0.15): 

            prevpoints = []
            nextpoints = []
            sidepoints = []
        
            for j in xrange(max([0,i-window]), i-1):
                prevpoints.append(yvals[j])
                sidepoints.append(yvals[j])
                
            for j in xrange(i+1, min([i+window, graph.GetN()])):
                nextpoints.append(yvals[j])
                sidepoints.append(yvals[j])

            if gRandom.Uniform(0.0,1.0) > 0.10:
                truncxvals.append(xvals[i])
                truncyvals.append(GetAvg(sidepoints))
        else:

            # newyval = None
            # for k in xrange(-4,4):
            #     if (fabs(yvals[i] - baseline + k * 2.0) < 0.30):
            #         newyval = baseline - k * 2.0
            #         print yvals[i], newyval
            #         break

            # # newyval = yvals[i]
            # if newyval:
            truncxvals.append(xvals[i])
            truncyvals.append(yvals[i])



    truncgr = TGraph(len(truncxvals), arr(truncxvals), arr(truncyvals))
    # truncgr.Draw("APL")
    # f2 = TF1("f2","[0]" , lowval, xvals[nvals-1])
    # f2.SetParameter(0,baseline)
    # f2.Draw("SAME")
    # f3 = TF1("f3","[0]+2.0" , lowval, xvals[nvals-1])
    # f3.SetParameter(0,baseline)
    # f3.Draw("SAME")
    # f4 = TF1("f4","[0]+4.0" , lowval, xvals[nvals-1])
    # f4.SetParameter(0,baseline)
    # f4.Draw("SAME")

    truncgr.SetName(graph.GetName())
    truncgr.SetTitle(graph.GetTitle())

    return truncgr


def SmoothPlot(graph, iteration=0):

    # avgtype 1 : Mean
    # avgtype 0 : Median

    avgtype = 1 #int(iteration % 3 == 0) #iteration

    # Window shifts upwards
    window = 3

    # Get initial values
    nvals, xvals, yvals = GetVals(graph)
    # Get the last 3 points
    for i in xrange(1,graph.GetN()-1):
        
        prevpoints = []
        nextpoints = []
        sidepoints = []
        
        for j in xrange(max([0,i-window]), i-1):
            prevpoints.append(yvals[j])
            sidepoints.append(yvals[j])
            
        for j in xrange(i+1, min([i+window, graph.GetN()])):
            nextpoints.append(yvals[j])
            sidepoints.append(yvals[j])
        

            prevavg = GetAvg(prevpoints) 
            nextavg = GetAvg(nextpoints)
            middavg = GetAvg(sidepoints)
            prevrms = GetRMS(prevpoints) 
            nextrms = GetRMS(nextpoints)
            middrms = GetRMS(sidepoints)

        if ((yvals[j] < prevavg + prevrms and yvals[j] > nextavg - nextrms)): continue
        if ((yvals[j] > prevavg - prevrms and yvals[j] < nextavg + nextrms)): continue

        graph.SetPoint(i, xvals[i], middavg)
    
    return graph
        
#_______________________________________________
def GetCorrectedVals(graph, timeslips):
    
    # Get Values
    nvals = graph.GetN()
    xvals = graph.GetX()
    yvals = graph.GetY()
    
    # Get Valid Slips
    name = graph.GetName()
    validslips = []
    for slip in timeslips:
        time = slip[0]
        sliptype = slip[1]
        offset = slip[2]

        if (sliptype == "ECalRMM1" and "RMM10" in graph.GetTitle()): continue
        if (sliptype == "ECalRMM1" and "RMM11" in graph.GetTitle()): continue
                   
        if (sliptype in graph.GetTitle() or \
            (sliptype == "MCMtoCTM" and "Cosmic" in graph.GetTitle()) or \
            (sliptype == "MCMtoECal" and "ECal" in graph.GetTitle() and "Cosmic" in graph.GetTitle()) or \
            (sliptype == "MCMtoP0D" and "P0D" in graph.GetTitle()) or \
            (sliptype == "MCMtoSMRD" and "SMRD" in graph.GetTitle())):
            validslips.append(slip)

    # Get Updated Values
    newyvals = []
    for i in range(nvals):
        newyvals.append(yvals[i])

    for i in range(nvals):
        total_offset  = 0.0
        for slip in validslips:
            time = slip[0]
            if time <= xvals[i]: 
                total_offset -= offset + 0.
            newyvals[i] = newyvals[i] + total_offset

    return nvals, (xvals), (newyvals)
   
# __________________________________________________________________________________________
def GetCorrectedGraph(graph, timeslips):

    nvals, xvals, yvals = GetCorrectedVals(graph, timeslips)
    gr = TGraph(nvals, (xvals), (yvals))
    gr.SetName(graph.GetName())
    gr.SetTitle(graph.GetTitle())

    return gr

# __________________________________________________________________________________________
def ApplyCorrections(graph, slips):

    xvals = graph.GetX()
    yvals = graph.GetY()
    
    newgraph = graph.Clone()
    name = graph.GetName()

    # Get Valid Slips
    name = graph.GetName()
    validslips = []
    for slip in slips:
        time = slip[0]
        sliptype = slip[1]
        offset = slip[2]

        if (sliptype == "ECalRMM1" and "RMM10" in graph.GetTitle()): continue
        if (sliptype == "ECalRMM1" and "RMM11" in graph.GetTitle()): continue
                   
        if (sliptype in graph.GetTitle() or \
            (sliptype == "MCMtoCTM" and "Cosmic" in graph.GetTitle()) or \
            (sliptype == "MCMtoECal" and "ECal" in graph.GetTitle() and "Cosmic" in graph.GetTitle()) or \
            (sliptype == "MCMtoP0D" and "P0D" in graph.GetTitle()) or \
            (sliptype == "MCMtoSMRD" and "SMRD" in graph.GetTitle())):
            validslips.append(slip)
    
    for i in range(graph.GetN()):
        
        total_offset  = 0.0
        
        for slip in validslips:
            time = slip[0]
            sliptype = slip[1]
            offset = slip[2]
            
            if time <= xvals[i]:                
                total_offset -= offset + 0.
            
            # print "Setting yvalsi = ", yvals[i] , "->",yvals[i] + total_offset
            newgraph.SetPoint(i, xvals[i], yvals[i] + total_offset)
    
    newgraph.SetTitle(graph.GetTitle())
    del graph
    
    return newgraph
                                                                                                                
       


# __________________________________________________________________________________________
def SearchForSlips(graph, threshold, window, timeslips, sliptype):

    # Get Values
    corgr = ApplyCorrections(graph, timeslips)
    corgr = SmoothPlot(corgr,0)
    nvals, xvals, yvals = GetVals(corgr)

    # First iterate and get forward/current/backward going MEAN+RMS at each stage
    curtime, curvals, avgtime, mintime, maxtime, bckmean, bckrms, curmean, currms, fwdmean, fwdrms = GetBoxCar(nvals, xvals, yvals, window)
    avgrms = GetMedian(currms)

    # Make Graphs
    makegraphs = False
    if (makegraphs):
        c1 = TCanvas("c1","c1",1000,600)
        c1.Divide(3,2)

        c1.cd(1)
        g0 = TGraph(len(curtime), arr(curtime), arr(curvals))
        g0.Draw("APL")
        c1.Update()

        c1.cd(2)
        g1 = TGraph(len(curtime), arr(curtime), arr(curmean))
        g1.Draw("APL")
        c1.Update()

        c1.cd(3)
        g2 = TGraph(len(curtime), arr(curtime), arr(currms))
        g2.Draw("APL")
        c1.Update()

        raw_input("GRAPHS")

        del c1

    # Set Internal Thresholds
    if threshold == 2:
        rmsthreshold = avgrms * 10
    else:
        rmsthreshold = avgrms * 4
    prepostthreshold = 1.8


    # Now iterate over boxval and look for slips
    n = len(avgtime)
    i = 0
    while i < n-1:
        i += 1
        xExceed = -1;
        xReturned = -1;

        # Check for dodgy values
        if (fabs(bckmean[i]) < 1E-100 or fabs(curmean[i]) < 1E-100 or fabs(curmean[i]) < 1E-100): continue
        if (fabs(bckrms[i]) < 1E-100 or fabs(currms[i]) < 1E-100 or fabs(currms[i]) < 1E-100): continue

        # Update RMS threshold
        rmsthreshold = bckrms[i] + fwdrms[i]

        # Check RMS for single offsets
        if (currms[i] > rmsthreshold):
            xExceed = i
            a = i
            while (a < n-1 and currms[a] > rmsthreshold):
                xReturned = a;
                a+=1;
            i = a


            avgPre  = curmean[xExceed]
            avgPost = curmean[xReturned]
            
            slipoffset = avgPost - avgPre

            # MCM Search
            if threshold == 4:
                if fabs(slipoffset) < 2.4: continue

                if (fabs(slipoffset) < 4.0):
                    slipoffset = 4.0 if slipoffset > 0.0 else -4.0

            # RMM SEarch
            if threshold == 2:
                if fabs(slipoffset) < 1.95: continue
                if fabs(slipoffset) > 5.0: continue

                if (fabs(slipoffset) < 2.0):
                    slipoffset = 2.0 if slipoffset > 0.0 else -2.0

                # Remove multiples of 3.0
                if slipoffset > 2.0 and slipoffset < 3.0: slipoffset = 2.0
                if slipoffset < -2.0 and slipoffset > -3.0: slipoffset = -2.0

                if slipoffset > 3.0 and slipoffset < 5.0: slipoffset = 4.0
                if slipoffset < -3.0 and slipoffset > -5.0: slipoffset = -4.0

            # print slipoffset
            sliptime  = (curtime[xExceed] + curtime[xReturned]) / 2.0 
            slipfound = AddTimeSlip(timeslips, sliptime, slipoffset, sliptype, maxtime[i] - mintime[i])
            if slipfound: 
                print " --> Adding timeslip : ", sliptime, avgPre, avgPost, slipoffset
            
    return timeslips

# __________________________________________________________________________________________
def GetBoxCar(nvals, xvals, yvals, window):

    # Get variable windows
    if len(window) == 1:
        window1 = window[0]
        window2 = window[0]
        window3 = window[0]
    else:
        window1, window2, window3 = window

    # Arrays for moving box car (SUPER INEFFICIENT!)
    bckmean = []
    bckrms  = []
    curtime = []
    curvals = []
    curmean = []
    currms  = []
    fwdmean = []
    fwdrms  = []
    avgtime = []
    mintime = []
    maxtime = []

    # Loop over and fill boxcars
    for i in range(nvals):

        # Get edges
        bcklow = int(i - window1 - 0.5*window2)
        bckhgh = int(i - window2 * 0.5)
        fwdlow = int(i + window2 * 0.5)
        fwdhgh = int(i + window2 * 0.5 + window3)
        bck = []
        cur = []
        fwd = []
        tim = []


        # Get Windows
        for j in xrange( bcklow, bckhgh ):
            if j < 0: j = 0
            if j > nvals: j = nvals-1
            bck.append(yvals[j])
            tim.append(xvals[j])

        for j in xrange( bckhgh, fwdlow ):
            if j < 0: j = 0
            if j > nvals: j = nvals-1
            cur.append(yvals[j])
            tim.append(xvals[j])

        for j in xrange( fwdlow, fwdhgh ):
            if j < 0: j = 0
            if j > nvals: j = nvals-1
            fwd.append(yvals[j])
            tim.append(xvals[j])

        # Get MEAN + RMS
        if (len(bck) > 0 and len(cur) > 0 and len(fwd) > 0) > 0:
            curtime.append(xvals[i])
            curvals.append(yvals[i])
            avgtime.append(GetAvg(tim))
            mintime.append(min(tim))
            maxtime.append(max(tim))
            bckmean.append(GetAvg(bck))
            bckrms .append(GetRMS(bck))
            curmean.append(GetAvg(cur))
            currms .append(GetRMS(cur))
            fwdmean.append(GetAvg(fwd))
            fwdrms .append(GetRMS(fwd))

            #print GetRMS(cur), cur
        if fwdhgh > nvals-1: break

    return curtime, curvals, avgtime, mintime, maxtime, bckmean, bckrms, curmean, currms, fwdmean, fwdrms

# Adds a time slip to the current list provided its not to close to existing slips
#_________________________________________________________________________________
def AddTimeSlip(timeslips, time, offset, sliptype, window):

    editindex = -1
    timedif = 1E54   # Set maximum timedif that says 2 slips are seperated.
    slipfound = False
    # Don't add if there are no steps
    if (offset == 0.0): return
    # print "Adding slip ffset : ", offset
    # Check if there are any matching slip types in a similar time period
    for i in range(len(timeslips)):

        if timeslips[i][1] != sliptype: continue

        if fabs(time - timeslips[i][0]) < window and fabs(time - timeslips[i][0]) < timedif and fabs(time - timeslips[i][0]) > 300:
            timedif = fabs(time - timeslips[i][0])
            editindex = i

    # If existing slip edit that one to use the new time and offset
    if editindex > 0:
        timeslips[editindex][0] = time
        timeslips[editindex][2] += offset

    # Otherwise add the slip to list
    else:
        slipfound = True
        timeslips.append([time, sliptype, offset])

    sorted(timeslips, key=lambda x: x[0])
    list.sort(timeslips)    
    
    return slipfound
    
# Removes any slips from the list below some threshold
# ______________________________________________________
def SkimSlips(inslips, threshold, type=""):

    # New list ot hold slips
    newslips = []

    # Loop over all slips
    for slip in inslips:
        
        # If absolute step size >= threshold then
        # we can keep the slip
        if (fabs(slip[2]) < threshold-0.25): continue
        if (fabs(slip[2]) > 50): continue
        if (fabs(slip[0]) < 1000000000): continue

        slip[2] = round(slip[2])
        newslips.append(slip)

    return newslips

# Reads all timeslips from all files in the current folder.
# Assumes slips saved in timeslips_TYPE.txt
# ____________________________________________________________
def GetSlipsFromFile(timeslipfile, sliptype=""):

    timeslips = []

    timesliplist = timeslipfile.split(",")
    if len(timesliplist) < 1 or timesliplist[0] == "":
        timesliplist = ["timeslips_MCMtoCTM.txt",
                        "timeslips_MCMtoECal.txt",
                        "timeslips_MCMtoP0D.txt",
                        "timeslips_MCMtoSMRD.txt"]

        if len(sliptype) > 0:
            timesliplist.append("timeslips_"+sliptype+".txt")
        else:
            for i in range(12):
                timesliplist.append("timeslips_ECalRMM"+str(i) + ".txt")
                
            for i in range(6):
                timesliplist.append("timeslips_P0DRMM"+str(i) + ".txt")
                    
            for i in range(4):
                timesliplist.append("timeslips_SMRDRMM"+str(i) + ".txt")



    # Loop over all possible timeslip files
    for filename in timesliplist:

        # Skip non existent files
        if not os.path.isfile(filename): continue

        # Open and parse file
        with open(filename,"r") as f:
            for line in f:
                
                # Skip comments and empty lines
                if len(line.strip()) == 0: continue
                if line[0] == '#': continue

                # Read and convert inputs
                opts = line.split()
                time = float(opts[0])
                sliptype = opts[1]
                offset = float(opts[2])

                # Remove slips with no step size
                if fabs(offset) < 1.0: continue

                # Check read slip not already in list
                foundslip = False
                for savedslip in timeslips:
                    if (time == savedslip[0] and
                        sliptype == savedslip[1] and
                        offset == savedslip[2]):
                        foundslip = True
                        break

                if foundslip: continue

                # Pushback slip
                timeslips.append([time, sliptype, offset])

    # print timeslips
    return timeslips


# Saves the full sliplist passed to timeslipfile
#________________________________________________________
def SaveSlips(timeslips, timeslipfile, sliptype):

    # Get only matching slip types
    slips = []
    for slip in timeslips:
        if slip[1] == sliptype:
            slips.append(slip)

    # Sort slips by time
    sorted(slips, key=lambda x: x[0])
    list.sort(slips)

    # Open relevant timeslipfile and save
    with open(timeslipfile,"w") as f:
        for slip in slips:            
            f.write(str(slip[0]) + " " + str(slip[1]) + " " + str(slip[2]) + "\n")

    return

    


#________________________________________________________
def RemoveMCMSlips(timeslips):
    validslips = []
    for slip in timeslips:
        if slip[1] == "MCMtoCTM": continue
        validslips.append(slip)
    return validslips


# Converts timeslip list into ns units and orders by time.
#________________________________________________________
def GetConvertedSlips(inslips, allowedstrings, rmm, det):

    # Create new timeslip list
    timelist = []

    # Loop over all slips and fill new list                                                                                                                                                                                            
    for slip in inslips:

        sliptime = slip[0]
        sliptype = slip[1]
        slipval  = slip[2]
        convval  = -2.5 # clock tick conversion

        # Skip Slips < 1.0
        if fabs(slipval) < 1.0: continue
        if fabs(slipval) > 8.0: continue

        if (sliptype in allowedstrings):
            print sliptype
            timelist.append([int(sliptime), slipval*-2.5, rmm, det])
            

    # Sort list by time
    return sorted(timelist)




#_________________________________
def GetSlipGraph(inslips, intype):

    validslips = []
    for slip in inslips:
        sliptype = slip[1]

        if ((sliptype == intype) or
            (intype == "ALLSLIPS") or
            (intype == "ALLSCMS" and (sliptype in "MCMtoECal MCMtoP0D MCMtoSMRD")) or
            (intype == "ALLRMMS" and ("RMM" in sliptype)) or
            (intype == "ALLECal" and ("ECal" in sliptype)) or
            (intype == "ALLP0D" and ("P0D" in sliptype)) or
            (intype == "ALLSMRD" and ("SMRD" in sliptype))):
            validslips.append(slip)

    #print validslips
    if len(validslips) == 0: return None
    gr = TGraph()
    count = 0

    sliptime = validslips[0][0]
    gr.SetPoint(0, sliptime, 0.0)

    for slip in validslips:
        count += 1
        sliptime = slip[0]
        gr.SetPoint(count, sliptime, float(count))

    gr.SetTitle(intype)
    gr.SetName(intype)

    color = kBlack
    if intype == "ALLSLIPS": color = kBlack
    if intype == "MCMtoCTM": color = kRed
    if intype == "ALLSCMS": color = kBlue
    if intype == "ALLRMMS": color = kGreen
    if intype == "MCMtoECal": color = kBlue
    if intype == "MCMtoP0D": color = kGreen
    if intype == "MCMtoSMRD": color = kViolet

    for i in range(0,12):
        if "M"+str(i) in intype:
            color = i + 2


#    if "RMM" in intype:
#        rmm = intype.replace("ECalRMM","").replace("SMRDRMM","").replace("P0DRMM","")
#        color = float(rmm) + 1

    gr.SetMarkerColor(color)
    gr.SetLineColor(color)
    gr.SetFillColor(0)
    gr.GetXaxis().SetTimeDisplay(1)

    return gr











