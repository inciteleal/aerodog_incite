"""
AERONET Data Organization & Graphics - AERODOG
Function to organize directsun and inversion AERONET data (level 1.0, 1.5 or 2.0) into standardized folder and cleaning up spurious data
Function created on Mon Nov 22 17:04:21 2021
AERODOG first version created on Wed Dec 23 17:45:08 2020
@author: Alexandre C. Yoshida, Fábio J. S. Lopes and Alexandre Cacheffo
"""
import os
import math
import numpy as np
import pandas as pd
import time

'''
=============================================
globaltime variable - concatenate Date and time 
=============================================
'''
def globaltime_function(row): 
    date = row['Date(dd:mm:yyyy)']+' '+row['Time(hh:mm:ss)']
    dateframe = pd.to_datetime(date,format= '%d:%m:%Y %H:%M:%S' )
    dateformat = dateframe.strftime('%Y-%m-%d %H:%M:%S')
    return dateformat

'''
=============================================
Function to set Date and Time as globaltime index
=============================================
'''
def globaltime_index(funcdata):
    funcdata['globaltime'] = pd.to_datetime(funcdata['globaltime'],format= '%Y-%m-%d %H:%M:%S' )
    funcdata = funcdata.set_index('globaltime')
    return funcdata

'''
=============================================
Function to read files from AERONET - direct-sun and inversion algorithm - level1.5 or level2.0 
=============================================
'''
def reading_aeronet_data(rootdir,filetype,rawdatadir):
    inputdir = os.sep.join([rootdir,rawdatadir])
    files = [name for name in os.listdir(inputdir) if name.endswith(filetype)]
    
    return files

'''
=============================================
Function for organization of AERONET Aerosol Optical Depth (V3) - level1.5 or level2.0 data - direct sun and inversion algorithm
=============================================
'''
def organizing_aeronet_data(rootdir,rawfile,filetype,use_cols,rowstoskip,rawlevel,rawdatadir,outputdir):
    inputdir = os.sep.join([rootdir,rawdatadir]) 
    newfiles = os.sep.join([inputdir, rawfile[0]])
    newfilepath = newfiles.replace(rawdatadir, outputdir).replace('_'+str(rawlevel)+'.'+filetype, '.'+str(rawlevel)+'_'+filetype+'_v01')
    f = pd.read_csv(newfiles,usecols=use_cols, skiprows=range(0, rowstoskip))
    f = f.replace(-999.,np.nan)
    f = f.replace(0,np.nan)
    f = f.dropna()
    f.insert(1,'globaltime',f.apply(globaltime_function, axis=1))
    f.to_csv(newfilepath,float_format="%.6f",index=False)  

'''
=============================================
Function to concatenate direct-sun and inversion algorithm from AERONET data measurements
=============================================
'''        
def mining_aeronet_data(rootdir,filetype,rawlevel,avgtime,rawdatadir,outputdir):
        inputdir = os.sep.join([rootdir,rawdatadir])
        files = [name for name in os.listdir(inputdir) if name.endswith(''.join([str(rawlevel),'.',filetype]))]
        lenfiles = len(files)
        
        for j in range(0, lenfiles):
            aeronetfile = pd.read_csv(os.sep.join([inputdir, files[j]]))
            
            '''Applying func1 (date&Time as index) in AOD, SSA, PFN and TAB files - resample as XX minutes mean data '''
            aeronetfile_index = globaltime_index(aeronetfile)
            aeronetfile_mean = aeronetfile_index.groupby('AERONET_Site').resample(avgtime).mean()
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

'''AOD calculation at 532 nm'''
def aod532(row):
        return row["AOD_500nm"]*(500/532)**((-1.)*row["AE_440_675nm"])

#'''Angstrom Exponent calculation at 355 nm'''
#def ae355(row):
#        return np.log((row["AOD_440nm"])/(row["AOD_340nm"]))/(np.log(340/440)) 

'''AOD calculation at 355 nm'''
def aod355(row):
        return row["AOD_380nm"]*(380/355)**((-1.)*row["AE_340_440nm"])

'''Lidar Ratio calculation at 440 nm'''
def lr440(row):
        return 4*(math.pi)/row['pfn180_440nm']*row['SSA_440nm']

'''The LR calculation at 675 nm'''
def lr675(row):
        return 4*(math.pi)/row['pfn180_675nm']*row['SSA_675nm']

'''The LR calculation at 870 nm'''
def lr870(row):
        return 4*(math.pi)/row['pfn180_870nm']*row['SSA_870nm']

'''The LR calculation at 1020 nm'''
def lr1020(row):
        return 4*(math.pi)/row['pfn180_1020nm']*row['SSA_1020nm']

'''The Lidar ratio - Angstrom Exponent relation using 440 and 870 nm'''
def lrae532(row):
        return np.log((row["LR_870nm"])/(row["LR_440nm"]))/(np.log(440/870))
    
'''The Lidar ratio calculation at 532 nm using LR values of 675 nm'''
def lr532(row):
        return row["LR_675nm"]*(532/675)**((-1.)*row["LRAE_532nm"])

'''The  spectral  variability  of  the  aerosol  single  scatterring  albedo  (dSSA) - Delta Single Scattering Albedo '''
def dssa(row):
   return row["SSA_440nm"]-row["SSA_675nm"]

'''Absorption AOD at 440 nm '''
def aaod440(row):
   return row["AOD_440nm"]*(1. - row["SSA_440nm"])

'''Absorption AOD at 675 nm '''
def aaod675(row):
   return row["AOD_675nm"]*(1. - row["SSA_675nm"])

'''Scattering AOD at 440 nm '''
def saod440(row):
   return row["AOD_440nm"]*(row["SSA_440nm"])

'''Scattering AOD at 675 nm '''
def saod675(row):
   return row["AOD_675nm"]*(row["SSA_675nm"])

'''Absorption Angstrom Exponent (AAE) at 440-675 nm '''
def aae(row):
   return (-1)*np.log((row["AAOD_440nm"])/(row["AAOD_675nm"]))/(np.log(440/675))

'''Scaterring Angstrom Exponent (SAE) at 440-675 nm ''' 
def sae(row):
   return (-1)*np.log((row["SAOD_440nm"])/(row["SAOD_675nm"]))/(np.log(440/675)) 

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
    aeronetmeanbp = aeronetdata.groupby(['Month']).mean()
     
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