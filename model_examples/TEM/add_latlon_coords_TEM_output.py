#!/usr/bin/env python
"""
Add latitude and longitude coordinates to TEM output files.

This script reads a TEM output NetCDF file with Albers Conical Equal Area projection
coordinates and adds 2D latitude and longitude coordinate arrays. The modified dataset
is saved to a new file with '_with_latlon' appended to the filename.
"""

import argparse
import pathlib
import sys
import textwrap
import pyproj
import affine

import numpy as np
import rioxarray as rio
import xarray as xr


def add_latlon_coords(input_file):
    """
    Add latitude and longitude coordinates to a TEM output file.
    
    Parameters
    ----------
    input_file : str or Path
        Path to the input NetCDF file
        
    Returns
    -------
    Path
        Path to the output file with coordinates added
    """
    input_path = pathlib.Path(input_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    print(f"Loading dataset from {input_file}...")
    
    # Load the dataset
    xds = xr.open_dataset(input_file, decode_coords="all", decode_cf=True)
    # Load the dataset
    xds = xr.open_dataset(input_file, decode_coords="all", decode_cf=True)

    # Set the CRS based on the attribute in the dataset
    xds.rio.set_crs(rio.crs.crs_from_user_input(xds['albers_conical_equal_area'].attrs['spatial_ref']))

    # Read the GeoTransform out of the dataset, 
    # Take the string representation, split it, convert to floats
    gT = [float(x) for x in xds.albers_conical_equal_area.GeoTransform.strip().split(' ')]

    # Unpack the GeoTransform into an Affine object and assign to xds
    xds.rio.transform = affine.Affine.from_gdal(*gT)

    # Make an object that can convert between projections
    transformer = pyproj.Transformer.from_crs(xds.rio.crs.to_epsg(), 4326)

    # 2D grids of x and y in projected coordinates
    X, Y = xds.rio.transform * (np.meshgrid(np.arange(xds.sizes['x']), np.arange(xds.sizes['y'])))

    # NOTE: Not sure how to confirm if the origin is upper left or lower left!!!
    
    # 2D grids of lat and lon
    LONS, LATS = transformer.transform(Y, X)

    # Assign to xds
    print("Adding latitude and longitude coordinates...")
    xds['lat'] = (('y','x'), LATS)
    xds['lat'].attrs['long_name'] = 'latitude'
    xds['lat'].attrs['units'] = 'degrees_north'
    xds['lat'].attrs['standard_name'] = 'latitude'
    
    xds['lon'] = (('y','x'), LONS)
    xds['lon'].attrs['long_name'] = 'longitude'
    xds['lon'].attrs['units'] = 'degrees_east'
    xds['lon'].attrs['standard_name'] = 'longitude'

    # Create output filename
    output_file = input_path.parent / f"{input_path.stem}_with_latlon{input_path.suffix}"
    
    print(f"Saving modified dataset to {output_file}...")
    xds.to_netcdf(output_file)
    xds.close()
    
    print("Successfully added lat/lon coordinates!")
    return output_file


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Add latitude and longitude coordinates to TEM output NetCDF files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
          Examples:
            %(prog)s output/GPP_yearly_tr.nc
            %(prog)s my_data/VEGC_monthly_tr.nc
        """)
    )
    
    parser.add_argument(
        'input_file',
        type=str,
        help='Path to the input NetCDF file'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    try:
        output_file = add_latlon_coords(args.input_file)
        print(f"\nOutput file: {output_file}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())





