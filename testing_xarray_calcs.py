import numpy as np
import pandas as pd
import xarray as xr
import netCDF4
import time
import xr_conversion

def pandas_merge_time(fileset):
	new = True
	for file in fileset:
		temp = pd.read_hdf(file)
		temp.set_index(['age_group_id', 'cause_id','sex_id','year_id','location_id'], inplace = True)
		if new:
			print("FIRST")
			df = temp
			new = False
		else:
			t0 = time.time()
			df = df*temp
			t1 = time.time()
			print("pandas time: {time}".format(time=t1-t0))

	print("done")

def xarray_merge_time(fileset):
	new = True
	for file in fileset:
		temp = xr.open_dataarray(file)
		if new:
			print("FIRST")
			da = temp
			da.squeeze('location_id')
			new = False
		else:
			t0 = time.time()
			da = da * temp
			t1 = time.time()
			print("xarray time: {time}".format(time = t1-t0))
	print("done")

def main():
	south_africa_subregions = [#scraped]
	netcdf_south_africa_subregions = [#scraped]
    	pandas_merge_time(south_africa_subregions)
    	xarray_merge_time(netcdf_south_africa_subregions)
    	print("DONE")

main()
