"""
AERONET Data Organization & Graphics - AERODOG
Function to organize directsun and inversion AERONET data (level 1.0, 1.5 or 2.0) into standardized folder and cleaning up spurious data
Function created on Mon Nov 22 17:04:21 2021
AERODOG first version created on Wed Dec 23 17:45:08 2020
@author: Alexandre C. Yoshida, Fábio J. S. Lopes and Alexandre Cacheffo

Last update: November 19, 2025 by hbarbosa
  - turned comments into docstrings
  - Bug fix: mining_aeronet_data() now concatenates all the files listed. 
"""
import os
import math
import numpy as np
import pandas as pd

def globaltime_function(row): 
    '''
=============================================
globaltime variable - concatenate Date and time 
=============================================
'''
    date = row['Date(dd:mm:yyyy)']+' '+row['Time(hh:mm:ss)']
    dateframe = pd.to_datetime(date,format= '%d:%m:%Y %H:%M:%S' )
    dateformat = dateframe.strftime('%Y-%m-%d %H:%M:%S')
    return dateformat

def globaltime_index(funcdata):
    '''
=============================================
Function to set Date and Time as globaltime index
=============================================
'''
    funcdata['globaltime'] = pd.to_datetime(funcdata['globaltime'],format= '%Y-%m-%d %H:%M:%S' )
    funcdata = funcdata.set_index('globaltime')
    return funcdata

def reading_aeronet_data(rootdir,filetype,rawdatadir):
    '''
=============================================
Function to read files from AERONET - direct-sun and inversion algorithm - level1.5 or level2.0 
=============================================
'''
    inputdir = os.sep.join([rootdir,rawdatadir])
    files = [name for name in os.listdir(inputdir) if name.endswith(filetype)]
    
    return files

def organizing_aeronet_data(rootdir,rawfile,filetype,use_cols,rowstoskip,rawlevel,rawdatadir,outputdir):
    '''
=============================================
Function for organization of AERONET Aerosol Optical Depth (V3) - level1.5 or level2.0 data - direct sun and inversion algorithm
=============================================
'''
    inputdir = os.sep.join([rootdir,rawdatadir])
    newfiles = os.sep.join([inputdir, rawfile])
    newfilepath = newfiles.replace(rawdatadir, outputdir).replace('_'+str(rawlevel)+'.'+filetype, '.'+str(rawlevel)+'_'+filetype+'_v01')
    #print("organizing_aeronet_data:: rootdir= ", rootdir)
    #print("organizing_aeronet_data:: rawfile= ", rawfile)
    #print("organizing_aeronet_data:: filetype= ", filetype)
    #print("organizing_aeronet_data:: use_cols= ", use_cols)
    #print("organizing_aeronet_data:: rowstoskip= ", rowstoskip)
    #print("organizing_aeronet_data:: rawlevel= ", rawlevel)
    #print("organizing_aeronet_data:: rawdatadir= ", rawdatadir)
    #print("organizing_aeronet_data:: outputdir= ", outputdir)
    #print("organizing_aeronet_data:: newfiles= ", newfiles)
    #print("organizing_aeronet_data:: newfilepath= ", newfilepath)
    f = pd.read_csv(newfiles,usecols=use_cols, skiprows=range(0, rowstoskip))
    f = f.replace(-999.,np.nan)
    f = f.replace(0,np.nan)
    f = f.dropna()
    f.insert(1,'globaltime',f.apply(globaltime_function, axis=1))
    f.to_csv(newfilepath,float_format="%.6f",index=False)  

def mining_aeronet_data(inputdir, files, avgtime):
'''
=============================================
Function to concatenate direct-sun and inversion algorithm from AERONET data measurements. 

Input: 
inputdir , string           Path to folder where files are
files    , list of strings  List of files to read from inputdir
avgtime  , string           Resample time (e.g. 15min, 1hour)

Output:
A single pandas DF with the data from all files concatenated. 
=============================================
'''        
        lenfiles = len(files)
        #print("mining_aeronet_data:: inputdir= ", inputdir)
        #print("mining_aeronet_data:: files= ", files)
        #print("mining_aeronet_data:: avgtime= ", avgtime)

        aeronetfile = []
        for afile in files:
            aeronetfile.append( pd.read_csv(os.sep.join([inputdir, afile])) )

        aeronetfile = pd.concat(aeronetfile, axis=0)
            
        # add time index to dataset
        aeronetfile_index = globaltime_index(aeronetfile)
        # resample as XX minutes mean data
        aeronetfile_mean = aeronetfile_index.groupby('AERONET_Site').resample(avgtime).mean(numeric_only=True)
        # exclude times when all values are NaN
        aeronetfile_mean = aeronetfile_mean.dropna()
        
        return aeronetfile_mean

'''
=============================================
Functions to calculate aerosol optical parameters from direct-sun and inversion products from AERONET data measurements
=============================================
'''  

#'''Angstrom Exponent calculation at 532 nm'''
#def ae532(row):
#        return np.log((row["AOD_675nm"])/(row["AOD_440nm"]))/(np.log(440/675))

def aod532(row):
        '''AOD calculation at 532 nm'''
        return row["AOD_500nm"]*(500/532)**((-1.)*row["AE_440_675nm"])

def ae355(row):
        '''Angstrom Exponent calculation at 355 nm'''
        return np.log((row["AOD_440nm"])/(row["AOD_340nm"]))/(np.log(340/440)) 

def aod355(row):
        '''AOD calculation at 355 nm'''
        return row["AOD_380nm"]*(380/355)**((-1.)*row["AE_340_440nm"])

def lr440(row):
        '''Lidar Ratio calculation at 440 nm'''
        return 4*(math.pi)/row['pfn180_440nm']*row['SSA_440nm']

def lr675(row):
        '''The LR calculation at 675 nm'''
        return 4*(math.pi)/row['pfn180_675nm']*row['SSA_675nm']

def lr870(row):
        '''The LR calculation at 870 nm'''
        return 4*(math.pi)/row['pfn180_870nm']*row['SSA_870nm']

def lr1020(row):
        '''The LR calculation at 1020 nm'''
        return 4*(math.pi)/row['pfn180_1020nm']*row['SSA_1020nm']

def lrae532(row):
        '''The Lidar ratio - Angstrom Exponent relation using 440 and 870 nm'''
        return np.log((row["LR_870nm"])/(row["LR_440nm"]))/(np.log(440/870))
    
def lr532(row):
        '''The Lidar ratio calculation at 532 nm using LR values of 675 nm'''
        return row["LR_675nm"]*(532/675)**((-1.)*row["LRAE_532nm"])

def lr355(row):
        '''The Lidar ratio calculation at 355 nm using LR values of 440 nm'''
        return row["LR_440nm"]*(355/440)**((-1.)*row["LRAE_532nm"])

def dssa(row):
   '''The  spectral  variability  of  the  aerosol  single  scatterring  albedo  (dSSA) - Delta Single Scattering Albedo '''
   return row["SSA_440nm"]-row["SSA_675nm"]

def aaod440(row):
   '''Absorption AOD at 440 nm '''
   return row["AOD_440nm"]*(1. - row["SSA_440nm"])

def aaod675(row):
   '''Absorption AOD at 675 nm '''
   return row["AOD_675nm"]*(1. - row["SSA_675nm"])

def saod440(row):
   '''Scattering AOD at 440 nm '''
   return row["AOD_440nm"]*(row["SSA_440nm"])

def saod675(row):
   '''Scattering AOD at 675 nm '''
   return row["AOD_675nm"]*(row["SSA_675nm"])

def aae(row):
   '''Absorption Angstrom Exponent (AAE) at 440-675 nm '''
   return (-1)*np.log((row["AAOD_440nm"])/(row["AAOD_675nm"]))/(np.log(440/675))

def sae(row):
   '''Scaterring Angstrom Exponent (SAE) at 440-675 nm ''' 
   return (-1)*np.log((row["SAOD_440nm"])/(row["SAOD_675nm"]))/(np.log(440/675)) 

'''Some aerosol products, such as AOD at 355 and 532 nm, or even Lidar ratio at 532 can be calculated appplying the Angstrom power law relationship (1,2)

1 - Ångström, A. (1929). On the Atmospheric Transmission of Sun Radiation and on Dust in the Air. Geografiska Annaler, 11, 156–166. https://doi.org/10.2307/519399

2 - Qian Li, Chengcai Li & Jietai Mao (2012) Evaluation of Atmospheric Aerosol Optical Depth Products at Ultraviolet Bands Derived from MODIS Products, Aerosol Science and Technology, 46:9, 1025-1034, DOI: 10.1080/02786826.2012.687475

3 - Kaufman, Y. J. (1993), Aerosol optical thickness and atmospheric path radiance, J. Geophys. Res., 98( D2), 2677– 2692, doi:10.1029/92JD02427.

The absorption and scattering components of AOD, AAOD and SAOD, the same components of Angstrom Exponent, AAE and SAE, were calculated using as reference 

1 - Moosmüller, H., Chakrabarty, R. K., Ehlers, K. M., and Arnott, W. P.: Absorption Ångström coefficient, brown carbon, and aerosols: basic concepts, bulk matter, 
and spherical particles, Atmos. Chem. Phys., 11, 1217–1225, https://doi.org/10.5194/acp-11-1217-2011, 2011.

2 - Cazorla, A., Bahadur, R., Suski, K. J., Cahill, J. F., Chand, D., Schmid, B., Ramanathan, V., and Prather, K. A.: Relating aerosol absorption due to soot, 
organic carbon, and dust to emission sources determined from in-situ chemical measurements, Atmos. Chem. Phys., 13, 9337–9350, 
https://doi.org/10.5194/acp-13-9337-2013, 2013.

3 - Cappa, C. D., Kolesar, K. R., Zhang, X., Atkinson, D. B., Pekour, M. S., Zaveri, R. A., Zelenyuk, A., and Zhang, Q.: Understanding the optical properties of 
ambient sub- and supermicron particulate matter: results from the CARES 2010 field study in northern California, Atmos. Chem. Phys., 16, 6511–6535, 
https://doi.org/10.5194/acp-16-6511-2016, 2016.

4 - Moosmüller, H. and Chakrabarty, R. K.: Technical Note: Simple analytical relationships between Ångström coefficients of aerosol extinction, scattering, 
absorption, and single scattering albedo, Atmos. Chem. Phys., 11, 10677–10680, https://doi.org/10.5194/acp-11-10677-2011, 2011.


'''

'''
=============================================
Functions to calculate aerosol optical parameters from direct-sun and inversion products from AERONET data measurements
=============================================
''' 
def optical_products(df_function):
#    df_function['AE_440_675nm'] = df_function.apply(ae532,axis=1)
#    df_function['AE_340_440nm'] = df_function.apply(ae355,axis=1)
    df_function['AOD_532nm'] = df_function.apply(aod532,axis=1)
    df_function['AOD_355nm'] = df_function.apply(aod355,axis=1)
    df_function['LR_440nm'] = df_function.apply(lr440,axis=1)
    df_function['LR_675nm'] = df_function.apply(lr675,axis=1)
    df_function['LR_870nm'] = df_function.apply(lr870,axis=1)
    df_function['LR_1020nm'] = df_function.apply(lr1020,axis=1)
    df_function['LRAE_532nm'] = df_function.apply(lrae532,axis=1)
    df_function['LR_532nm'] = df_function.apply(lr532,axis=1)
    df_function['LR_355nm'] = df_function.apply(lr355,axis=1)
    df_function["AAOD_440nm"]=df_function.apply(aaod440,axis=1)
    df_function["AAOD_675nm"]=df_function.apply(aaod675,axis=1)
    df_function["SAOD_440nm"]=df_function.apply(saod440,axis=1)
    df_function["SAOD_675nm"]=df_function.apply(saod675,axis=1)
    df_function["AAE"]=df_function.apply(aae,axis=1)
    df_function["SAE"]=df_function.apply(sae,axis=1)
    df_function["dSSA"]=df_function.apply(dssa,axis=1)
    return df_function

def boxplotfunc(v3aeronetdata):
    '''Adjusting Month variable for boxplot graphics ''' 
    aeronetdata = globaltime_index(v3aeronetdata)
    aeronetdata = aeronetdata.reset_index()
    aeronetdata['Month'] = aeronetdata['globaltime'].dt.strftime('%m')
     
    '''Calculation of monthly average values for the boxplot graphics'''
    aeronetmeanbp = aeronetdata.groupby(['Month']).mean(numeric_only=True)
     
    return aeronetdata, aeronetmeanbp

def angmatrixfunc(df_aeronetdata):
    
    derivssa = df_aeronetdata['SSA_440nm'] - df_aeronetdata['SSA_870nm']
    num = np.log(df_aeronetdata['SSA_440nm']) - np.log(df_aeronetdata['SSA_870nm']) 
    den = np.log(1.0 - df_aeronetdata['SSA_440nm']) - np.log(1.0 - df_aeronetdata['SSA_870nm'])
    ssa_data = (1.0 - (num/den))**(-1.0)
    weigth_1 = ((ssa_data - 1.0)/ssa_data)
    weigth_2 = (1.0/ssa_data)
    sae_data = weigth_1 * df_aeronetdata['AAE_440-870nm'] + weigth_2 * df_aeronetdata['EAE_440-870nm']

    return ssa_data, sae_data, derivssa

''' The Angstrom Matrix Function was derived from the articles references
The absorption and scattering components of AOD, AAOD and SAOD, the same components of Angstrom Exponent, AAE and SAE, were calculated using as reference 

1 - Moosmüller, H., Chakrabarty, R. K., Ehlers, K. M., and Arnott, W. P.: Absorption Ångström coefficient, brown carbon, and aerosols: basic concepts, bulk matter, 
and spherical particles, Atmos. Chem. Phys., 11, 1217–1225, https://doi.org/10.5194/acp-11-1217-2011, 2011.

2 - Cazorla, A., Bahadur, R., Suski, K. J., Cahill, J. F., Chand, D., Schmid, B., Ramanathan, V., and Prather, K. A.: Relating aerosol absorption due to soot, 
organic carbon, and dust to emission sources determined from in-situ chemical measurements, Atmos. Chem. Phys., 13, 9337–9350, 
https://doi.org/10.5194/acp-13-9337-2013, 2013.

3 - Cappa, C. D., Kolesar, K. R., Zhang, X., Atkinson, D. B., Pekour, M. S., Zaveri, R. A., Zelenyuk, A., and Zhang, Q.: Understanding the optical properties of 
ambient sub- and supermicron particulate matter: results from the CARES 2010 field study in northern California, Atmos. Chem. Phys., 16, 6511–6535, 
https://doi.org/10.5194/acp-16-6511-2016, 2016.

4 - Moosmüller, H. and Chakrabarty, R. K.: Technical Note: Simple analytical relationships between Ångström coefficients of aerosol extinction, scattering, 
absorption, and single scattering albedo, Atmos. Chem. Phys., 11, 10677–10680, https://doi.org/10.5194/acp-11-10677-2011, 2011
'''
