
import h5py
import numpy as np
import pandas as pd
import xarray as xr
import netCDF4
import time
import memory_profiler

#@profile
def test(region_list, compare_file, compare_num):
    """
    aggregating location files together by concatenating locations together and summing their values together
    along the location dimension so that all of the information is aggregated to represent the super region. Each
    time a file is concatenated and summed, the dataset is reindexed to include the location dimension so that 
    new location files can be added and summed in
    (like sub-saharan africa) for timing, comment out the call to compare
    """
    new = True
    for file in region_list: 
        df = pd.read_hdf(file)
        df.set_index(['age_group_id', 'cause_id','sex_id','year_id','location_id'], inplace = True)
        print(file)
        if new:
            ds = df.to_xarray()
            new = False
        else:
            temp = df.to_xarray()
            ds = xr.concat([ds, temp], dim = 'location_id')#extend along location dimension
            ds = ds.sum('location_id')#sum along location dimension 
            ds.coords['location_id'] = (compare_num)#add location coordinate   
            ds = ds.expand_dims('location_id')#add location dimension
        
    compare_temp(ds, compare_file)
    

def compare_temp(aggregated_ds, comp_file):
    """
    compares the aggregated values to the sub-saharan country file to make sure that the locations were
    aggregated correctly and the values match. 
    """
    print("In temp_compare function")

    #read in the compare file to an xarray dataset
    comp_df = pd.read_hdf(comp_file)
    comp_df.set_index(['location_id', 'age_group_id', 'cause_id', 'sex_id', 'year_id'], inplace = True)
    comp_ds = comp_df.to_xarray()

    #checking to make sure that they both have the same dimensions and dataset size
    print("SIZE OF COMPARE DATASET: {comp_size}".format(comp_size = comp_ds.sizes))
    print("Aggregated Size: {agg_size}".format(agg_size = aggregated_ds.sizes))


    check = True
    for el in comp_ds:
        comp_val = comp_ds[el]
        agg_val = aggregated_ds[el]

        #compares the calculated values for equality within a margin and counts nan values and 0 as equal
        compare = np.isclose(comp_val, agg_val, rtol=1e-05, atol=1e-08, equal_nan=True)
        
        #if it is not equal
        if compare is False:
            print("not the same")
            check = False
            print("COMP {comp}".format(comp=comp_val))
            print("AGG {agg}".format(agg=agg_val))


    if check is True:
        print("ALL EQUAL!!!")
    else:
        print("NOT all equal")



def main():
    # files containing all of the relevant files for sub-saharan africa
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

    list = [south_africa_subregions, kenya_subregions, countries_without_subregions]

    #test(regions, '', 166)

    
    #start timing
    t0 = time.time()
    test(countries, '', 166)
    t1=time.time()
    total = t1-t0
    print("Total Time Taken on countries: {time}".format(time=total))

    
    t0 = time.time()
    test(western_sub_saharan_africa, '', 199)
    t1=time.time()
    total = t1-t0
    print("Total Time Taken on West: {time}".format(time=total))

    t0 = time.time()
    test(eastern_sub_saharan_africa, '', 174)
    t1=time.time()
    total = t1-t0
    print("Total Time Taken on East: {time}".format(time=total))

    t0 = time.time()
    test(central_sub_saharan_africa, '', 167)
    t1=time.time()
    total = t1-t0
    print("Total Time Taken on Central: {time}".format(time=total))

    t0 = time.time()
    test(southern_sub_saharan_africa, '', 192)
    t1=time.time()
    total = t1-t0
    print("Total Time Taken on South: {time}".format(time=total))
    
    
    t0 = time.time()
    test(regions, '', 166)
    t1=time.time()
    total = t1-t0
    print("Total Time Taken on Regions: {time}".format(time=total))


main()


