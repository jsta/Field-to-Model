#!/bin/bash -f

# Make a place to save our output...
# Would put this in actual /tmp, but in some (many?) cases it leads
# to "no space left on device" errors...
mkdir -p tmp/tem_test_run 

# Use the helper tool to setup a working directory for your experiment
# has copies of parameters, config files, and 
pyddt-swd --force --input-data-path /opt/dvmdostem/demo-data/cru-ts40_ar5_rcp85_ncar-ccsm4_toolik_field_station_10x10/ tmp/tem_test_run/EE1_warming

# Fiddle with the settings...single pixel, turn on some output variables...
cd tmp/tem_test_run/EE1_warming/
pyddt-runmask --reset --yx 5 5 run-mask.nc
pyddt-runmask --reset --yx 5 5 run-mask.nc 

pyddt-outspec config/output_spec.csv --on LAYERDZ m l
pyddt-outspec config/output_spec.csv --on TLAYER m l 

# check the outspec file to see what we have...
pyddt-outspec -s config/output_spec.csv 

# Run the model
dvmdostem -p 25 -e 25 -s 15 -t 25 -n 0

# outputs are in the output folder!
ls output/
