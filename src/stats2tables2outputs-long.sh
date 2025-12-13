#!/usr/bin/env bash
#
# Compute regional volume/area/thickness measures
#
# Needs SUBJECTS_DIR, out_dir

echo stats2tables2outputs

# FIXME we need a list of the long out dirs only, not anything else that might be in SUBJECTS_DIR
subj_dirs=$(ls "${SUBJECTS_DIR}")
subj_dirs=${subj_dirs//$'\n'/ }
tmp_dir="${out_dir}"/tmp

mkdir -p "${tmp_dir}"

# aseg volumes
echo "aseg for ${subj_dirs}"
asegstats2table \
    --delimiter comma \
    --meas volume \
    --subjects ${subj_dirs} \
    --all-segs \
    --stats aseg.stats \
    --tablefile "${tmp_dir}"/aseg.csv

# sclimbic volumes
asegstats2table \
    --delimiter comma \
    --meas volume \
    --subjects ${subj_dirs} \
    --all-segs \
    --stats sclimbic.stats \
    --tablefile "${tmp_dir}"/sclimbic.csv

# Surface parcellations
#    aparc, aparc.pial, aparc.a2009s, aparc.DKTatlas, BA_exvivo
#    lh, rh
#    volume, area, thickness
for aparc in aparc aparc.a2009s aparc.pial aparc.DKTatlas BA_exvivo ; do
	for meas in volume area thickness ; do
		for hemi in lh rh ; do
			aparcstats2table --delimiter comma \
			-m $meas --hemi $hemi --subjects ${subj_dirs} --parc $aparc \
			-t "${tmp_dir}"/"${hemi}-${aparc}-${meas}.csv"
		done
	done
done

# WM parcellation
asegstats2table \
    --delimiter comma \
    --meas volume \
    --subjects ${subj_dirs} \
    --all-segs \
    --stats wmparc.stats \
    --tablefile "${tmp_dir}"/wmparc.csv

# Convert FS CSVs to dax-friendly CSVs
process_BA_exvivo_long.py --csv_dir "${tmp_dir}" --out_dir "${out_dir}"/APARCSTATS_BA_exvivo
process_DKTatlas_long.py --csv_dir "${tmp_dir}" --out_dir "${out_dir}"/APARCSTATS_DKTatlas
process_a2009s_long.py --csv_dir "${tmp_dir}" --out_dir "${out_dir}"/APARCSTATS_a2009s
process_aparc_long.py --csv_dir "${tmp_dir}" --out_dir "${out_dir}"/APARCSTATS_aparc
process_pial_long.py --csv_dir "${tmp_dir}" --out_dir "${out_dir}"/APARCSTATS_pial

process_aseg_long.py --aseg_csv "${tmp_dir}"/aseg.csv --out_dir "${out_dir}"/VOLSTATS_std
process_wmparc_long.py --wmparc_csv "${tmp_dir}"/wmparc.csv --out_dir "${out_dir}"/VOLSTATS_std

# Hi-res segs
let c=0
for subj_dir in ${subj_dirs}; do
    (( c ++ ))
    cstr=$(printf "%03d" ${c})

    ./process_brainstem_volumes_long.py \
        --subject_dir "${SUBJECTS_DIR}/${subj_dir}" \
        --timepoint ${subj_dir} \
        --out_csv "${out_dir}"/BSvol-${cstr}.csv

    ./process_hippamyg_volumes_long.py \
        --subject_dir "${SUBJECTS_DIR}/${subj_dir}" \
        --timepoint ${subj_dir} \
        --out_csv "${out_dir}"/HAvol-${cstr}.csv

    ./process_thalamus_volumes_long.py \
        --subject_dir "${SUBJECTS_DIR}/${subj_dir}" \
        --timepoint ${subj_dir} \
        --out_csv "${out_dir}"/TNvol-${cstr}.csv

    ./compute_MM_volumes_long.py \
        --havol_csv "${out_dir}"/HAvol-${cstr}.csv \
        --timepoint ${subj_dir} \
        --out_csv "${out_dir}"/MMhippvol-${cstr}.csv

done

mkdir -p "${out_dir}"/VOLSTATS_highres

combine_csvs.py --in_csvs "${out_dir}"/BSvol-*.csv --out_csv "${out_dir}"/VOLSTATS_highres/BSvol.csv
combine_csvs.py --in_csvs "${out_dir}"/HAvol-*.csv --out_csv "${out_dir}"/VOLSTATS_highres/HAvol.csv
combine_csvs.py --in_csvs "${out_dir}"/TNvol-*.csv --out_csv "${out_dir}"/VOLSTATS_highres/TNvol.csv
combine_csvs.py --in_csvs "${out_dir}"/MMhippvol-*.csv --out_csv "${out_dir}"/VOLSTATS_highres/MMhippvol.csv

process_sclimbic_long.py --sclimbic_csv "${tmp_dir}"/sclimbic.csv --out_dir "${out_dir}"/VOLSTATS_highres
process_sclimbic_long_qa.py --sclimbic_csvdir "${out_dir}" --out_dir "${out_dir}"/SCLIMBIC_QA


