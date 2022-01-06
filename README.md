# AERONET Data Organization & Graphics - AERODOG

This repository provides a python script to organize directsun and inversion AERONET data, using level 1.5 or 2.0. 

The Dataset from AERONET Aerosol Optical Depth - Version 3 - level 1.5 or level 2.0 data (direct sun algorithm) and AERONET inversion data can be downloaded using [DAD script](https://github.com/inciteleal/dad_download_aeronet_data).

AERODOG consists of four different modules. 

The first has as its main function the reading of raw directsun and inversion data from AERONET and organize it, removing NaN or incorrect values.
These organized files is saved as version 01 raw data (v01).

The second module group all raw data from first module and apply a time average and merge all direct-sun and inversion data in to a single dataframe, and changing some column name variables. At the end of this module the dataframe is saved as version 02 data (v02).

The third module employ the calculus of new optical products using direct-sun and inversion data. The new products are merged with the previous version 02 data in to a single dataframe and saved as version 03 data (v03). 

The fourth module use v03 data to provide graphics for temporal distribution, boxplot and Angstrom Matrix using several AERONET products.

## Input files

In the AERODOG script one should use different files as input. In module 1 is used the raw AERONET data (directsun and inversion data) and the 01-inputfile_rawdata.

**MODULE 1**

1. The AERONET raw data (directsun and inversion data) is used as input in in this Module 1, as the example in the folder [00-rawdata_Sao_Paulo_2017_2021](https://github.com/inciteleal/aerodog_incite/tree/master/00-rawdata_Sao_Paulo_2017_2021)

2. **01-inputfile_rawdata** - Version 01 data are similar with raw data with removed NaN or incorrect values. This input file contains 7 columns:
   - filetype - directsun and inversion data type downloaded from AERONET database.
   - use_cols - columns products from each AERONET data.
   - rows_to_skip - rows to be skipped in the head of each AERONET data file.
   - level - AERONET data level (1.5 or 2.0).
   - rawdatadir - directory name where contains the AERONET raw data.
   - outputdir - directory name to be saved the organized AERONET data (also called version 01 organized data).
   - process - use "on" to turn it on the data organize process or "off" to turn it off.

**MODULE 2 & 3**

3. **02-inputfile_organized_v02&v03** - Version 02 data are direct-sun and inversion products merged and time-averaged. Version 03 are similar to version 02 data with addition of new optical products calculated using direct-sun and inversion data products. This input file contains 6 columns with information to process version 02 and version 03 data products:
   - **filetype** - directsun and inversion data type organized from AERONET raw data (version 01 organized data). 
   - **level** - AERONET data level (1.5 or 2.0).
   - **average_time** - time value to set temporal average of AERONET data products (in minutes).
   - **v01datadir** - directory name where contains the version 01 organized AERONET data.
   - **v02outputdir** - directory name to be saved the merged AERONET data (also called version 02 merged and time-averaged data).
   - **process** - use "on" to turn it on the data merging process or "off" to turn it off.

**MODULE 4**

4. **03-inputfile_graphics_v04** - Version 04 data are compounded by graphics from several AERONET products. This input file contains 13 columns:
   - **aod** - wavelength values from AERONET channels products
   - **processed_aod** - variable to select single AOD wavelength to be plotted (one AOD by graphic). Use "on" to turn it on the graphic plot process or "off" to turn it off.
   - **processed_boxplot_aod** - variable to select AOD wavelength to plot boxplot graphic. Use "on" to turn it on the graphic plot process or "off" to turn it off.
   - **processed_aod_allgraphics** - variable to select all AOD wavelength values to be plotted in one graphic. Use "on" to turn it on the graphic plot process or "off" to turn it off.
   - **AE** - wavelength values (pair) to plot Angstrom Exponent relation
   - **processed_AE** - variable to select Angstrom Exponent wavelengths to be plotted (one AE relation by graphic). Use "on" to turn it on the graphic plot process or "off" to turn it off.
   - **processed_AE_allgraphics** - variable to select all Angstrom Exponent wavelength values to be plotted in one graphic. Use "on" to turn it on the graphic plot process or "off" to turn it off.
   - **LR** - wavelength values from AERONET channel used as input to Lidar ratio plots.
   - **processed_boxplot_LR** - variable to select Lidar ratio wavelength to plot boxplot graphic. Use "on" to turn it on the graphic plot process or "off" to turn it off.
   - **AOD_vs_AE** - variable to select which wavelength relation to plot AOD vs AE graphics.
   - **AOD_vs_AE_graphics** - variable to select which AOD vs AE graphics to plot . Use "on" to turn it on the graphic plot process or "off" to turn it off.
   - **v04outputdir** - directory name to be saved all graphics plotted from AERONET data (also called version 04 data).
   - **graphic_file_type** - type of graphics to be saved (.png, .gif, .pdf, etc.)
   
   
## References

Some aerosol products, such as AOD at 355 and 532 nm, or even Lidar ratio at 532 can be calculated appplying the Angstrom power law relationship

1 - Ångström, A. (1929). On the Atmospheric Transmission of Sun Radiation and on Dust in the Air. Geografiska Annaler, 11, 156–166. https://doi.org/10.2307/519399

2 - Qian Li, Chengcai Li & Jietai Mao (2012) Evaluation of Atmospheric Aerosol Optical Depth Products at Ultraviolet Bands Derived from MODIS Products, Aerosol Science and Technology, 46:9, 1025-1034, DOI: 10.1080/02786826.2012.687475

3 - Kaufman, Y. J. (1993), Aerosol optical thickness and atmospheric path radiance, J. Geophys. Res., 98( D2), 2677– 2692, doi:10.1029/92JD02427.

The absorption and scattering components of AOD, AAOD and SAOD, the same components of Angstrom Exponent, AAE and SAE, were calculated using as reference 

4 - Moosmüller, H., Chakrabarty, R. K., Ehlers, K. M., and Arnott, W. P.: Absorption Ångström coefficient, brown carbon, and aerosols: basic concepts, bulk matter, and spherical particles, Atmos. Chem. Phys., 11, 1217–1225, https://doi.org/10.5194/acp-11-1217-2011, 2011.

5 - Moosmüller, H. and Chakrabarty, R. K.: Technical Note: Simple analytical relationships between Ångström coefficients of aerosol extinction, scattering, 
absorption, and single scattering albedo, Atmos. Chem. Phys., 11, 10677–10680, https://doi.org/10.5194/acp-11-10677-2011, 2011.

6 - Cazorla, A., Bahadur, R., Suski, K. J., Cahill, J. F., Chand, D., Schmid, B., Ramanathan, V., and Prather, K. A.: Relating aerosol absorption due to soot, organic carbon, and dust to emission sources determined from in-situ chemical measurements, Atmos. Chem. Phys., 13, 9337–9350, 
https://doi.org/10.5194/acp-13-9337-2013, 2013.

7 - Cappa, C. D., Kolesar, K. R., Zhang, X., Atkinson, D. B., Pekour, M. S., Zaveri, R. A., Zelenyuk, A., and Zhang, Q.: Understanding the optical properties of ambient sub- and supermicron particulate matter: results from the CARES 2010 field study in northern California, Atmos. Chem. Phys., 16, 6511–6535, 
https://doi.org/10.5194/acp-16-6511-2016, 2016.



