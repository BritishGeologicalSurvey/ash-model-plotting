'''
To plot air concentration time series at Icelandic monitoring stations from VAAC resuspended ash runs.

Owned by the Atmospheric Dispersion and Air Quality team (ADAQ).

Last updated Nov 2017.

'''

import sys
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib import rc
rc('mathtext', default='regular')
import iris.plot as iplt
import pandas
import iris
import argparse
from sys import path as syspath
from PIL import Image
from pylab import *

WORKDIR = syspath[0]

#Met Office logo
im = Image.open('/data/local/vaac/public_html/images/MO_RGB_whitebackg_online.jpg')
width_org, height_org = im.size
factor = 0.7
width = int(width_org * factor)
height = int(height_org * factor)
im = im.resize((width, height), Image.NEAREST) 
im = np.array(im).astype(np.float) / 255


def plot_timeseries(workdir, timeseriesfile='Time_series_grid1.txt'):

    '''
    Plotting routine for VAAC resuspended ash runs
    Plot air concentration time series at Icelandic monitoring stations    
    '''

    # Name of input file including full path
    filename = workdir + '/' + timeseriesfile
    
     # Make font size of axis ticks smaller
    plt.rc('xtick', labelsize=6)
    plt.rc('ytick', labelsize=8)

    # set size of whole figure
    fig = plt.figure(figsize=(8, 10))
    
    # Add Met Office logo
    fig.figimage(im, 0, 920) 
    figtext(0.35, 0.02, r'Met Office Crown Copyright')

    # Load data into iris
    name = iris.load(filename)
   
    # List of titles for the plots
    Titles = ['Hvolsvollur','Heimaland','Vik','Hvaleyrarholt','Reykjavik City',
              'Reykjavik','Keflavik']    

    #	  #	#     #     #	  #	#     #     #	  #
    # Read through fields and take the ones we want to plot
    #	  #	#     #     #	  #	#     #     #	  #	

    length = len(name)
    List = np.arange(length)
    timeseries = [None] * length

    # 0 = Hvolsvollur
    # 1 = Heimaland
    # 2 = Vik
    # 3 = Hvaleyrarholt
    # 4 = ReykjavikCity
    # 5 = Reykjavik -- separate figure
    # 6 = Keflavik  -- separate figure

    for line in List:
	field = name[line].attributes['Location']
	if field == 'Hvolsvollur':
	    timeseries[0] = name[line]
	elif field == 'Heimaland':
	    timeseries[1] = name[line]
	elif field == 'Vik':
	    timeseries[2] = name[line]
	elif field == 'Hvaleyrarholt':
	    timeseries[3] = name[line]
	elif field == 'ReykjavikCity':
	    timeseries[4] = name[line]
	elif field == 'Reykjavik':
	    timeseries[5] = name[line]
	elif field == 'Keflavik':
	    timeseries[6] = name[line]

    List = np.arange(5) # first 5 stations, i.e. not airports
    
    for line in List:
        
   	plt.subplot(3, 2, len(List)-line)   
   	ax1 = plt.gca()
	
   	iplt.plot(timeseries[line]) # plot data
	
	# set logarithmic yscale.
	ax1.set_yscale('symlog',linthreshy=1e-20)		
	
	#set fixed yscale limits
	ax1.set_ylim(1e-08, 1e-04)
	
  	# Add 5% of white space at the top and bottom of the graph
   	# (so plotted lines aren't obscured by the axis)
   	ax1.margins(0, 0.05)
       
   	# format time axis
   	adl = md.AutoDateLocator()
   	formatter = md.AutoDateFormatter(adl)
   	formatter.scaled[1./(24. * 60)] = '%H:%M'
   	formatter.scaled[1./24.] = '%HZ\n%d/%m'
   	formatter.scaled[1.] = '%d/%m/%y'
   	ax1.xaxis.set_major_locator(adl)
   	ax1.xaxis.set_major_formatter(formatter)        

	# set minor ticks every 3 hours
	hours = md.HourLocator(interval=3)  # every 3 hour
	ax1.xaxis.set_minor_locator(hours)
	
   	plt.title(Titles[line], fontsize=10)     

	# Ylabel for the subplot on the left hand side
	if (line == 0) or (line == 2) or (line == 4): 	  
	    plt.ylabel('Relative air concentrations', fontsize=8)   

    # Main title 
    plt.suptitle('Time series of relative air concentrations at monitoring stations')
       
    # Add space above and below plots
    plt.subplots_adjust(hspace=0.7)

    # Or Save
    plt.savefig(workdir + '/' + 'RESUSPENDED_ASH_time_series.png')
    print 'Saved figure:', workdir + '/' + 'RESUSPENDED_ASH_time_series.png' 

    # close figure
    plt.close()


    #---------------------------------------------------------
    # Second figure with time series at airports
    # -------------------------------------------------------------

    # Make font size of axis ticks smaller
    plt.rc('xtick', labelsize=8)
    plt.rc('ytick', labelsize=10)

    # set size of whole figure
    fig = plt.figure(figsize=(8, 10))    
         
    # Add Met Office logo
    fig.figimage(im, 0, 920) 
    figtext(0.35, 0.02, r'Met Office Crown Copyright')

    #List = np.arange(2) # last 2 stations (airports)
    List = [5 ,6] # last 2 stations (airports)
    
    sp=0
    for line in List:
        sp+=1
	
   	plt.subplot(2,1, sp)   
   	ax1 = plt.gca()
	
   	iplt.plot(timeseries[line]) # plot data
       
	# set logarithmic yscale. 
	ax1.set_yscale('symlog',linthreshy=1e-20)		
	
	#set fixed yscale limits
	ax1.set_ylim(1e-08, 1e-04)
	
   	# Add 5% of white space at the top and bottom of the graph
   	# (so plotted lines aren't obscured by the axis)
   	ax1.margins(0, 0.05)
             
      	# format time axis
   	adl = md.AutoDateLocator()
   	formatter = md.AutoDateFormatter(adl)
   	formatter.scaled[1./(24. * 60)] = '%H:%M'
   	formatter.scaled[1./24.] = '%HZ\n%d/%m'
   	formatter.scaled[1.] = '%d/%m/%y'
   	ax1.xaxis.set_major_locator(adl)
   	ax1.xaxis.set_major_formatter(formatter)
	
	# set minor ticks every 3 hours
	hours = md.HourLocator(interval=3)  # every 3 hour
	ax1.xaxis.set_minor_locator(hours)       
             
   	plt.title(Titles[line], fontsize=12)          	
     	plt.ylabel('Relative air concentrations', fontsize=10)   

    # Main title 
    plt.suptitle('Time series of relative air concentrations at Airports')
       
    # Add space above and below plots
    plt.subplots_adjust(hspace=0.7)

    # Or Save
    plt.savefig(workdir + '/' + 'RESUSPENDED_ASH_time_series_airport.png')
    print 'Saved figure:', workdir + '/' + 'RESUSPENDED_ASH_time_series_airport.png' 

    # close figure
    plt.close()

if __name__ == "__main__":       
    plot_timeseries(WORKDIR)

