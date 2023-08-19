
i=0
d='/glade/scratch/djk2120/esgf/mpi12/'
mems=$(ls $d"nep_Emon_MPI-ESM1-2-LR_ssp370_r"*"i1p1"* | cut -d_ -f5 | uniq)

for mem in ${mems[@]}; do
    ((i++))

    echo $mem


    file=$mem'.txt'
    job=$mem'.job'
    

    ls $d"nep"*$mem* > $file
    ls $d"mrso"*$mem* >> $file

    sed 's/num/'$mem'/g' template.sh > $job
    sed -i 's/file/'$file'/g' $job

    qsub $job
    
done
