import numpy as np
import pandas as pd
import xarray as xr
import netCDF4
import time
import xr_conversion


def read_to_netcdf(filelist):
    
    #reading all of the files to netcdf before manipulating them for better speedup
    
    netcdf_list = []
    for file in filelist:
    	#t0 = time.time()
        #print(filelist)
        print(file)
        df = pd.read_hdf(file)
        df.set_index(['age_group_id', 'cause_id','sex_id','year_id','location_id'], inplace = True)
        #figure out if there is a way to convert the specific draw directly to netcdf rather than converting the whole file to a netcdf
        
        ds = df.to_xarray()
        #df_xarray = df[df.columns[103]].to_xarray()
        #print(df_xarray)

        split = file.split(".")
        #print(split)
        #print("Save: {first}".format(first=split[0]))
        netcdf_name = split[0]+".nc"
        print(netcdf_name)

        ds.to_netcdf(netcdf_name)
        netcdf_list.append(netcdf_name)
        #print(netcdf_list)
        #t1 = time.time()
        #print("time was: {time}".format(time = (t1-t0)))

	#return netcdf_list

def read_to_data_array(filelist):
    netcdf_list = []
    for file in filelist:
        t2=time.time()
        df = pd.read_hdf(file)
        da = xr_conversion.df_to_xr(df, dims = ['age_group_id', 'sex_id', 'year_id', 'cause_id', 'location_id'], wide_dim_name = 'draws')
        print(file)
        split = file.split(".")
        netcdf_name = split[0]+".nc"
        da.to_netcdf(netcdf_name)
        t3=time.time()
        netcdf_list.append(netcdf_name)
        print("Time to read and save to netcdf: {time}".format(time=t3-t2))


def main():
    countries = [#scraped]
    regions = [#scraped]

    eastern_sub_saharan_africa = [#scraped]

    central_sub_saharan_africa = [#scraped]
    southern_sub_saharan_africa = [#scraped]
    western_sub_saharan_africa = [#scraped]

    south_africa_subregions = [#scraped]

    kenya_subregions = [#scraped]
  
    """
    #scraped
    """

    t0 = time.time()
    data_array_regions = read_to_data_array(kenya_subregions)
    t1 = time.time()
    total = t1 - t0
    print("Total time taken: {time}".format(time=total))

    #print("SOUTH AFRICA")
    #netcdf_south_africa = read_to_netcdf(south_africa_subregions)
    #print("DONE")    
	#netcdf_regions = read_to_netcdf(regions)
    	#netcdf_east = read_to_netcdf(eastern_sub_saharan_africa)
    	#netcdf_central = read_to_netcdf(central_sub_saharan_africa)
    	#netcdf_south = read_to_netcdf(southern_sub_saharan_africa)
    	#netcdf_west = read_to_netcdf(western_sub_saharan_africa)

    
	

print("Starting")
main()
