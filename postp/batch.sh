

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

# while read f; do
#     ((i++))
#     printf -v j "%03d" $i

# done <cesm1.list

# for i in {000..099}; do
#     job="job"$i".job"
#     sed 's/zqz/'$i'/g' template.sh > $job 
#     qsub $job
# done



