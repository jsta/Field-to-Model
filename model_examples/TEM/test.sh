#!/bin/bash -f

# Make a place to save our output...
mkdir runs

# Use the helper tool to setup a working directory for your experiment
# has copies of parameters, config files, and 
pyddt-swd --input-data-path ${HOME}/install_dvmdostem/demo-data/cru-ts40_ar5_rcp85_ncar-ccsm4_toolik_field_station_10x10/ runs/EE3_warming

# Fiddle with the settings...single pixel, turn on some output variables...
cd runs/EE3_warming/
pyddt-runmask --reset --yx 5 5
pyddt-runmask --reset --yx 5 5 run-mask.nc 

pyddt-outspec config/output_spec.csv --on LAYERDZ m l
pyddt-outspec config/output_spec.csv --on TLAYER m l 

# check the outspec file to see what we have...
pyddt-outspec -s config/output_spec.csv 

# Run the model
dvmdostem -p 25 -e 25 -s 15 -t 115 -n 85

# outputs are in the output folder!
ls output/
