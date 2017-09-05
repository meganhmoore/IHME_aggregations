import h5py
import numpy as np
import pandas as pd
import xarray as xr
import netCDF4
import time


"""
this function goes through and determines the location of the draw that we want to use in each file so that we know 
which draw to reference in order to aggregate the correct information for this example, we are using the case of 
year = 1990, sex = 1, age = 2, cause = 695 
"""

def find_draw_in_xarray(filename):
    print("new")
    #read in the .h5 file
    df = pd.read_hdf(filename,key='draws',dims='draws')

    if len(df.columns) == 1:
        #creating a dataArray
        df[df.columns[0]].to_xarray()
    else:
        #create a dataset in xarry using draws as indices
        ds=df.to_xarray()
        ds = ds.rename({"index": "draw"})
        net_file='test.nc'

        #save it to a netcdf file (maybe just do this at the end to save time)
        ds.to_netcdf(net_file)
        new_ds = xr.open_dataset('test.nc')

    """
    print("LOCATION {vars}".format(vars=new_ds.data_vars['location_id']))
    print("YEAR {vars}".format(vars=new_ds.data_vars['year_id']))
    print("SEX {vars}".format(vars=new_ds.data_vars['sex_id']))
    print("AGE GROUP {vars}".format(vars=new_ds.data_vars['age_group_id']))
    print("CAUSE {vars}".format(vars=new_ds.data_vars['cause_id']))
    """


    """
    this loop iterates through the file draw by draw to determine which one contains the right
    info so that we can take the numbers from there (ex. 1990,1,2,695)
    """
    i = 0 #iterates through the file's draws
    draw_num = 0 #keeps track of which draw contains the correct information
    for element in new_ds:
        year_val = new_ds.data_vars['year_id']
        year = year_val[i]
        sex_val = new_ds.data_vars['sex_id']
        sex = sex_val[i]
        age_val = new_ds.data_vars['age_group_id']
        age = age_val[i]
        cause_val = new_ds.data_vars['cause_id']
        cause = cause_val[i]

        #printing the right draw that all of the matching information appears in
        if year == 1990 and sex == 1 and age == 2 and cause == 695:
             print(i)
             draw_num = element
             print("Draw: {draw_num}".format(draw_num=element))
        i=i+1


"""
This function compares the current pandas values that have already been aggregated to the xarray aggregated values to
make sure that they are equal and returns success if they are the same, if this is the case then we can go forward with 
timing the aggregation and comparing it to the pandas aggregation

This function takes in the file for the region that we are aggregating to (ex. eastern sub saharan africa or sub saharan africa)
as well as the the draw file that we aggregated for in the previous function. After extracting the right draw from the 
region file, we can compare that to our aggregated draw

This returns a print statement as to the success or error in comparison
"""
def compare_values(agg_vals, compare_region):
    print("In compare function")

    compare = pd.read_hdf(compare_region, coords = 'draws', dims = 'draws')
    ds_compare = compare.to_xarray()
    ds_compare = ds_compare.rename({"index": "draw"})
    da_compare = ds_compare[u'draw_97']

    da_size = da_compare.size
    agg_vals_size = agg_vals.size
    if da_size != agg_vals_size:
        print("ERROR: these draws are of different sizes")
        print(da_size)
        print(agg_vals_size)

    else:
        i = 0
        equal = True
        while (equal == True) and (i < da_size):
            #to ensure that the values are equal within a range use np.isclose
            compare = np.isclose(da_compare[i], agg_vals[i], rtol=1e-05, atol=1e-08, equal_nan=False)

            if compare == False:
                print("ERROR: there are different values in the two different aggregate arrays")
                print("{original} vs. {comp}".format(original=da_compare[i], comp=agg_vals[i]))
                equal = False
            else:
                i=i+1
        if equal == True:
            print("SUCCESS!")
            #if this is a success then we can go ahead and concatenate the xarray aggregation, and then time these
    print("Finished with comparison")





"""
after finding the right draw in each file we want to aggregate those draws together to create an overall sum for the region
by iterating through each column in each draw we will sum together the matching data points to produce an aggregate value.

takes in a given list depending on the region you want to end up with (central, easter, western, southern sub-saharan africa, or
sub-saharan africa overall)

returns a draw containing all of the aggregated data
"""
final = xr.DataArray(np.zeros((70833, )), dims = "draws")

def aggregate_region(region_list, compare_region):

    """ONLY NEED THIS CHUNK IF YOU WANT TO CONCATENATE THE DRAW ONTO THE REGION FILE"""
    #temp = pd.read_hdf('1_166.h5',key='draws',dims='draws')
    #temp_net = temp.to_xarray()
    #temp_net= temp_net.rename({'index':'draw'})
    #agg_file = 'aggregations.nc'
    #temp_net.to_netcdf(agg_file)
    #agg_ds = xr.open_dataset(agg_file)



    #creates a new draw to aggregate the values
    concat_da = xr.DataArray(np.zeros((70833, )), dims = "draws")



    for file in region_list:
        temp = pd.read_hdf(file, coords = 'draws', dims = 'draws')
        ds_temp = temp.to_xarray()
        ds_temp = ds_temp.rename({"index": "draw"})
        print(file)
        array = ds_temp[u'draw_97']
        print(array.size)

        # going through every element in the specific draw of the file and adding them to the current aggregation draw
        for i in range(70833):
            if i > (array.size-1):
                new = 0
            else:
                new = ds_temp[u'draw_97'][i]
            concat_da[i]= concat_da[i]+new


    #xr.concat([agg_ds, concat_da], dim="draws")
    print(concat_da)
    compare_values(concat_da,compare_region)
    final = concat_da
    print final
    final_file = 'final.nc'
    final.to_netcdf(final_file)
    return(concat_da)



def main():
    # files containing all of the relevant files for sub-saharan africa
    sub_saharan_africa_filenames = [#scraped]]

    practice = [#scraped]

    eastern_sub_saharan_africa = [#scraped]
    central_sub_saharan_africa = [#scraped]
    southern_sub_saharan_africa = [#scraped]
    western_sub_saharan_africa = [#scraped]
    countries = [#scraped]
    kenya_subregions = [#scraped]

    south_africa_subregions = [#scraped]


    # time the aggregation of all of the countries in sub saharan africa and print the time
    print("Aggregation of countries: ")
    t0 = time.time()
    aggregate_region(countries, '')
    t1 = time.time()
    total = t1 - t0
    print(total)

    print("Practice aggregation: should produce an error in compare")
    aggregate_region(practice, '')

    print("Aggregation of Central Sub-Saharan Africa")
    aggregate_region(central_sub_saharan_africa, '')

    print("Aggregation of Western Sub-Saharan Africa")
    aggregate_region(western_sub_saharan_africa, '')

    print("Aggregation of Eastern Sub-Saharan Africa")
    aggregate_region(eastern_sub_saharan_africa, '')

    print("Aggregation of Southern Sub-Saharan Africa")
    aggregate_region(southern_sub_saharan_africa, '')

    print("Aggregation of the subregions of Kenya")
    aggregate_region(kenya_subregions, '')

    print("Aggregation of the subregions of South Africa")
    aggregate_region(south_africa_subregions, '')


main()