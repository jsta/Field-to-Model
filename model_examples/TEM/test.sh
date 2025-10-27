#!/bin/bash -f

ORIGINAL_DIR=$(pwd)
TEST_RUN_DIR="tem_test_run"

# Make a place to save our output...
# Would put this in actual /tmp, but in some (many?) cases it leads
# to "no space left on device" errors...
mkdir -p $TEST_RUN_DIR

# Use the helper tool to setup a working directory for your experiment
# has copies of parameters, config files, and
pyddt-swd --force --input-data-path /opt/dvmdostem/demo-data/cru-ts40_ar5_rcp85_ncar-ccsm4_toolik_field_station_10x10/ $TEST_RUN_DIR/basic_test_run/

# Fiddle with the settings...single pixel, turn on some output variables...
cd $TEST_RUN_DIR/basic_test_run/
pyddt-runmask --reset --yx 5 5 run-mask.nc
pyddt-runmask --reset --yx 5 5 run-mask.nc 

pyddt-outspec config/output_spec.csv --on LAYERDZ m l
pyddt-outspec config/output_spec.csv --on TLAYER m l 

# check the outspec file to see what we have...
pyddt-outspec -s config/output_spec.csv 

# Run the model
dvmdostem -p 10 -e 15 -s 20 -t 25 -n 0 -l monitor

# outputs are in the output folder!
ls output/

# Clean up so we don't leave junk in user's directories
cd $ORIGINAL_DIR
rm -rf $TEST_RUN_DIR