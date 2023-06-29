import xarray as xr
import numpy as np
import sys
from utils import *

f=sys.argv[1]

f = open(f, "r")
fs=np.array([f.strip() for f in f.readlines()])
vs=np.array([f.split('/')[-1].split('_')[0] for f in fs ])

fout='/glade/scratch/djk2120/postp/twsnbp/mpige.'+fs[0].split('_')[-2]+'.1976.nc'

vmap={'nbp':'NBP','mrso':'SW','pr':'PREC','tas':'TSA'}
ds=xr.Dataset()
das=[xr.open_dataset(f)[v].sel(time=slice('1976','1990')) for f,v in zip(fs,vs)]
yr0=das[0]['time.year'][0].values
nt=len(das[0].time)
for da in das:
    da['time']=xr.cftime_range(str(yr0),periods=nt,freq='MS')
    if da.name=='hus':
        ds['QBOT']=da.sel(plev=1e5)
        ds['QBOT'].attrs={'units':'-'}
    else:
        ds[vmap[da.name]]=da


dsout=xr.Dataset({v:amean(ds[v]) for v in ds.data_vars})
x=calcvpdq(ds.TSA,ds.QBOT)
for x in x:
    dsout[x.name]=amean(x)

dsout.to_netcdf(fout)





