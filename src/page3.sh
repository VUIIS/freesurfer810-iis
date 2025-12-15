#!/usr/bin/env bash
#
# Page 3, thalamus
#
# Several coronal slices in series to get overview.
# Add a coronal slice at center of mass of LGN for thalamus segmentation. 
#
# Also take a look at LGN-centered axial cut.
#
# Include a plain T1 next to e.g. the axial thalamus for comparison.

img_nu="${mri_dir}"/nu.mgz
img_thal="${mri_dir}"/ThalamicNuclei.mgz
if [[ ! -f "${img_thal}" ]]; then
    img_thal="${mri_dir}"/ThalamicNuclei.long.mgz
fi
img_aseg="${mri_dir}"/aseg.mgz

# Get LGN location: left is 8109, right is 8209
# /usr/local/freesurfer/FreeSurferColorLUT.txt
RL=$(get_com.py --roi_niigz "${img_thal}" --axis x --imgval 8109 )
AL=$(get_com.py --roi_niigz "${img_thal}" --axis y --imgval 8109 )
SL=$(get_com.py --roi_niigz "${img_thal}" --axis z --imgval 8109 )

RR=$(get_com.py --roi_niigz "${img_thal}" --axis x --imgval 8209 )
AR=$(get_com.py --roi_niigz "${img_thal}" --axis y --imgval 8209 )
SR=$(get_com.py --roi_niigz "${img_thal}" --axis z --imgval 8209 )

LGNR=$(echo "(${RL} + ${RR}) / 2" | bc)
LGNA=$(echo "(${AL} + ${AR}) / 2" | bc)
LGNS=$(echo "(${SL} + ${SR}) / 2" | bc)

# Get RAS mm coords of region centroid, averaging over two regions
# https://surfer.nmr.mgh.harvard.edu/fswiki/CoordinateSystems
#    10   L thalamus
#    49   R thalamus
RL=$(get_com.py --roi_niigz "${img_aseg}" --axis x --imgval 10 )
AL=$(get_com.py --roi_niigz "${img_aseg}" --axis y --imgval 10 )
SL=$(get_com.py --roi_niigz "${img_aseg}" --axis z --imgval 10 )

RR=$(get_com.py --roi_niigz "${img_aseg}" --axis x --imgval 49 )
AR=$(get_com.py --roi_niigz "${img_aseg}" --axis y --imgval 49 )
SR=$(get_com.py --roi_niigz "${img_aseg}" --axis z --imgval 49 )

THALR=$(echo "(${RL} + ${RR}) / 2" | bc)
THALA=$(echo "(${AL} + ${AR}) / 2" | bc)
THALS=$(echo "(${SL} + ${SR}) / 2" | bc)


# Freeview command line chunks
V_STR="-viewsize 400 350 --layout 1 --zoom 4"
T1_STR="-v ${img_nu}"
SEG_STR="-v ${img_thal}:visible=1:colormap=lut"

# Coronal slices, A to P
freeview --viewport coronal ${V_STR} ${T1_STR} \
	-ras "${THALR}" "$((THALA+14))" "${THALS}" \
    -ss "${tmp_dir}"/cor_a14_plain.png
freeview --viewport coronal ${V_STR} ${T1_STR} ${SEG_STR} \
	-ras "${THALR}" "$((THALA+14))" "${THALS}" \
    -ss "${tmp_dir}"/cor_a14.png

freeview --viewport coronal ${V_STR} ${T1_STR} \
	-ras "${THALR}" "$((THALA+7))" "${THALS}" \
    -ss "${tmp_dir}"/cor_a7_plain.png
freeview --viewport coronal ${V_STR} ${T1_STR} ${SEG_STR} \
	-ras "${THALR}" "$((THALA+7))" "${THALS}" \
    -ss "${tmp_dir}"/cor_a7.png

freeview --viewport coronal ${V_STR} ${T1_STR} \
	-ras "${THALR}" "${THALA}" "${THALS}" \
    -ss "${tmp_dir}"/cor_0_plain.png
freeview --viewport coronal ${V_STR} ${T1_STR} ${SEG_STR} \
	-ras "${THALR}" "${THALA}" "${THALS}" \
    -ss "${tmp_dir}"/cor_0.png

freeview --viewport coronal ${V_STR} ${T1_STR} \
	-ras "${THALR}" "$((THALA-7))" "${THALS}" \
    -ss "${tmp_dir}"/cor_p7_plain.png
freeview --viewport coronal ${V_STR} ${T1_STR} ${SEG_STR} \
	-ras "${THALR}" "$((THALA-7))" "${THALS}" \
    -ss "${tmp_dir}"/cor_p7.png

freeview --viewport coronal ${V_STR} ${T1_STR} \
	-ras "${THALR}" "${LGNA}" "${THALS}" \
    -ss "${tmp_dir}"/cor_lgn_plain.png
freeview --viewport coronal ${V_STR} ${T1_STR} ${SEG_STR} \
	-ras "${THALR}" "${LGNA}" "${THALS}" \
    -ss "${tmp_dir}"/cor_lgn.png

# Axial slices
freeview --viewport axial ${V_STR} ${T1_STR} \
	-ras "${THALR}" "${THALA}" "${LGNS}" \
    -ss "${tmp_dir}"/axi_lgn_plain.png
freeview --viewport axial ${V_STR} ${T1_STR} ${SEG_STR} \
	-ras "${THALR}" "${THALA}" "${LGNS}" \
    -ss "${tmp_dir}"/axi_lgn.png

freeview --viewport axial ${V_STR} ${T1_STR} \
	-ras "${THALR}" "${THALA}" "${THALS}" \
    -ss "${tmp_dir}"/axi_0_plain.png
freeview --viewport axial ${V_STR} ${T1_STR} ${SEG_STR} \
	-ras "${THALR}" "${THALA}" "${THALS}" \
    -ss "${tmp_dir}"/axi_0.png

freeview --viewport axial ${V_STR} ${T1_STR} \
	-ras "${THALR}" "${THALA}" "$((THALS+7))" \
    -ss "${tmp_dir}"/axi_s7_plain.png
freeview --viewport axial ${V_STR} ${T1_STR} ${SEG_STR} \
	-ras "${THALR}" "${THALA}" "$((THALS+7))" \
    -ss "${tmp_dir}"/axi_s7.png

# Sagittal
freeview --viewport sagittal ${V_STR} ${T1_STR} \
	-ras "${RL}" "${AL}" "${SL}" \
	-ss "${tmp_dir}"/sag_L_plain.png
freeview --viewport sagittal ${V_STR} ${T1_STR} ${SEG_STR} \
	-ras "${RL}" "${AL}" "${SL}" \
	-ss "${tmp_dir}"/sag_L.png

freeview --viewport sagittal ${V_STR} ${T1_STR} \
	-ras "${RR}" "${AR}" "${SR}" \
	-ss "${tmp_dir}"/sag_R_plain.png
freeview --viewport sagittal ${V_STR} ${T1_STR} ${SEG_STR} \
	-ras "${RR}" "${AR}" "${SR}" \
	-ss "${tmp_dir}"/sag_R.png


# Layout. 20 panels, 4 wide (2 pairs) by 5 high.
cd "${tmp_dir}"
montage -mode concatenate \
    cor_lgn_plain.png cor_lgn.png cor_p7_plain.png cor_p7.png \
    cor_0_plain.png cor_0.png cor_a7_plain.png cor_a7.png \
    cor_a14_plain.png cor_a14.png sag_L_plain.png sag_L.png \
    sag_R_plain.png sag_R.png axi_s7_plain.png axi_s7.png \
    axi_0_plain.png axi_0.png axi_lgn_plain.png axi_lgn.png \
    -tile 4x5 -quality 100 -background white -gravity center \
    -trim -border 5 -bordercolor white -resize 600x twenty.png

# Add info
# 8.5 x 11 at 144dpi is 1224 x 1584
# inside 15px border is 1194 x 1554
convert \
    -size 1224x1584 xc:white \
    -gravity center \( twenty.png -resize 1194x1554 \) -composite \
    -gravity NorthEast -pointsize 24 -annotate +20+50 "ThalamicNuclei" \
    -gravity SouthEast -pointsize 24 -annotate +20+20 "${the_date}" \
    -gravity SouthWest -pointsize 24 -annotate +20+20 "$(cat $FREESURFER_HOME/build-stamp.txt)" \
    -gravity NorthWest -pointsize 24 -annotate +20+50 "${label_info}" \
    page3.png

