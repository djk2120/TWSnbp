

cp cesm2.list tmp.txt
for i in {001..095};do
    f="job"$i".txt"
    head -n 20 tmp.txt > $f
    tail -n +21 tmp.txt > tmp2.txt
    mv tmp2.txt tmp.txt
    job="job"$i".job"  
    sed 's/num/'$i'/g' template.sh > $job 
    sed -i 's:file:'$f':g' $job
    qsub $job

done
