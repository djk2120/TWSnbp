
i=0
while read f; do
    ((i++))
    printf -v j "%03d" $i
    job="job"$j".job"  
    sed 's/num/'$j'/g' template.sh > $job 
    sed -i 's:file:'$f':g' $job
    qsub $job
done <cesm1.list

# for i in {000..099}; do
#     job="job"$i".job"
#     sed 's/zqz/'$i'/g' template.sh > $job 
#     qsub $job
# done



