#!/bin/python
# -*- coding: iso-8859-1 -*-
#
# Python script for plotting total column mass loadings (g/m2) 
#
# Author: Frances Beckett, ADAQ, 2016
#


import iris
import numpy as np
import datetime
import iris.plot as iplt
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib
import os

# Specify Location of input and output directories 
outDir = '.'
outputFile1=list()

for outputFile in sorted(os.listdir(outDir)):
	if outputFile.startswith("TotCol"): 
		outputFile1.append(outputFile)
count = 0
for file in outputFile1:
    count += 1
    # Loading NAME data with IRIS
    cubes=iris.load_cube(file)

    # Extracting time data (from the NAME fields file)
    UTC_format = '%H:%M%Z %d/%m/%Y'
    phenom_time = cubes.coord('time')
    time_date = phenom_time.units.num2date(phenom_time.bounds[0][0]).strftime(UTC_format)


    # Setting up contour levels (hardwired, there are other ways of doing this)
    contours = [1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,0.1,1,10,100]
    threshold = contours[0]

    # Setting up colour scale (again hardwired, there are other ways!)
    colorscale = ('#b4dcff','#04fdff','#00ff00','#fdff00','#ffbd02','#ff6a00','#fe0000', '#0000A0', '#800080')
    normDosage=matplotlib.colors.BoundaryNorm(contours,ncolors=256,clip = False)

    # Setting up the figure and axes
    fig = plt.figure(figsize=(15,20))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines('10m')
    ax.set_ylim(35, 70)
    ax.set_xlim(-30, 10)
    ax.gridlines(draw_labels=True)


    # This allows you to mask data less than the specified threshold
    DataField = np.ma.masked_less(cubes.data,threshold)
    cubes.data = DataField


    # I have set up two ways to plot the data - the first uses pcolormesh the second contourf
    # You just need to uncomment. Take a look at the matplotlib website for details.

    # 1. Using pcolourmesh. Note: you can also exploare the use of BoundaryNorm here. You can then get discrete rather than continuous output. This is what I used in the paper.
    mappable = iplt.pcolormesh(cubes,
                           cmap='jet',
                           norm=normDosage,
                           edgecolors='none')

    # 2. Using contourf
    #mappable = iplt.contourf(cubes, levels=contours, colors=colorscale)



    # Setting up the colour bar
    cb = plt.colorbar(mappable, orientation='vertical', format='%.1e', shrink=0.5,ticks=contours)
    cb.set_label('Total Column Mass Loading (g m$^{-2}$)')


    # Add a title
    plt.title('My NAME run\n'+time_date+'\n')

    # Save and show
    plt.savefig('Tot_Column_'+str(count)+'.png')
    #plt.show()


