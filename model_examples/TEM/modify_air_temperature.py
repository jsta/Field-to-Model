#!/usr/bin/env python

# T. Carman, 2025, October
# Demonstration script to modify air temperature in a TEM input dataset
# by adding a constant offset during specified months and years. For use in 
# ModEx Workshop.

import pathlib
import argparse

import xarray as xr


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description="Modify air temperature in a TEM input dataset by adding a constant offset."
  )
  parser.add_argument(
    "--input-file", type=str, required=True,
    help="Path to the input NetCDF file containing TEM data."
  )
  parser.add_argument(
    "--deviation", type=float, required=True,
    help="Temperature offset (in degrees Celsius) to add to air temperature."
  )
  parser.add_argument(
     "--years", required=True, type=int, nargs='+',
     help="Year(s) to modify."
  )
  parser.add_argument(
     "--months", required=True, type=int, nargs='+',
     help="Month(s) to modify."
  )

  args = parser.parse_args()
  #print(f"{args=}")

  print(f"This script will modify air temperature in {args.input_file} by "
        f"{args.deviation}°C during the months {args.months} of the years {args.years}.")

  if not pathlib.Path(args.input_file).is_file():
    raise RuntimeError(f"Error: Input file {args.input_file} does not exist!")

  print(f"Opening dataset {args.input_file}...")
  with xr.open_dataset(args.input_file) as ds:
    print(f"Creating time mask for years {args.years} and months {args.months}...")
    time_mask = ((ds.time.dt.year.isin(args.years)) & 
                (ds.time.dt.month.isin(args.months)))

    print("Adjustments will be applied to the following time points:")
    print(ds.time[time_mask].values)

    print(f"Adjusting air temperature by {args.deviation}°C for selected times...")

    # Where time_mask is True, add deviation; else keep original values
    ds['tair'] = ds['tair'].where(~time_mask, ds['tair'] + args.deviation)

  print("Saving modified dataset...")
  ds.to_netcdf(pathlib.Path(args.input_file).parent / f"modified_{pathlib.Path(args.input_file).name}")

