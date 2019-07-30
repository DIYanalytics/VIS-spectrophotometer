#-------------------------------------------------------------------------------
# Name:        calibrate wavelenght
# Purpose:     learning science
#
# Author:      Alessandro Volpato
#
# Created:     25/07/2018
# Copyright:   (c) Alessandro Volpato 2018
# Licence:     Oh yeah!!!
#-------------------------------------------------------------------------------

import io,sys
import math
import matplotlib.image as img
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import matplotlib.pylab as pl
import numpy as np


######## INSERT HERE THE FILE NAME ################
                                                  #
# NOTE: Check the format!! png or csv             #
calibFile = "cfl.png"
referenceFile = "oliveoil1.png"

samples = ["oliveoil2.png","oliveoil3.png","oliveoil4.png","oliveoil5.png",]
plotDirectly = []#"tube_water.png", "water_dye.png"]

title = "ex-Teppichladen experiments"
colors = ["yellow","orange","pink","blue","purple","lime"]
# Don't change them!!
                                                  #
###################################################


###### INSERT HERE YOUR PIXEL CORRELATIONS ########
                                                  #
pixel =      [ 23, 56,107,161,223,318,371,418,450,526]
wavelength = [406,438,486,546,611,713,772,827,863,920]
                                                  #
###################################################
                                            


####################################################################
                                                                   #
# This is a function. Each time we call getSpectrum_PNG            #
# for the filename in brackets, we will execute these operations   #
                                                                   #
def getSpectrum_PNG(filename):                                     #
    '''From a PNG file taken with spectralworkbench                
    extracts a spectrum. Each channel's spectrum                   
    is calculated as column mean for the whole picture'''          #
                                                                   #
    # Reading the image                                            #
    print("Reading image")                                         #
    image = img.imread(filename)                                   #
                                                                   #
    # Preparing the variables                                      #
    imageR = []                                                    #
    imageG = []                                                    #
    imageB = []                                                    #
    imgWidth = len(image[0])                                       #
    imgHeight = len(image)                                         #
                                                                   #
    # Preparing the RGB arrays                                     #
    for i in range(imgWidth):                                      #
        imageR.append(image[0][i][0])                              #
        imageG.append(image[0][i][1])                              #
        imageB.append(image[0][i][2])                              #
                                                                   #
    # Columns summatory                                            #
    for i in range(imgHeight):                                     #
        for j in range(imgWidth):                                  #
            imageR[j]=imageR[j]+image[i][j][0]                     #
            imageG[j]=imageG[j]+image[i][j][1]                     #
            imageB[j]=imageB[j]+image[i][j][2]                     #
                                                                   #
    # Calculating the mean for every RGB column                    #
    for i in range(imgWidth):                                      #
        imageR[i]=imageR[i]/imgHeight                              #
        imageG[i]=imageG[i]/imgHeight                              #
        imageB[i]=imageB[i]/imgHeight                              #
                                                                   #
    # Merging the RGB channels by addition                         #
    spectrum = []                                                  #
    for i in range(imgWidth):                                      #
        spectrum.append((imageR[i]+imageG[i]+imageB[i])/3)         #
                                                                   #
    # returning the results of the operation                       #
    return spectrum                                                #
                                                                   #
def getSpectrum_CSV(filename):                                     #
    '''From a CSV file containing the serie of measurements,
    splits the values and returns them as a list, the spectrum'''
                                                                   #
    # Reading the file                                             #
    print("Reading csv file")                                      #
    inFile = open(filename, "r")                                   #
    CSVline = inFile.read()                                        #
                                                                   #
    # Splitting the values                                         #
    spectrumSTR = CSVline.split(",")                               #
                                                                   #
    # Transforming the values from string to float type            #
    spectrum = []                                                  #
    for i in range(len(spectrumSTR)):                              #
        spectrum.append(float(spectrumSTR[i]))                     #
                                                                   #
    # Returning the results of the operation                       #
    return spectrum                                                #
                                                                   #

# ----------- Function ----------------------------

def normalise(spectrumIn):

    spectrumOut = []

    maxPoint = max(spectrumIn)

    for value in spectrumIn:
        spectrumOut.append(value/maxPoint)

    return spectrumOut

def spectrumTo3dFormat(spectrum):
    # Takes a list of values and tranforms it to this format:
    # [(0,x0),(1,x1),(2,x2)] where (index,value)

    table = []
    for i in range(0,639):
        table.append((i, spectrum[i]))

    return table

def calibrate(filename):
    '''From a CFL png picture, evinces where mercury peaks are located and maps the wavelenghts on the pixel matrix'''
    # This way of calibrating is really weak, because relies on the number of pixels of a sensor.

    # Getting RGB channels spactra ------------------

    # Loading the image
    image = img.imread(filename)

    imageR = []
    imageG = []
    imageB = []
    imgWidth = len(image[0])
    imgHeigth = len(image)

    # Preparing arrays of zeros of the same width of the picture
    for i in range(imgWidth):
        imageR.append(image[0][i][0])
        imageG.append(image[0][i][1])
        imageB.append(image[0][i][2])

    # Columns summatory
    for i in range(imgHeigth):
        for j in range(imgWidth):
            imageR[j]=imageR[j]+image[i][j][0]
            imageG[j]=imageG[j]+image[i][j][1]
            imageB[j]=imageB[j]+image[i][j][2]

    # Calculating the mean for every column
    for i in range(imgWidth):
        imageR[i]=imageR[i]/imgWidth
        imageG[i]=imageG[i]/imgWidth
        imageB[i]=imageB[i]/imgWidth

    #getSpectrumPNG(calibFile):
    # Finding peaks --------------------------------------

    red611index = imageR.index(max(imageR))
    green546index = imageG.index(max(imageG))

    center = round(- red611index + 1.82* green546index)
    dist = round((red611index - green546index)/4)

    blue436index = imageB.index(max(imageB[int(center-dist):int(center+dist)]))

    # The x axis is not linear

    findStart = 436 - blue436index

    return  findStart

def calibreateSpectrum(spectrum, start):
    # Adds the start point to the spectrum

    spectrumCal = [0] * start + spectrum

    return spectrumCal

def calcAbs(reference, sample):
    # Calculate transmittance and absorbance spectrum

    transmittance = []
    absorbance = []

    for i in range(len(reference)):
        if sample[i] == 0:
            transmittance.append(0)
            absorbance.append(0) # Conceptually wrong, if sample > reference, artificious data distortion has happened
        else:
            transmittance.append(sample[i]/reference[i])
            absorbance.append(-math.log(transmittance[i],10)/5)

    return absorbance


                                                                   
####################################################################




# Preparing the plot

# Initialize and load spectra
reference = getSpectrum_PNG(referenceFile)
calibration = calibrate(calibFile)

colorCounter = 0

# Samples
samplesSpectra = []
for filenName in samples:
    samplesSpectra.append(getSpectrum_PNG(filenName))

absorbances = []
for spectrum in samplesSpectra:
    absorbances.append(normalise(calcAbs(reference, spectrum)))

calibrated = []
for spectrum in absorbances:
    calibrated.append(calibreateSpectrum(spectrum, calibration))
    print("ok")

for spectrum in calibrated:
    plt.plot(spectrum, color = colors[colorCounter])
    colorCounter += 1

# Calibration process
print("Calibrating")

# Finding out the coefficients
params = np.polyfit(pixel,wavelength,3)
#return p = np.poly1d(range)

# Solving the equation for every pixel
# (Assigning to every pixel a wavelength)
nmAxis = []
for i in range(len(spectrum)):
    v1 = params[0]*float(i**3)
    v2 = params[1]*float(i**2)
    v3 = params[2]*float(i**1)
    v4 = params[3]*float(i**0)
    nmAxis.append(v1+v2+v3+v4)
# NOTE: This operation is quickly done with the later used:
# nmAxis = np.poly1d(len(spectrum))

# Plot without calculations
plotDirectlySpectra = []
for filenName in plotDirectly:
    plotDirectlySpectra.append((getSpectrum_PNG(filenName)))

calibrated2 = []
for spectrum in plotDirectlySpectra:
    calibrated2.append(calibreateSpectrum(spectrum, calibration))

for spectrum in calibrated2:
    plt.plot(spectrum, color = colors[colorCounter])
    colorCounter += 1

patch0 = mpatches.Patch(color="yellow", label='yellow')
patch1 = mpatches.Patch(color="orange", label='orange')
patch2 = mpatches.Patch(color="pink", label='pink')
patch3 = mpatches.Patch(color="blue", label='blue')
patch4 = mpatches.Patch(color="purple", label='CFL')
patch5 = mpatches.Patch(color="lime", label='The red data')
plt.legend(handles=[patch0, patch1,patch2,patch3])

plt.title(title)
plt.xlim(350, 950)
#plt.ylim(0,2)
plt.xlabel('Wavelegth (nm)')
plt.ylabel('Absorbance')

plt.show()

"""
A list of colors to use in python
colors = [indigo , gold , hotpink , firebrick , indianred , yellow ,
mistyrose , darkolivegreen , olive , darkseagreen , pink , tomato ,
lightcoral , orangered , navajowhite , lime , palegreen , darkslategrey ,
greenyellow , burlywood , seashell , mediumspringgreen , fuchsia ,
papayawhip , blanchedalmond , chartreuse , dimgray , black , peachpuff ,
springgreen , aquamarine , white , orange , lightsalmon , darkslategray ,
brown , ivory , dodgerblue , peru , lawngreen , chocolate , crimson ,
forestgreen , darkgrey , lightseagreen , cyan , mintcream , silver ,
antiquewhite , mediumorchid , skyblue , gray , darkturquoise , goldenrod ,
darkgreen , floralwhite , darkviolet , darkgray , moccasin , saddlebrown ,
grey , darkslateblue , lightskyblue , lightpink , mediumvioletred ,
slategrey , red , deeppink , limegreen , darkmagenta , palegoldenrod ,
plum , turquoise , lightgrey , lightgoldenrodyellow , darkgoldenrod ,
lavender , maroon , yellowgreen , sandybrown , thistle , violet , navy ,
magenta , dimgrey , tan , rosybrown , olivedrab , blue , lightblue ,
ghostwhite , honeydew , cornflowerblue , slateblue , linen , darkblue ,
powderblue , seagreen , darkkhaki , snow , sienna , mediumblue , royalblue ,
lightcyan , green , mediumpurple , midnightblue , cornsilk , paleturquoise ,
bisque , slategray , darkcyan , khaki , wheat , teal , darkorchid , salmon ,
deepskyblue , rebeccapurple , darkred , steelblue , palevioletred ,
lightslategray , aliceblue , lightslategrey , lightgreen , orchid ,
gainsboro , mediumseagreen , lightgray , mediumturquoise , lemonchiffon ,
cadetblue , lightyellow , lavenderblush , coral , purple , aqua , whitesmoke ,
mediumslateblue , darkorange , mediumaquamarine , darksalmon , beige ,
blueviolet , azure , lightsteelblue , oldlace]
"""
