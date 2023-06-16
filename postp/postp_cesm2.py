import xarray as xr
import numpy as np
import sys

from utils import *

file=sys.argv[1]
f = open(file, "r")
files=[x.strip() for x in f]

lfile='/glade/u/home/djk2120/TWSnbp/postp/mask_grnlnd_antarc.nc'
la=xr.open_dataset(lfile).landarea
wfile='/glade/u/home/djk2120/TWSnbp/postp/whitfull.nc'
w=xr.open_dataset(wfile)

dvs=['GPP','HR','AR','COL_FIRE_CLOSS','NPP','NEP','NBP',
          'FCTR','FCEV','FGEV','QRUNOFF','SOILWATER_10CM',
          'TLAI','FSDS','RAIN','SNOW','TWS','BTRANMN','EFLX_LH_TOT']

dout='/glade/scratch/djk2120/postp/twsnbp/'

for f in files:
    fout=dout+'cesm2.globann.'+f.split('.')[4]+'-'+f.split('.')[5]+'.'+f.split('.')[-2][:4]+'.nc'
    dsout=xr.Dataset()
    dsout.attrs={'landarea':lfile,'biomes':wfile}


    for v in [*dvs,'SW','VPD']:
        print(v)
        if v in dvs:
            das=[preprocess(xr.open_dataset(f.replace('NBP',v)))[v]]
        elif v=='SW':
            das=[get_sw(f)]
        elif v=='VPD':
            das=get_vpd(f)
            
            for da in das:
                xb=gmean(amean(da),la,w.biome)
                xg=gmean(amean(da),la)
                x=xr.concat([xg,xb],dim='biome')
                x['biome']=['Global',*w.biome_name.values]
                dsout[v]=x
                
    dsout.to_netcdf(fout,unlimited_dims='year')

