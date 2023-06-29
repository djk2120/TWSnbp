import xarray as xr
import numpy as np
import sys
from utils import *

f=sys.argv[1]

dsout=xr.Dataset()
for v in ['TLAI','GPP','HR','AR','COL_FIRE_CLOSS','NPP','NEP','NBP','SW','SW1M','RAIN','SNOW','FSDS','SNOWDP','TG','FSDSVI']:
    if v=='SW':
        da=get_sw(f)
    elif v=='SW1M':
        da=get_sw1m(f)
    else:
        ds=preprocess(xr.open_dataset(f.replace('NBP',v)))
        da=ds[v]
    dsout[v]=amean(da.sel(time=slice('1976','1990')))


rh2m=preprocess(xr.open_dataset(f.replace('NBP','RH2M')))['RH2M']
tsa=preprocess(xr.open_dataset(f.replace('NBP','TSA')))['TSA']

dsout['TSA']=amean(tsa.sel(time=slice('1976','1990')))
dsout['RH2M']=amean(rh2m.sel(time=slice('1976','1990')))
dsout['PREC']=dsout['RAIN']+dsout['SNOW']

x=calc_vpd(tsa,rh2m)
for x in x:
    dsout[x.name]=amean(x.sel(time=slice('1976','1990')))




dout='/glade/scratch/djk2120/postp/twsnbp/'
fout=dout+'postp.'+f.split('.')[4]+'.amean.1976.nc'
dsout.to_netcdf(fout)
