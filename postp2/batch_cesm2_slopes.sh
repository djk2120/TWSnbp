
dir_path="/glade/derecho/scratch/djk2120/postp/twsnbp/cesm2/gridded"

for file in "$dir_path"/*; do
    mem=$(echo $file | cut -d. -f2)"."$(echo $file | cut -d. -f3)
    echo $mem
    sed 's/mem/'$mem'/g' cesm2_slopes.template > $mem".job"
    sed -i 's:file:'$file':g' $mem".job"
    qsub $mem".job"
done
