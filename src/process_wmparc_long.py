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
parser.add_argument('--wmparc_csv', required=True)
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
wmparc = pandas.read_csv(args.wmparc_csv)

# Rename first column (subject label is actually timepoint label)
wmparc.rename(columns={wmparc.columns[0]: 'timepoint'}, inplace=True, errors='raise')

# Sanitize varnames
wmparc.columns = [sanitize(x) for x in wmparc.columns]

#for x in wmparc.columns:
#    print(f"    '{x}',")
#sys.exit(0)

# Use known list of desired outputs. Fill with 0 any missing (and drop any
# that are unexpected)
rois = [
    'wm_lh_bankssts',
    'wm_lh_caudalanteriorcingulate',
    'wm_lh_caudalmiddlefrontal',
    'wm_lh_cuneus',
    'wm_lh_entorhinal',
    'wm_lh_fusiform',
    'wm_lh_inferiorparietal',
    'wm_lh_inferiortemporal',
    'wm_lh_isthmuscingulate',
    'wm_lh_lateraloccipital',
    'wm_lh_lateralorbitofrontal',
    'wm_lh_lingual',
    'wm_lh_medialorbitofrontal',
    'wm_lh_middletemporal',
    'wm_lh_parahippocampal',
    'wm_lh_paracentral',
    'wm_lh_parsopercularis',
    'wm_lh_parsorbitalis',
    'wm_lh_parstriangularis',
    'wm_lh_pericalcarine',
    'wm_lh_postcentral',
    'wm_lh_posteriorcingulate',
    'wm_lh_precentral',
    'wm_lh_precuneus',
    'wm_lh_rostralanteriorcingulate',
    'wm_lh_rostralmiddlefrontal',
    'wm_lh_superiorfrontal',
    'wm_lh_superiorparietal',
    'wm_lh_superiortemporal',
    'wm_lh_supramarginal',
    'wm_lh_frontalpole',
    'wm_lh_temporalpole',
    'wm_lh_transversetemporal',
    'wm_lh_insula',
    'wm_rh_bankssts',
    'wm_rh_caudalanteriorcingulate',
    'wm_rh_caudalmiddlefrontal',
    'wm_rh_cuneus',
    'wm_rh_entorhinal',
    'wm_rh_fusiform',
    'wm_rh_inferiorparietal',
    'wm_rh_inferiortemporal',
    'wm_rh_isthmuscingulate',
    'wm_rh_lateraloccipital',
    'wm_rh_lateralorbitofrontal',
    'wm_rh_lingual',
    'wm_rh_medialorbitofrontal',
    'wm_rh_middletemporal',
    'wm_rh_parahippocampal',
    'wm_rh_paracentral',
    'wm_rh_parsopercularis',
    'wm_rh_parsorbitalis',
    'wm_rh_parstriangularis',
    'wm_rh_pericalcarine',
    'wm_rh_postcentral',
    'wm_rh_posteriorcingulate',
    'wm_rh_precentral',
    'wm_rh_precuneus',
    'wm_rh_rostralanteriorcingulate',
    'wm_rh_rostralmiddlefrontal',
    'wm_rh_superiorfrontal',
    'wm_rh_superiorparietal',
    'wm_rh_superiortemporal',
    'wm_rh_supramarginal',
    'wm_rh_frontalpole',
    'wm_rh_temporalpole',
    'wm_rh_transversetemporal',
    'wm_rh_insula',
    'left_unsegmentedwhitematter',
    'right_unsegmentedwhitematter',
    'lhcerebralwhitemattervol',
    'rhcerebralwhitemattervol',
    'cerebralwhitemattervol',
    'maskvol',
    'estimatedtotalintracranialvol',
    ]
vals = pandas.DataFrame(wmparc.timepoint)
for roi in rois:
    mask = [x==roi for x in wmparc.columns]
    if sum(mask)==0:
        print(f'  WARNING - no volume found for ROI {roi}')
        vals[roi] = numpy.zeros(vals.timepoint.shape)
    elif sum(mask)>1:
        raise Exception(f'Found >1 value for {roi}')
    else:
        vals = pandas.concat([vals,wmparc[roi]], axis=1)
        
# Check for unexpected ROIs being present
for srcroi in wmparc.columns:
    if (not srcroi in rois) and (not srcroi=='timepoint'):
        print(f'  WARNING - unexpected data found for ROI {srcroi}')

# Make data frame and write to file
os.makedirs(args.out_dir, exist_ok=True)
vals.to_csv(os.path.join(args.out_dir,'wmparc.csv'), 
    header=True, index=False)
