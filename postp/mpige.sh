

d='/glade/scratch/djk2120/esgf/mpige/'



for i in {001..100}; do


    mem="r"$i


    file=$mem'.txt'
    job=$mem'.job'
    

    ls $d"nep"*$mem* > $file
    ls $d"mrso"*$mem* >> $file

    sed 's/num/'$mem'/g' template.sh > $job
    sed -i 's/file/'$file'/g' $job

    qsub $job
    
done
