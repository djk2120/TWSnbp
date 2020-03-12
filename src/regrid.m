function out = regrid(lat,lon,f,latf,lonf)

ota = 1:length(latf);
oto = 1:length(lonf);
out = nan(length(latf),length(lonf));

for k=1:length(lat)
i = ota(latf==lat(k));
j = oto(lonf==lon(k));
out(i,j) = f(k);



end

