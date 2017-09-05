import h5py
import logging
import numpy as np
import pandas as pd
import xarray as xr
import netCDF4
from netCDF4 import Dataset
import time
import cython
import setuptools
#import memory_profiler
import xr_conversion



def read_hdf_to_netcdf(hdf_list):
	for file in hdf_list:
		print(file)
		df = pd.read_hdf(file)
		da = xr_conversion.df_to_xr(df, dims = ['location_id', 'age_group_id', 'cause_id','sex_id','year_id'], wide_dim_name='draw')
		split = file.split(".")
		netcdf_name = split[0]+".nc"
		da.to_netcdf(netcdf_name)

def netcdf_query(netcdf_list):
	for file in netcdf_list:
		print(file)
		#rootgrp = Dataset(file, "a")
		#locgrp = rootgrp.createGroup("locations")
		#yeargrp = rootgrp.createGroup("years")
		#print(rootgrp.groups)
		#print(rootgrp.data_model)
		#print(rootgrp.dimensions)
		#print(rootgrp.variables)
		#print(rootgrp.file_format)
		#vals = netCDF4.get_variables_by_attributes(year_id = 1990)
		#print(rootgrp.disk_format)
		#print(rootgrp.dimensions.values)
		#print(rootgrp.variables['year_id'])
		#print(rootgrp['location_id'])
		#print(locations)
		#da = xr.open_dataarray(file['loction_id'])

		
		

def main():
	regions = [#scraped]
	netcdf_regions = [#scraped]

	#read_hdf_to_netcdf(regions)
	netcdf_query(netcdf_regions)
	print("finished")

main()

