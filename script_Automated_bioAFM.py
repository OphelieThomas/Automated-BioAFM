# Python code for JPK ExperimentPlanner
"""
// ------------------------------------------------- //
//                                                   //
//            **Autobiotip_scan :**                  //
//     Automation Script for JPK Nanowizard AFM      //
//                                                   //
// ------------------------------------------------- //
// **Original algorithm :**                          //
//   Childérick SEVERAC,  Etienne DAGUE              //
//                                                   //
// **Script developers :**                           //
//   Sergio  PROA CORONADO, Childérick SEVERAC       //
//   Ophélie Thomas-Chemin                           //
// ------------------------------------------------- //


## In case you use the results of this script with your article, please don't forget to cite us:
- Séverac, C., Proa-Coronado, S., Formosa-Dague, C., Martinez-Rivas A., Dague, E., "*Automation of Bio-Atomic Force Microscope Measurements on Hundreds of C. albicans Cells*". JOVE 2020 
- Proa-Coronado, S., Séverac, C., Martinez-Rivas, A., Dague, E., "*Beyond the paradigm of nanomechanical measurements on cells using AFM: an automated methodology to rapidly analyse thousands of cells*". Nanoscale Horizons 5, 131–138 (2020). https://doi.org/10.1039/C9NH00438F
- Thomas-Chemin, O., Severac, C., Moumen, A., Martinez-Rivas, A., Vieu, C., Le Lann, M-V., Trevisiol, E. and Dague, E.; "Automated bio-AFM generates large mechanome data set and their analysis by machine learning classifies non-malignant and malignant prostatic cell lines"; Nature Methods 2023

## Purpose:
This script automatise the AFM acquisition of force curves on hundreds of cells. 
It can be executed on a JPK nanowizard AFM. For procedures please refer to the Nature Methods article cited above.

## Copyrights (C) 2019-2023 CNRS (France)

## License:
Autobiotip_scan is a free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version. https://www.gnu.org/licenses/gpl-3.0.en.html  

## Commercial use:
The GPLv3 license cited above does not permit any commercial (profit-making or proprietary) use or 
re-licensing or re-distributions. Persons interested in for-profit use 
should contact the author. 

"""
# Version: 20230202-17h 
# Elapsed time to finish iterations: --:--:--
# JPK Script
from __future__ import division
checkVersion('SPM', 6, 1, 186);
import math
import time
import datetime
import os
import sys


#New data type declaration
class Point(object):
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

# set working directory
Directory = "Log-dir"
Parent_dir = "/Path/To/Your/Experiment/Folder/"
path = os.path.join(Parent_dir,Directory)
# print(path)
if not os.path.exists(path):
    os.mkdir(path)
    print("Directory'%s' created" % Directory)


# export prints to log file
Logfile= 'Autolog.txt'
import logging
logging.basicConfig(filename=Parent_dir+Directory+'/'+Logfile, level=logging.DEBUG, format='')
sys.stdout = open(path+'/'+Logfile, "a")
print "the log starts here"


# Function to calculate angle
def calculateAngle(A = [], B = []):
    """ Given two points (x,y) an angle is calculated
    """
    Time_angleS = time.time()
    if A[0] != B[0]:
        print 'angle calculated: ' + str(math.atan((B[1] - A[1])/(B[0]-A[0])))
        Time_angleF = time.time()
        print'Time for calculate angle: ' + str(Time_angleF - Time_angleS)
        return math.atan((B[1] - A[1])/(B[0]-A[0]))
        
        
    else:
        Time_angleF = time.time()
        print'Time for calculate angle: ' + str(Time_angleF - Time_angleS)        
        return 0

# Function to determine plane equations
def planeEq(Ph, Qh, Rh, P = [], Q = [],R = []):
    """Given three points (coordinates x, y) and its heights calculates the plane equation
    """
    coef = []
    coef.append((R.y - P.y) * (Qh - Ph) - (Q.y - P.y) * (Rh - Ph))
    coef.append((Rh - Ph) * (Q.x - P.x) - (Qh - Ph) * (R.x - P.x))
    coef.append((R.x - P.x) * (Q.y - P.y) - (Q.x - P.x) * (R.y - P.y))
    coef.append(-(coef[0] * P.x + coef[1] * P.y + coef[2] * Ph))
    #print 'Zero plane equation: ' + str(coef[0]) + ' X +' + str(coef[1]) + ' Y +' + str(coef[2]) + ' Z +' + str(coef[3]) + ' = 0'
    return coef

#*****************************************Inputs block************************************************************

#--------------The scanning area is defined as 100 x 100 micrometers------------------------------------
#Points 1 and 2, take this coordinates from the approximate center of each cell, MANUAL INPUT

P1=[1.1423e-3 , -0.7455e-3] #Coordinates of P1 oint that is in the lower right corner of your array
P2=[1.3750e-3 , -0.6913e-3]  #Coordinates of P2 point that is on the lower left corner of your array

print "P1: " + str(P1[0])+", " + str(P1[1])
print "P2: " + str(P2[0])+", " + str(P2[1])

#nFP means the number of cells to visit between P1 & P2 (include P1 & P2 on the total)
nFP = 4
print "Nomber of squares: " + str(nFP)

#Path for saving directory 
path = Parent_dir


#If you want force maps from the cells set value to 0 if you want to indent set value to 1
choice = 0

# ForceScan matrix for the wells
numScans=[1,1]

# variable for the ForceMaps
ScanSize=[3e-6, 3e-6]
ScanPixels=[2, 2]
ScanOffsetCenter=[0,0]
ScanOffset=[5e-6,5e-6]



#***************************************************************************************************************
startTime = time.time()
Scanner.retract()
#Angle calculation
#angle = math.fabs(calculateAngle(P1, P2))
angle = abs(calculateAngle(P1, P2))  
angleD = angle*180/3.14159
print "Angle calculated in radian: " + str(angle)
print "Angle calculated in degres: " + str(angleD)

#Pitch calculation
#pitch = math.sqrt((P2[0]-P1[0])**2 + (P2[1]-P1[1])**2)
da = math.sqrt((P2[0]-P1[0])**2 + (P2[1]-P1[1])**2)
pitch = da/(nFP - 1)
print "Pitch: " + str(pitch)
#logging.debug("Pitch: " + str(pitch))
#########################################################


#Point to indent, this coordinate is inside the scanning area
P = [0,0]# # Rajouté pour atterir dans un coin du forceMap sans celulle
ForceSpectroscopy.setPosition(P[0], P[1])

print "P: " + str(P[0]) + ", " + str(P[1])

#Checking for a positive or negative slope in the tilt
if P1[1] > P2[1]:
    option = 0
else:
    option = 1
if option == 0: 
    msg = "negative" 
else: 
    msg = "positive"
print'Slope = ' + msg
#option = 0
print'option= ' + str(option)


#MotorizedStage.moveToAbsolutePosition(P1[0],P1[1])
#ForceSpectroscopy.moveToForcePositionIndex(0)
Scanner.retract()
Scanner.retract()
MotorizedStage.moveToAbsolutePosition(P1[0],P1[1], 400e-6)
MotorizedStage.disengage() 


#Variable MSCoord stores MotorStage coordinates
MSCoord = []


#nFP = int(da/pitch+0.4) + 1 # alternative if one does not impose nFP
print "Number of cells to visit: " + str(nFP) 

# Create a MSCoord list full of zeros
for f in range(nFP * nFP):
    MSCoord.append(Point(0,0))

# Assign the first motor stage coordinate to the first position
MSCoord[0].x = MotorizedStage.getPosition().getX()
MSCoord[0].y = MotorizedStage.getPosition().getY()


#Scanner.approach()
if option == 0: 
    print'optionBoucle= ' + str(option)
if option == 1:  
    for f in range(1, nFP):
        MSCoord[f].x = MSCoord[f-1].x + pitch * math.cos(angle) # 
        MSCoord[f].y = MSCoord[f-1].y - pitch * math.sin(angle) # 
    i = (nFP*2) -1
    for f in range(0, len(MSCoord) - nFP):
        if i < 1:
            i = (nFP*2) -1
  
        MSCoord[f+i].x = MSCoord[f].x - pitch * math.sin(angle) # 
        MSCoord[f+i].y = MSCoord[f].y - pitch * math.cos(angle) #
     
        i = i-2
else:
    for f in range(1, nFP):
        MSCoord[f].x = MSCoord[f-1].x + pitch * math.cos(angle) # 
        MSCoord[f].y = MSCoord[f-1].y + pitch * math.sin(angle) # 
    i = (nFP*2) -1
    for f in range(0, len(MSCoord) - nFP):
        if i < 1:
            i = (nFP*2) -1

        MSCoord[f+i].x = MSCoord[f].x + pitch * math.sin(angle) #
        MSCoord[f+i].y = MSCoord[f].y - pitch * math.cos(angle) #
      
        i = i-2
            
for ele in MSCoord:
    print str(ele.x) + ", " + str(ele.y)

#Iterating through the MotorStage coordinates
g = 0
while g < len(MSCoord):
    #initialMStime=time.time()
    #Retract the scanner to avoid damages
    Scanner.retract()
    
    ForceSpectroscopy.setPosition(P[0], P[1])
    print "g: " + str(g) + "P: " + str(P[0]) + ", " + str(P[1])
    if g > 0:
        #Engaging MotorStage
        MotorizedStage.engage()
    
        #Moving the MotorStage to a particular coordinate
        MotorizedStage.moveToAbsolutePosition(MSCoord[g].x, MSCoord[g].y, 400e-6)
        
        #logFile.write('Motor stage current coordinate '+ str(g)+': '+str(MSCoord[g].x)+str(MSCoord[g].y) + "\n")
        #logFile.close()
        MotorizedStage.disengage()
        print 'Motor stage current coordinate '+ str(g)+': '+str(MotorizedStage.getPosition().getX())+str(MotorizedStage.getPosition().getY())
       
        #MotorizedStage.disengage()
        #calculatePoints(Ws,angle,fileName, fineCoord)
        MotorizedStage.disengage()

    MotorizedStage.disengage()
    MotorizedStage.disengage()
    Scanner.approach()
  
    ForceMapping.activateGUIMode()
    print "GUI"
    ForceMapping.Autosave.on()
    print "Autosave"
    now = datetime.datetime.now()
    print "datetime"
    timestamp = str(now.strftime("%Y%m%d_%H%M%S"))
    print "timestamp: " + timestamp
    ForceMapping.setOutputDirectory(path+"Cell"+str(g) + '--' + str(timestamp)) # we change time.asctime() with timestamp to get rid off ":" in the directory name
    print "directory"
    ForceMapping.setScanSize(ScanSize[0],ScanSize[1])
    print "Scansize"
    ForceMapping.setScanPixels(ScanPixels[0], ScanPixels[1])
    print "Scanpixel"
    ForceMapping.setScanOffset(ScanOffsetCenter[0], ScanOffsetCenter[1]) #coordinates where the force map is going to be obtained
    print "scanoffset"
    ForceMapping.setScanAngle(angle) #
    print "scanangle"
    time.sleep(5.0) # this delay is there to avoid error due to movement of the tip not finished when the forcemapping starts
    ForceMapping.startScanning(1) #Number of force maps you want from this region

    Scanner.retract()
    print "retract center"
   
    Scanner.retract()
   
    g += 1
endTime = time.time()
print "Total time = " + str((endTime - startTime) / 60) + " minutes"
