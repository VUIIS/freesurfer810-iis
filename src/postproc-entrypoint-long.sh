#!/bin/bash
#
# Entrypoint for post-freesurfer QA report and data reorg - LONGITUDINAL

# Defaults
export SUBJECTS_DIR=/OUTPUTS
export out_dir=/OUTPUTS
export label_info="Unlabeled scan"

# Parse inputs
while [[ $# -gt 0 ]]
do
  key="$1"
  case $key in
    --subjects_dir)
        export SUBJECTS_DIR="$2"; shift; shift;;
    --label_info)
        export label_info="$2"; shift; shift;;
    --out_dir)
        export out_dir="$2"; shift; shift;;
    *)
		echo "Unknown argument $key"; shift;;
  esac
done

# Show what we got
echo SUBJECTS_DIR = "${SUBJECTS_DIR}"
echo label_info   = "${label_info}"
echo out_dir      = "${out_dir}"

# Convert FS text stats output to dax-friendly CSV. 
# Also compute for MM relabeling
stats2tables2outputs-long.sh

# Images with MM relabeling (after finding longitudinal subject dirs only)
subj_dirs=$(ls -d ${SUBJECTS_DIR}/*.long.*)
subj_dirs=${subj_dirs//$'\n'/ }
for subj_dir in $subj_dirs; do
    export subj_dir
    create_MM_labelmaps_long.sh
done

# Make screenshots and PDFs
#xwrapper.sh make_pdf.sh

# Clean up SUBJECT dir
#rm -fr "${SUBJECTS_DIR}"/SUBJECT/trash
#rm -fr "${SUBJECTS_DIR}"/SUBJECT/tmp

