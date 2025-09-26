#!/usr/bin/env python3
#
# Need in path: /usr/local/freesurfer/python/bin

import argparse
import os
import pandas
import string

print(f'Running {__file__}')

parser = argparse.ArgumentParser()
parser.add_argument('--sclimbic_csv', required=True)
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
sclimbic = pandas.read_csv(args.sclimbic_csv)

# Drop first column (subject label)
sclimbic = sclimbic.drop(sclimbic.columns[0], axis=1)

#print(aseg)

# Sanitize varnames
sclimbic.columns = [sanitize(x) for x in sclimbic.columns]

#for x in sclimbic.columns:
#    print(f"    '{x}',")
#sys.exit(0)

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
vals = list()
for roi in rois:
    mask = [x==roi for x in sclimbic.columns]
    if sum(mask)==0:
        print(f'  WARNING - no volume found for ROI {roi}')
        vals.append(0)
    elif sum(mask)>1:
        raise Exception(f'Found >1 value for {roi}')
    else:
        vals.append(sclimbic[roi].array[0])

# Make data frame and write to file
sclimbicout = pandas.DataFrame([rois, vals])
os.makedirs(args.out_dir, exist_ok=True)
sclimbicout.to_csv(os.path.join(args.out_dir,'sclimbic.csv'), 
    header=False, index=False)
