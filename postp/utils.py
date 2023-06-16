import xarray as xr
import numpy as np

def amean(da):
    #annual mean
    m  = da['time.daysinmonth']
    xa = 1/365*(m*da).groupby('time.year').sum().compute()
    xa.name=da.name
    xa.attrs=da.attrs
    return xa

def gmean(da,la,g=[]):
    if len(g)==0:
        g=xr.DataArray(np.tile('global',la.shape),
                       coords=la.coords,
                       name='biome').where(la>0)
    #mean across g groups
    cf = 1/la.groupby(g).sum()
    xg = cf*(la*da).groupby(g).sum().compute()
    xg.name=da.name
    xg.attrs=da.attrs
    return xg

def preprocess(ds):
    dvs=[]
    if float(abs((ds.time[1]-ds.time[0])/(28*24*60*60*1e9)-1))<0.05:
        nt=len(ds.time)
        yr0=ds['time.year'].values[0]
        ds['time']=xr.cftime_range(str(yr0),periods=nt,freq='MS',calendar='noleap')
    if len(dvs)>0:
        ds=ds[dvs]
    return ds

def get_sw(file):
    ds=preprocess(xr.open_dataset(file.replace('NBP','H2OSOI')))
    for dim in ds.H2OSOI.dims:
        if 'lev' in dim:
            sdim=dim
    ns=len(ds.H2OSOI[sdim])
    dz=xr.DataArray(1000*ds.DZSOI.sel(lat=30,lon=105,method='nearest')[:ns].values,
                    dims=sdim,name='Soil thickness',attrs={'units':'m'})
    sw=(dz*ds.H2OSOI).sum(dim=sdim).compute()
    
    return sw

def get_vpd(file):
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

    return [rh2m,tsa,vpd,vp]
