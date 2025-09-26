#!/usr/bin/env bash

# Defaults
export t1_niigz=/INPUTS/t1.nii.gz
export SUBJECTS_DIR=/OUTPUTS
export out_dir=/OUTPUTS
export label_info="Unlabeled scan"
export nextbrain_gpu=0
export nextbrain_threads=1
export nextbrain_basis=dct


# Parse inputs
while [[ $# -gt 0 ]]
do
  key="$1"
  case $key in
    --t1_niigz)
        export t1_niigz="$2"; shift; shift;;
    --subjects_dir)
        export SUBJECTS_DIR="$2"; shift; shift;;
    --label_info)
        export label_info="$2"; shift; shift;;
    --out_dir)
        export out_dir="$2"; shift; shift;;
    --nextbrain_gpu)
        export nextbrain_gpu="$2"; shift; shift;;
    --nextbrain_threads)
        export nextbrain_threads="$2"; shift; shift;;
    --nextbrain_basis)
        export nextbrain_basis="$2"; shift; shift;;
    *)
		echo "Unknown argument $key"; shift;;
  esac
done

# Show what we got
echo SUBJECTS_DIR = "${SUBJECTS_DIR}"
echo t1_niigz     = "${t1_niigz}"
echo label_info   = "${label_info}"
echo out_dir      = "${out_dir}"

# Main freesurfer pipelines
recon-all -all -i /INPUTS/t1.nii.gz -s SUBJECT -hires
segment_subregions thalamus --cross SUBJECT
segment_subregions hippo-amygdala --cross SUBJECT
segment_subregions brainstem --cross SUBJECT
mri_sclimbic_seg -s SUBJECT --conform --write_qa_stats

# NextBrain (skip due to memory demands)
#mri_histo_atlas_segment_fireants /INPUTS/t1.nii.gz "${out_dir}"/NextBrain \
#    ${nextbrain_gpu} ${nextbrain_threads} ${nextbrain_basis}

# Post processing
postproc-entrypoint.sh \
    --subjects_dir "${SUBJECTS_DIR}" \
    --label_info "${label_info}" \
    --out_dir "${out_dir}"

