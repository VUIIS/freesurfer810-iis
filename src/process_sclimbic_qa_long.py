#!/usr/bin/env python3
#
# Need in path: /usr/local/freesurfer/python/bin

# FIXME do we get full QC stats with this command?
#      mri_sclimbic_seg -s v000mo.long.template2 v024mo.long.template2 --conform --write_qa_stats
# If so, fix the below to work with its output

import argparse
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

# Drop first column (subject label)
zqa = zqa.drop(zqa.columns[0], axis=1)
confs = confs.drop(confs.columns[0], axis=1)

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
vals = list()
for roi in rois:
    mask = [x==roi for x in zqa.columns]
    if sum(mask)==0:
        print(f'  WARNING - no volume found for ROI {roi}')
        vals.append(0)
    elif sum(mask)>1:
        raise Exception(f'Found >1 value for {roi}')
    else:
        vals.append(zqa[roi].array[0])

zqaout = pandas.DataFrame([rois, vals])
os.makedirs(args.out_dir, exist_ok=True)
zqaout.to_csv(os.path.join(args.out_dir,'sclimbic_zqa_scores.csv'), 
    header=False, index=False)


# confidences
vals = list()
for roi in rois:
    mask = [x==roi for x in confs.columns]
    if sum(mask)==0:
        print(f'  WARNING - no volume found for ROI {roi}')
        vals.append(0)
    elif sum(mask)>1:
        raise Exception(f'Found >1 value for {roi}')
    else:
        vals.append(confs[roi].array[0])

confsout = pandas.DataFrame([rois, vals])
os.makedirs(args.out_dir, exist_ok=True)
confsout.to_csv(os.path.join(args.out_dir,'sclimbic_confidences.csv'), 
    header=False, index=False)
