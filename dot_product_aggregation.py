
import h5py
import numpy as np
import pandas as pd
import xarray as xr
import netCDF4
import time
#import memory_profiler

#@profile
def test(region_list, compare_file, compare_num):
    """
    aggregating location files together by concatenating locations together and summing their values together
    along the location dimension so that all of the information is aggregated to represent the super region. Each
    time a file is concatenated and summed, the dataset is reindexed to include the location dimension so that 
    new location files can be added and summed in
    (like sub-saharan africa)
    """
    new = True
    for file in region_list:
        #temp = xr.open_dataarray(file)
        temp = xr.open_dataset(file)
        temp = temp.squeeze('location_id')
        print(file)
        
        if new:
            da = temp.to_array()
            new = False
        else:
            temp_da = temp.to_array()
            #da = ds.to_array()
            da = da.dot(temp_da)
            #ds = temp.dot(ds)
            ds = da.to_dataset() 
            ds = ds.expand_dims('location_id')
           
    #ds = da.to_dataset() 
    ds.coords['location_id'] = compare_num
    #ds = ds.expand_dims('location_id')
    df = ds.to_dataframe()

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
    #print(comp_ds)
    #print(aggregated_ds)


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
    sub_saharan_africa_filenames = [#scraped]]

    practice = [#scraped]

    eastern_sub_saharan_africa = [#scraped]

    central_sub_saharan_africa = [#scraped]
    southern_sub_saharan_africa = [#scraped]
    western_sub_saharan_africa = [#scraped]
    netcdf_eastern_sub_saharan_africa = [#scraped]

    netcdf_central_sub_saharan_africa = [#scraped]
    netcdf_southern_sub_saharan_africa = [#scraped]
    netcdf_western_sub_saharan_africa = [#scraped]
    countries = [#scraped]
    netcdf_countries = [#scraped]

    netcdf_regions = [#scraped]
    kenya_subregions = [#scraped]

    south_africa_subregions = [#scraped]

    countries_without_subregions = [#scraped]
    subregions_and_countries = [#scraped]
    regions = [#scraped]

    list = [south_africa_subregions, kenya_subregions, countries_without_subregions]

    print("XARRAY + netCDF")

    #start timing
    """t0 = time.time()
    test(netcdf_countries, '', 166)
    t1=time.time()
    total = t1-t0
    print("Time Taken on Countries: {time}".format(time=total))"""
    
    """
    
    t0 = time.time()
    test(netcdf_western_sub_saharan_africa, '', 199)
    t1=time.time()
    total = t1-t0
    print("Time Taken on West: {time}".format(time=total))

    t0 = time.time()
    test(netcdf_eastern_sub_saharan_africa, '', 174)
    t1=time.time()
    total = t1-t0
    print("Time Taken on East: {time}".format(time=total))

    t0 = time.time()
    test(netcdf_central_sub_saharan_africa, '', 167)
    t1=time.time()
    total = t1-t0
    print("Time Taken on Central: {time}".format(time=total))

    t0 = time.time()
    test(netcdf_southern_sub_saharan_africa, '', 192)
    t1=time.time()
    total = t1-t0
    print("Time Taken on South: {time}".format(time=total))
    """

    t0 = time.time()
    test(netcdf_regions, '', 166)
    t1=time.time()
    total = t1-t0
    print("Time Taken on Regions: {time}".format(time=total))

main()
