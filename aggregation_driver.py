#import reshaped_aggregation
import reworked_nopandas_aggregation
#import pandas_aggregation
#import dataArray_aggregation
#import trying_dotproduct
import dataArray_from_netcdf
import numpy as np
import pandas as pd
import xarray as xr
import netCDF4
import time

def main():
	
  eastern_sub_saharan_africa = [#scraped]

  central_sub_saharan_africa = [#scraped]
  southern_sub_saharan_africa = [#scraped]
  western_sub_saharan_africa = [#scraped]
  countries = [#scraped]
  regions = [#scraped]

  netcdf_eastern_sub_saharan_africa = [#scraped]

  netcdf_central_sub_saharan_africa = [#scraped]
  netcdf_southern_sub_saharan_africa = [#scraped]
  netcdf_western_sub_saharan_africa = [#scraped]

  netcdf_countries = [#scraped]
  netcdf_regions = [#scraped]
  south_africa_subregions = [#scraped]
    
  #for i in range(5):
  reworked_nopandas_aggregation.main()
      
  #for i in range(5):
  #print("RUnning pandas now")
  #pandas_aggregation.main()
    
  #for i in range(5):
  #reshaped_aggregation.main()
  #dataArray_aggregation.main()
  dataArray_from_netcdf.main()
  #trying_dotproduct.main()


main()
main()
main()
main()
main()
