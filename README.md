# pystac GCS COG Kik project DEM topo

activate geopy2020

gdalinfo /vsicurl/https://storage.googleapis.com/geo-assets/est-topo-mtr/dem_5m_pzone_10_cog.tif


## AWS

BUCKET = "geo-assets"
KEY = "est-topo-mtr/dem_5m_pzone_10_cog.tif"

AWS_NO_SIGN_REQUEST=YES

AWS_S3_ENDPOINT=https://storage.googleapis.com

~/.aws/credentials

gdalinfo /vsis3/BUCKET/KEY

AWS_NO_SIGN_REQUEST=YES AWS_S3_ENDPOINT=storage.googleapis.com gdalinfo /vsis3/geo-assets/est-topo-mtr/dem_5m_pzone_10_cog.tif

## Google GCS

GS_SECRET_ACCESS_KEY and GS_ACCESS_KEY_ID configuration options can be set for AWS-style authentication

GOOGLE_APPLICATION_CREDENTIALS  for  service account credentials json

~/.boto

gdalinfo /vsigs/BUCKET/KEY

gdalinfo /vsigs/geo-assets/est-topo-mtr/dem_5m_pzone/dem_5m_pzone_10_cog.tif


## STAC TODO

- add COG geodata (CHM zones, buffer zones and specific slope as COG, others are already)

https://stacspec.org/

https://github.com/radiantearth/stac-browser/

Demo:

https://aoraki.domenis.ut.ee/est-topo-stac/?t=catalogs

References:

https://raw.githubusercontent.com/cholmes/sample-stac/master/stac/catalog.json

https://raw.githubusercontent.com/cholmes/sample-stac/master/stac/hurricane-harvey/0831/Houston-East-20170831-103f-100d-0f4f-RGB.json

## idea layout

Origin:

https://storage.googleapis.com/geo-assets/est-topo-mtr/catalog.json

children per type

dem_5m_pzone
estsoil_labeled_pzone
flowacc_5m_pzone
flowlength_5m_pzone
ls_faktor5m_pzone

open: CHM zones, buffer zones log / nolog / and specific slope , dem_slope as COG

R:\kmoch\nomograph\chm_zones

chm_5m_pzone

R:\kmoch\nomograph\

slope_5m_pzone

R:\kmoch\nomograph\tests\v4

buffer_size_default_pzone
specific_slopenlength_default_pzone
buffer_size_with_log_pzone
specific_slopenlength_with_log_pzone
buffer_size_with_log_interp250m_pzone


## COGEO

https://www.cogeo.org/


```bash

rio-cogeo on aoraki geopy2020 pip

make folders online

gsutil mv gs://geo-assets/est-topo-mtr/dem_5m_pzone_10_cog.tif gs://geo-assets/est-topo-mtr/

for i in ...
    https://cogeotiff.github.io/rio-cogeo/profile/
    rio cogeo create -p LZW from to
    gsutil upload


for i in ...
    gsutil list?
    rio cogeo validate /media/rocket_gis/kmoch/nomograph/soil_prep/ls_faktor5m_pzone_10_cog.tif

for tps in estsoil_labeled_pzone flowacc_5m_pzone flowlength_5m_pzone ls_faktor5m_pzone; do
    for i in $(seq 1 22); do
        gsutil mv gs://geo-assets/est-topo-mtr/${tps}_${i}_cog.tif gs://geo-assets/est-topo-mtr/${tps}/
    done
done
```
