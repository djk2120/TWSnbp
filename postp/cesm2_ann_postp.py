import sys
import xarray
from utils import *

i=int(sys.argv[1])

dout='/glade/scratch/djk2120/postp/'
dvs=['TSA','RH2M','RAIN','SNOW','GPP','HR','AR','COL_FIRE_CLOSS','NPP','NEP','NBP','TWS','SOILWATER_10CM','FCTR','FCEV','FGEV','TLAI']
data={}

for v in dvs:
    files=lens_files('CESM2',v)[i]
    ds=xr.open_mfdataset(files,combine='nested',concat_dim='time',preprocess=preprocess)
    data[v]=amean(ds[v])
    
ds=xr.Dataset(data)
mem=files[0].split('/')[-1].split('clm2')[0]
ds['mem']=mem
derived(ds)

fout=dout+mem+'ann.nc'
ds.to_netcdf(fout,unlimited_dims='mem')
