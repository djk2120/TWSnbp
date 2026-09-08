while read mem; do
    sed 's/mem/'$mem'/g' cesm2_gridded.template > $mem".job"
    qsub $mem".job"
done< cesm2.mems
