#!/usr/bin/env bash
#
# Produce PDF reports
#
# Needs SUBJECTS_DIR, out_dir

# Find longitudinal subject dirs
subj_dirs=$(ls -d ${SUBJECTS_DIR}/*.long.*)
subj_dirs=${subj_dirs//$'\n'/ }


# Source and working dirs
export src_dir=$(realpath $(dirname $(which ${0})))
export tmp_dir="${out_dir}"/imgtmp && mkdir -p "${tmp_dir}"
export XDG_RUNTIME_DIR="${tmp_dir}"/runtime-root


# Make screenshots and PDFs
export the_date=$(date)
export label_info_orig="${label_info}"
let c=0
for subj_dir in ${subj_dirs}; do

    (( c ++ ))
    cstr=$(printf "%03d" ${c})

    export subj_dir
    export mri_dir="${subj_dir}"/mri
    export surf_dir="${subj_dir}"/surf
    export label_info="${label_info_orig} $(basename ${subj_dir})"

    page1.sh
    page2.sh
    page3.sh
    page4.sh
    convert \
        "${tmp_dir}"/page1.png \
        "${tmp_dir}"/page2.png \
        "${tmp_dir}"/page3.png \
        "${tmp_dir}"/page4.png \
        "${tmp_dir}"/Freesurfer-QA-${cstr}.pdf

    make_slice_screenshots.sh
    mv "${out_dir}"/PDF_DETAIL/Freesurfer-QA-detailed.pdf "${tmp_dir}"/Freesurfer-QA-detailed-${cstr}.pdf 

done
export label_info="${label_info_orig}"


mkdir -p "${out_dir}"/PDF
convert \
    "${tmp_dir}"/Freesurfer-QA-???.pdf \
    "${out_dir}"/PDF/Freesurfer-QA.pdf

convert \
    "${tmp_dir}"/Freesurfer-QA-detailed-???.pdf \
    "${out_dir}"/PDF_DETAIL/Freesurfer-QA-detailed.pdf
