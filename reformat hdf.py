import numpy as np
import pandas as pd
import xarray as xr
import netCDF4
import time
import xr_conversion

def reformat(filelist):
        for file in filelist:
                t2 = time.time()
                temp = pd.read_hdf(file)
                temp.set_index(['age_group_id', 'cause_id','sex_id','year_id','location_id'], inplace = True)
                print(file)
                name = "new"+file
                temp.to_hdf(name, 'w')
                t3 = time.time()
                print("Time to read and save to netcdf: {time}".format(time=t3-t2))
def main():
        kenya_subregions = [#scraped]

        south_africa_subregions = [#scraped]

        reformat(south_africa_subregions)
        print("Done")

main()