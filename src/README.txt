
Tests:

SUBJECTS_DIR=$(pwd)/../OUTPUTS/longout
subj_dirs=$(ls $SUBJECTS_DIR)
subj_dirs=${subj_dirs//$'\n'/ }

let c=0
for subj_dir in ${subj_dirs}; do
    (( c ++ ))
    cstr=$(printf "%03d" ${c})
    ./process_hippamyg_volumes_long.py --subject_dir "${SUBJECTS_DIR}/${subj_dir}" --timepoint ${subj_dir} --out_csv "$(pwd)/../OUTPUTS/longout-postproc/HAvol-${cstr}.csv"
done


./combine_csvs.py --in_csvs $(pwd)/../OUTPUTS/longout-postproc/HAvol*.csv --out_csv $(pwd)/../OUTPUTS/longout-postproc/HAvol.csv





export csvdir=$(pwd)/../OUTPUTS/longout-postproc/tmp
export outdir=$(pwd)/../OUTPUTS/longout-postproc/csvouts

./process_a2009s_long.py --csv_dir ${csvdir} --out_dir ${outdir}
./process_aparc_long.py --csv_dir ${csvdir} --out_dir ${outdir}
./process_BA_exvivo_long.py --csv_dir ${csvdir} --out_dir ${outdir}
./process_DKTatlas_long.py --csv_dir ${csvdir} --out_dir ${outdir}
./process_pial_long.py --csv_dir ${csvdir} --out_dir ${outdir}

./process_aseg_long.py --aseg_csv ${csvdir}/aseg.csv --out_dir ${outdir}
./process_wmparc_long.py --wmparc_csv ${csvdir}/wmparc.csv --out_dir ${outdir}



These work on a single fs output and need to be combined across timepoints:

process_brainstem_volumes.py
process_hippamyg_volumes.py
process_sclimbic.py
process_sclimbic_qa.py
process_thalamus_volumes.py




Not sure:

compute_MM_volumes.py

