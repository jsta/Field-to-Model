#!/usr/bin/env python

# Helper script to limp thru tem experiments with the demo data till we 
# have proper inputs...

import pathlib
import xarray as xr

def run_glue_transient_scenario(input_folder):

  hds = xr.open_dataset(pathlib.Path(input_folder) / "historic-climate.nc")
  pds = xr.open_dataset(pathlib.Path(input_folder) / "projected-climate.nc")

  full_data = xr.concat([hds, pds], 
                        dim="time", 
                        data_vars="minimal", 
                        coords="minimal", 
                        compat="override", 
                        join="outer")




  full_data.to_netcdf(pathlib.Path(input_folder) / "transient-scenario-climate.nc", 
                      mode='w', format='NETCDF4_CLASSIC',
                      engine='netcdf4')

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
  