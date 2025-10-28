#!/bin/bash -f

# test if ATS is on path
ats --version

# test if TEM is on path
dvmdostem --sha

# check home directory contents
ls ~

# check volume mounts:
ls /mnt
