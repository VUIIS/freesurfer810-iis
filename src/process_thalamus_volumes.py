#!/usr/bin/env python3
#
# Need in path: /usr/local/freesurfer/python/bin

import argparse
import os
import pandas
import string

print(f'Running {__file__}')

parser = argparse.ArgumentParser()
parser.add_argument('--subject_dir', required=True)
parser.add_argument('--out_dir', required=True)
args = parser.parse_args()

mri_dir = f'{args.subject_dir}/mri'

# Function to sanitize varnames. Alphanumeric or underscore only
def sanitize(input_string):
    validchars = string.ascii_letters + string.digits + '_'
    output_string = ''
    for i in input_string:
        if i in validchars:
            output_string += i.lower()
        else:
            output_string += '_'
    return output_string

# Load freesurfer volumes data
thal = pandas.read_csv(os.path.join(mri_dir,'ThalamicNuclei.volumes.txt'),
    sep=' ',header=None)

# Sanitize varnames
thal[0] = [sanitize(x) for x in thal[0]]

# Use known list of desired outputs. Fill any missing (and drop any
# that are unexpected)
rois = [
    'left_lgn',
    'right_lgn',
    'right_mgn',
    'left_mgn',
    'left_pui',
    'left_pum',
    'left_l_sg',
    'left_vpl',
    'left_cm',
    'left_vla',
    'left_pua',
    'left_mdm',
    'left_pf',
    'left_vamc',
    'left_mdl',
    'left_cem',
    'left_va',
    'left_mv_re_',
    'left_vm',
    'left_cl',
    'left_pul',
    'left_pt',
    'left_av',
    'left_pc',
    'left_vlp',
    'left_lp',
    'right_pui',
    'right_pum',
    'right_l_sg',
    'right_vpl',
    'right_cm',
    'right_vla',
    'right_pua',
    'right_mdm',
    'right_pf',
    'right_vamc',
    'right_mdl',
    'right_va',
    'right_mv_re_',
    'right_cem',
    'right_vm',
    'right_pul',
    'right_cl',
    'right_vlp',
    'right_pc',
    'right_pt',
    'right_av',
    'right_lp',
    'left_ld',
    'right_ld',
    'left_whole_thalamus',
    'right_whole_thalamus',
    ]
vals = list()
for roi in rois:
    mask = [x==roi for x in rois]
    if sum(mask)>1:
        raise Exception(f'Found >1 value for {roi}')
    elif sum(mask)==1:
        vals.append(thal[1].loc[thal[0]==roi].array[0])
    else:
        print(f'  WARNING - no volume found for ROI {roi}')
        vals.append(0)

# Make data frame and write to file
thalout = pandas.DataFrame([rois, vals])
os.makedirs(args.out_dir, exist_ok=True)
thalout.to_csv(os.path.join(args.out_dir,'TNvol.csv'), 
    header=False, index=False)
