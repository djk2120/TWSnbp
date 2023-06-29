import xarray as xr
import numpy as np
import sys

from utils import *

f=sys.argv[1]

lfile='/glade/u/home/djk2120/TWSnbp/postp/mpi_mask_grnlnd_antarc.nc'
la=xr.open_dataset(lfile).landarea


dout='/glade/scratch/djk2120/postp/twsnbp/'
fout=dout+'mpi12.globann.'+f.split('_')[-3]+'.'+f.split('_')[-1][:4]+'.nc'

dsout=xr.Dataset()
dsout.attrs={'landarea':lfile}

da=1e3*xr.open_dataset(f).nbp
da.attrs['units']='gC/m2/s'
x=gmean(amean(da),la)
dsout['NBP']=x

da=xr.open_dataset(f.replace('nbp','mrso')).mrso
x=gmean(amean(da),la)
dsout['SW']=x

dsout.to_netcdf(fout,unlimited_dims='year')

