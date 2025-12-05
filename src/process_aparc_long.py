#!/usr/bin/env python3
#
# Need in path: /usr/local/freesurfer/python/bin

import argparse
import numpy
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
area_lh = pandas.read_csv(os.path.join(args.csv_dir,'lh-aparc-area.csv'))
area_rh = pandas.read_csv(os.path.join(args.csv_dir,'rh-aparc-area.csv'))
vol_lh = pandas.read_csv(os.path.join(args.csv_dir,'lh-aparc-volume.csv'))
vol_rh = pandas.read_csv(os.path.join(args.csv_dir,'rh-aparc-volume.csv'))
thk_lh = pandas.read_csv(os.path.join(args.csv_dir,'lh-aparc-thickness.csv'))
thk_rh = pandas.read_csv(os.path.join(args.csv_dir,'rh-aparc-thickness.csv'))

# Get timepoint labels for each and confirm they match
timepoint = pandas.DataFrame(area_lh.iloc[:,0])
timepoint.rename(columns={timepoint.columns[0]: 'timepoint'}, inplace=True, errors='raise')

for x in [area_rh, vol_lh, vol_rh, thk_lh, thk_rh]:
    tp = pandas.DataFrame(x.iloc[:,0])
    tp.rename(columns={tp.columns[0]: 'timepoint'}, inplace=True, errors='raise')
    if not all(tp==timepoint):
        raise Exception('Timepoint labels not matching')

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
        timepoint,
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
    'lh_bankssts_area',
    'lh_caudalanteriorcingulate_area',
    'lh_caudalmiddlefrontal_area',
    'lh_cuneus_area',
    'lh_entorhinal_area',
    'lh_fusiform_area',
    'lh_inferiorparietal_area',
    'lh_inferiortemporal_area',
    'lh_isthmuscingulate_area',
    'lh_lateraloccipital_area',
    'lh_lateralorbitofrontal_area',
    'lh_lingual_area',
    'lh_medialorbitofrontal_area',
    'lh_middletemporal_area',
    'lh_parahippocampal_area',
    'lh_paracentral_area',
    'lh_parsopercularis_area',
    'lh_parsorbitalis_area',
    'lh_parstriangularis_area',
    'lh_pericalcarine_area',
    'lh_postcentral_area',
    'lh_posteriorcingulate_area',
    'lh_precentral_area',
    'lh_precuneus_area',
    'lh_rostralanteriorcingulate_area',
    'lh_rostralmiddlefrontal_area',
    'lh_superiorfrontal_area',
    'lh_superiorparietal_area',
    'lh_superiortemporal_area',
    'lh_supramarginal_area',
    'lh_frontalpole_area',
    'lh_temporalpole_area',
    'lh_transversetemporal_area',
    'lh_insula_area',
    'lh_whitesurfarea_area',
    'rh_bankssts_area',
    'rh_caudalanteriorcingulate_area',
    'rh_caudalmiddlefrontal_area',
    'rh_cuneus_area',
    'rh_entorhinal_area',
    'rh_fusiform_area',
    'rh_inferiorparietal_area',
    'rh_inferiortemporal_area',
    'rh_isthmuscingulate_area',
    'rh_lateraloccipital_area',
    'rh_lateralorbitofrontal_area',
    'rh_lingual_area',
    'rh_medialorbitofrontal_area',
    'rh_middletemporal_area',
    'rh_parahippocampal_area',
    'rh_paracentral_area',
    'rh_parsopercularis_area',
    'rh_parsorbitalis_area',
    'rh_parstriangularis_area',
    'rh_pericalcarine_area',
    'rh_postcentral_area',
    'rh_posteriorcingulate_area',
    'rh_precentral_area',
    'rh_precuneus_area',
    'rh_rostralanteriorcingulate_area',
    'rh_rostralmiddlefrontal_area',
    'rh_superiorfrontal_area',
    'rh_superiorparietal_area',
    'rh_superiortemporal_area',
    'rh_supramarginal_area',
    'rh_frontalpole_area',
    'rh_temporalpole_area',
    'rh_transversetemporal_area',
    'rh_insula_area',
    'rh_whitesurfarea_area',
    'lh_bankssts_volume',
    'lh_caudalanteriorcingulate_volume',
    'lh_caudalmiddlefrontal_volume',
    'lh_cuneus_volume',
    'lh_entorhinal_volume',
    'lh_fusiform_volume',
    'lh_inferiorparietal_volume',
    'lh_inferiortemporal_volume',
    'lh_isthmuscingulate_volume',
    'lh_lateraloccipital_volume',
    'lh_lateralorbitofrontal_volume',
    'lh_lingual_volume',
    'lh_medialorbitofrontal_volume',
    'lh_middletemporal_volume',
    'lh_parahippocampal_volume',
    'lh_paracentral_volume',
    'lh_parsopercularis_volume',
    'lh_parsorbitalis_volume',
    'lh_parstriangularis_volume',
    'lh_pericalcarine_volume',
    'lh_postcentral_volume',
    'lh_posteriorcingulate_volume',
    'lh_precentral_volume',
    'lh_precuneus_volume',
    'lh_rostralanteriorcingulate_volume',
    'lh_rostralmiddlefrontal_volume',
    'lh_superiorfrontal_volume',
    'lh_superiorparietal_volume',
    'lh_superiortemporal_volume',
    'lh_supramarginal_volume',
    'lh_frontalpole_volume',
    'lh_temporalpole_volume',
    'lh_transversetemporal_volume',
    'lh_insula_volume',
    'rh_bankssts_volume',
    'rh_caudalanteriorcingulate_volume',
    'rh_caudalmiddlefrontal_volume',
    'rh_cuneus_volume',
    'rh_entorhinal_volume',
    'rh_fusiform_volume',
    'rh_inferiorparietal_volume',
    'rh_inferiortemporal_volume',
    'rh_isthmuscingulate_volume',
    'rh_lateraloccipital_volume',
    'rh_lateralorbitofrontal_volume',
    'rh_lingual_volume',
    'rh_medialorbitofrontal_volume',
    'rh_middletemporal_volume',
    'rh_parahippocampal_volume',
    'rh_paracentral_volume',
    'rh_parsopercularis_volume',
    'rh_parsorbitalis_volume',
    'rh_parstriangularis_volume',
    'rh_pericalcarine_volume',
    'rh_postcentral_volume',
    'rh_posteriorcingulate_volume',
    'rh_precentral_volume',
    'rh_precuneus_volume',
    'rh_rostralanteriorcingulate_volume',
    'rh_rostralmiddlefrontal_volume',
    'rh_superiorfrontal_volume',
    'rh_superiorparietal_volume',
    'rh_superiortemporal_volume',
    'rh_supramarginal_volume',
    'rh_frontalpole_volume',
    'rh_temporalpole_volume',
    'rh_transversetemporal_volume',
    'rh_insula_volume',
    'lh_bankssts_thickness',
    'lh_caudalanteriorcingulate_thickness',
    'lh_caudalmiddlefrontal_thickness',
    'lh_cuneus_thickness',
    'lh_entorhinal_thickness',
    'lh_fusiform_thickness',
    'lh_inferiorparietal_thickness',
    'lh_inferiortemporal_thickness',
    'lh_isthmuscingulate_thickness',
    'lh_lateraloccipital_thickness',
    'lh_lateralorbitofrontal_thickness',
    'lh_lingual_thickness',
    'lh_medialorbitofrontal_thickness',
    'lh_middletemporal_thickness',
    'lh_parahippocampal_thickness',
    'lh_paracentral_thickness',
    'lh_parsopercularis_thickness',
    'lh_parsorbitalis_thickness',
    'lh_parstriangularis_thickness',
    'lh_pericalcarine_thickness',
    'lh_postcentral_thickness',
    'lh_posteriorcingulate_thickness',
    'lh_precentral_thickness',
    'lh_precuneus_thickness',
    'lh_rostralanteriorcingulate_thickness',
    'lh_rostralmiddlefrontal_thickness',
    'lh_superiorfrontal_thickness',
    'lh_superiorparietal_thickness',
    'lh_superiortemporal_thickness',
    'lh_supramarginal_thickness',
    'lh_frontalpole_thickness',
    'lh_temporalpole_thickness',
    'lh_transversetemporal_thickness',
    'lh_insula_thickness',
    'lh_meanthickness_thickness',
    'rh_bankssts_thickness',
    'rh_caudalanteriorcingulate_thickness',
    'rh_caudalmiddlefrontal_thickness',
    'rh_cuneus_thickness',
    'rh_entorhinal_thickness',
    'rh_fusiform_thickness',
    'rh_inferiorparietal_thickness',
    'rh_inferiortemporal_thickness',
    'rh_isthmuscingulate_thickness',
    'rh_lateraloccipital_thickness',
    'rh_lateralorbitofrontal_thickness',
    'rh_lingual_thickness',
    'rh_medialorbitofrontal_thickness',
    'rh_middletemporal_thickness',
    'rh_parahippocampal_thickness',
    'rh_paracentral_thickness',
    'rh_parsopercularis_thickness',
    'rh_parsorbitalis_thickness',
    'rh_parstriangularis_thickness',
    'rh_pericalcarine_thickness',
    'rh_postcentral_thickness',
    'rh_posteriorcingulate_thickness',
    'rh_precentral_thickness',
    'rh_precuneus_thickness',
    'rh_rostralanteriorcingulate_thickness',
    'rh_rostralmiddlefrontal_thickness',
    'rh_superiorfrontal_thickness',
    'rh_superiorparietal_thickness',
    'rh_superiortemporal_thickness',
    'rh_supramarginal_thickness',
    'rh_frontalpole_thickness',
    'rh_temporalpole_thickness',
    'rh_transversetemporal_thickness',
    'rh_insula_thickness',
    'rh_meanthickness_thickness',
    'brainsegvolnotvent',
    'etiv',
    ]
vals = timepoint
for roi in rois:
    mask = [x==roi for x in aparc.columns]
    if sum(mask)==0:
        print(f'  WARNING - no volume found for ROI {roi}')
        vals[roi] = numpy.zeros(vals[roi].shape)
    elif sum(mask)>1:
        raise Exception(f'Found >1 value for {roi}')
    else:
        vals = pandas.concat([vals,aparc[roi]], axis=1)

# Check for unexpected ROIs being present
for srcroi in aparc.columns:
    if (not srcroi in rois) and (not srcroi=='timepoint'):
        print(f'  WARNING - unexpected data found for ROI {srcroi}')

# Make data frame and write to file
os.makedirs(args.out_dir, exist_ok=True)
vals.to_csv(os.path.join(args.out_dir,'aparc.csv'), 
    header=True, index=False)
