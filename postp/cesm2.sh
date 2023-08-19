
i=0
j=1
printf -v k "%03d" $j
file='job001.txt'
:>$file
while read f; do
    ((i++))
    
    echo $f >> $file

    if [[ $i == 19 ]];then
	sed 's/num/'$k'/g' template.sh > "job"$k".job"
	sed -i 's/file/'$file'/g' "job"$k".job"
	qsub "job"$k".job"

	((j++))
	i=0
	printf -v k "%03d" $j
	file='job'$k'.txt'
	:>$file
    fi

done<cesm2.list
