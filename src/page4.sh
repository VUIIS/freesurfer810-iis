#!/usr/bin/env bash
#
# Page 4, hippocampus/brainstem

img_nu="${mri_dir}"/nu.mgz
img_aseg="${mri_dir}"/aseg.mgz
img_lhip="${mri_dir}"/lh.hippoAmygLabels.mgz
img_rhip="${mri_dir}"/rh.hippoAmygLabels.mgz
img_bs="${mri_dir}"/brainstemSsLabels.mgz

##########################################################################
# Hipp snaps

# Get RAS mm coords of region centroid
# https://surfer.nmr.mgh.harvard.edu/fswiki/CoordinateSystems
#    17   L hippocampus
#    53   R hippocampus
RL=$(get_com.py --roi_niigz "${img_aseg}" --axis x --imgval 17 )
AL=$(get_com.py --roi_niigz "${img_aseg}" --axis y --imgval 17 )
SL=$(get_com.py --roi_niigz "${img_aseg}" --axis z --imgval 17 )

RR=$(get_com.py --roi_niigz "${img_aseg}" --axis x --imgval 53 )
AR=$(get_com.py --roi_niigz "${img_aseg}" --axis y --imgval 53 )
SR=$(get_com.py --roi_niigz "${img_aseg}" --axis z --imgval 53 )


# View selected slices on T1, with surfaces
freeview \
    -v "${img_nu}" \
    -v "${img_lhip}":visible=1:colormap=lut \
    -viewsize 400 400 --layout 1 --zoom 2.5 --viewport sag \
    -ras ${RL} ${AL} ${SL} \
    -ss "${tmp_dir}"/Lhipp_sag.png

freeview \
    -v "${img_nu}" \
    -v "${img_rhip}":visible=1:colormap=lut \
    -viewsize 400 400 --layout 1 --zoom 2.5 --viewport sag \
    -ras ${RR} ${AR} ${SR} \
    -ss "${tmp_dir}"/Rhipp_sag.png


##########################################################################
# Brainstem snaps

# Get RAS mm coords of region centroid
# https://surfer.nmr.mgh.harvard.edu/fswiki/CoordinateSystems
#    16   brainstem
R=$(get_com.py --roi_niigz "${img_aseg}" --axis x --imgval 16 )
A=$(get_com.py --roi_niigz "${img_aseg}" --axis y --imgval 16 )
S=$(get_com.py --roi_niigz "${img_aseg}" --axis z --imgval 16 )

# View selected slices on T1, with surfaces
freeview \
    -v "${img_nu}" \
    -v "${img_bs}":visible=1:colormap=lut \
    -viewsize 400 400 --layout 1 --zoom 2.5 --viewport sagittal \
    -ras ${R} ${A} ${S} \
    -ss "${tmp_dir}"/brainstem_sag.png

freeview \
    -v "${img_nu}" \
    -v "${img_bs}":visible=1:colormap=lut \
    -viewsize 400 400 --layout 1 --zoom 2.5 --viewport coronal \
    -ras ${R} ${A} ${S} \
    -ss "${tmp_dir}"/brainstem_cor.png



##########################################################################
# Join up
cd "${tmp_dir}"

montage -mode concatenate \
    Lhipp_sag.png Rhipp_sag.png brainstem_sag.png brainstem_cor.png \
    -tile 2x -quality 100 -background black -gravity center \
    -trim -border 10 -bordercolor black -resize 300x page4fig.png

convert page4fig.png \
    -background white -resize 1194x1479 -extent 1194x1479 -bordercolor white \
    -border 15 -gravity SouthEast -background white -splice 0x15 -pointsize 24 \
    -annotate +15+10 "${the_date}" \
    -gravity SouthWest -annotate +15+10 "$(cat ${FREESURFER_HOME}/build-stamp.txt)" \
    -gravity NorthWest -background white -splice 0x60 -pointsize 24 -annotate +15+0 \
        'FreeSurfer brainstemSsLabels' \
    -gravity NorthWest -background white -splice 0x60 -pointsize 24 -annotate +15+10 \
        'FreeSurfer hippoAmygLabels' \
    -gravity NorthEast -pointsize 24 -annotate +15+10 "${label_info}" \
    page4.png

convert \
    -size 1224x1584 xc:white \
    -gravity center \( page4fig.png -resize 1194x1554 \) -composite \
    -gravity NorthEast -pointsize 24 -annotate +20+50 "hippoAmygLabels (top)" \
    -gravity NorthEast -pointsize 24 -annotate +20+90 "brainstemSsLabels (bottom)" \
    -gravity SouthEast -pointsize 24 -annotate +20+20 "${the_date}" \
    -gravity SouthWest -pointsize 24 -annotate +20+20 "$(cat ${FREESURFER_HOME}/build-stamp.txt)" \
    -gravity NorthWest -pointsize 24 -annotate +20+50 "${label_info}" \
    page4.png
