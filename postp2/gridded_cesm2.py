import xarray as xr
import numpy as np
import sys
import glob
from utils import *

mem=sys.argv[1]

ds=xr.Dataset()
dvs=['NBP','TSA','RAIN','SNOW','H2OSOI','RH2M']
for v in dvs:
    print(v)
    d='/glade/campaign/cgd/cesm/CESM2-LE/timeseries/lnd/proc/tseries/month_1/'+v+'/'
    m=d+'b.e21.*'+mem+'*h0*.nc'
    files=sorted(glob.glob(m))[7:]
    print('m=', m)
    print(files)
    das=[]
    
    for f in files:
        if v=='H2OSOI':
            da=amean(get_sw(f))
        else:
            tmp=fix_time(xr.open_dataset(f))
            da=amean(tmp[v])
        das.append(da)
    if v=='H2OSOI':
        v='SW'
    ds[v]=xr.concat(das,dim='year')

for v in ['area','landfrac']:
    ds[v]=tmp[v]
ds['PREC']=ds.RAIN+ds.SNOW
ds.PREC.attrs={'long_name':'Precipitation','units':'mm/s'}
s='/glade/derecho/scratch/djk2120/postp/twsnbp/cesm2/gridded/'
fout=s+f.split('370')[1].split('.')[0]+'.'+mem+'.gridded.nc'

ds.to_netcdf(fout)

