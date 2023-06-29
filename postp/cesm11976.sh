

d='/glade/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/lnd/proc/tseries/monthly/NBP/'

i=0
for f in $d*"B20TRC5CNBDRD"*".NBP."*"2005"*".nc"; do
    ((i++))
    if  [ $i -le 40 ]; then
	printf -v j "%03d" $i
	job="job"$j".job"  
	sed 's/num/'$j'/g' template.sh > $job 
	sed -i 's:file:'$f':g' $job
	qsub $job	
    fi
done
