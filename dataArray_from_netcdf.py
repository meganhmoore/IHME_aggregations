
import h5py
import logging
import numpy as np
import pandas as pd
import xarray as xr
import netCDF4
import time
import memory_profiler
import xr_conversion

@profile
def dataArray_run(region_list, compare_file, compare_num):
    """
    using a dataArray datastructure rather than a dataset
    This function also uses a different way to read files into xarray
    so that it minimizes the overhead from to_xarray that is provided in pandas

    """

    new = True
    for file in region_list:
        print(file)
        temp = xr.open_dataarray(file)
        temp = temp.squeeze('location_id')
        if new:
            da = temp
            new = False
        else:
            da = da + temp        
    da.coords['location_id'] = compare_num
    da = da.expand_dims('location_id')


    #df = da.to_dataframe()
    #da.to_netcdf('array.nc')


    #compare_temp(da, compare_file)
    

def compare_temp(aggregated_da, comp_file):
    """
    compares the aggregated values to the sub-saharan country file to make sure that the locations were
    aggregated correctly and the values match. 
    """
    print("In temp_compare function")

    #read in the compare file to an xarray dataset
    comp_df = pd.read_hdf(comp_file)
    comp_da = xr_conversion.df_to_xr(comp_df, dims = ['location_id','age_group_id', 'sex_id', 'year_id', 'cause_id'], wide_dim_name = 'draw')
    #compare = np.isclose(comp_da, aggregated_da, rtol=1e-05, atol=1e-08, equal_nan=True)
    #print("COMPARE VALUE {comp}".format(comp=compare))
    if comp_da.equals(aggregated_da):
        print("EQUAL")
    else:
        print("NOT EQUAL")
    #for el in comp_da:
        #print(comp_da.size())
        #print(el)
        #print(el.sizes())
    #xr.testing.assert_allclose(aggregated_da, comp_da, rtol=1e-02, atol=1e-04)
    #print("done comparing")
    print("Next equality test:")
    good_coords = [
        val for val in aggregated_da.coords['location_id'].values
        if val in comp_da.coords['location_id'].values]
    matched = comp_da.loc[{'location_id': good_coords}]
    print("GOOD COORD VALS: {good}".format(good=good_coords))
    print("MATCHED VALS: {matched}".format(matched=matched))
    
    print("Final test")    
    check = True
    print("AGG {agg}".format(agg=aggregated_da))
    print("COMP {comp}".format(comp=comp_da))
    draw_vals = comp_da.coords['draw'].values
    print("DRAW_VALS {draw}".format(draw=draw_vals))
    for el in draw_vals:
        print("HERE")
        print("VALUE {el}".format(el=el))
        #print(el.length())
        #print("Size {len}".format(len = el.size()))
        
        comp_val = comp_da.__getitem__(el)
        agg_val = aggregated_da.__getitem__(el)
                #print(comp_val)
                #print(agg_val)

            #compares the calculated values for equality within a margin and counts nan values and 0 as equal
        compare = np.isclose(comp_val, agg_val, rtol=1e-05, atol=1e-08, equal_nan=True)
            
            #if it is not equal
        if compare.all() is False:
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
    netcdf_eastern_sub_saharan_africa = [#scraped]

    netcdf_central_sub_saharan_africa = [#scraped]
    netcdf_southern_sub_saharan_africa = [#scraped]
    netcdf_western_sub_saharan_africa = [#scraped]
    countries = [#scraped]
    netcdf_countries = [#scraped]
    netcdf_regions = [#scraped]
    kenya_subregions = [#scraped]

    south_africa_subregions = [#scraped]

    netcdf_south_africa_subregions = [#scraped]
    countries_without_subregions = [#scraped]
    subregions_and_countries = [#scraped]
    regions = [#scraped]
    list = [south_africa_subregions, kenya_subregions, countries_without_subregions]
    print("DataArrays from netcdf") 

    t0 = time.time()
    dataArray_run(netcdf_south_africa_subregions, '', 196)
    t1=time.time()
    total = t1-t0
    print("Time Taken on Regions: {time}".format(time=total))

    
    #temp = xr.open_dataarray('array.nc')
    #compare_temp(temp, '')

    """
    t0 = time.time()
    test(countries, '', 166)
    t1=time.time()
    total = t1-t0
    print("Time Taken on Countries: {time}".format(time=total))
    
    
    t0 = time.time()
    test(western_sub_saharan_africa, '', 199)
    t1=time.time()
    total = t1-t0
    print("Time Taken on West: {time}".format(time=total))

    t0 = time.time()
    test(eastern_sub_saharan_africa, '', 174)
    t1=time.time()
    total = t1-t0
    print("Time Taken on East: {time}".format(time=total))

    t0 = time.time()
    test(central_sub_saharan_africa, '', 167)
    t1=time.time()
    total = t1-t0
    print("Time Taken on Central: {time}".format(time=total))

    t0 = time.time()
    test(southern_sub_saharan_africa, '', 192)
    t1=time.time()
    total = t1-t0
    print("Time Taken on South: {time}".format(time=total))
    """

    #start timing
    """
    t0 = time.time()
    test(netcdf_countries, '', 166)
    t1=time.time()
    total = t1-t0
    print("Time Taken on Countries: {time}".format(time=total))
    
    
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

    t0 = time.time()
    test(netcdf_regions, '', 166)
    t1=time.time()
    total = t1-t0
    print("Time Taken on Regions: {time}".format(time=total))
    """

main()

