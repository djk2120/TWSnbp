import xarray as xr
import numpy as np
import sys
from utils import *

f=sys.argv[1]
f = open(f, "r")
fs=np.array([f.strip() for f in f.readlines()])

dvs=['NEE', 'GPP', 'HR', 'AR', 'COL_FIRE_CLOSS', 'NBP',
     'FSDS', 'TSA', 'RH2M', 'RAIN', 'SNOW', 'SW']

dsout = xr.Dataset()
for v in dvs:
    print(v)
    das = []
    for f in fs:
        if v=='SW':
            f_v = f.replace('NBP', 'H2OSOI')
            da = amean(get_sw(f_v))
        else:
            f_v = f.replace('NBP', v)
            ds = fix_time(xr.open_dataset(f_v))
            da = amean(ds[v])
        das.append(da)
    da = xr.concat(das, dim='year')
    dsout[v] = da.sel(year=slice(1920, 2100))

vpd, vp = calc_vpd(dsout.TSA, dsout.RH2M)
dsout['VPD'] = vpd
dsout['VP'] = vp
dsout['PREC'] = dsout.RAIN+dsout.SNOW

fout='/glade/derecho/scratch/djk2120/postp/twsnbp/cesm1/cesm1.'+fs[0].split('.')[4]+'.gridded.nc'
dsout.to_netcdf(fout)

