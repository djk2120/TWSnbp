function [] = data_io()

dir = '/glade/collections/cdg/timeseries-cmip6/';
exp = 'b.e21.BHIST.f09_g17.CMIP6-historical.001';
proc = '/lnd/proc/tseries/month_1/';
fstr1  = '.clm2.h0.';
fstr2  = '.185001-201412.nc';


the_var = 'NBP';
f = [dir,exp,proc,exp,fstr1,the_var,fstr2];
nbp = getmonthly(the_var,f,[],[],[],[]);
nbpstd = std(nbp,0,2);
subset = nbpstd>0&~isnan(nbpstd);
lat = lat(subset);
lon = lon(subset);
landarea = landarea(subset);
nbp = nbp(subset,:);

assignin('caller','lat',lat)
assignin('caller','lon',lon)
assignin('caller','landarea',landarea)



yy  = [1964,2013];
ny  = 1+yy(2)-yy(1);

extrazero = cell(11,1);
extrazero(1:9) = {'0'};

nmodels = 11;
varlist = {'TWS','NBP'};

for v = 1:length(varlist)

the_var = varlist{v};
x = zeros(length(lat),12*ny*nmodels);

for i = 1:6
    exp = ['b.e21.BHIST.f09_g17.CMIP6-historical.0',extrazero{i},num2str(i)];
    fstr2  = '.185001-201412.nc';
    f = [dir,exp,proc,exp,fstr1,the_var,fstr2];
    t1  = (yy(1)-1850)*12+1;
    t2  = (yy(2)-1849)*12;
    ix  = (1:12*ny)+(i-1)*12*ny; 
    x(:,ix) = getmonthly(the_var,f,subset,ng,t1,t2);
end

for i = 7:11
    exp = ['b.e21.BHIST.f09_g17.CMIP6-historical.0',extrazero{i},num2str(i)];
    fstr2 = '.195001-199912.nc';
    t1  = (yy(1)-1950)*12+1;
    t2  = (1999-1949)*12;
    tt1 = length(t1:t2);
    ix  = (1:tt1)+(i-1)*12*ny;
    f = [dir,exp,proc,exp,fstr1,the_var,fstr2];
    x(:,ix) = getmonthly(the_var,f,subset,ng,t1,t2);
    fstr2 = '.200001-201412.nc';
    t1  = 1;
    t2  = (yy(2)-1999)*12;
    tt2 = length(t1:t2);
    ix  = (tt1+1:tt1+tt2)+(i-1)*12*ny;
    f = [dir,exp,proc,exp,fstr1,the_var,fstr2];
    x(:,ix) = getmonthly(the_var,f,subset,ng,t1,t2);
end

assignin('caller',lower(the_var),x)
end

end