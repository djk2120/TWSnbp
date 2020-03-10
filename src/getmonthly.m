function x=getmonthly(the_var,f,subset,ng,t1,t2)

    nt = length(t1:t2);


    if length(subset)==0
        lats = ncread(f,'lat');
        lons = ncread(f,'lon');
        ng  = length(lats)*length(lons);
   
        lat = reshape(repmat(lats',length(lons),1),[ng,1]);
        lon = reshape(repmat(lons',1,length(lats)),[ng,1]);        

        lf     = reshape(ncread(f,'landfrac'),[ng,1]);
        area   = reshape(ncread(f,'area'),[ng,1]);
        landarea = lf.*area;


        lon(lon>180) = lon(lon>180)-360;
        x = reshape(ncread(f,the_var),[ng,1980]);




        assignin('caller','lat',lat)
        assignin('caller','lon',lon)
        assignin('caller','landarea',landarea)
        assignin('caller','ng',ng)

    else
        x = reshape(...
                    ncread(f,the_var,[1,1,t1],[inf,inf,nt]),...
                    [ng,nt]);
        x = x(subset,:);
    end


    

    



