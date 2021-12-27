"""
AERONET Data Organization & Graphics - AERODOG
Function to create graphics from directsun and inversion AERONET data (level 1.0, 1.5 or 2.0)
Function created on Fri Dec  3 13:25:12 2021
AERODOG first version created on Wed Dec 23 17:45:08 2020
@author: Alexandre C. Yoshida, Fábio J. S. Lopes and Alexandre Cacheffo
"""

import os
import time
import glob
import math
import datetime
import numpy as np
import pandas as pd
from os import path
import seaborn as sns
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

def aod_temporal_evolution(graphicflag, datalevel, avgtime, aoddata, lambdaaod1,filegraphpath,graphname):
    dateinstr = str.capitalize(aoddata['globaltime'][0].strftime('%b %Y'))
    datefinalstr =  str.capitalize(aoddata['globaltime'][len(aoddata['globaltime'])-1].strftime('%b %Y'))
    leveldata = ''.join(['Level ',str(datalevel)[0],'.',str(datalevel)[1]])
    station_name = aoddata['AERONET_Site'][0].replace('_',' ')
    measurement_title = 'AERONET Data - ' + dateinstr + ' to ' + datefinalstr + ' - ' + graphicflag + ' Retrieval '\
                 + leveldata + '\n' + station_name + ' Station'
    if lambdaaod1 == 340:
        colorgraph = 'magenta'
    elif lambdaaod1 == 355:
        colorgraph = 'rebeccapurple'
    elif lambdaaod1 == 380:
        colorgraph = 'mediumslateblue'
    elif lambdaaod1 == 440:
        colorgraph = 'dodgerblue'
    elif lambdaaod1 == 500:
        colorgraph = 'green'
    elif lambdaaod1 == 532:
        colorgraph = 'forestgreen'
    elif lambdaaod1 == 675:
        colorgraph = 'orangered'
    elif lambdaaod1 == 870:
        colorgraph = 'firebrick'        
    elif lambdaaod1 == 1020:
        colorgraph = 'crimson'
    elif lambdaaod1 == 1640:
        colorgraph = 'maroon'
    
    if graphicflag == 'AOD':
        gflag = 'Aerosol Optical Depth'
           
    '''Graphics for individual AOD measurements - temporal evolution'''
    yminlim = 0
    ymaxlim = 2
    xminlim = aoddata['globaltime'][0].to_pydatetime() + datetime.timedelta(days=-12)
    xmaxlim = aoddata['globaltime'][len(aoddata['globaltime'])-1].to_pydatetime() + datetime.timedelta(days=2) 
    mdpi=120
    
    sns.set(style = 'darkgrid')
    fig,ax = plt.subplots(1,1, sharey = 'row', figsize=(1200/mdpi, 800/mdpi),dpi=mdpi)
    fig.suptitle(measurement_title, fontsize=18, fontweight='bold')
    fig.subplots_adjust(top = 0.91)
#    ax.plot(globaltime, aoddata, 'o--', color = 'red',
#             linewidth = 0.5, markersize = 3, label = '$\\tau_a(1020)$')
    ax.plot(aoddata['globaltime'].to_numpy(), aoddata[''.join([graphicflag,'_',str(lambdaaod1),'nm'])].to_numpy(), 'o--',  markerfacecolor='none', color = colorgraph, 
            linewidth = 1, label = '$\\tau_a(' + str(lambdaaod1) + ')$ - Time Avg. ' + avgtime )
#    ax.plot(globaltime, aoddata, 'o--', color = 'forestgreen',
#             linewidth = 0.5, markersize = 3, label = '$\\tau_a(' + str(lambdaaod1) + ')$')
#    ax.plot(globaltime, aoddata['AOD_355nm'], 'o--', color = 'rebeccapurple',
#             linewidth = 0.5, markersize = 3, label = '$\\tau_a(355)$')
    ax.set_ylabel(gflag + '($\\tau_a$)', fontsize=20, fontweight='bold');
    ax.set_xlabel('Date', fontsize=20, fontweight='bold');
    ax.set_xlim(xminlim, xmaxlim)
    ax.set_ylim(yminlim, ymaxlim)
    fig.autofmt_xdate(rotation=45, ha='right')
    ax.tick_params(axis='both', which='major', labelsize=14, width=1, length=5, color='black', direction='in')
    for label in ax.get_xticklabels():
        label.set_fontweight(550)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=8))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %y'))
    for label in ax.get_yticklabels():
        label.set_fontweight(550)
    ax.legend(fontsize = 12, loc = 'best', markerscale = 1.5, handletextpad = 0.2)
    auxname = os.sep.join([filegraphpath,graphname])
    plt.savefig(auxname)
#    auxnamepdf = auxname.replace(figpng,figpdf)
#    plt.savefig(auxnamepdf)
    plt.show()
    plt.close(fig)

def allaod_temporal_evolution(graphicflag, datalevel, avgtime, aoddata, aod, processed_aod,filegraphpathall,graphnameall):
    dateinstr = str.capitalize(aoddata['globaltime'][0].strftime('%b %Y'))
    datefinalstr =  str.capitalize(aoddata['globaltime'][len(aoddata['globaltime'])-1].strftime('%b %Y'))
    leveldata = ''.join(['Level ',str(datalevel)[0],'.',str(datalevel)[1]])
    station_name = aoddata['AERONET_Site'][0].replace('_',' ')
    measurement_title = 'AERONET Data - ' + dateinstr + ' to ' + datefinalstr + ' - ' + graphicflag + ' Retrieval '\
                 + leveldata + '\n' + station_name + ' Station'

    '''Graphics for all wavelengths measurements - temporal evolution'''
    yminlim = 0
    ymaxlim = 2
    xminlim = aoddata['globaltime'][0].to_pydatetime() + datetime.timedelta(days=-12)
    xmaxlim = aoddata['globaltime'][len(aoddata['globaltime'])-1].to_pydatetime() + datetime.timedelta(days=2) 
    mdpi=120 

    if graphicflag == 'AOD':
        gflag = 'Aerosol Optical Depth'
        
    sns.set(style = 'darkgrid')
    fig,ax = plt.subplots(1,1, sharey = 'row', figsize=(1200/mdpi, 800/mdpi),dpi=mdpi)
    fig.suptitle(measurement_title, fontsize=18, fontweight='bold')
    fig.subplots_adjust(top = 0.91)
    for i in range(0,len(aod)):
        if processed_aod[i] == 'on':
            if aod[i] == 340:
                colorgraph = 'magenta'
            elif aod[i] == 355:
                colorgraph = 'rebeccapurple'
            elif aod[i] == 380:
                colorgraph = 'mediumslateblue'
            elif aod[i] == 440:
                colorgraph = 'dodgerblue'
            elif aod[i] == 500:
                colorgraph = 'green'
            elif aod[i] == 532:
                colorgraph = 'forestgreen'
            elif aod[i] == 675:
                colorgraph = 'yellow'
            elif aod[i] == 870:
                colorgraph = 'orangered'
            elif aod[i] == 1020:
                colorgraph = 'crimson'
            elif aod[i] == 1640:
                colorgraph = 'maroon'
                
            ax.plot(aoddata['globaltime'].to_numpy(), aoddata[''.join([graphicflag,'_',str(aod[i]),'nm'])].to_numpy(), 'o--',  markerfacecolor='none', color = colorgraph,
                    linewidth = 1, label = '$\\tau_a(' + str(aod[i]) + ')$ - Time Avg. ' + avgtime )

        ax.set_ylabel(gflag + '($\\tau_a$)', fontsize=20, fontweight='bold');
        ax.set_xlabel('Date', fontsize=20, fontweight='bold');
        ax.set_xlim(xminlim, xmaxlim)
        ax.set_ylim(yminlim, ymaxlim)
        fig.autofmt_xdate(rotation=45, ha='right')
        ax.tick_params(axis='both', which='major', labelsize=14, width=1, length=5, color='black', direction='in')
        for label in ax.get_xticklabels():
            label.set_fontweight(550)
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=8))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %y'))
        for label in ax.get_yticklabels():
            label.set_fontweight(550)
        ax.legend(fontsize = 12, loc = 'best', markerscale = 1.5, handletextpad = 0.2)
    auxname = os.sep.join([filegraphpathall,graphnameall])
    plt.savefig(auxname)
#    auxnamepdf = auxname.replace(figpng,figpdf)
#    plt.savefig(auxnamepdf)
    plt.show()
    plt.close(fig)

def angexp_temporal_evolution(graphicflag, datalevel, avgtime, angexpdata, lambdaAE, filegraphpathae,graphnameae):
    dateinstr = str.capitalize(angexpdata['globaltime'][0].strftime('%b %Y'))
    datefinalstr =  str.capitalize(angexpdata['globaltime'][len(angexpdata['globaltime'])-1].strftime('%b %Y'))
    leveldata = ''.join(['Level ',str(datalevel)[0],'.',str(datalevel)[1]])
    station_name = angexpdata['AERONET_Site'][0].replace('_',' ')
    measurement_title = 'AERONET Data - ' + dateinstr + ' to ' + datefinalstr + ' - ' + graphicflag  + ' Retrieval '\
                 + leveldata + '\n' + station_name + ' Station'
    if lambdaAE[0] == 340 and lambdaAE[1] == 380:
        colorgraph = 'royalblue'
    elif lambdaAE[0] == 340 and lambdaAE[1] == 440:
        colorgraph = 'blue'
    elif lambdaAE[0] == 340 and lambdaAE[1] == 500:
        colorgraph = 'dodgerblue'
    elif lambdaAE[0] == 340 and lambdaAE[1] == 675:
        colorgraph = 'mediumslateblue'
    elif lambdaAE[0] == 340 and lambdaAE[1] == 1020:
        colorgraph = 'mediumblue'
        
    elif lambdaAE[0] == 380 and lambdaAE[1] == 440:
        colorgraph = 'magenta'
    elif lambdaAE[0] == 380 and lambdaAE[1] == 500:
        colorgraph = 'fuchsia'
    elif lambdaAE[0] == 380 and lambdaAE[1] == 675:
        colorgraph = 'violet'
    elif lambdaAE[0] == 380 and lambdaAE[1] == 1020:
        colorgraph = 'm'
        
    elif lambdaAE[0] == 440 and lambdaAE[1] == 500:
        colorgraph = 'orange'
    elif lambdaAE[0] == 440 and lambdaAE[1] == 675:
        colorgraph = 'darkorange'
    elif lambdaAE[0] == 440 and lambdaAE[1] == 870:
        colorgraph = 'orangered'
    elif lambdaAE[0] == 440 and lambdaAE[1] == 1020:
        colorgraph = 'darksalmon'
        
    elif lambdaAE[0] == 500 and lambdaAE[1] == 870:
        colorgraph = 'darkgreen'
        
    elif lambdaAE[0] == 675 and lambdaAE[1] == 1020:
        colorgraph = 'red'
    
    if graphicflag == 'AE':
        gflag = 'Angström Exponent Relation'
        
    '''Graphics of temporal evolution of Angstrom Exponent data'''
    yminlim = 0
    ymaxlim = 2.5
    xminlim = angexpdata['globaltime'][0].to_pydatetime() + datetime.timedelta(days=-12)
    xmaxlim = angexpdata['globaltime'][len(angexpdata['globaltime'])-1].to_pydatetime() + datetime.timedelta(days=2) 
    mdpi=120
    
    sns.set(style = 'darkgrid')
    fig,ax = plt.subplots(1, 1, sharey = 'row', figsize=(1200/mdpi, 800/mdpi),dpi=mdpi)
    fig.suptitle(measurement_title, fontsize=18, fontweight='bold')
    fig.subplots_adjust(top = 0.91)
#    ax.plot(globaltime, angexpdata['AOD_1020nm'], 'o--', color = 'red',
#             linewidth = 0.5, markersize = 3, label = '$\\tau_a(1020)$')
    ax.plot(angexpdata['globaltime'].to_numpy(), angexpdata[''.join([graphicflag,'_',str(lambdaAE[0]),'_',str(lambdaAE[1]),'nm'])].to_numpy(), 'o--', markerfacecolor= colorgraph, color = colorgraph,
             linewidth = 1, label = '$\\AAngström \; Exponent \; ('+ str(lambdaAE[0])+'/'+str(lambdaAE[1])+'nm)$  - Time Avg. ' + avgtime)
#    ax.plot(globaltime, angexpdata['AOD_355nm'], 'o--', color = 'rebeccapurple',
#             linewidth = 0.5, markersize = 3, label = '$\\tau_a(355)$')
    ax.set_ylabel('Angström Exponent', fontsize=20, fontweight='bold');
    ax.set_xlabel('Date', fontsize=20, fontweight='bold');
    ax.set_xlim(xminlim, xmaxlim)
    ax.set_ylim(yminlim, ymaxlim)
    fig.autofmt_xdate(rotation=45, ha='right')
    ax.tick_params(axis='both', which='major', labelsize=14, width=1, length=5, color='black', direction='in')
    for label in ax.get_xticklabels():
        label.set_fontweight(550)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=8))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %y'))
    for label in ax.get_yticklabels():
        label.set_fontweight(550)
    ax.legend(fontsize = 12, loc = 'best', markerscale = 1.5, handletextpad = 0.2)
    auxname = os.sep.join([filegraphpathae, graphnameae])
    plt.savefig(auxname)
#    auxnamepdf = auxname.replace(figpng,figpdf)
#    plt.savefig(auxnamepdf)
    plt.show()
    plt.close(fig)
    
def boxplot_temporal_evolution(graphicflag, datalevel, aeronetdatabp, aeronetmeanbp, lambdagraph, filegraphpathlr,graphnamelr):
    dateinstr = str.capitalize(aeronetdatabp['globaltime'][0].strftime('%b %Y'))
    datefinalstr =  str.capitalize(aeronetdatabp['globaltime'][len(aeronetdatabp['globaltime'])-1].strftime('%b %Y'))
    leveldata = ''.join(['Level ',str(datalevel)[0],'.',str(datalevel)[1]])
    station_name = aeronetdatabp['AERONET_Site'][0].replace('_',' ')
    measurement_title = 'AERONET Data - ' + dateinstr + ' to ' + datefinalstr + ' - ' + graphicflag + ' Retrieval '\
                 + leveldata + '\n' + station_name + ' Station'
    if lambdagraph == 340:
        colorgraphmean = 'magenta'
        colorbox = 'darkmagenta'
    elif lambdagraph == 355:
        colorgraphmean = 'rebeccapurple'
        colorbox = 'plum'
    elif lambdagraph == 380:
        colorgraphmean = 'mediumslateblue'
        colorbox = 'plum'
    elif lambdagraph == 440:
        colorgraphmean = 'dodgerblue'
        colorbox = 'blueviolet'
    elif lambdagraph == 500:
        colorgraphmean = 'green'
        colorbox = 'springgree'
    elif lambdagraph == 532:
        colorgraphmean = 'turquoise'
        colorbox = 'forestgreen'
    elif lambdagraph == 675:
        colorgraphmean = 'yellow'
        colorbox = 'goldenrod'
    elif lambdagraph == 870:
        colorgraphmean = 'coral'
        colorbox = 'orangered'
    elif lambdagraph == 1020:
        colorgraphmean = 'crimson'
        colorbox = 'hotpink'
    elif lambdagraph == 1640:
        colorgraphmean = 'maroon'
        colorbox = 'coral'
    
    if graphicflag == 'LR':
        gflag = 'Lidar Ratio'
    else:
        gflag == graphicflag
    
    yminlim = 0
    ymaxlim = 120
    mdpi=120
    
    sns.set(style = 'darkgrid')
    fig,ax = plt.subplots(1, 1, sharey = 'row', figsize=(1200/mdpi, 800/mdpi),dpi=mdpi)
    fig.suptitle(measurement_title, fontsize=18, fontweight='bold')
    fig.subplots_adjust(top = 0.91)
    ax.plot(aeronetmeanbp[''.join([graphicflag,'_',str(lambdagraph),'nm'])].to_numpy(), 'o--', markerfacecolor= colorgraphmean, color = colorgraphmean,
             linewidth = 1, label = 'Monthly mean ' + graphicflag + ' at ' + str(lambdagraph) + ' nm')
    sns.boxplot(x = 'Month', y = graphicflag + '_' + str(lambdagraph) + 'nm', data = aeronetdatabp, color = colorbox, 
                linewidth = 1, saturation = 1, flierprops = dict(marker = 'o', markersize = 3))
    ax.grid(b = True)
    ax.set_ylabel(gflag + ' at ' +str(lambdagraph) + 'nm \nMonthly Columns', fontsize=18, fontweight='bold');
    ax.set_xlabel('Month of the Year', fontsize=18, fontweight='bold');
    ax.set_ylim(yminlim, ymaxlim)
    fig.autofmt_xdate(rotation=45, ha='right')
    ax.tick_params(axis='both', which='major', labelsize=14, width=1, length=5, color='black', direction='in')
    for label in ax.get_xticklabels():
        label.set_fontweight(550)
    for label in ax.get_yticklabels():
        label.set_fontweight(550)
    ax.legend(fontsize = 12, loc = 'best', markerscale = 1.5, handletextpad = 0.2)
    auxname = os.sep.join([filegraphpathlr, graphnamelr])
    plt.savefig(auxname)
#    auxnamepdf = auxname.replace(figpng,figpdf)
#    plt.savefig(auxnamepdf)
    plt.show()
    plt.close(fig)