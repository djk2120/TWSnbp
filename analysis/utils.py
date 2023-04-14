import xarray as xr
import glob
import numpy as np

def amean(da,cf=None):
    #annual mean
    if not cf:
        cf=1/365
    m  = da['time.daysinmonth']
    xa = cf*(m*da).groupby('time.year').sum().compute()
    xa.name=da.name
    return xa

def gmean(da,la,cf=None,ln=None,u=None):
    #global mean
    if not cf:
        cf=1/la.sum()
    xg = cf*(la*da).sum(dim=['lat','lon']).compute()
    xg.name=da.name
    xg.attrs={'long_name':ln,'units':u}
    return xg

def get_vpd(model,yy=(1850,2100)):
    
    #esat
    files=lens_files(model,'TBOT',yy=yy)
    def preprocess(ds):
        t=ds.TBOT-273.15
        esat=0.61094*np.exp(17.625*t/(t+234.04))
        esat.name='ESAT'
        esat.attrs={'units':'kPa'}
        return esat
    esat=xr.open_mfdataset(files,combine='nested',concat_dim=['ens','time'],
                         parallel=True,preprocess=preprocess)
    #rh
    files=lens_files(model,'RH2M',yy=yy)
    def preprocess(ds):
        rh=ds.RH2M/100
        rh.name='RH'
        rh.attrs={'units':'fraction'}
        return rh

    rh=xr.open_mfdataset(files,combine='nested',concat_dim=['ens','time'],
                         parallel=True,preprocess=preprocess)
    rh['time']=ds.time
    
    ds=xr.Dataset()
    ds['ESAT']=esat
    ds['RH']=rh
    ds['VPD']=esat*rh
    ds['VPD'].attrs={'units':'kPa'}
    ds.RH.attrs['long_name']='relative humidity'
    ds.VPD.attrs['long_name']='vapor pressure deficit'
    ds.ESAT.attrs['long_name']='saturated vapor pressure'
    
    yr0=str(ds['time.year'][0].values)
    nt=len(ds.time)
    ds['time'] = xr.cftime_range(yr0,periods=nt,freq='MS',calendar='noleap') #fix time bug
    
    return ds