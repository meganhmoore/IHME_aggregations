import h5py
import numpy as np
import pandas as pd
import xarray as xr
import netCDF4
import time
import memory_profiler

@profile
def pandas_agg(file_list, comp_file, comp_num):

	new = True
	for file in file_list:
        	print(file)
		temp = pd.read_hdf(file) 
        	temp.set_index(['age_group_id', 'cause_id','sex_id','year_id','location_id'], inplace = True)
        	if new == True:
			new = False
			df = temp
        	else:
			df = pd.concat([df, temp])
			df = df.groupby(['age_group_id','cause_id','sex_id','year_id'], as_index = True).sum()
        	


		
	#compare_pandas_agg(df, comp_file)


def compare_pandas_agg(aggregated_df, comp_file):
	print("Comparing Now:")
	comp_df = pd.read_hdf(comp_file)
	comp_df.set_index(['age_group_id','cause_id','sex_id','year_id','location_id'], inplace = True)
	#print("Size of compare dataframe: {comp}".format(comp = comp_df.size))
	#print("Size of aggregated dataframe: {agg}".format(agg = aggregated_df.size))

	check = True
	for el in comp_df:
		comp_val = comp_df[el]
		agg_val = aggregated_df[el]

		compare = np.isclose(comp_val, agg_val, rtol=1e-05, atol=1e-08, equal_nan=True)

		if compare is False:
			print("Not the same")
			check = False
			print("{comp} compared to {agg}".format(comp=comp_val, agg=agg_val))

	if check:
		print("All Equal!!!")
	else:
		print("Not all equal")


def main():
	#file lists
	sub_saharan_africa_filenames = [#scraped]
	practice = [#scraped]

	eastern_sub_saharan_africa = [#scraped]
	central_sub_saharan_africa = [#scraped]
	southern_sub_saharan_africa = [#scraped]
	western_sub_saharan_africa = [#scraped]
	countries = [#scraped]
   	kenya_subregions = [#scraped]
   	south_africa_subregions = [#scraped]

   	countries_without_subregions = [#scraped]
   	subregions_and_countries = [#scraped]
   	regions = [#scraped]

    	new_south_africa_subregions = [new_#scraped]

   	#pandas_agg(regions, '', 166)
	
	print("PANDAS from HDF5")

   	t0 = time.time()
   	pandas_agg(south_africa_subregions, '', 196)
   	t1 = time.time()
   	total = t1-t0
   	print("Time taken on Countries: {time}".format(time = total))
	
	"""
	t0 = time.time()
    	pandas_agg(western_sub_saharan_africa, '', 199)
    	t1 = time.time()
    	total = t1-t0
    	print("Time taken on West: {time}".format(time = total))

    	t0 = time.time()
    	pandas_agg(eastern_sub_saharan_africa, '', 174)
    	t1 = time.time()
    	total = t1-t0
    	print("Time taken on East: {time}".format(time = total))

    	t0 = time.time()
    	pandas_agg(central_sub_saharan_africa, '', 167)
    	t1 = time.time()
    	total = t1-t0
    	print("Time taken on Central: {time}".format(time = total))

    	t0 = time.time()
    	pandas_agg(southern_sub_saharan_africa, '', 192)
    	t1 = time.time()
    	total = t1-t0
    	print("Time taken on South: {time}".format(time = total))

    	t0 = time.time()
    	pandas_agg(regions, '', 166)
    	t1 = time.time()
    	total = t1-t0
    	print("Time taken on Regions: {time}".format(time = total))
        """

main()



