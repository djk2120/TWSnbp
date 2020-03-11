

yy = [1965,2014];
ny = length(yy(1):yy(2));


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



g = year+model*ny;
tws_ann = splitapply(@sum,(repmat(eomday(2001,1:12),nl,50*11).*tws)',findgroups(g)')'/365;
nbp_ann = 24*60*60*splitapply(@sum,(repmat(eomday(2001,1:12),nl,50*11).*nbp)', ...
               findgroups(g)')';


for i = 1:11
    ix = (1:ny)+(i-1)*ny;
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

printme = 1;
if printme 
   xdk = gcf;
    xdk.Units = 'inches';
    xdk.PaperSize = [10,7];
    xdk.PaperPosition = [0,0,xdk.PaperSize];
    print('./figs/tws_nbp_scatters','-dpdf')
end
