import xarray as xr
import numpy as np
from scipy import stats
from utils import *
import sys

f=sys.argv[1]

if 'mpi' in f:
    la=xr.open_dataset('mpi_mask_grnlnd_antarc.nc').landarea
    v1='mrso'
    v2='nbp'
else:
    la=xr.open_dataset('mask_grnlnd_antarc.nc').landarea
    v1='SW'
    v2='NBP'

#load data
ds=xr.open_dataset(f)

ixys={'1960':get_ix(ds,1960,1989),
      '1989':get_ix(ds,1989,2018),
      '2073':get_ix(ds,2073,2099)}
yrs=[yr for yr in ixys]

for yr in yrs:
    print(yr)
    #detrend
    cf=24*60*60*365
    ixy=ixys[yr]
    x=detrend_dim(ds[v1].sel(year=ixy),'year')
    y=cf*detrend_dim(ds[v2].sel(year=ixy),'year')
    
    #calc slopes (only where relevant)
    ix=(x.std(dim='year')>0)&(la>0)
    ixg=ix.stack({'gc':['lat','lon']})
    xg=x.stack({'gc':['lat','lon']})
    yg=y.stack({'gc':['lat','lon']})
    mgs=[stats.linregress(x,y)[0] for x,y in zip(xg.isel(gc=ixg).T,yg.isel(gc=ixg).T)]
    
    #convert to DataArray with lat/lon coords
    mg=xr.DataArray(np.zeros(la.shape)+np.nan, coords=la.coords).stack({'gc':['lat','lon']})
    mg[ixg]=mgs
    m=mg.unstack()
    
    #write to file
    fout = f.replace('gridded', 'slopes')
    fout = fout.replace('.slopes.', '.{}.slopes.'.format(yr))
    dsout = xr.Dataset({'nbp_tws_slope':m})
    dsout['SM_variance'] = x.var(dim='year')
    dsout.to_netcdf(fout)
