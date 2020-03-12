function [] = data_io()

dir = '/glade/collections/cdg/timeseries-cmip6/';
exp = 'b.e21.BHIST.f09_g17.CMIP6-historical.001';
proc = '/lnd/proc/tseries/month_1/';
fstr1  = '.clm2.h0.';
fstr2  = '.185001-201412.nc';


the_var = 'GPP';
f = [dir,exp,proc,exp,fstr1,the_var,fstr2];
gpp = 24*60*60*getmonthly(the_var,f,[],[],[],[]); %gC/m2/d

subset = mean(gpp,2)>0.05;
lat = lat(subset);
lon = lon(subset);
landarea = landarea(subset);


assignin('caller','lat',lat)
assignin('caller','lon',lon)
assignin('caller','landarea',landarea)



yy  = [1965,2014];
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



    lats    = unique(lat);
    dlat    = min(lats(2:end)-lats(1:end-1));
    latfull = lats;
    go = 1;
    i  = 1;
    j  = 2;
    prev = latfull(1);
    while go
        i = i+1;
        if (lats(j)-prev)<1.05*dlat
            latfull(i) = lats(j);
            prev = lats(j);
            j = j+1;
        else
            latfull(i) = latfull(i-1)+dlat;
            prev = latfull(i);
        end
        if j>length(lats)
            go = 0;
        end
    end

    lons    = unique(lon);
    dlon    = min(lons(2:end)-lons(1:end-1));
    lonfull = lons;
    go = 1;
    i  = 1;
    j  = 2;
    prev = lonfull(1);
    while go
        i = i+1;
        if (lons(j)-prev)<1.05*dlon
            lonfull(i) = lons(j);
            prev = lons(j);
            j = j+1;
        else
            lonfull(i) = lonfull(i-1)+dlon;
            prev = lonfull(i);
        end
        if j>length(lons)
            go = 0;
        end
    end

assignin('caller','latfull',latfull)
assignin('caller','lonfull',lonfull)


    ccc = [103,0,31;...
           178,24,43;...
           214,96,77;...
           244,165,130;...
           253,219,199;...
           247,247,247;...
           209,229,240;...
           146,197,222;...
           67,147,195;...
           33,102,172;...
           5,48,97];

assignin('caller','ccc',ccc/256)

end

