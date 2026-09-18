#!/usr/bin/env bash

# Xorg setup for freeview in postproc
export DISPLAY=:$(($$ + 99))
Xorg $DISPLAY -config /opt/xorg-dummy.conf -noreset -nolisten tcp -logfile "${out_dir}"/Xorg.log &
sleep 1

# Run the provided command
exec "$@"

# Previous xvfb version had issues with freesurfer rendering
#xvfb-run -n $(($$ + 99)) -s '-screen 0 1600x1200x24 -ac +extension GLX' "$@"
