#!/usr/bin/env bash
#
# MM reorg of hippocampus regions
#
# We have to get these from the hires resampled images:
#     lh.hippoAmygLabels.mgz
#     rh.hippoAmygLabels.mgz
# Both hemispheres are labeled with the same codes.
#
# Label info is in $FREESURFER_HOME/FreeSurferColorLUT.txt
#
# Resample with mri_vol2vol

echo MM label maps

mri_dir="${subj_dir}"/mri
mm_dir="${mri_dir}"

##############################################################################
# MMAP anterior/posterior
#
#   Anterior (1)
#        233  presubiculum-head
#        235  subiculum-head
#        237  CA1-head
#        239  CA3-head
#        241  CA4-head
#        243  GC-ML-DG-head
#        245  molecular_layer_HP-head
#
#   Posterior (2)
#        226  Hippocampal_tail   
#        234  presubiculum-body
#        236  subiculum-body
#        238  CA1-body
#        240  CA3-body
#        242  CA4-body
#        244  GC-ML-DG-body
#        246  molecular_layer_HP-body
#
#   Discard (0)
#        203  parasubiculum
#        211  HATA
#        212  fimbria
#        215  hippocampal-fissure
#       7...  amygdala
for hemi in lh rh ; do
	
mri_binarize \
--i "${mri_dir}/${hemi}.hippoAmygLabels.long.mgz" \
\
--replace 233 1 \
--replace 235 1 \
--replace 237 1 \
--replace 239 1 \
--replace 241 1 \
--replace 243 1 \
--replace 245 1 \
\
--replace 226 2 \
--replace 234 2 \
--replace 236 2 \
--replace 238 2 \
--replace 240 2 \
--replace 242 2 \
--replace 244 2 \
--replace 246 2 \
\
--replace 203 0 \
--replace 211 0 \
--replace 212 0 \
--replace 215 0 \
\
--replace 7001 0 \
--replace 7003 0 \
--replace 7005 0 \
--replace 7006 0 \
--replace 7007 0 \
--replace 7008 0 \
--replace 7009 0 \
--replace 7010 0 \
--replace 7015 0 \
\
--o "${mm_dir}"/${hemi}.hippoLabels.long.MMAP.mgz

mri_vol2vol --nearest --regheader \
    --mov "${mm_dir}"/${hemi}.hippoLabels.long.MMAP.mgz \
    --targ "${mri_dir}"/${hemi}.hippoAmygLabels.long.FSvoxelSpace.mgz \
    --o "${mm_dir}"/${hemi}.hippoLabels.long.MMAP.FSVoxelSpace.mgz

done


# Make corresponding label file
cat <<EOF > "${mm_dir}/hippoLabels.long.MMAP.csv"
Label,Region
1,Anterior-Hippocampus
2,Posterior-Hippocampus
EOF


##############################################################################
# MMHBT head/body/tail
#
#  Head-CA (1)
#        235  subiculum-head
#        237  CA1-head
#        239  CA3-head
#        245  molecular_layer_HP-head
#
#  Head-DG (2)
#        241  CA4-head
#        243  GC-ML-DG-head
#
#  Head-subiculum (3)
#        233  presubiculum-head
#
#  Body-CA (4)
#        236  subiculum-body
#        238  CA1-body
#        240  CA3-body
#        246  molecular_layer_HP-body
#
#  Body-DG (5)
#        242  CA4-body
#        244  GC-ML-DG-body
#
#  Body-subiculum (6)
#        234  presubiculum-body
#
#  Tail (7)
#        226  Hippocampal_tail   
#
#  Discard (0)
#        203  parasubiculum
#        211  HATA
#        212  fimbria
#        215  hippocampal-fissure
#       7...  amygdala
for hemi in lh rh ; do

mri_binarize \
--i "${mri_dir}/${hemi}.hippoAmygLabels.long.mgz" \
\
--replace 235 1 \
--replace 237 1 \
--replace 239 1 \
--replace 245 1 \
\
--replace 241 2 \
--replace 243 2 \
\
--replace 233 3 \
\
--replace 236 4 \
--replace 238 4 \
--replace 240 4 \
--replace 246 4 \
\
--replace 242 5 \
--replace 244 5 \
\
--replace 234 6 \
\
--replace 226 7 \
\
--replace 203 0 \
--replace 211 0 \
--replace 212 0 \
--replace 215 0 \
\
--replace 7001 0 \
--replace 7003 0 \
--replace 7005 0 \
--replace 7006 0 \
--replace 7007 0 \
--replace 7008 0 \
--replace 7009 0 \
--replace 7010 0 \
--replace 7015 0 \
\
--o "${mm_dir}"/${hemi}.hippoLabels.long.MMHBT.mgz

mri_vol2vol --nearest --regheader \
    --mov "${mm_dir}"/${hemi}.hippoLabels.long.MMHBT.mgz \
    --targ "${mri_dir}"/${hemi}.hippoAmygLabels.long.FSvoxelSpace.mgz \
    --o "${mm_dir}"/${hemi}.hippoLabels.long.MMHBT.FSVoxelSpace.mgz

done

# Make corresponding label file
cat <<EOF > "${mm_dir}/hippoLabels.long.MMHBT.csv"
Label,Region
1,Head-CA
2,Head-DG
3,Head-subiculum
4,Body-CA
5,Body-DG
6,Body-subiculum
7,Tail
EOF

