#!/usr/bin/env python

# Helper script to limp thru tem experiments with the demo data till we 
# have proper inputs...

import pathlib
import xarray as xr

def run_glue_transient_scenario(input_folder):

  print(f"Opening historic and projected climate datasets from {input_folder}...")
  hds = xr.open_dataset(pathlib.Path(input_folder) / "historic-climate.nc")
  pds = xr.open_dataset(pathlib.Path(input_folder) / "projected-climate.nc")

  print("Gluing historic and projected climate datasets...")
  full_data = xr.concat([hds, pds], 
                        dim="time", 
                        data_vars="minimal", 
                        coords="minimal", 
                        compat="override", 
                        join="outer")
  print("Saving transient scenario climate dataset...")
  full_data.to_netcdf(pathlib.Path(input_folder) / "transient-scenario-climate.nc", 
                      mode='w', format='NETCDF4_CLASSIC',
                      engine='netcdf4')

  hds.close()
  pds.close()

  print(f"Opening historic and projected CO2 datasets from {input_folder}...")
  hds = xr.open_dataset(pathlib.Path(input_folder) / "co2.nc")
  pds = xr.open_dataset(pathlib.Path(input_folder) / "projected-co2.nc")

  print("Gluing historic and projected CO2 datasets...")
  full_data = xr.concat([hds, pds], 
                        dim="year", 
                        # data_vars="minimal", 
                        # coords="minimal", 
                        # compat="override", 
                        # join="outer"
                        ) 
  print("Saving transient scenario CO2 dataset...")
  full_data.to_netcdf(pathlib.Path(input_folder) / "transient-scenario-co2.nc", 
                      mode='w', format='NETCDF4_CLASSIC',
                      engine='netcdf4')                      

  hds.close()
  pds.close()

if __name__ == "__main__":
  import sys

  if len(sys.argv) != 2:
    print("Usage: python glue_transient_scenario.py <input_folder>")
    sys.exit(1)

  input_folder = sys.argv[1]

  if not pathlib.Path(input_folder).exists():
    raise ValueError(f"Input folder {input_folder} does not exist!")
  
  run_glue_transient_scenario(input_folder)
  
  print("Done.")
  