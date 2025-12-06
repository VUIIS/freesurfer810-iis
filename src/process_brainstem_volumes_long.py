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
bs = pandas.read_csv(os.path.join(mri_dir,'brainstemSsLabels.long.volumes.txt'),
    sep=' ',header=None)

# Sanitize varnames and convert to dataframe
bs[0] = [sanitize(x) for x in bs[0]]
bs2 = pandas.DataFrame([numpy.transpose(bs[1])])
bs2.columns = bs[0].to_list()

# Use known list of desired outputs. Fill any missing (and drop any
# that are unexpected)
rois = [
    'medulla',
    'pons',
    'scp',
    'midbrain',
    'whole_brainstem',
    ]
vals = pandas.DataFrame([args.timepoint], columns=['timepoint'])
for roi in rois:
    mask = [x==roi for x in rois]
    if sum(mask)>1:
        raise Exception(f'Found >1 value for {roi}')
    elif sum(mask)==1:
        vals[roi] = bs2[roi].values
    else:
        print(f'  WARNING - no volume found for ROI {roi}')
        vals[roi] = numpy.zeros(vals.timepoint.shape)

# Check for unexpected ROIs being present
for srcroi in bs[0]:
    if (not srcroi in rois):
        print(f'  WARNING - unexpected data found for ROI {srcroi}')

# Make data frame and write to file
vals.to_csv(args.out_csv, header=True, index=False)
