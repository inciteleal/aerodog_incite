"""
AERONET Data Organization & Graphics - AERODOG
Script to organize directsun and inversion AERONET data (level 1.0, 1.5 or 2.0) into standardized folder and cleaning up spurious data
Created on Wed Dec 23 17:45:08 2020
@author: Alexandre C. Yoshida, Fábio J. S. Lopes and Alexandre Cacheffo

Last update: November 11, 2025 by hbarbosa
  - prints info to the user
  - removed index for loop on filenames
  - input files in a separate folder (like dad.py)
  - output file in separate folders, per level (01-organized, 02-merged, 03-derived, 04-graphics)
"""

import os
import sys
import ast
import pandas as pd
import aerodog_function as adf
import aerodog_graphics_function as agf

# During development, force the reload of our libraries
import importlib
importlib.reload(adf)
importlib.reload(agf)

print('''
=============================================
MODULE 1 

Reading the input raw directsun and inversion data from AERONET to organize - removing NaN or incorrect values
These organized files is saved as version 01 raw data, i.e., v01)
=============================================
''')

# This follows the convection defined for the download tool (dad.py),
# where input files go in a separate folder (input_dir).  That helps,
# for example, if the user is processing multiple sites at the same
# time.
rootdir = os.getcwd()
print('Locating input files...')
inputdatadir = 'input_dir'
inputfilename = '01-inputfile_rawdata'
inputdir = os.sep.join([rootdir, inputdatadir])

#inputfilenames = [name for name in os.listdir(rootdir) if name.startswith('01-inputfile_rawdata')]
inputfilenames = [name for name in os.listdir(inputdir) if name.startswith(inputfilename)]
print('Number of 01-inputfiles to read:', len(inputfilenames))
print('List of 01-inputfiles found:')
print(inputfilenames)

# loop over multiple 01-inputfiles
for afile in inputfilenames:

    # read the input file
    # step1 input file has the following format: 
    #    filetype,use_cols,rows_to_skip,level,rawdatadir,outputdir,process
    newfile = os.sep.join([inputdir, afile])
    print('Reading input file:', newfile)

    inputfile = pd.read_csv(newfile, sep = ',')
    print('Number of variables requested:', len(inputfile))

    # bug 6-nov-2025
    # Here, the code assumed only one input file for each product (e.g., aod).
    # However, reading_aeronet_data() can return multiple files, which would cause
    # a missmatch (rawfilenames[j] would not point to the j-th product file).
    #
    #rawfilenames = []

    # process all the lines in the input file
    for j in range(0,len(inputfile)):

        # only process the lines marked as 'on' in the input file
        if inputfile['process'][j] == 'on':
            print("processing variable: " + inputfile['filetype'][j])

            # Output from step 1 is saved in 01-organized/ folder
            outputdir = os.sep.join(['01-organized', inputfile['outputdir'][j]])
            if not os.path.exists(os.sep.join([rootdir, outputdir])):
                os.makedirs(os.sep.join([rootdir, outputdir]))
            
            # Rawdata (downloaded with dad.py) is found in 00-rawdata/ folder
            rawdatadir = os.sep.join(['00-rawdata', inputfile['rawdatadir'][j]])
            # bug 6-nov-2025
            # create a fresh list, instead of appending
            #rawfilenames.append(adf.reading_aeronet_data(rootdir,inputfile['filetype'][j],rawdatadir))
            rawfilenames = adf.reading_aeronet_data(rootdir,inputfile['filetype'][j],rawdatadir)
            print("List of files with that variable:")
            print(rawfilenames)
            
            # bug 6-nov-2025
            # we cannot just read the j-th file from the cumulative list, we have to process all of them
            #adf.organizing_aeronet_data(rootdir, rawfilenames[j],inputfile['filetype'][j],list(ast.literal_eval(inputfile['use_cols'][j])),
            #                            inputfile['rows_to_skip'][j],inputfile['level'][j],rawdatadir,outputdir)

            # loop over all the files for this variable
            for arawfile in rawfilenames: 
                adf.organizing_aeronet_data(rootdir, arawfile,inputfile['filetype'][j],list(ast.literal_eval(inputfile['use_cols'][j])),
                                            inputfile['rows_to_skip'][j],inputfile['level'][j],rawdatadir,outputdir)

print('''
=============================================
MODULE 2

Reading the organized raw data in order to make a time average and merge all direct-sun and inversion data in to a single dataframe
=============================================
''')

print('Locating input files...')
inputdatadirv02 = 'input_dir'
inputfilenamev02 = '02-inputfile_organized'
inputdirv02 = os.sep.join([rootdir, inputdatadirv02])

inputfilenamesv02 = [name for name in os.listdir(inputdirv02) if name.startswith(inputfilenamev02)]
print('Number of input files to read:', len(inputfilenamesv02))
print('List of input files found:')
print(inputfilenamesv02)

# loop over multiple input files
for afile in inputfilenamesv02:
        
        # read the input file
        # step2 input file has the following format: 
        #    filetype,level,average_time,v01datadir,v02outputdir,process
        newfilev02 = os.sep.join([inputdirv02, afile])
        print('Reading input file:', newfilev02)

        inputfilev02 = pd.read_csv(newfilev02, sep = ',')
        print('Number of variables requested:', len(inputfilev02))

        filenamesv02 = []
        aeronetfilev02 = []

        # process all the lines in the input file (typically one product per line, all from the same site)
        # then, merge all variables into a single file
        for j in range(0,len(inputfilev02)):

            # only process the lines marked as 'on' in the input file
            if inputfilev02['process'][j] == 'on':                
                print("processing variable: " + inputfilev02['filetype'][j])

                # Output from step 2 is saved in 02-merged/ folder
                outputdirv02 = os.sep.join(['02-merged', inputfilev02['v02outputdir'][j]])
                if not os.path.exists(os.sep.join([rootdir, outputdirv02])):
                    os.makedirs(os.sep.join([rootdir, outputdirv02]))

                # Output from step 1 is found in 01-organized/ folder
                outputdirv01 = os.sep.join(['01-organized', inputfilev02['v01datadir'][j]])
                filenamesv02.append(adf.reading_aeronet_data(rootdir,inputfilev02['filetype'][j],outputdirv01))                    
                print("List of files with that variable:")
                print(filenamesv02[j])

                # why do we list the files above, if the next function will list them again??
                aeronetfilev02.append(adf.mining_aeronet_data(rootdir,inputfilev02['filetype'][j],inputfilev02['level'][j],inputfilev02['average_time'][j],outputdirv01,outputdirv02))

                print("number of PDs in concat = ",len(aeronetfilev02))
                # this is wrong... how can we concat() before finish reading all files/variables?
                main_aeronet_df = pd.concat(aeronetfilev02,axis=1,join='inner')
                # this is also wrong... how can we manually change the column names? what if the user don't download the same columns?
                # or if the products in the input file come in a different order ?!?!?
                print(main_aeronet_df)
                print("number of clumns after concat = ", len(main_aeronet_df.columns))
                # uhm... what happens if we rename columns that don't exist? maybe it doesn't give an error?
                # anyway, it would be better to concat/rename only once, after reading all files/products/variables
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

            # potential bug: if 'directsun' is not one of the variables, savefilename_v02 is never defined
            # even if it is present, but it is not the first line... then filename will be used before being defined
            if inputfilev02['filetype'][j] == 'directsun':
                #bug - filename should not depend on the variables read.
                # this is the 'merged' file, we should just use that instead
                savefilename_v02 = os.sep.join([rootdir,outputdirv02,filenamesv02[j][0].replace('directsun','merged')])
                #savefilename_v02 = os.sep.join([rootdir,outputdirv02,''.join([filenamesv02[j][0],'_inversion_merged_v02'])])

            print('saving the merged DF...')
            # BUG: we are saving the merged DF after reading each line (even the ones not processed = off)
            # the merge should be saved only once
            main_aeronet_df.to_csv(savefilename_v02,float_format="%.6f",index=False)


print('''
# =============================================
# MODULE 3

# Calculation of new optical products using direct-sun and inversion data 
# The new products are merged with the previous version 02 data (v02) in to a single dataframe and saved as version 03 data (v03)
# This module uses the same input file as module 2
# =============================================
# ''')

# BUG - code below would only process main_aeronet_df (the last merged dataframe in memory)
# and it would save it based on the savefilename_v02 (the last saved filename)

# we need to read the list of merged CSV files saved to disk

df_aeronetdata = adf.optical_products(main_aeronet_df)
savefilename_v03 = savefilename_v02.replace('02-merged','03-derived').replace('datav02','datav03').replace('merged','derived')
print('savefilename_v03 = ',savefilename_v03)
if not os.path.exists(os.path.dirname(savefilename_v03)):
    os.makedirs(os.path.dirname(savefilename_v03))
df_aeronetdata.to_csv(savefilename_v03,float_format="%.6f",index=False)


print('''
=============================================
MODULE 4

Using the version 3 organized data to plot graphics from AERONET products
=============================================
''')

'''Organizing data to boxplot graphics'''
aeronetdatabp, aeronetmeanbp = adf.boxplotfunc(df_aeronetdata)

'''Organizing data to boxplot graphics to Angstrom matrix graphics'''
ssa_data, sae_data, derivssa = adf.angmatrixfunc(df_aeronetdata)

print('Locating input files...')
inputdatadirv04 = 'input_dir'
inputfilenamev04 = '04-inputfile_graphics'
inputdirv04 = os.sep.join([rootdir, inputdatadirv04])

#inputfilenamesv04 = [name for name in os.listdir(rootdir) if name.startswith('03-inputfile_graphics')]
inputfilenamesv04 = [name for name in os.listdir(inputdirv04) if name.startswith(inputfilenamev04)]
print('Number of input files to read:', len(inputfilenamesv04))
print('List of input files found:')
print(inputfilenamesv04)

# loop over multiple input files
for afile in inputfilenamesv04:

        # read the input file
        # step3 input file has the following format: 
        #    <TBD>

        #newfilev04 = os.sep.join([rootdir, inputfilenamesv04[i]])
        newfilev04 = os.sep.join([inputdirv04, afile])
        print('Reading input file:', newfilev04)

        inputfilev04 = pd.read_csv(newfilev04, sep = ',')
        print('Number of variables requested:', len(inputfilev04))
                
        if not os.path.exists(os.sep.join([rootdir, '04-graphics', inputfilev04['v04outputdir'][0]])):
                    os.makedirs(os.sep.join([rootdir, '04-graphics', inputfilev04['v04outputdir'][0]]))
        
        # for j in range(0,len(inputfilev04['processed_aod'])):
        #     if inputfilev04['processed_aod'][j] == 'on':
        #         print('The AOD graphic at '+ str(inputfilev04['AOD'][j]) + ' nm will be plotted' )
        #         filegraphpath = os.sep.join([rootdir, inputfilev04['v04outputdir'][0],inputfilev04.columns[1],''.join([inputfilev04.columns[1],'_',str(inputfilev04['AOD'][j]),'nm'])])
        #         graphname = ''.join([rawfilenames[0][0].replace('.directsun','_AOD_'),str(inputfilev04['AOD'][j]),'nm.',inputfilev04['graphic_file_type'][0]])
        #         if not os.path.exists(filegraphpath):
        #             os.makedirs(filegraphpath)
        #         agf.aod_temporal_evolution(inputfilev04.columns[0], inputfile['level'][0], inputfilev02['average_time'][0], df_aeronetdata,inputfilev04['AOD'][j],filegraphpath,graphname)
                       
        # for k in range(0,len(inputfilev04['processed_aod_allgraphics'].dropna())):
        #     if inputfilev04['processed_aod_allgraphics'][k] == 'on':
        #         print('The AOD graphics of all wavelengths will be plotted')
        #         filegraphpathall = os.sep.join([rootdir, inputfilev04['v04outputdir'][0],inputfilev04.columns[3].replace('graphics','wavelengths')])
        #         graphnameall = ''.join([rawfilenames[0][0].replace('.directsun','_AOD_'),'allwavelengths.',inputfilev04['graphic_file_type'][0]])
        #         if not os.path.exists(filegraphpathall):
        #             os.makedirs(filegraphpathall)
        #         agf.allaod_temporal_evolution(inputfilev04.columns[0],inputfile['level'][0], inputfilev02['average_time'][0], df_aeronetdata, inputfilev04['AOD'], inputfilev04['processed_aod'],filegraphpathall,graphnameall)

        # for l in range(0,len(inputfilev04['processed_AE'].dropna())):
        #     if inputfilev04['processed_AE'][l] == 'on':
        #         print('The Angstrom Exponent graphic relation at '+ str(list(ast.literal_eval(inputfilev04['AE'][l]))[0]) + '-' + str(list(ast.literal_eval(inputfilev04['AE'][l]))[1]) + ' nm will be plotted' )
        #         filegraphpathae = os.sep.join([rootdir, inputfilev04['v04outputdir'][0],inputfilev04.columns[5],''.join([inputfilev04.columns[5],str(list(ast.literal_eval(inputfilev04['AE'][l]))[0]),'-',str(list(ast.literal_eval(inputfilev04['AE'][l]))[1]),'nm'])])
        #         graphnameae = ''.join([rawfilenames[0][0].replace('.directsun','_AE'),''.join([str(list(ast.literal_eval(inputfilev04['AE'][l]))[0]),'-',str(list(ast.literal_eval(inputfilev04['AE'][l]))[1])]),'nm.',inputfilev04['graphic_file_type'][0]])
        #         if not os.path.exists(filegraphpathae):
        #             os.makedirs(filegraphpathae)        
        #         agf.angexp_temporal_evolution(inputfilev04.columns[4],inputfile['level'][0], inputfilev02['average_time'][0], df_aeronetdata,list(ast.literal_eval(inputfilev04['AE'][l])),filegraphpathae,graphnameae)

        # for m in range(0,len(inputfilev04['AOD_vs_AE_graphics'].dropna())):
        #     if inputfilev04['AOD_vs_AE_graphics'][m] == 'on':
        #         print('The AOD x AE scatter plot graphic with AOD at '+ str(list(ast.literal_eval(inputfilev04['AOD_vs_AE'][m]))[0]) + ' and AE relation at ' + str(list(ast.literal_eval(inputfilev04['AOD_vs_AE'][m]))[1]) + '-' + str(list(ast.literal_eval(inputfilev04['AOD_vs_AE'][m]))[2]) + ' nm will be plotted' )
        #         filegraphpathAODvsAE = os.sep.join([rootdir, inputfilev04['v04outputdir'][0],inputfilev04.columns[9],''.join([str(list(ast.literal_eval(inputfilev04['AOD_vs_AE'][m]))[0]),'vs',str(list(ast.literal_eval(inputfilev04['AOD_vs_AE'][m]))[1]),str(list(ast.literal_eval(inputfilev04['AOD_vs_AE'][m]))[2]),'nm'])])
        #         graphnameAODvsAE = ''.join([rawfilenames[0][0].replace('.directsun','_AODvsAE_'),str(list(ast.literal_eval(inputfilev04['AOD_vs_AE'][m]))[0]),'vs',str(list(ast.literal_eval(inputfilev04['AOD_vs_AE'][m]))[1]),str(list(ast.literal_eval(inputfilev04['AOD_vs_AE'][m]))[2]) ,'nm.',inputfilev04['graphic_file_type'][0]])
        #         if not os.path.exists(filegraphpathAODvsAE):
        #             os.makedirs(filegraphpathAODvsAE)
        #         agf.scatterplot_AODvsAE(inputfilev04.columns[9], inputfile['level'][0], df_aeronetdata, inputfilev04['AOD_vs_AE'][m], filegraphpathAODvsAE, graphnameAODvsAE)
                
        for n in range(0,len(inputfilev04['processed_boxplot_LR'])):
            if inputfilev04['processed_boxplot_LR'][n] == 'on':
                print('The boxplot LR graphic at '+ str(inputfilev04['LR'][n]) + ' nm will be plotted' )
                filegraphpathlr = os.sep.join([rootdir, '04-graphics', inputfilev04['v04outputdir'][0],inputfilev04.columns[8],''.join([inputfilev04.columns[8],'_',str(inputfilev04['LR'][n]),'nm'])])
                print('filegraphpathlr = ',filegraphpathlr)
                graphnamelr = ''.join([rawfilenames[0][0].replace('.directsun','_LR_'),str(inputfilev04['LR'][n]),'nm.',inputfilev04['graphic_file_type'][0]])
                print('graphnamelr = ',graphnamelr)
                if not os.path.exists(filegraphpathlr):
                    os.makedirs(filegraphpathlr)
                agf.boxplot_temporal_evolution(inputfilev04.columns[7], inputfile['level'][0], aeronetdatabp, aeronetmeanbp, inputfilev04['LR'][n], filegraphpathlr, graphnamelr)

'''Plotting Angstrom Matrix graphics'''
filegraphpath_angmatrix = os.sep.join([rootdir, '04-graphics', inputfilev04['v04outputdir'][0],'processed_angstrom_matrix','processed_angstrom_matrix_440-870nm'])
graphname_angmatrix = ''.join([rawfilenames[0][0].replace('.directsun','_Angs_Matrix_'),'440-870nm.',inputfilev04['graphic_file_type'][0]])
if not os.path.exists(filegraphpath_angmatrix):
    os.makedirs(filegraphpath_angmatrix)
agf.angsmatrix_plot(inputfile['level'][0], ssa_data, sae_data, derivssa, df_aeronetdata, filegraphpath_angmatrix,graphname_angmatrix)
