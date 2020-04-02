#!/usr/bin/env python

import os
import string
from sys import argv
import operator
import datetime
import time

def main():

    if len(argv) < 2:
        print "No files passed at the command line"
        return

    if '.txt' in argv[1]:
        slipsFile = open(argv[1],'r')
    else:
        print "Text file not passed at the command line"
        return

    # Sort timeslips in order of time
    slipsTable = []

    for line in slipsFile:
        time, offset, rmm, det = line.split()
        slipsTable.append([time, offset, rmm, det])
        
    slipsTable = sort_table(slipsTable)
    
    slipsTableECal = []
    slipsTableP0D = []
    slipsTableSMRD = []


    # Start time
    starttime = int(slipsTable[0][0]) - 1
    slipsTable.append([str(starttime), '0', '0', '0'])
    slipsTable.append([str(starttime), '0', '0', '2'])
    slipsTable.append([str(starttime), '0', '0', '3'])
    slipsTable = sort_table(slipsTable)

    for a in slipsTable:
        if int(a[3]) == 2:
            slipsTableECal.append(a)

        if int(a[3]) == 0:
            slipsTableP0D.append(a)
            
        if int(a[3]) == 3:
            slipsTableSMRD.append(a)

    # Lists to track change in offsets
    changingOffsetECal = [0 for a in range(12)]
    changingOffsetP0D = [0 for a in range(6)]
    changingOffsetSMRD = [0 for a in range(4)]

    for a in range(len(slipsTableECal)):        
        if int(slipsTableECal[a][3]) == 2:
            changingOffsetECal[int(slipsTableECal[a][2])] = (
                changingOffsetECal[int(slipsTableECal[a][2])] + 
                float(slipsTableECal[a][1])/2.5)

        if (a == len(slipsTableECal)-1) or (
            slipsTableECal[a][0] != slipsTableECal[a+1][0]):
            produce_table_ecal(slipsTableECal[a], changingOffsetECal)
        else:
            continue

    for a in range(len(slipsTableP0D)):        
        if int(slipsTableP0D[a][3]) == 0:
            changingOffsetP0D[int(slipsTableP0D[a][2])] = (
                changingOffsetP0D[int(slipsTableP0D[a][2])] + 
                float(slipsTableP0D[a][1])/2.5)

        if (a == len(slipsTableP0D)-1) or (
            slipsTableP0D[a][0] != slipsTableP0D[a+1][0]):
            produce_table_p0d(slipsTableP0D[a], changingOffsetP0D)
            pass
        else:
            continue

    for a in range(len(slipsTableSMRD)):        
        if int(slipsTableSMRD[a][3]) == 3:
            changingOffsetSMRD[int(slipsTableSMRD[a][2])] = (
                changingOffsetSMRD[int(slipsTableSMRD[a][2])] + 
                float(slipsTableSMRD[a][1])/2.5)

        if (a == len(slipsTableSMRD)-1) or (
            slipsTableSMRD[a][0] != slipsTableSMRD[a+1][0]):
            produce_table_smrd(slipsTableSMRD[a], changingOffsetSMRD)
            pass
        else:
            continue

    slipsFile.close()
    
    return

def sort_table(table, col=0):
    return sorted(table, key=operator.itemgetter(col))

def produce_table_ecal(table, offsets):
    # 0, 1, 3, 4, 5, 6, 8, 9, 10, 11
    RMM_ChanID = {0 : '2281704448', 
                  1 : '2282228736',
                  2 : '2282753024',
                  3 : '2283277312', 
                  4 : '2283801600', 
                  5 : '2284325888', 
                  6 : '2284850176',
                  7 : '2285374464',
                  8 : '2285898752', 
                  9 : '2286423040', 
                  10 : '2286947328', 
                  11 : '2287471616'}

    outfile = open('tables/Det_' + table[3] + '_Time_' + table[0] + '.dat', 'w')
    
    outfile.write("BEGIN_TABLE RMM_TIME_SLIPS_TABLE '" + datetime.datetime.fromtimestamp(time.mktime(time.gmtime(int(table[0])))).strftime('%Y-%m-%d %H:%M:%S') + "' '2038-01-01 00:00:00' 400 '" + datetime.datetime.fromtimestamp(time.mktime(time.gmtime())).strftime('%Y-%m-%d %H:%M:%S') + "' 0 EPOCH=0\n")

    for a in range(12):
            offset = int(offsets[a]) * -1
            outfile.write(RMM_ChanID[a] + ", " + str(offset) + ", 0\n")

    outfile.close()

    return

def produce_table_p0d(table, offsets):
    # 0, 1, 3, 4, 5, 6, 8, 9, 10, 11
    RMM_ChanID = {0 : '2181041152',
                  1 : '2181565440',
                  2 : '2182089728',
                  3 : '2182614016',
                  4 : '2183138304',
                  5 : '2183662592'}

    outfile = open('tables/Det_' + table[3] + '_Time_' + table[0] + '.dat', 'w')
    
    outfile.write("BEGIN_TABLE RMM_TIME_SLIPS_TABLE '" + datetime.datetime.fromtimestamp(time.mktime(time.gmtime(int(table[0])))).strftime('%Y-%m-%d %H:%M:%S') + "' '2038-01-01 00:00:00' 100 '" + datetime.datetime.fromtimestamp(time.mktime(time.gmtime())).strftime('%Y-%m-%d %H:%M:%S') + "' 0 EPOCH=0\n")

    for a in range(6):
            offset = int(offsets[a]) * -1
            outfile.write(RMM_ChanID[a] + ", " + str(offset) + ", 0\n")

    outfile.close()

    return

def produce_table_smrd(table, offsets):
    # 0, 1, 3, 4, 5, 6, 8, 9, 10, 11
    RMM_ChanID = {0 : '2382367744',
                  1 : '2382892032',
                  2 : '2383416320',
                  3 : '2383940608'}

    outfile = open('tables/Det_' + table[3] + '_Time_' + table[0] + '.dat', 'w')
    
    outfile.write("BEGIN_TABLE RMM_TIME_SLIPS_TABLE '" + datetime.datetime.fromtimestamp(time.mktime(time.gmtime(int(table[0])))).strftime('%Y-%m-%d %H:%M:%S') + "' '2038-01-01 00:00:00' 700 '" + datetime.datetime.fromtimestamp(time.mktime(time.gmtime())).strftime('%Y-%m-%d %H:%M:%S') + "' 0 EPOCH=0\n")

    for a in range(4):
            offset = int(offsets[a]) * -1
            outfile.write(RMM_ChanID[a] + ", " + str(offset) + ", 0\n")

    outfile.close()

    return

if __name__ == '__main__':
    main()
