import xarray as xr
import numpy as np
import sys
from utils import *

f=sys.argv[1]

f = open(f, "r")
fs=np.array([f.strip() for f in f.readlines()])
vs=np.array([f.split('/')[-1].split('_')[0] for f in fs ])

fout='/glade/scratch/djk2120/postp/twsnbp/mpi12.'+fs[0].split('_')[-3]+'.1976.nc'

ds=xr.Dataset()
for v in np.unique(vs):
    ds[v]=xr.open_mfdataset(fs[vs==v],combine='nested',concat_dim='time')[v].sel(time=slice('1976','1990'))


vmap={'hurs':'RH2M','mrso':'SW','nbp':'NBP','pr':'PREC','tas':'TSA'}

dsout=xr.Dataset({vmap[v]:amean(ds[v]) for v in np.unique(vs)})
x=calc_vpd(ds.tas,ds.hurs)
for x in x:
    dsout[x.name]=amean(x)

dsout.to_netcdf(fout)
