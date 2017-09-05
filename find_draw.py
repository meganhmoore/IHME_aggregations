import h5py
import numpy as np
import pandas as pd
import xarray as xr
import netCDF4



def find_draw_in_xarray(filename):
    """
    this function goes through and determines the location of the draw that we want to use in each file so that we know
    which draw to reference in order to aggregate the correct information for this example, we are using the case of
    year = 1990, sex = 1, age = 2, cause = 695
    """
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

subregions_and_countries = [#scraped]
for file in subregions_and_countries:
    find_draw_in_xarray(file)