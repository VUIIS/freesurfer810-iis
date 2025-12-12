#!/usr/bin/env python3
#
# Need in path: /usr/local/freesurfer/python/bin

import argparse
import numpy
import os
import pandas
import string

print(f'Running {__file__}')

parser = argparse.ArgumentParser()
parser.add_argument('--sclimbic_csvdir', required=True)
parser.add_argument('--out_dir', required=True)
args = parser.parse_args()

# Function to sanitize varnames. Alphanumeric or underscore only
# Fix ventricle names so they don't start with digit
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
zqa = pandas.read_csv(os.path.join(args.sclimbic_csvdir,'sclimbic_zqa_scores_all.csv'))
confs = pandas.read_csv(os.path.join(args.sclimbic_csvdir,'sclimbic_confidences_all.csv'))

# Rename first column (subject label is actually timepoint label)
zqa.rename(columns={zqa.columns[0]: 'timepoint'}, inplace=True, errors='raise')
confs.rename(columns={confs.columns[0]: 'timepoint'}, inplace=True, errors='raise')

# Sanitize varnames
zqa.columns = [sanitize(x) for x in zqa.columns]
confs.columns = [sanitize(x) for x in confs.columns]

# Use known list of desired outputs. Fill with 0 any missing (and drop any
# that are unexpected)
rois = [
    'left_nucleus_accumbens',
    'right_nucleus_accumbens',
    'left_hypothal_nomb',
    'right_hypothal_nomb',
    'left_fornix',
    'right_fornix',
    'left_mammillarybody',
    'right_mammillarybody',
    'left_basal_forebrain',
    'right_basal_forebrain',
    'left_septalnuc',
    'right_septalnuc',
    ]

# zqa
vals = pandas.DataFrame(zqa.timepoint)
for roi in rois:
    mask = [x==roi for x in zqa.columns]
    if sum(mask)==0:
        print(f'  WARNING - no volume found for ROI {roi}')
        vals[roi] = numpy.zeros(vals.timepoint.shape)
    elif sum(mask)>1:
        raise Exception(f'Found >1 value for {roi}')
    else:
        vals = pandas.concat([vals, zqa[roi]], axis=1)

# Check for unexpected ROIs being present
for srcroi in zqa.columns:
    if (not srcroi in rois) and (not srcroi in ['timepoint']):
        print(f'  WARNING - unexpected data found for ROI {srcroi}')

zqaout = vals
os.makedirs(args.out_dir, exist_ok=True)
zqaout.to_csv(os.path.join(args.out_dir, 'sclimbic_zqa_scores.csv'), 
    header=True, index=False)


# confidences
vals = pandas.DataFrame(confs.timepoint)
for roi in rois:
    mask = [x==roi for x in confs.columns]
    if sum(mask)==0:
        print(f'  WARNING - no volume found for ROI {roi}')
        vals[roi] = numpy.zeros(vals.timepoint.shape)
    elif sum(mask)>1:
        raise Exception(f'Found >1 value for {roi}')
    else:
        vals = pandas.concat([vals, confs[roi]], axis=1)

confsout = vals
os.makedirs(args.out_dir, exist_ok=True)
confsout.to_csv(os.path.join(args.out_dir,'sclimbic_confidences.csv'), 
    header=True, index=False)
