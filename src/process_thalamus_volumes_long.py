#!/usr/bin/env python3
#
# Need in path: /usr/local/freesurfer/python/bin

import argparse
import numpy
import os
import pandas
import string

parser = argparse.ArgumentParser()
parser.add_argument('--subject_dir', required=True)
parser.add_argument('--timepoint', required=True)
parser.add_argument('--out_csv', required=True)
args = parser.parse_args()

mri_dir = f'{args.subject_dir}/mri'

print(f'Running {__file__} for {mri_dir}')

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
thal = pandas.read_csv(os.path.join(mri_dir,'ThalamicNuclei.long.volumes.txt'),
    sep=' ',header=None)

# Sanitize varnames and convert to dataframe
thal[0] = [sanitize(x) for x in thal[0]]
thal2 = pandas.DataFrame([numpy.transpose(thal[1])])
thal2.columns = thal[0].to_list()

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
vals = pandas.DataFrame([args.timepoint], columns=['timepoint'])
for roi in rois:
    mask = [x==roi for x in rois]
    if sum(mask)>1:
        raise Exception(f'Found >1 value for {roi}')
    elif sum(mask)==1:
        vals[roi] = thal2[roi].values
    else:
        print(f'  WARNING - no volume found for ROI {roi}')
        vals[roi] = numpy.zeros(vals.timepoint.shape)

# Check for unexpected ROIs being present
for srcroi in thal[0]:
    if (not srcroi in rois):
        print(f'  WARNING - unexpected data found for ROI {srcroi}')

# Make data frame and write to file
vals.to_csv(args.out_csv, header=True, index=False)
