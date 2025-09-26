#!/usr/bin/env python3
#
# Need in path: /usr/local/freesurfer/python/bin

import argparse
import os
import pandas
import string

print(f'Running {__file__}')

pandas.set_option('display.max_rows', None)

parser = argparse.ArgumentParser()
parser.add_argument('--csv_dir', required=True)
parser.add_argument('--out_dir', required=True)
args = parser.parse_args()

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
area_lh = pandas.read_csv(os.path.join(args.csv_dir,'lh-BA_exvivo-area.csv'))
area_rh = pandas.read_csv(os.path.join(args.csv_dir,'rh-BA_exvivo-area.csv'))
vol_lh = pandas.read_csv(os.path.join(args.csv_dir,'lh-BA_exvivo-volume.csv'))
vol_rh = pandas.read_csv(os.path.join(args.csv_dir,'rh-BA_exvivo-volume.csv'))
thk_lh = pandas.read_csv(os.path.join(args.csv_dir,'lh-BA_exvivo-thickness.csv'))
thk_rh = pandas.read_csv(os.path.join(args.csv_dir,'rh-BA_exvivo-thickness.csv'))

# Drop first columns (subject label)
area_lh = area_lh.drop(area_lh.columns[0], axis=1)
area_rh = area_rh.drop(area_rh.columns[0], axis=1)
vol_lh = vol_lh.drop(vol_lh.columns[0], axis=1)
vol_rh = vol_rh.drop(vol_rh.columns[0], axis=1)
thk_lh = thk_lh.drop(thk_lh.columns[0], axis=1)
thk_rh = thk_rh.drop(thk_rh.columns[0], axis=1)

# Concatenate
aparc = pandas.concat(
    [
        area_lh, 
        area_rh, 
        vol_lh, 
        vol_rh,
        thk_lh, 
        thk_rh,
    ],
    axis=1)

# Sanitize varnames
aparc.columns = [sanitize(x) for x in aparc.columns]

# Remove duplicate columns (e.g. etiv)
aparc = aparc.loc[:,~aparc.columns.duplicated()].copy()

# Show cols
#for x in aparc.columns:
#    print(f"    '{x}',")

# Use known list of desired outputs. Fill with 0 any missing (and drop any
# that are unexpected)
rois = [
    'lh_ba1_exvivo_area',
    'lh_ba2_exvivo_area',
    'lh_ba3a_exvivo_area',
    'lh_ba3b_exvivo_area',
    'lh_ba4a_exvivo_area',
    'lh_ba4p_exvivo_area',
    'lh_ba6_exvivo_area',
    'lh_ba44_exvivo_area',
    'lh_ba45_exvivo_area',
    'lh_v1_exvivo_area',
    'lh_v2_exvivo_area',
    'lh_mt_exvivo_area',
    'lh_perirhinal_exvivo_area',
    'lh_entorhinal_exvivo_area',
    'lh_whitesurfarea_area',
    'rh_ba1_exvivo_area',
    'rh_ba2_exvivo_area',
    'rh_ba3a_exvivo_area',
    'rh_ba3b_exvivo_area',
    'rh_ba4a_exvivo_area',
    'rh_ba4p_exvivo_area',
    'rh_ba6_exvivo_area',
    'rh_ba44_exvivo_area',
    'rh_ba45_exvivo_area',
    'rh_v1_exvivo_area',
    'rh_v2_exvivo_area',
    'rh_mt_exvivo_area',
    'rh_perirhinal_exvivo_area',
    'rh_entorhinal_exvivo_area',
    'rh_whitesurfarea_area',
    'lh_ba1_exvivo_volume',
    'lh_ba2_exvivo_volume',
    'lh_ba3a_exvivo_volume',
    'lh_ba3b_exvivo_volume',
    'lh_ba4a_exvivo_volume',
    'lh_ba4p_exvivo_volume',
    'lh_ba6_exvivo_volume',
    'lh_ba44_exvivo_volume',
    'lh_ba45_exvivo_volume',
    'lh_v1_exvivo_volume',
    'lh_v2_exvivo_volume',
    'lh_mt_exvivo_volume',
    'lh_perirhinal_exvivo_volume',
    'lh_entorhinal_exvivo_volume',
    'rh_ba1_exvivo_volume',
    'rh_ba2_exvivo_volume',
    'rh_ba3a_exvivo_volume',
    'rh_ba3b_exvivo_volume',
    'rh_ba4a_exvivo_volume',
    'rh_ba4p_exvivo_volume',
    'rh_ba6_exvivo_volume',
    'rh_ba44_exvivo_volume',
    'rh_ba45_exvivo_volume',
    'rh_v1_exvivo_volume',
    'rh_v2_exvivo_volume',
    'rh_mt_exvivo_volume',
    'rh_perirhinal_exvivo_volume',
    'rh_entorhinal_exvivo_volume',
    'lh_ba1_exvivo_thickness',
    'lh_ba2_exvivo_thickness',
    'lh_ba3a_exvivo_thickness',
    'lh_ba3b_exvivo_thickness',
    'lh_ba4a_exvivo_thickness',
    'lh_ba4p_exvivo_thickness',
    'lh_ba6_exvivo_thickness',
    'lh_ba44_exvivo_thickness',
    'lh_ba45_exvivo_thickness',
    'lh_v1_exvivo_thickness',
    'lh_v2_exvivo_thickness',
    'lh_mt_exvivo_thickness',
    'lh_perirhinal_exvivo_thickness',
    'lh_entorhinal_exvivo_thickness',
    'rh_ba1_exvivo_thickness',
    'rh_ba2_exvivo_thickness',
    'rh_ba3a_exvivo_thickness',
    'rh_ba3b_exvivo_thickness',
    'rh_ba4a_exvivo_thickness',
    'rh_ba4p_exvivo_thickness',
    'rh_ba6_exvivo_thickness',
    'rh_ba44_exvivo_thickness',
    'rh_ba45_exvivo_thickness',
    'rh_v1_exvivo_thickness',
    'rh_v2_exvivo_thickness',
    'rh_mt_exvivo_thickness',
    'rh_perirhinal_exvivo_thickness',
    'rh_entorhinal_exvivo_thickness',
    'brainsegvolnotvent',
    'etiv',
    ]
vals = list()
for roi in rois:
    mask = [x==roi for x in aparc.columns]
    if sum(mask)==0:
        print(f'  WARNING - no volume found for ROI {roi}')
        vals.append(0)
    elif sum(mask)>1:
        raise Exception(f'Found >1 value for {roi}')
    else:
        vals.append(aparc[roi].array[0])


# Make data frame and write to file
aparcout = pandas.DataFrame([rois, vals])
os.makedirs(args.out_dir, exist_ok=True)
aparcout.to_csv(os.path.join(args.out_dir,'BA_exvivo.csv'), 
    header=False, index=False)
