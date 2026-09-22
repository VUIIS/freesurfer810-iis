#!/usr/bin/env bash

# Older xvfb version had issues with freesurfer rendering
xvfb-run -n $(($$ + 99)) -s '-screen 0 1600x1200x24 -ac +extension GLX' "$@"


# Xorg setup for freeview in postproc. Xorg not really compatible with containers though
#export DISPLAY=:$(($$ + 99))
#Xorg $DISPLAY -config /opt/xorg-dummy.conf -noreset -nolisten tcp -logfile "${out_dir}"/Xorg.log &
#sleep 1

# Run the provided command
#exec "$@"

