
for i in {001..100};do
    f="job"$i".txt"
    job="job"$i".job"  
    sed 's/num/'$i'/g' template.sh > $job 
    sed -i 's:file:'$f':g' $job
    qsub $job
done
