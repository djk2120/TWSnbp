

yy = [1965,2014];
nyears = length(yy(1):yy(2));


if ~exist('nbp','var')
    data_io()
end


month = repmat(1:12,1,50*11);
model = repmat(1:11,50*12,1);
model = model(:)';
year  = repmat(yy(1):yy(2),12,11);
year  = year(:)';
nl    = length(lat);
extrazero = cell(11,1);
extrazero(1:9) = {'0'};
ylist = unique(year);


if ~exist('tws_ann','var')

    %compute NBP(sum) and TWS(mean) annual values
    g = year+model*nyears;
    tws_ann = splitapply(@sum,(repmat(eomday(2001,1:12),nl,50*11).*tws)',findgroups(g)')'/365;
    nbp_ann = 24*60*60*splitapply(@sum,(repmat(eomday(2001,1:12),nl,50*11).*nbp)', ...
               findgroups(g)')';

    %detrend NBP and TWS annual values
    G = [ones(nyears,1),(1:nyears)'];
    tws_ann_dt = nan*tws_ann;
    nbp_ann_dt = nan*tws_ann;
    for i = 1:nl
        t = tws_ann(i,:);
        n = nbp_ann(i,:);
        for j = 1:11
            ix = (1:nyears)+(j-1)*nyears;
            d = t(ix)';
            m = G\d;
            tws_ann_dt(i,ix) = d-G*m;
            d = n(ix)';
            m = G\d;
            nbp_ann_dt(i,ix) = d-G*m;
        end
    end

    %compute slope, pixel-by-pixel, for each ENS
    nx = 11;
    ix0 = year(month==1)>1999;
    ny  = sum(ix0&model(month==1)==1);
    tws_nbp_slopes = zeros(nl,nx);
    tws_nbp_corrs  = zeros(nl,nx);
    for ee = 1:nx
    for i = 1:nl
        ix = ix0&model(month==1)==ee;
        x = tws_ann_dt(i,ix)';
        G = [x];
        d = nbp_ann_dt(i,ix)';
        m = G\d;
        tws_nbp_slopes(i,ee) = m;
        tws_nbp_corrs(i,ee)  = corr(x,d);
    end
    end



end

gg = zeros(500,1);
gg(1:5)  = [0,0,0,0,0];
gg(6:10) = [0,0,0,0,1];

if gg(10)>0

    yy = 1999;
    ix = year(month==1)>yy;
    twsvar = splitapply(@var,tws_ann_dt(:,ix)',model(year>yy&month==1)')';
    maxx = 10000;
    for i = 1:4
        subplot(2,2,i)
        out =  regrid(lat,lon,twsvar(:,i),latfull,lonfull);
        aa = imagesc(lonfull,latfull,out,[0,maxx]);
        set(aa,'AlphaData',~isnan(out))
        set(gca,'YDir','Normal')     
        c = colorbar;
        ylabel(c,'var(TWS) [mm^2]')
        ylim([-60,75])
        title(['e0',num2str(i)])
        set(gca,'xtick',-180:30:180)
        set(gca,'ytick',-60:30:90)
    end

    a = repmat(landarea,1,11);
    a = a/sum(a(:));

    ix = abs(twsvar)<maxx;
    sum(a(ix))

    printme = 1;
    if printme
    xdk = gcf;
    xdk.Units = 'inches';
    xdk.PaperSize = [10,4];
    xdk.PaperPosition = [0,0,xdk.PaperSize];
    print('figs/twsvar_maps','-dpdf')
    end


end


if gg(9)>0
    Rthresh = 0.514;
    m = zeros(11,1);
    for i = 1:11
        lx = tws_nbp_corrs(:,i)>=Rthresh;
        ix = year(month==1)>1999&model(month==1)==i;
        wt = var(tws_ann_dt(lx,ix),0,2);
        wt = wt/sum(wt);
        m(i) = wt'*tws_nbp_slopes(lx,i);
    end

    mean(m)

    subplot(1,2,2)
    bar(m)
    xlabel('Ensemble member')
    ylabel('Slope NBP~TWS (gC/kgH2O)')
    ylim([0,1])
    
    for i = 1:11
        ix = model(month==1)==i&year(month==1)>1999;
        G  = (landarea'*tws_ann_dt(:,ix)/1e9)';
        d  = (landarea'*nbp_ann_dt(:,ix)/1e9)';
        m(i) = G\d;
    end

    subplot(1,2,1)
    bar(m)
    xlabel('Ensemble member')
    ylabel('Slope NBP~TWS (gC/kgH2O)')
    ylim([0,1])


    xdk = gcf;
    xdk.Units = 'inches';
    xdk.PaperSize = [8,3];
    xdk.PaperPosition = [0,0,8,3];
    %print('figs/tws_nbp_slopebars','-dpdf')

end



if gg(8)>0

    %corr vs. p-value, 15 points
    x = (1:15)';
    for i = 1:500
    y = 0.05*x+rand(15,1);
    c(i) = corr(x,y);
    lm = fitlm(x,y);
    p(i) = lm.Coefficients.pValue(2);
    end

    hold off
    plot(p,c,'.')
    xlim([0,0.2])
    
    [a,b] = min(abs(p-0.05))
    % R = 0.514

end


if gg(7)>0
    ix = year(month==1)>1999;

    x  = landarea'*tws_ann_dt(:,ix)/1e9;
    y  = landarea'*nbp_ann_dt(:,ix)/1e9;

    ix = y==y3;

    subplot(1,1,1)
    hold off
    plot(x,y,'.')
    lm = fitlm(x,y,'Intercept',false);
    c  = lm.Coefficients.Estimate;
    c  = [0,c];
    ylim([-3.5,3.5])
    xlim([-3.5,3.5])
    hold on
    plot([-3.5,3.5],c(1)+c(2)*[-3,3],'LineWidth',1.5);

    text(-3,3,['R= ',num2str(round(corr(x',y'),2))])
    text(-3,2.65,['m= ',num2str(round(c(2),2))])
    ax = gca;
    ax.Position = [0.1300 0.1100 0.8 0.8];
    xlabel('TWS anomaly (TtH2O)')
    ylabel('NBP anomaly (GtC)')
    plot(x(ix),y(ix),'ro','MarkerSize',12,'LineWidth',3)


    xdk = gcf;
    xdk.Units = 'inches';
    xdk.PaperSize = [4,4];
    xdk.PaperPosition = [0,0,4,4];
    
    print('figs/tws_nbp_pooled2','-dpdf')


end


if gg(6)>0


    x = landarea'*tws_ann_dt/1e9;
    y = landarea'*nbp_ann_dt/1e9;

    ix = x>-1.1&x<-0.9;
    xx = x(ix);
    yy = y(ix);
    y2 = max(yy);
    %y2 = yy(4);
    %y3 = max(yy);
    [~,ix2] = min(abs(y-y2));
    e2 = 1+floor(ix2/50.001);
    yr = year(month==1);
    yr(ix2)


    out2 = regrid(lat,lon,tws_ann_dt(:,ix2),latfull,lonfull);
    m2   = regrid(lat,lon,tws_nbp_slopes(:,e2),latfull,lonfull);
    altg2 = nbp_ann_dt(:,ix2).*landarea/10^6;


    val = 5;
    sum(abs(altg2(abs(altg2)<val)))/sum(abs(altg2))
    altg2   = regrid(lat,lon,altg2,latfull,lonfull); %MtC


    subplot('Position',[0.04,0.57,0.42,0.38])
    aa = imagesc(lonfull,latfull,out2,[-500,500]);
    set(aa,'AlphaData',~isnan(out2))
    set(gca,'YDir','Normal')
    colormap(gca,ccc2)
    c = colorbar;
    ylabel(c,'TWS anomaly (mm)')
    title([num2str(round(x(ix2),2)),' TtH2O'])
    ylim([-60,75])
    set(gca,'xtick',-180:60:180)
    set(gca,'ytick',-60:30:90)

    subplot('Position',[0.54,0.57,0.42,0.38])
    aa = imagesc(lonfull,latfull,m2,[-3,3]);
    set(aa,'AlphaData',~isnan(m2))
    set(gca,'YDir','Normal')
    colormap(gca,ccc2)
    c = colorbar;
    ylabel(c,'NBP sensitivity (gC/kgH2O)')
    ylim([-60,75])
    set(gca,'xtick',-180:60:180)
    set(gca,'ytick',-60:30:90)

    subplot('Position',[0.54,0.08,0.42,0.38])
    aa = imagesc(lonfull,latfull,altg2,[-val,val]);
    set(aa,'AlphaData',~isnan(altg2))
    set(gca,'YDir','Normal')
    colormap(gca,ccc2)
    c = colorbar;
    ylabel(c,'NBP anomaly (gC/m2)')
    ylim([-60,75])
    set(gca,'xtick',-180:60:180)
    set(gca,'ytick',-60:30:90)
    title([num2str(round(y(ix2),2)),' GtC'])

    xdk = gcf;
    xdk.Units = 'inches';
    xdk.PaperSize= [8,4];
    xdk.PaperPosition = [0,0,8,4];
    %print('figs/example_anomaly1','-dpdf')


end




if gg(4)>0

    %what R-value corresponds to p=0.05 for n=50?
    %     abs(R)>=0.28
    if ~exist('m_tws_nbp','var')
    m_tws_nbp = nan(nl,11);
    r_tws_nbp = zeros(nl,11);
    for i = 1:nl
        t = tws_ann_dt(i,:);
        n = nbp_ann_dt(i,:);
        for j = 1:11
            ix = (1:nyears)+(j-1)*nyears;
            G  = t(ix)';
            d  = n(ix)';
            r  = corr(G,d);
            if r>=0.28
                m_tws_nbp(i,j) = G\d;
            end
            r_tws_nbp(i,j) = r;
        end
    end
    end

    g       = year+model*nyears;
    g       = splitapply(@mean,model',findgroups(g)')'; 
    tws_var = splitapply(@var,tws_ann',g')';

    xv = -0.5:0.2:2.1;
    nx = length(xv)-1;
    out = zeros(nx,1);
    m_agg = zeros(11,1);
    for j = 1:11
        lx = ~isnan(m_tws_nbp(:,j));
        a = landarea(lx).*tws_var(lx,j);
        a = a/sum(a);
        for i = 1:nx
            ix       = m_tws_nbp(lx,j)>xv(i)&m_tws_nbp(lx,j)<=xv(i+1);
            out(i,j) = sum(a(ix));
        end
        m_agg(j) = a'*m_tws_nbp(lx,j);
    end
    
    x = 0.5*(xv(2:end)+xv(1:end-1));
    avgslope = mean(m_agg);
    subplot(2,1,1)
    plot(x,out,'Color',[0.7,0.7,0.7])
    xlim([-0.5,2])
    set(gca,'Layer','top')
    xlabel('Slope (gC/yr/kgH2O)')
    ylabel({'Density';'weighted by var(TWS)'})
    legend('e001','e002','...','e011')
    subplot(2,1,2)
    hold off
    plot([-1,20],[avgslope,avgslope],'k:','LineWidth',1.5)
    hold on
    bar(m_agg,'FaceColor',[0.6,0.6,0.6],'FaceAlpha',0.8)
    xlim([0,12])
    set(gca,'xtick',1:11)
    xlabel('Ensemble member')
    ylabel({'Slope';'(derived from pdf)'})

    printme = 0;
    if printme 
        xdk = gcf;
        xdk.Units = 'inches';
        xdk.PaperSize = [5,4];
        xdk.PaperPosition = [0,0,xdk.PaperSize];
        print('./figs/tws_nbp_pdfs','-dpdf')
    end

    

end





if gg(2)==1

    ix   = year>1999;
    ylistix = unique(year(ix));
    ot   = 1:nyears;
    otix = ot(ismember(ylist,ylistix));

    maxx = 0;
    maxy = 0;
    p = zeros(11,1);
    for i = 1:11
        ix = otix+(i-1)*nyears;
        x  = landarea'*tws_ann(:,ix)/1e9;
        lm = fitlm(1:length(otix),x);
        x  = lm.Residuals.raw;
        y  = landarea'*nbp_ann(:,ix)/1e9;
        lm = fitlm(1:length(otix),y);
        y  = lm.Residuals.raw;
        subplot(3,4,i)
        hold off
        plot(x,y,'k.','MarkerSize',7)
        lm = fitlm(x,y);
        p(i) = lm.Coefficients.pValue(2);
        c  = lm.Coefficients.Estimate;
        r  = corr(x,y);
        hold on
        x1 = [-3,3];
        if p(i)<0.05
            plot(x1,c(1)+c(2)*x1,'LineWidth',1.5)
        end
        xlim([-3,3])
        ylim([-2,2])
        text(-2.8,1.7,['R= ',num2str(round(r,2))]) 
        text(-2.8,1.3,['m= ',num2str(round(c(2),2))])
        title(['e0',extrazero{i},num2str(i)])
        maxx = max(maxx,max(abs(x)));
        maxy = max(maxy,max(abs(y)));
    end

    ax = axes('Position',[0.1 0.085 0.864 0.855],'Visible','off');
    ax.XLabel.Visible='on';
    ax.YLabel.Visible='on';
    xlabel('Global annual TWS anomaly (TtH2O)')
    ylabel('Global annual NBP anomaly (PgC/yr)')

    printme = 1;
    if printme
        xdk = gcf;
        xdk.Units = 'inches';
        xdk.PaperSize = [10,7];
        xdk.PaperPosition = [0,0,xdk.PaperSize];
        print('./figs/tws_nbp_scatters','-dpdf')
    end


end





if gg(1)==1
    p = zeros(11,1);
    for i = 1:11
        ix = (1:nyears)+(i-1)*nyears;
        x  = landarea'*tws_ann(:,ix)/1e9;
        lm = fitlm(1:50,x);
        x  = lm.Residuals.raw;
        y  = landarea'*nbp_ann(:,ix)/1e9;
        lm = fitlm(1:50,y);
        y  = lm.Residuals.raw;
        subplot(3,4,i)
        hold off
        plot(x,y,'.')
        lm = fitlm(x,y);
        p(i) = lm.Coefficients.pValue(2);
        c  = lm.Coefficients.Estimate;
        r  = corr(x,y);
        hold on
        x1 = [-4,4];
        plot(x1,c(1)+c(2)*x1,'LineWidth',1.5)
        xlim([-4,4])
        ylim([-2,2])
        text(-3.8,1.7,['R= ',num2str(round(r,2))]) 
        text(-3.8,1.3,['m= ',num2str(round(c(2),2))])
        title(['e0',extrazero{i},num2str(i)])
    end
    
    ax = axes('Position',[0.1 0.085 0.864 0.855],'Visible','off');
    ax.XLabel.Visible='on';
    ax.YLabel.Visible='on';
    xlabel('Global annual TWS anomaly (TtH2O)')
    ylabel('Global annual NBP anomaly (PgC/yr)')
    
    printme = 0;
    if printme 
        xdk = gcf;
        xdk.Units = 'inches';
        xdk.PaperSize = [10,7];
        xdk.PaperPosition = [0,0,xdk.PaperSize];
        print('./figs/tws_nbp_scatters','-dpdf')
    end
end