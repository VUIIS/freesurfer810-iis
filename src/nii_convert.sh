#!/usr/bin/env bash

echo NIFTI conversion

mri_dir="${SUBJECTS_DIR}"/SUBJECT/mri
nii_dir="${out_dir}"/NIFTIS

mkdir -p "${nii_dir}"

for f in \
        nu \
        aparc+aseg \
        wmparc \
        brainmask \
        ThalamicNuclei \
        brainstemSsLabels \
        lh.hippoAmygLabels \
        rh.hippoAmygLabels \
        ; do
    mri_convert "${mri_dir}/${f}.mgz" "${nii_dir}"/$(basename "${f}" .mgz).nii.gz
done
