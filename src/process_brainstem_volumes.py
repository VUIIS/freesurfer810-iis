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
bs = pandas.read_csv(os.path.join(mri_dir,'brainstemSsLabels.volumes.txt'),
    sep=' ',header=None)

# Sanitize varnames
bs[0] = [sanitize(x) for x in bs[0]]

# Use known list of desired outputs. Fill any missing (and drop any
# that are unexpected)
rois = [
    'medulla',
    'pons',
    'scp',
    'midbrain',
    'whole_brainstem',
    ]
vals = list()
for roi in rois:
    mask = [x==roi for x in rois]
    if sum(mask)>1:
        raise Exception(f'Found >1 value for {roi}')
    elif sum(mask)==1:
        vals.append(bs[1].loc[bs[0]==roi].array[0])
    else:
        print(f'  WARNING - no volume found for ROI {roi}')
        vals.append(0)

# Make data frame and write to file
bsout = pandas.DataFrame([rois, vals])
os.makedirs(args.out_dir, exist_ok=True)
bsout.to_csv(os.path.join(args.out_dir,'BSvol.csv'), 
    header=False, index=False)
