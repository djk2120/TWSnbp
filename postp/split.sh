cp $1 tmp.txt

nl=$(wc -l < tmp.txt)

i=0
while (( $nl > 50 )); do
    ((i++))
    printf -v j "%03d" $i
    head -n 50 tmp.txt > "f"$j".txt"
    tail -n +50 tmp.txt > tmp2.txt
    mv tmp2.txt tmp.txt
    nl=$(wc -l < tmp.txt)
done

((i++))
printf -v j "%03d" $i
mv tmp.txt "f"$j".txt"

