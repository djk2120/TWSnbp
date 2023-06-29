import xarray as xr
import numpy as np
import sys
from utils import *

f=sys.argv[1]

f = open(f, "r")
fs=[f.strip() for f in f.readlines()]
dsout=xr.Dataset()
for v in ['SW1M','Vcmx25Z','TLAI','GPP','HR','AR','COL_FIRE_CLOSS','NPP','NEP','NBP','TWS','SW','RAIN','SNOW','FSDS','FSDSVI','SNOWDP','TG']:
    if v=='SW':
        da=xr.concat([get_sw(f) for f in fs],dim='time')
    elif v=='SW1M':
        da=xr.concat([get_sw1m(f) for f in fs],dim='time')
    else:
        files=[f.replace('NBP',v) for f in fs]
        da=xr.concat([preprocess(xr.open_dataset(f))[v] for f in files],dim='time')

    dsout[v]=amean(da.sel(time=slice('1976','1990')))

rh2m=xr.concat([preprocess(xr.open_dataset(f.replace('NBP','RH2M')))['RH2M'] for f in fs],dim='time')
tsa=xr.concat([preprocess(xr.open_dataset(f.replace('NBP','TSA')))['TSA'] for f in fs],dim='time')

dsout['TSA']=amean(tsa.sel(time=slice('1976','1990')))
dsout['RH2M']=amean(rh2m.sel(time=slice('1976','1990')))
dsout['PREC']=dsout['RAIN']+dsout['SNOW']

x=calc_vpd(tsa,rh2m)
for x in x:
    dsout[x.name]=amean(x.sel(time=slice('1976','1990')))

dout='/glade/scratch/djk2120/postp/twsnbp/'
fout=dout+files[0].split('g17.')[1].split('.clm2')[0]+'.amean.1976-1990.nc'
dsout.to_netcdf(fout)
