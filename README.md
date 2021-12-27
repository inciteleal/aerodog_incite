# AERONET Data Organization & Graphics - AERODOG

This repository provides a python script to organize directsun and inversion AERONET data, using level 1.5 or 2.0. 

The Dataset includes AERONET Aerosol Optical Depth - Version 3 - level 1.5 or level 2.0 data (direct sun algorithm) and AERONET inversion data downloaded using [DAD script](https://github.com/inciteleal/dad_download_aeronet_data).

## Input files

In the AERODOG script one should use different files as input. 

1. The AERONET raw data (directsun and inversion data) as input, as the example in the folder [00-rawdata_Sao_Paulo_2017_2021](https://github.com/inciteleal/aerodog_incite/tree/master/00-rawdata_Sao_Paulo_2017_2021)

2. **01-inputfile_rawdata** - Version 01 data are similar with raw data with removed NaN or incorrect values. This input file contains 7 columns:
   - filetype - directsun and inversion data type downloaded from AERONET database.
   - use_cols - columns products from each AERONET data.
   - rows_to_skip - rows to be skipped in the head of each AERONET data file.
   - level - AERONET data level (1.5 or 2.0).
   - rawdatadir - directory name where contains the AERONET raw data.
   - outputdir - directory name to be saved the organized AERONET data (also called version 01 organized data).
   - process - use "on" to turn it on the data organize process or "off" to turn it off.

3. **02-inputfile_organized_v02&v03** - Version 02 data are direct-sun and inversion products merged and time-averaged. Version 03 are similar to version 02 data with addition of new optical products calculated using direct-sun and inversion data products. This input file contains 6 columns with information to process version 02 and version 03 data products:
   - **filetype** - directsun and inversion data type organized from AERONET raw data (version 01 organized data). 
   - **level** - AERONET data level (1.5 or 2.0).
   - **average_time** - time value to set temporal average of AERONET data products (in minutes).
   - **v01datadir** - directory name where contains the version 01 organized AERONET data.
   - **v02outputdir** - directory name to be saved the merged AERONET data (also called version 02 merged and time-averaged data).
   - **process** - use "on" to turn it on the data merging process or "off" to turn it off.

4. **03-inputfile_graphics_v04** - Version 04 data are compounded by graphics from several AERONET products. This input file contains 8 columns:
   - **aod** - wavelength values from AERONET channels products
   - **processed_aod** - variable to select single AOD wavelength to be plotted (one AOD by graphic). Use "on" to turn it on the graphic plot process or "off" to turn it off.
   - **processed_boxplot_aod** - variable to select AOD wavelength to plot boxplot graphic. Use "on" to turn it on the graphic plot process or "off" to turn it off.
   - **processed_aod_allgraphics** - variable to select all AOD wavelength values to be plotted in one graphic. Use "on" to turn it on the graphic plot process or "off" to turn it off.
   - **AE** - wavelength values (pair) to plot Angstrom Exponent relation
   - **processed_AE** - variable to select Angstrom Exponent wavelengths to be plotted (one AE relation by graphic). Use "on" to turn it on the graphic plot process or "off" to turn it off.
   - **processed_AE_allgraphics** - variable to select all Angstrom Exponent wavelength values to be plotted in one graphic. Use "on" to turn it on the graphic plot process or "off" to turn it off.
   - **LR** - wavelength values from AERONET channel used as input to Lidar ratio plots.
   - **processed_boxplot_LR** - variable to select Lidar ratio wavelength to plot boxplot graphic. Use "on" to turn it on the graphic plot process or "off" to turn it off.
   - **v04outputdir** - directory name to be saved all graphics plotted from AERONET data (also called version 04 data).
   - **graphic_file_type** - type of graphics to be saved (.png, .gif, .pdf, etc.)
