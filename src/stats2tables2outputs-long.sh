#!/usr/bin/env bash
#
# Compute regional volume/area/thickness measures
#
# Needs SUBJECTS_DIR, out_dir

echo stats2tables2outputs

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

# FIXME we are here
# Convert FS CSVs to dax-friendly CSVs
process_BA_exvivo.py --csv_dir "${tmp_dir}" --out_dir "${out_dir}"/APARCSTATS_BA_exvivo
process_DKTatlas.py --csv_dir "${tmp_dir}" --out_dir "${out_dir}"/APARCSTATS_DKTatlas
process_a2009s.py --csv_dir "${tmp_dir}" --out_dir "${out_dir}"/APARCSTATS_a2009s
process_aparc.py --csv_dir "${tmp_dir}" --out_dir "${out_dir}"/APARCSTATS_aparc
process_pial.py --csv_dir "${tmp_dir}" --out_dir "${out_dir}"/APARCSTATS_pial

process_aseg.py --aseg_csv "${tmp_dir}"/aseg.csv --out_dir "${out_dir}"/VOLSTATS_std
process_wmparc.py --wmparc_csv "${tmp_dir}"/wmparc.csv --out_dir "${out_dir}"/VOLSTATS_std

# FIXME This overwrites outputs each time through - we need a longitudinal mode
for subj_dir in ${subj_dirs}; do
    process_brainstem_volumes.py --subject_dir "${subj_dir}" --out_dir "${out_dir}"/VOLSTATS_highres
    process_hippamyg_volumes.py --subject_dir "${subj_dir}" --out_dir "${out_dir}"/VOLSTATS_highres
    process_thalamus_volumes.py --subject_dir "${subj_dir}" --out_dir "${out_dir}"/VOLSTATS_highres
done

# FIXME prob need long mode below here also

# sclimbic outputs (FS sclimbic run has created these csvs already)
process_sclimbic.py --sclimbic_csv "${tmp_dir}"/sclimbic.csv --out_dir "${out_dir}"/VOLSTATS_highres
process_sclimbic_qa.py --sclimbic_csvdir "${SUBJECTS_DIR}" --out_dir "${out_dir}"/SCLIMBIC_QA

# Extra computations for MM relabeling of hippocampus subfields
compute_MM_volumes.py --havol_csv "${out_dir}"/VOLSTATS_highres/HAvol.csv \
    --stats_dir "${out_dir}"/VOLSTATS_highres

