import xarray as xr
import numpy as np
import sys
from utils import *

la=xr.open_dataset('mpi_mask_grnlnd_antarc.nc').landarea
latrop=la*(abs(la.lat)<24)
vmap={'hurs':'RH2M','mrso':'SW','nbp':'NBP','pr':'PREC','tas':'TSA','tlai':'TLAI','nep':'NEE'}

f=sys.argv[1]
f = open(f, "r")
fs=np.array([f.strip() for f in f.readlines()])
vs=np.array([f.split('/')[-1].split('_')[0] for f in fs ])

cfs={'NBP':1000,'NEE':-1000}
units={'NBP':'gC/m2/s','NEE':'gC/m2/s'}


dvs=['nep','mrso']
das={vmap[v]:xr.open_mfdataset(fs[vs==v],combine='by_coords')[v] for v in dvs}

if ('TSA' in das)&('RH2M' in das):
    das['VPD'],das['VP']=calc_vpd(das['TSA'],das['RH2M'])

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
    
fout='/glade/scratch/djk2120/postp/twsnbp/mpige.'+fs[0].split('_')[4][:4]+'.postp.nc'
print(fout)
ds.to_netcdf(fout)
