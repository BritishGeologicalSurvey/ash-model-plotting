#!/bin/python
# -*- coding: iso-8859-1 -*-
#
# Python script for plotting air concentrations over a defined vertical level (g/m3) 
# Here we loop over the vertical levels, but you could also loop over time, just remove the 'hardwired' outputFile
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
	if outputFile.startswith("Air_Conc_grid"): 
		outputFile1.append(outputFile)

# Identified as the midpoint of your vertical level
ZLevels = [3000, 4000, 5000, 6000]

fig = plt.figure(figsize=(15,20))

count = 0
for file in outputFile1:
    count += 1
    for i, Level in enumerate(ZLevels):
        # Loading NAME data with IRIS
        z_constraint = iris.Constraint(altitude=Level)
        cubes = iris.load_cube(file, z_constraint)

        # Extracting time data (from the NAME fields file)
        UTC_format = '%H:%M%Z %d/%m/%Y'
        phenom_time = cubes.coord('time')
        time_date = phenom_time.units.num2date(phenom_time.bounds[0][0]).strftime(UTC_format)
        plt.suptitle('Air Concentration\n'+time_date)

        ## Setting up contour levels (hardwired, there are other ways of doing this)
        contours = [1E-8,1E-7,1E-6,1E-5,1E-4,1E-3,0.01, 0.1,1]
        threshold = contours[0]

        ## Setting up colour scale (again hardwired, there are other ways!)
        colorscale = ('#b4dcff', '#04fdff', '#00ff00', '#fdff00', '#ffbd02', '#ff6a00', '#fe0000', '#0000A0', '#800080')
        normDosage = matplotlib.colors.BoundaryNorm(contours, ncolors=256, clip=False)

        # Setting up the axes
        ax = plt.subplot(2, 2, i + 1, projection=ccrs.PlateCarree())
#        ax = plt.subplot(2, 2, i + 1, projection=ccrs.Mercator())
        ax.coastlines('10m')
        ax.set_ylim(55, 70)
        ax.set_xlim(-30, 0)
        ax.gridlines(draw_labels=True)

        # This allows you to mask data less than the specified threshold
        DataField = np.ma.masked_less(cubes.data,threshold)
        cubes.data = DataField


        # Plot Using contourf
        #mappable = iplt.contourf(cubes, levels=contours, colors=colorscale)

        mappable = iplt.pcolormesh(cubes,
                            cmap='jet',
                            norm=normDosage,
                            edgecolors='none')

        # Add a title
        plt.title('mid-point '+str(Level)+' m asl\n')

    # Setting up the Colour Bar
    cbaxes = fig.add_axes([0.15, 0.05, 0.6, 0.02])
    cbartext='Air Concentration (g m$^{-3}$)'
    cb = plt.colorbar(mappable, cax=cbaxes, orientation='horizontal', format='%.1e')
    cb.ax.set_xlabel(cbartext, fontsize =12)
    cl = plt.getp(cb.ax, 'xmajorticklabels')
    plt.setp(cl, fontsize=12)

    ## Save and show
    plt.savefig('AirConc_Multi_Example_'+str(count)+'.png')
    #plt.show()


