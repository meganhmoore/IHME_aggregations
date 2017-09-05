
import h5py
import numpy as np
import pandas as pd
import xarray as xr
import netCDF4
import time
import pdb


"""def read_to_netcdf(filelist, draw_num):
    
    #reading all of the files to netcdf before manipulating them for better speedup
    
    netcdf_list = []
    for file in filelist:
        df = pd.read_hdf(file, key='draws', dims='draws')
        #figure out if there is a way to convert the specific draw directly to netcdf rather than converting the whole file to a netcdf
        df_xarray = df[df.columns[103]].to_xarray()
        print(df_xarray)

        print(file)
        split = file.split(".")
        print(split)
        print("Save: {first}".format(first=split[0]))
        netcdf_name = split[0]+".nc"
        print(netcdf_name)

        df_xarray.to_netcdf(netcdf_name)
        netcdf_list.append(netcdf_name)
        print(netcdf_list)

    return netcdf_list"""
        




def compare_values(agg_vals, compare_region):
    """
    This function compares the current pandas values that have already been aggregated to the xarray aggregated values to
    make sure that they are equal and returns success if they are the same, if this is the case then we can go forward with
    timing the aggregation and comparing it to the pandas aggregation

    This function takes in the file for the region that we are aggregating to (ex. eastern sub saharan africa or sub saharan africa)
    as well as the the draw file that we aggregated for in the previous function. After extracting the right draw from the
    region file, we can compare that to our aggregated draw

    This returns a print statement as to the success or error in comparison
    """
    print("In compare function")

    compare = pd.read_hdf(compare_region, coords = 'draws', dims = ['location_id', 'age_group_id', 'cause_id','sex_id','year_id'])
    ds_compare = compare.to_xarray()
    ds_compare = ds_compare.rename({"index": "draw"})
    da_compare = ds_compare[u'draw_97']
    print(da_compare)
   # print(da_compare.coords)
    #print(da_compare.dims)

    da_size = da_compare.sizes
    agg_vals_size = agg_vals.sizes
    if da_size != agg_vals_size:
        print("ERROR: these draws are of different sizes")
        print(da_size)
        print(agg_vals_size)

    else:
        i = 0
        equal = True
        while (equal == True) and (i < da_size):
            #compare equality within a margin in order to ensure that the agg values are equal
            compare = np.isclose(da_compare[i], agg_vals[i], rtol=1e-05, atol=1e-08, equal_nan=False)
            print(compare) #if it is equal or not

            if compare == False:
                print("ERROR: there are different values in the two different aggregate arrays")
                print("{original} vs. {comp}".format(original=da_compare[i], comp=agg_vals[i]))
                equal = False
            else:
                i=i+1

            """
            if da_compare[i] != agg_vals[i]:
                temp_compare and temp_agg are values used to compare the aggregate value to the value that has already 
                been calculated and to ensure that the difference between the two values is within a small margin
                this is because the two numbers were different but only to a very very small margin
                temp_compare = da_compare[i] + .0000000001
                temp_agg = agg_vals[i] + .0000000001
                if(temp_compare > agg_vals[i]) and (temp_agg > da_compare[i]):
                    i=i+1
                    print("CONTINUING")
                else:
                    print("ERROR: there are different values in the two different aggregate arrays")
                    print("{original} vs. {comp}".format(original=da_compare[i], comp=agg_vals[i]))
                    equal = False
            else:
                i=i+1
            """
        if equal == True:
            print("SUCCESS!")
            #if this is a success then we can go ahead and concatenate the xarray aggregation, and then time these
    print("Finished with comparison")

#final = xr.DataArray(np.zeros((70833, )), dims = "draws")



def aggregate_region(region_list, compare_region):

    """
    after finding the right draw in each file we want to aggregate those draws together to create an overall sum for the region
    by iterating through each column in each draw we will sum together the matching data points to produce an aggregate value.

    takes in a given list depending on the region you want to end up with (central, easter, western, southern sub-saharan africa, or
    sub-saharan africa overall)

    returns a draw containing all of the aggregated data
    """

    """ONLY NEED THIS CHUNK IF YOU WANT TO CONCATENATE THE DRAW ONTO THE REGION FILE"""
    #temp = pd.read_hdf('#scraped',key='draws',dims='draws')
    #temp_net = temp.to_xarray()
    #temp_net= temp_net.rename({'index':'draw'})
    #agg_file = 'aggregations.nc'
    #temp_net.to_netcdf(agg_file)
    #agg_ds = xr.open_dataset(agg_file)

    print("Starting")

    #creates a new draw to aggregate the values
    #concat_da = xr.DataArray(np.zeros((70833, )), dims = 'draw')
    #concat_ds = xr.DataSet(dims='draws')
    #concat_ds = xr.concat([concat_ds, concat_da], dim = "draws")
    #print(concat_ds)


    for file in region_list:
        df = pd.read_hdf(file)
        df.set_index(['location_id', 'age_group_id', 'cause_id','sex_id','year_id'], inplace = T)
        ds = df.to_xarray()
        print(ds)
        da = ds.to_array(dim = 'draw')





        temp = pd.read_hdf(file, coords = 'draws', dims = ['draw','location_id', 'age_group_id', 'cause_id','sex_id','year_id']) #MAYBE ADD COORDS=DRAWS BACK HERE         key = 'draws',
        ds_temp = temp.to_xarray()
        #ds_temp = ds_temp.to_dataset(dim = 'draw')
        ds_temp = ds_temp.rename({"index": "draw"})
        #ds_temp = xr.open_dataset(file)
        print(ds_temp)
        print(file)
        print("DIMS {dims}".format(dims=ds_temp.dims))
       # print("DATA {data}".format(data=ds_temp.data_vars))
        print("COORDS {coords}".format(coords=ds_temp.coords))
        #print(ds_temp)

        index=0
        for el in ds_temp:
            #iterating through each row to see if it is the right combination of (sex, year, cause, age)
            year_ar=ds_temp.data_vars['year_id']
            year = year_ar[index]
            print("YEAR {year}".format(year=year_ar))
            sex_ar=ds_temp.data_vars['sex_id']
            sex = sex_ar[index]
            age_ar=ds_temp.data_vars['age_group_id']
            age = age_ar[index]
            cause_ar=ds_temp.data_vars['cause_id']
            cause = cause_ar[index]
            #print("Year {year},{sex},{age},{cause}".format(year=year, sex=sex, age=age, cause=cause))
            
            if year == 1990 and sex == 1 and age == 2 and cause == 695:
                print(el)
                correct_draw = el
                print("Index: {ind}".format(ind=index))
                draw_num = index
            index = index + 1
        

        array = ds_temp[correct_draw]
        #print("Dimension {dim}".format(dim=array.dims))
        #print(array)
        print(array.size)
        if region_list[0] != file:
            concat_ds = xr.concat([concat_ds, array], dim = 'draw')#coords = 'draws', dim = 'draws'
        else:
            concat_ds = array.to_dataset(dim = 'draw')    
        #concat_da = array.groupby('draw')
        #concat_ds = xr.concat([concat_ds, concat_da], dims='draws')
        #concat_da = xr.concat([concat_da, array], dim = 'draw')
        print("CONCAT {concat}".format(concat=concat_ds))
        print(concat_ds.dims)
        """

    
    if it is going to be concatenated as a new draw on an existing file use:
    xr.concat([agg_ds, concat_da], dim="draws")
    """
    #concat_da = concat_ds.groupby('draws')
    #print(concat_da)
    #compare_values(concat_ds,compare_region)
    #final = concat_ds
    #final_file = 'final.nc'
    #final.to_netcdf(final_file)
    #return(concat_da)

def test(region_list, compare_file, compare_num):
    new = True
    for file in region_list:
        df = pd.read_hdf(file)
        print(file)
        df.set_index(['age_group_id', 'cause_id','sex_id','year_id','location_id'], inplace = True)
        if new:
            ds = df.to_xarray()
            new = False
        else:
            temp = df.to_xarray()
            ds = xr.concat([ds, temp], dim = 'location_id')#, 'age_group_id', 'cause_id', 'sex_id', 'year_id'])
        
        #print(ds)
        print("SIZE {size}".format(size = ds.sizes))
        ds = ds.sum('location_id')#(dim='location_id', keep_attrs = True)
        ds.coords['location_id'] = (compare_num)
        ds = ds.expand_dims('location_id')
        
    #this might not be super scalable, it might be better to sum and reindex within the for loop
    #ds = ds.sum('location_id')#(dim='location_id', keep_attrs = True)
    #ds.coords['location_id'] = (compare_num)
    #ds = ds.expand_dims('location_id')
    #print(ds)


    #ds.transpose('location_id')
   # print(ds['age_group_id'].ndim())
   # print(ds['location_id'].ndim())
   # ds['location_id'].to_index()
    #ds.data_vars['location_id'] = (167)
   # ds.swap_dims({'location_id':'location_id'})

    

    #ds.set_index(['location_id', 'age_group_id', 'cause_id','sex_id','year_id'], inplace = True)
    #ds.reindex(location_id = 167)
    #ds = ds['location_id'] = 167
    #ds.transpose()
    #ds = ds.isel(location_id: 167)
    #ds.expand_dims('location_id')
    #print("up to DATE")
    #ds = ds.groupby('location_id').sum()

    #print(ds)
    print("FINAL SIZE {size}".format(size = ds.sizes))


    compare_temp(ds, compare_file)
    

    """test_file = xr.open_dataset(nc_file)
    print("TEST FILE: {test}".format(test=test_file))
    print(test_file.dims)
    for draw in test_file:
        print(draw)
    concat_da = test_file.groupby(u'draw').sum()
    print("GROUPED {group}".format(group=concat_da))
    print("SIZE {size}".format(size=concat_da.sizes))

    compare_da = concat_da.data_vars['draw_97']
    print("COMPARE ARRAY: {comp}".format(comp=compare_da))

    #for el in concat_da:
     #   print(el)

    compare_values(concat_da, '')"""

def compare_temp(aggregated_ds, comp_file):
    print("In temp_compare function")
    comp_df = pd.read_hdf(comp_file)
    comp_df.set_index(['location_id', 'age_group_id', 'cause_id', 'sex_id', 'year_id'], inplace = True)
    comp_ds = comp_df.to_xarray()
    print("SIZE OF COMPARE DATASET: {comp_size}".format(comp_size = comp_ds.sizes))
    print("Aggregated Size: {agg_size}".format(agg_size = aggregated_ds.sizes))


    #aggregated_ds = aggregated_ds.reindex_like(comp_ds) NOT WORKING
    
    #aggregated_ds = aggregated_ds.align(comp_ds)
    #print(aggregated_ds)
    check = True
    for el in comp_ds:
        
        #print(el)
        comp_val = comp_ds[el]
        agg_val = aggregated_ds[el]
        compare = np.isclose(comp_val, agg_val, rtol=1e-05, atol=1e-08, equal_nan=True)
        
        if compare is False:
            print("not the same")
            check = False
            print("COMP {comp}".format(comp=comp_val))
            print("AGG {agg}".format(agg=agg_val))

        else:
            print("COMP {comp}".format(comp=comp_val))
            print("AGG {agg}".format(agg=agg_val))
            #print("continue")

    if check is True:
        print("ALL EQUAL!!!")
    else:
        print("not all equal")



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

    list = [south_africa_subregions, kenya_subregions, countries_without_subregions]


    test(central_sub_saharan_africa, '', 167)
    #test(southern_sub_saharan_africa, '', 192)
    #test(western_sub_saharan_africa, '', 199)
    #test(eastern_sub_saharan_africa, '', 174)
    #test(regions, '', 166)
    test(countries, '', 166)

    #aggregate_region(countries, '')

    # time the aggregation of all of the countries in sub saharan africa and print the time
    """t0 = time.time()
    aggregate_region(countries, '')
    t1 = time.time()
    total = t1 - t0
    print(total)
    aggregate_region(practice, '')
    aggregate_region(central_sub_saharan_africa, '')
    aggregate_region(western_sub_saharan_africa, '')
    aggregate_region(eastern_sub_saharan_africa, '')
    aggregate_region(southern_sub_saharan_africa, '')
    aggregate_region(kenya_subregions, '')
    aggregate_region(south_africa_subregions, '')"""

main()
countries = [#scraped]
#test(countries)
