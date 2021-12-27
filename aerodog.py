"""
AERONET Data Organization & Graphics - AERODOG
Script to organize directsun and inversion AERONET data (level 1.0, 1.5 or 2.0) into standardized folder and cleaning up spurious data
Created on Wed Dec 23 17:45:08 2020
@author: Alexandre C. Yoshida, Fábio J. S. Lopes and Alexandre Cacheffo
"""

import os
import ast
import pandas as pd
from os import path
from pathlib import Path
import aerodog_function as adf
import aerodog_graphics_function as agf

'''
=============================================
Reading the input raw directsun and inversion data from AERONET to organize - removing NaN or incorrect values
These organized files is saved as version 01 raw data, i.e., v01)
=============================================
'''

rootdir = os.getcwd()
inputfilenames = [name for name in os.listdir(rootdir) if name.startswith('01-inputfile_rawdata')]

for i in range(0, len(inputfilenames)):
    newfile = os.sep.join([rootdir, inputfilenames[i]])
    inputfile = pd.read_csv(newfile, sep = ',')
    rawfilenames = []
    
    for j in range(0,len(inputfile)):
        if inputfile['process'][j] == 'on':
            if not os.path.exists(os.sep.join([rootdir, inputfile['outputdir'][j]])):
                os.makedirs(os.sep.join([rootdir, inputfile['outputdir'][j]]))
                    
            rawfilenames.append(adf.reading_aeronet_data(rootdir,inputfile['filetype'][j],inputfile['rawdatadir'][j]))
            
            adf.organizing_aeronet_data(rootdir,rawfilenames[j],inputfile['filetype'][j],list(ast.literal_eval(inputfile['use_cols'][j])),inputfile['rows_to_skip'][j],inputfile['level'][j],inputfile['rawdatadir'][j],inputfile['outputdir'][j])
                

'''
=============================================
Reading the organized raw data in order to make a time average and merge all direct-sun and inversion data in to a single dataframe
=============================================
'''

inputfilenamesv02 = [name for name in os.listdir(rootdir) if name.startswith('02-inputfile_organized')]

for i in range(0, len(inputfilenamesv02)):
        newfilev02 = os.sep.join([rootdir, inputfilenamesv02[i]])
        inputfilev02 = pd.read_csv(newfilev02, sep = ',')

        filenamesv02 = []
        aeronetfilev02 = []
        for j in range(0,len(inputfilev02)):
            if inputfilev02['process'][j] == 'on':                
                if not os.path.exists(os.sep.join([rootdir, inputfilev02['v02outputdir'][j]])):
                    os.makedirs(os.sep.join([rootdir, inputfilev02['v02outputdir'][j]]))

                filenamesv02.append(adf.reading_aeronet_data(rootdir,inputfilev02['filetype'][j],inputfilev02['v01datadir'][j]))                    
                aeronetfilev02.append(adf.mining_aeronet_data(rootdir,inputfilev02['filetype'][j],inputfilev02['level'][j],inputfilev02['average_time'][j],inputfilev02['v01datadir'][j],inputfilev02['v02outputdir'][j]))
                
                main_aeronet_df = pd.concat(aeronetfilev02,axis=1,join='inner')
                main_aeronet_df = main_aeronet_df.rename(columns = {'440-870_Angstrom_Exponent': 'AE_440_870nm', '380-500_Angstrom_Exponent': 'AE_380_500nm', '440-675_Angstrom_Exponent': 'AE_440_675nm', '500-870_Angstrom_Exponent': 'AE_500_870nm', '340-440_Angstrom_Exponent': 'AE_340_440nm',\
                                                                    'Single_Scattering_Albedo[440nm]': 'SSA_440nm', 'Single_Scattering_Albedo[675nm]': 'SSA_675nm', 'Single_Scattering_Albedo[870nm]': 'SSA_870nm', 'Single_Scattering_Albedo[1020nm]': 'SSA_1020nm', \
                                                                    '180.000000[440nm]': 'pfn180_440nm', '180.000000[675nm]': 'pfn180_675nm', '180.000000[870nm]': 'pfn180_870nm', '180.000000[1020nm]': 'pfn180_1020nm', \
                                                                    'Absorption_AOD[440nm]': 'AAOD_440nm', 'Absorption_AOD[675nm]': 'AAOD_675nm', 'Absorption_AOD[870nm]': 'AAOD_870nm','Absorption_AOD[1020nm]': 'AAOD_1020nm', \
                                                                    'Absorption_Angstrom_Exponent_440-870nm': 'AAE_440-870nm',\
                                                                    'AOD_Extinction-Total[440nm]': 'EAOD_Total_440nm', 'AOD_Extinction-Total[675nm]': 'EAOD_Total_675nm', 'AOD_Extinction-Total[870nm]': 'EAOD_Total_870nm', 'AOD_Extinction-Total[1020nm]': 'EAOD_Total_1020nm', \
                                                                    'AOD_Extinction-Fine[440nm]': 'EAOD_Fine_440nm','AOD_Extinction-Fine[675nm]': 'EAOD_Fine_675nm', 'AOD_Extinction-Fine[870nm]': 'EAOD_Fine_870nm', 'AOD_Extinction-Fine[1020nm]': 'EAOD_Fine_1020nm', \
                                                                    'AOD_Extinction-Coarse[440nm]':'EAOD_Coarse_440nm','AOD_Extinction-Coarse[675nm]':'EAOD_Coarse_675nm','AOD_Extinction-Coarse[870nm]':'EAOD_Coarse_870nm', 'AOD_Extinction-Coarse[1020nm]':'EAOD_Coarse_1020nm', \
                                                                    'Extinction_Angstrom_Exponent_440-870nm-Total': 'EAE_440-870nm',\
                                                                    'Depolarization_Ratio[440nm]': 'DepRatio_440nm', 'Depolarization_Ratio[675nm]': 'DepRatio_675nm', 'Depolarization_Ratio[870nm]': 'DepRatio_870nm', 'Depolarization_Ratio[1020nm]': 'DepRatio_1020nm'})
                main_aeronet_df = main_aeronet_df.reset_index()
            
            if inputfilev02['filetype'][j] == 'directsun':
                savefilename_v02 = os.sep.join([rootdir,inputfilev02['v02outputdir'][j],''.join([filenamesv02[j][0],'&inversion_merged_v02'])])
            main_aeronet_df.to_csv(savefilename_v02,float_format="%.6f",index=False)

'''
=============================================
Calculation of new optical products using direct-sun and inversion data 
The new products are merged with the previous version 02 data (v02) in to a single dataframe and saved as version 03 data (v03)
=============================================
'''
df_aeronetdata = adf.optical_products(main_aeronet_df)
savefilename_v03 = savefilename_v02.replace('02-merged','03-merged').replace('datav02','datav03').replace('directsun&inversion_merged_v02','directsun&inversion_merged_v03')
if not os.path.exists(os.sep.join([rootdir, inputfilev02['v02outputdir'][0].replace('02-merged','03-merged').replace('datav02','datav03')])):
    os.makedirs(os.sep.join([rootdir, inputfilev02['v02outputdir'][0].replace('02-merged','03-merged').replace('datav02','datav03')]))
df_aeronetdata.to_csv(savefilename_v03,float_format="%.6f",index=False)

'''
=============================================
Using the version 3 organized data to plot boxplot graphics from AERONET products
=============================================
'''
aeronetdatabp, aeronetmeanbp = adf.boxplotfunc(df_aeronetdata)

'''
=============================================
Using the organized data to plot graphics from AERONET products
=============================================
'''
inputfilenamesv04 = [name for name in os.listdir(rootdir) if name.startswith('03-inputfile_graphics')]

for i in range(0, len(inputfilenamesv04)):
        newfilev04 = os.sep.join([rootdir, inputfilenamesv04[i]])
        inputfilev04 = pd.read_csv(newfilev04, sep = ',')
                
        if not os.path.exists(os.sep.join([rootdir, inputfilev04['v04outputdir'][0]])):
                    os.makedirs(os.sep.join([rootdir, inputfilev04['v04outputdir'][0]]))
        
        for j in range(0,len(inputfilev04['processed_aod'])):
            if inputfilev04['processed_aod'][j] == 'on':
                print('The AOD graphic at '+ str(inputfilev04['AOD'][j]) + ' nm will be plotted' )
                filegraphpath = os.sep.join([rootdir, inputfilev04['v04outputdir'][0],inputfilev04.columns[1],''.join([inputfilev04.columns[1],'_',str(inputfilev04['AOD'][j]),'nm'])])
                graphname = ''.join([rawfilenames[0][0].replace('.directsun','_AOD_'),str(inputfilev04['AOD'][j]),'nm.',inputfilev04['graphic_file_type'][0]])
                if not os.path.exists(filegraphpath):
                    os.makedirs(filegraphpath)
                agf.aod_temporal_evolution(inputfilev04.columns[0], inputfile['level'][0], inputfilev02['average_time'][0], df_aeronetdata,inputfilev04['AOD'][j],filegraphpath,graphname)
                       
        for k in range(0,len(inputfilev04['processed_aod_allgraphics'].dropna())):
            if inputfilev04['processed_aod_allgraphics'][k] == 'on':
                print('The AOD graphics of all wavelengths will be plotted')
                filegraphpathall = os.sep.join([rootdir, inputfilev04['v04outputdir'][0],inputfilev04.columns[3].replace('graphics','wavelengths')])
                graphnameall = ''.join([rawfilenames[0][0].replace('.directsun','_AOD_'),'allwavelengths.',inputfilev04['graphic_file_type'][0]])
                if not os.path.exists(filegraphpathall):
                    os.makedirs(filegraphpathall)
                agf.allaod_temporal_evolution(inputfilev04.columns[0],inputfile['level'][0], inputfilev02['average_time'][0], df_aeronetdata, inputfilev04['AOD'], inputfilev04['processed_aod'],filegraphpathall,graphnameall)

        for l in range(0,len(inputfilev04['processed_AE'].dropna())):
            if inputfilev04['processed_AE'][l] == 'on':
                print('The Angstrom Exponent graphic relation at '+ str(list(ast.literal_eval(inputfilev04['AE'][l]))[0]) + '-' + str(list(ast.literal_eval(inputfilev04['AE'][l]))[1]) + ' nm will be plotted' )
                filegraphpathae = os.sep.join([rootdir, inputfilev04['v04outputdir'][0],inputfilev04.columns[5],''.join([inputfilev04.columns[5],str(list(ast.literal_eval(inputfilev04['AE'][l]))[0]),'-',str(list(ast.literal_eval(inputfilev04['AE'][l]))[1]),'nm'])])
                graphnameae = ''.join([rawfilenames[0][0].replace('.directsun','_AE'),''.join([str(list(ast.literal_eval(inputfilev04['AE'][l]))[0]),'-',str(list(ast.literal_eval(inputfilev04['AE'][l]))[1])]),'nm.',inputfilev04['graphic_file_type'][0]])
                if not os.path.exists(filegraphpathae):
                    os.makedirs(filegraphpathae)        
                agf.angexp_temporal_evolution(inputfilev04.columns[4],inputfile['level'][0], inputfilev02['average_time'][0], df_aeronetdata,list(ast.literal_eval(inputfilev04['AE'][l])),filegraphpathae,graphnameae)

        for m in range(0,len(inputfilev04['processed_boxplot_LR'])):
            if inputfilev04['processed_boxplot_LR'][m] == 'on':
                print('The boxplot LR graphic at '+ str(inputfilev04['LR'][m]) + ' nm will be plotted' )
                filegraphpathlr = os.sep.join([rootdir, inputfilev04['v04outputdir'][0],inputfilev04.columns[8],''.join([inputfilev04.columns[8],'_',str(inputfilev04['LR'][m]),'nm'])])
                graphnamelr = ''.join([rawfilenames[0][0].replace('.directsun','_LR_'),str(inputfilev04['LR'][m]),'nm.',inputfilev04['graphic_file_type'][0]])
                if not os.path.exists(filegraphpathlr):
                    os.makedirs(filegraphpathlr)
                agf.boxplot_temporal_evolution(inputfilev04.columns[7], inputfile['level'][0], aeronetdatabp, aeronetmeanbp, inputfilev04['LR'][m], filegraphpathlr, graphnamelr)
