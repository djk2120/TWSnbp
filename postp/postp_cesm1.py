import xarray as xr
import numpy as np
import sys
from utils import *

la=xr.open_dataset('mask_grnlnd_antarc.nc').landarea
latrop=la*(abs(la.lat)<24)

f=sys.argv[1]
f = open(f, "r")
fs=np.array([f.strip() for f in f.readlines()])

dvs=['GPP','HR','AR','COL_FIRE_CLOSS','NPP','NEP','NBP','NEE',
          'FCTR','FCEV','FGEV','QRUNOFF','SOILWATER_10CM','TSA','RH2M',
          'TLAI','FSDS','RAIN','SNOW']

das={v:preprocess(xr.open_mfdataset([f.replace('NBP',v) for f in fs],combine='by_coords')[v]) for v in dvs}
p=das['RAIN']+das['SNOW']
p.attrs=das['RAIN'].attrs
p.attrs['long_name']='precipitation'
das['PREC']=p
das['VPD'],das['VP']=calc_vpd(das['TSA'],das['RH2M'])
das['SW']=get_sw(fs)

cfs={}
units={}

ds=xr.Dataset()
for v in das:
    if v in cfs:
        cf=cfs[v]
    else:
        cf=1

    da=das[v]
    x=cf*amean(da)
    ds[v]=gmean(x,la)
    ds[v+'_TROP']=gmean(x,latrop)
    
    attrs=da.attrs
    
    if v in units:
        attrs['units']=units[v]
        
    ds[v].attrs=attrs
    ds[v+'_TROP'].attrs=attrs

ds=ds.sel(year=slice('1920','2100'))    
fout='/glade/scratch/djk2120/postp/twsnbp/cesm1.'+fs[0].split('.')[4]+'.postp.nc'
ds.to_netcdf(fout)

