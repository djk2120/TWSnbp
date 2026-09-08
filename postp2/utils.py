import xarray as xr
import numpy as np
import dask

def getg(pps,tts,t,p,c,cthresh):
    g=xr.DataArray(np.zeros(t.shape),coords=[t.lat,t.lon])
    o=xr.DataArray(np.ones(t.shape),coords=[t.lat,t.lon])
    ivals=[]
    jvals=[]
    z=0
    for i,pp in enumerate(pps):
        for j,tt in enumerate(tts):
            z+=1
            ixt=(t>tt)&(t<=tt+2)
            ixp=(p>pp)&(p<=pp+200)
            if (ixt*ixp*c).sum()>cthresh:
                g=g+z*ixt*ixp*o
                ivals.append(i)
                jvals.append(j)
    g=g.where(g>0)
    g=g-1
    g.name='zone'
    return g,ivals,jvals

def tpgrid(m,ivals,jvals,pps,tts):
    out=np.zeros([len(pps),len(tts)])+np.nan
    out[ivals,jvals]=m
    da=xr.DataArray(out,dims=['P','T'])
    da['P']=pps+0.5*(pps[1]-pps[0])
    da['T']=tts+0.5*(tts[1]-tts[0])
    da['P'].attrs={'units':'mm/yr'}
    da['T'].attrs={'units':'°C'}
    return da

def get_ix(ds,yr0,yr1):
    avoids=[1962,1963,1982,1991,1992,1993]
    ix=(ds['year']>=yr0)&(ds['year']<=yr1)
    for yr in avoids:
        ix=(ix)&(ds['year']!=yr)
    return ix

def detrend_dim(da, dim, deg=1):
    # detrend along a single dimension (h/t rabernat)
    p = da.polyfit(dim=dim, deg=deg)
    fit = xr.polyval(da[dim], p.polyfit_coefficients)
    return da - fit

def amean(da):
    #annual mean
    m  = da['time.daysinmonth']
    xa = 1/m.groupby('time.year').sum()*(m*da).groupby('time.year').sum().compute()
    xa.name=da.name
    xa.attrs=da.attrs
    return xa

def gmean(da,la):
    cf = 1/la.sum()
    xg = cf*(la*da).sum(dim=['lat','lon']).compute()
    xg.name=da.name
    xg.attrs=da.attrs
    return xg

def fix_time(ds):
    yr0=str(ds['time.year'][0].values)
    ds['time']=xr.date_range(yr0,periods=len(ds.time),freq='MS',calendar='noleap')
    return ds

def preprocess(ds):
    nt=len(ds.time)
    yr0=ds['time.year'].values[0]
    ds['time']=xr.cftime_range(str(yr0),periods=nt,freq='MS',calendar='noleap')
    return ds

def get_sw(f):
    if 'CESM2' in f:
        dz,sdim=get_dz('CESM2')
    else:
        dz,sdim=get_dz('CESM1')

    ds=fix_time(xr.open_dataset(f))
    sw=(dz*ds.H2OSOI).sum(dim=sdim).compute()
    sw.name='SW'
    sw.attrs={'long_name':'total column soil water','units':'mm'}
    return sw

def get_dz(mdl):
    if mdl=='CESM2':
        sdim='levsoi'
        ns=20
        f='/glade/campaign/cgd/cesm/CESM2-LE/timeseries/lnd/proc/tseries/month_1/NBP/b.e21.BHISTcmip6.f09_g17.LE2-1001.001.clm2.h0.NBP.192001-192912.nc'
        tmp=xr.open_dataset(f)
    else:
        sdim='levgrnd'
        ns=15
        f='/glade/campaign/cesm/collections/cesmLE/CESM-CAM5-BGC-LE/lnd/proc/tseries/monthly/NBP/b.e11.B20TRC5CNBDRD.f09_g16.104.clm2.h0.NBP.192001-200512.nc'
        tmp=xr.open_dataset(f)
        
    dz=xr.DataArray(1000*tmp.DZSOI.sel(lat=30,lon=105,method='nearest')[:ns].values,
                    dims=sdim,name='Soil thickness',attrs={'units':'mm'})
    return dz,sdim
    
def get_dz1m(mdl):
    dz,sdim=get_dz(mdl)
    ns=len(dz)
    dz1m=0*dz
    for i in range(ns):
        zc=dz[:i+1].sum()
        if zc<1000:
            dz1m[i]=dz[i]
        else:
            dz1m[i]=1000-dz[:i].sum()
            break
    return dz1m,sdim
    
    


def get_sw1m(file):
    if 'CESM2' in file:
        dz,sdim=get_dz1m('CESM2')
    else:
        dz,sdim=get_dz1m('CESM1')

    ds=preprocess(xr.open_dataset(file.replace('NBP','H2OSOI')))
    sw=(dz*ds.H2OSOI).sum(dim=sdim).compute()
    sw.name='SW1M'
    
    return sw

def calcvpdq(tas,huss):
    t=tas-273.15
    esat=0.61094*np.exp(17.625*t/(t+234.04)).compute()
    vp=1e2/(1+0.622/huss)  #kpa
    vp.name='VP'
    vp.attrs={'long_name':'2m vapor pressure','units':'kPa'}
    vpd=esat-vp
    vpd.name='VPD'
    vpd.attrs={'long_name':'2m vapor pressure deficit','units':'kPa'}
    
    return [vpd,vp]


def calc_vpd(tsa,rh2m):

    #enforce rh in [0,100]
    rh2m=rh2m*(rh2m>0)
    rh2m=rh2m*(rh2m<100)+100*(rh2m>=100)
    #convert K to C
    t=tsa-273.15
    
    esat=0.61094*np.exp(17.625*t/(t+234.04)).compute()
    vpd=(esat*(1-rh2m/100)).compute()
    vpd.name='VPD'
    vpd.attrs={'long_name':'2m vapor pressure deficit','units':'kPa'}
    vp=(esat*rh2m/100).compute()
    vp.name='VP'
    vp.attrs={'long_name':'2m vapor pressure','units':'kPa'}
    
    return [vpd,vp]


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
    
    ix=abs(vpd.lat)<=24
    vpdt=la.sum()/la.where(ix).sum()*vpd.where(ix)
    vpdt.name='VPD_TROP'
    vpdt.attrs={'long_name':'2m vapor pressure deficit','units':'kPa'}

    return [rh2m,tsa,vpd,vp,vpdt]

def get_tsatrop(f,la):
    ds=preprocess(xr.open_dataset(f.replace('NBP','TSA')))
    ix=abs(ds.lat)<=24
    da=la.sum()/la.where(ix).sum()*ds['TSA'].where(ix)
    da.name='TSA_TROP'
    return da



