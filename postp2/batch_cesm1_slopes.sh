
mdl='cesm1'
in_dir="/glade/derecho/scratch/djk2120/postp/twsnbp/"$mdl"/gridded"
out_dir="/glade/derecho/scratch/djk2120/postp/twsnbp/"$mdl"/slopes"
mkdir -p $out_dir

i=0
for file in "$in_dir"/*; do
    ((i++))
    printf -v mem "%03d" $i
    job=$mdl"_slopes_"$mem".job"
    sed 's/mem/'$mem'/g' slopes.template > $job
    sed -i 's:file:'$file':g' $job
    qsub $job
done
