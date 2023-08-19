
for m in {001..035}; do
    file="job"$m".txt"
    ls "/glade/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/lnd/proc/tseries/monthly/NBP/b.e11"*"BDRD.f09_g16."$m"."* > $file

    sed 's/num/'$m'/g' template.sh > "job"$m".job"
    sed -i 's/file/'$file'/g' "job"$m".job"
    qsub "job"$m".job"

done

for m in {101..105}; do
    file="job"$m".txt"
    ls "/glade/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/lnd/proc/tseries/monthly/NBP/b.e11"*"BDRD.f09_g16."$m"."* > $file

    sed 's/num/'$m'/g' template.sh > "job"$m".job"
    sed -i 's/file/'$file'/g' "job"$m".job"
    qsub "job"$m".job"

done
