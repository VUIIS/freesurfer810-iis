
Tests:

subj_dirs=$(ls -d ${SUBJECTS_DIR}/*.long.*)
subj_dirs=${subj_dirs//$'\n'/ }
for subj_dir in $subj_dirs; do
    export subj_dir
    ./create_MM_labelmaps_long.sh
done





export PATH=$(pwd):$PATH
export SUBJECTS_DIR=$(pwd)/../OUTPUTS/longout
export out_dir=$(pwd)/../OUTPUTS/longout-postproc
./stats2tables2outputs-long.sh



#SUBJECTS_DIR=$(pwd)/../OUTPUTS/longout
#subj_dirs=$(ls $SUBJECTS_DIR)
#subj_dirs=${subj_dirs//$'\n'/ }
subj_dirs="v000mo.long.template2 v024mo.long.template2"

let c=0
for subj_dir in ${subj_dirs}; do
    (( c ++ ))
    cstr=$(printf "%03d" ${c})
    ./compute_MM_volumes_long.py \
        --havol_csv "$(pwd)/../OUTPUTS/longout-postproc/HAvol-${cstr}.csv" \
        --timepoint ${subj_dir} \
        --out_csv "$(pwd)/../OUTPUTS/longout-postproc/MMhippvol-${cstr}.csv"
done


./combine_csvs.py --in_csvs $(pwd)/../OUTPUTS/longout-postproc/MMhippvol-*.csv --out_csv $(pwd)/../OUTPUTS/longout-postproc/MMhippvol.csv





export csvdir=$(pwd)/../OUTPUTS/longout-postproc/tmp
export outdir=$(pwd)/../OUTPUTS/longout-postproc/csvouts

./process_a2009s_long.py --csv_dir ${csvdir} --out_dir ${outdir}
./process_aparc_long.py --csv_dir ${csvdir} --out_dir ${outdir}
./process_BA_exvivo_long.py --csv_dir ${csvdir} --out_dir ${outdir}
./process_DKTatlas_long.py --csv_dir ${csvdir} --out_dir ${outdir}
./process_pial_long.py --csv_dir ${csvdir} --out_dir ${outdir}

./process_aseg_long.py --aseg_csv ${csvdir}/aseg.csv --out_dir ${outdir}
./process_wmparc_long.py --wmparc_csv ${csvdir}/wmparc.csv --out_dir ${outdir}


./process_sclimbic_long.py --sclimbic_csv "${csvdir}"/sclimbic.csv --out_dir "${outdir}"

./process_sclimbic_qa_long.py --sclimbic_csvdir $(pwd)/../OUTPUTS/longout --out_dir $(pwd)/../OUTPUTS/SCLIMBIC_QA



