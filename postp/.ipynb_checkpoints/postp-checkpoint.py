import numpy as np
import pandas as pd
import xarray as xr
import re
import sys

def preprocess(ds):
    dvs=[]
    if float(abs((ds.time[1]-ds.time[0])/(28*24*60*60*1e9)-1))<0.05:
        nt=len(ds.time)
        yr0=ds['time.year'].values[0]
        ds['time']=xr.cftime_range(str(yr0),periods=nt,freq='MS',calendar='noleap')
    if len(dvs)>0:
        ds=ds[dvs]
    return ds.sel(time=slice('1920','2100'))

def amean(da,cf=None,u=None):
    #annual mean
    if not cf:
        cf=1/365
    m  = da['time.daysinmonth']
    xa = cf*(m*da).groupby('time.year').sum().compute()
    xa.name=da.name
    xa.attrs=da.attrs
    if u:
        xg.attrs['units']=u
    return xa

def gmean(da,la,cf=None,ln=None,u=None):
    #global mean
    if not cf:
        cf=1/la.sum()
    xg = cf*(la*da).sum(dim=['lat','lon']).compute()
    xg.name=da.name
    xg.attrs=da.attrs
    if u:
        xg.attrs['units']=u
    return xg

def get_sw(file,la,dz):
    ds=preprocess(xr.open_dataset(file.replace('NBP','H2OSOI')))
    sdim=dz.dims[0]
    sw=(dz*ds.H2OSOI).sum(dim=sdim).compute()
    return gmean(amean(sw),la)

def get_vpd(file,la):
    rh2m=preprocess(xr.open_dataset(file.replace('NBP','RH2M'))).RH2M
    tsa=preprocess(xr.open_dataset(file.replace('NBP','TSA'))).TSA
    t=tsa-273.15
    esat=0.61094*np.exp(17.625*t/(t+234.04)).compute()
    vpd=(esat*(1-rh2m/100)).compute()
    vpd.name='VPD'
    vpd.attrs={'long_name':'2m vapor pressure deficit','units':'kPa'}
    vp=(esat*rh2m/100).compute()
    vp.name='VP'
    vp.attrs={'long_name':'2m vapor pressure','units':'kPa'}
    
    ds=xr.Dataset()
    ds['RH2M']=gmean(amean(rh2m),la)
    ds['TSA']=gmean(amean(tsa),la)
    ds['VPD']=gmean(amean(vpd),la)
    ds['VP']=gmean(amean(vp),la)

    return ds

def makeann(f):
    files=pd.read_csv(f,header=None)[0].values
    la=xr.open_dataset('mask_grnlnd_antarc.nc').landarea

    f=files[0]
    if 'CESM2' in f:
        tmp=xr.open_dataset('/glade/campaign/cgd/cesm/CESM2-LE/timeseries/lnd/proc/tseries/month_1/H2OSOI/b.e21.BHISTcmip6.f09_g17.LE2-1001.001.clm2.h0.H2OSOI.192001-192912.nc')
        ns=len(tmp.levsoi)
        dz=xr.DataArray(1000*tmp.DZSOI.sel(lat=30,lon=105,method='nearest')[:ns].values,
                        dims='levsoi',name='Soil thickness',attrs={'units':'mm'})

    
    for f in files:
        dout='/glade/scratch/djk2120/postp/'
        fout=dout+'cesm2.globann.'+f.split('.')[4]+'-'+f.split('.')[5]+'.'+f.split('.')[-2][:4]+'.nc'
        #fout=dout+'cesm1.globann.'+f.split('.')[-6]+'.'+f.split('.')[-2][:4]+'.nc'
        ds=get_vpd(f,la)
        dvs=['GPP','HR','AR','NPP','NEP','NBP','SOILWATER_10CM','FCTR','FGEV','FCEV','QRUNOFF','SW']
        for v in dvs:
            if v=='VPD':
                ds=get_vpd(f,la)
            elif v=='SW':
                ds[v]=get_sw(f,la,dz)
            else:
                tmp=preprocess(xr.open_dataset(f.replace('NBP',v)))
                ds[v]=gmean(amean(tmp[v]),la)
        ds.to_netcdf(fout,unlimited_dims='year')

f=sys.argv[1]
makeann(f)
