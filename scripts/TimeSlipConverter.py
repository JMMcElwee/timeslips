import sys
from SearchRoutines import *

slipfile = ""
if len(sys.argv) > 1:
    slipfile = sys.argv[1]

timeslips = GetSlipsFromFile(slipfile)

if slipfile == "":
    slipfile = "final_timeslips.txt"

outputfile = open(slipfile.strip(".txt") + "_converted.txt","w")

for i in range(12):
    slips = GetConvertedSlips(timeslips, ["ECalRMM"+str(i),"MCMtoECal"], i, 2)
    for slip in slips:
        print slip[0], slip[1], slip[2], slip[3]
        outputfile.write(str(slip[0]) + " " + str(slip[1]) +  " " + str(slip[2]) + " " + str(slip[3]) + "\n")

for i in range(6):
    slips = GetConvertedSlips(timeslips, ["P0DRMM"+str(i),"MCMtoP0D"], i, 0)
    for slip in slips:
        print slip[0], slip[1], slip[2], slip[3]
        outputfile.write(str(slip[0]) + " " + str(slip[1]) +  " " + str(slip[2]) + " " + str(slip[3]) + "\n")


for i in range(4):
    slips = GetConvertedSlips(timeslips, ["SMRDRMM"+str(i),"MCMtoSMRD"], i, 3)
    for slip in slips:
        print slip[0], slip[1], slip[2], slip[3]
        outputfile.write(str(slip[0]) + " " + str(slip[1]) +  " " + str(slip[2]) + " " + str(slip[3]) + "\n")


outputfile.close()

