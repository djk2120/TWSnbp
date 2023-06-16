import xarray as xr
import numpy as np
import sys
from utils import *
from scipy import stats

def calc_slopes(f,v1,v2,y1,y2):
    
    cf=24*60*60*365
    ds=xr.open_dataset(f).sel(year=slice(y1,y2))
    la=xr.open_dataset('mask_grnlnd_antarc.nc').landarea
    xa=detrend_dim(ds[v1],'year')
    ya=cf*detrend_dim(ds[v2],'year')
    
    ix=xa.std(dim='year')>0
    ivals=np.tile(np.arange(192).reshape([-1,1]),[1,288])[ix]
    jvals=np.tile(np.arange(288),[192,1])[ix]
    slopes=np.zeros([192,288])+np.nan
    rvals=np.zeros([192,288])+np.nan
    pvals=np.zeros([192,288])+np.nan
    for i,j in zip(ivals,jvals):
        x=xa[:,i,j]
        y=ya[:,i,j]
        m,b,r,p,err=stats.linregress(x,y)
        slopes[i,j]=m
        rvals[i,j]=r
        pvals[i,j]=p

    dsout=xr.Dataset()
    for v,n in zip([slopes,rvals,pvals],['slope','rho','p']):
        dsout[n]=xr.DataArray(v,coords=la.coords)
    dsout['years']=str(y1)+'-'+str(y2)
    dsout['xvar']=v1
    dsout['yvar']=v2
    
    x=gmean(ds[v1],la).values.ravel()
    y=cf*gmean(ds[v2],la).values.ravel()
    m,b,r,p,err=stats.linregress(x,y)
    dsout['glob']=xr.DataArray([m,r,p],coords={'lm':['m','r','p']})
    dsout['mem']=ds.mem
    
    dout='/glade/scratch/djk2120/postp/'
    fout=dout+str(ds.mem.values)+'slopes.'+v2+'-'+v1+'.'+str(y1)+'-'+str(y2)+'.nc'
    
    dsout.to_netcdf(fout,unlimited_dims=['xvar','yvar','years','mem'])


f=sys.argv[1]
calc_slopes(f,'TWS','NBP',1976,1990)
