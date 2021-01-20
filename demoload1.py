"""
demo loading COG from cloud bucket either AWS or GCS

building a demo PySTAC catalog

- https://pystac.readthedocs.io/en/latest/tutorials/how-to-create-stac-catalogs.html
- https://creodias.eu/forum/-/message_boards/message/89497
- https://gdal.org/user/virtual_file_systems.html

"""

# AWS S3 credentials in boto3 config enabled and session can be instantiated

import boto3

import pystac
from pystac import STAC_IO

from urllib.parse import urlparse
import requests

import os
import json
from datetime import datetime

import rasterio

# from rasterio.session import AWSSession

import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, box, mapping


def my_read_method(uri):
    parsed = urlparse(uri)
    if parsed.scheme == "s3":
        bucket = parsed.netloc
        key = parsed.path[1:]
        s3 = boto3.resource("s3")
        obj = s3.Object(bucket, key)
        return obj.get()["Body"].read().decode("utf-8")
    else:
        return STAC_IO.default_read_text_method(uri)


def my_read_method2(uri):
    parsed = urlparse(uri)
    if parsed.scheme.startswith("http"):
        return requests.get(uri).text
    else:
        return STAC_IO.default_read_text_method(uri)


def my_write_method(uri, txt):
    parsed = urlparse(uri)
    if parsed.scheme == "s3":
        bucket = parsed.netloc
        key = parsed.path[1:]
        s3 = boto3.resource("s3")
        s3.Object(bucket, key).put(Body=txt)
    else:
        STAC_IO.default_write_text_method(uri, txt)


# # AWS_HTTPS='YES', AWS_VIRTUAL_HOSTING='FALSE'
# def get_bbox_and_footprint_aws(raster_uri):
#
#     with rasterio.Env(
#         AWSSession(session),
#         AWS_S3_ENDPOINT="storage.googleapis.com",
#         GDAL_CACHEMAX=1024,
#     ) as env:
#         with rasterio.open(raster_uri, "r") as ds:
#             bounds = ds.bounds
#             footprint = Polygon(
#                 [
#                     [bounds.left, bounds.bottom],
#                     [bounds.left, bounds.top],
#                     [bounds.right, bounds.top],
#                     [bounds.right, bounds.bottom],
#                 ]
#             )
#
#             est_geo = gpd.GeoDataFrame(
#                 pd.DataFrame({"geometry": [footprint]}),
#                 geometry="geometry",
#                 crs="EPSG:3301",
#             )
#             wgs84_geo = est_geo.to_crs("EPSG:4326")
#
#             wgs84_bounds = wgs84_geo.total_bounds.tolist()
#             wgs84_footprint = wgs84_geo.loc[0, "geometry"]
#
#             return (wgs84_bounds, mapping(wgs84_footprint))


def get_bbox_and_footprint_gcs(raster_uri):

    print(f"Loading {raster_uri}")
    try:
        with rasterio.open(raster_uri, "r") as ds:
            bounds = ds.bounds
            footprint = Polygon(
                [
                    [bounds.left, bounds.bottom],
                    [bounds.left, bounds.top],
                    [bounds.right, bounds.top],
                    [bounds.right, bounds.bottom],
                ]
            )

            est_geo = gpd.GeoDataFrame(
                pd.DataFrame({"geometry": [footprint]}),
                geometry="geometry",
                crs="EPSG:3301",
            )
            wgs84_geo = est_geo.to_crs("EPSG:4326")

            wgs84_bounds = wgs84_geo.total_bounds.tolist()
            wgs84_footprint = wgs84_geo.loc[0, "geometry"]

            return (wgs84_bounds, mapping(wgs84_footprint))
    except Exception as err:
        print(f"ERROR loading {raster_uri}")
        print(err)


if __name__ == "__main__":

    # array([ 365000., 6335000.,  765000., 6635000.])
    ESTONIA_EXTENT = pystac.SpatialExtent(
        bboxes=[[21.62436849, 57.10738332, 28.71945853, 59.851432]]
    )

    TEMPORAL_EXTENT = pystac.TemporalExtent(
        intervals=[
            [
                datetime.fromisoformat("2020-01-20T12:00:00+03:00"),
                datetime.fromisoformat("2021-02-20T12:00:00+03:00"),
            ]
        ]
    )

    MAAAMET_PROVIDER = pystac.Provider(
        name="Land Board Estonia",
        description="Land Board Estonia - Maa-Amet, provider of the source datasets 5m DEM grids, 4m CHM lidar grids, the soilmap of Estonia, ETAK topographic database, adminstrative units, under Estonian Landboard Open Data License (https://geoportaal.maaamet.ee/docs/Avaandmed/Licence-of-open-data-of-Estonian-Land-Board.pdf)",
        roles=["licensor", "producer"],
        url="https://www.maaamet.ee/en",
    )

    LANDSCAPEGEO_PROVIDER = pystac.Provider(
        name="Landscape Geoinformatics",
        description="Landscape Geoinformatics Lab, University of Tartu, Estonia, produced all derived products, mosaics",
        roles=["licensor", "producer", "processor", "host"],
        url="https://landscape-geoinformatics.ut.ee",
    )

    collections = [
        "dem_5m_pzone",
        "slope_5m_pzone",
        "flowacc_5m_pzone",
        "flowlength_5m_pzone",
        "ls_faktor5m_pzone",
        "estsoil_labeled_pzone",
        "buffer_size_default_pzone",
        "specific_slopenlength_default_pzone",
        "buffer_size_with_log_pzone",
        "specific_slopenlength_with_log_pzone",
        "buffer_size_with_log_interp250m_pzone",
        "chm_5m_pzone",
        "twi_5m_pzone",
        "tri_5m_pzone",
    ]

    # session = boto3.session.Session()
    # s3_client = session.client(service_name="s3", endpoint_url="storage.googleapis.com")
    # print(s3_client.list_buckets())

    # STAC_IO.read_text_method = my_read_method
    # STAC_IO.read_text_method = my_read_method2
    # STAC_IO.write_text_method = my_write_method

    catalog = pystac.Catalog(
        id="est-topo-mtr",
        title="Landscape Geoinformatics Estonian topographic variables",
        description="GeoTiff catalog for 5m Estonian topographic and terrain data.",
    )

    count = 22

    BUCKET = "geo-assets"

    collections_handles = []

    for idx, coll in enumerate(collections):

        collection1 = pystac.Collection(
            id=coll,
            description=f"{coll.replace('_pzone', '')} in 22 mosaic processing zones",
            extent=pystac.Extent(spatial=ESTONIA_EXTENT, temporal=TEMPORAL_EXTENT),
            title="Landboard Estonain 5m DEM COG Mosaic in 22 processing zones by Landscape Geoinformatics, UT",
            license="Creative Commons Attribution 4.0 International (CC BY 4.0) https://creativecommons.org/licenses/by/4.0/",
            keywords=["DEM"],
            providers=[LANDSCAPEGEO_PROVIDER, MAAAMET_PROVIDER],
            properties=None,
            summaries=None,
        )

        collections_handles.append(collection1.clone())
        del collection1

        catalog.add_child(collections_handles[idx])
        collections_handles[idx].set_parent(catalog)

        # demo img_path
        # https://storage.googleapis.com/geo-assets/est-topo-mtr/dem_5m_pzone_10_cog.tif

        for i in range(1, count + 1):

            KEY = f"est-topo-mtr/{coll}/{coll}_{i}_cog.tif"

            GCS_TARGET = "/vsigs/{}/{}".format(BUCKET, KEY)

            bbox, footprint = get_bbox_and_footprint_gcs(GCS_TARGET)
            print(bbox)
            print(footprint)

            item = pystac.Item(
                id=f"{coll}_{i}_cog",
                geometry=footprint,
                bbox=bbox,
                datetime=datetime.fromisoformat(
                    "2021-01-20T12:00:00+03:00"
                ),  # datetime.utcnow(),
                properties={},
                collection=collections_handles[idx],
            )

            item.add_asset(
                key="image",
                # title=f"{collections[0]}_10_cog.tif",
                asset=pystac.Asset(
                    href="https://storage.googleapis.com/{}/{}".format(BUCKET, KEY),
                    roles=["data"],
                    media_type=pystac.MediaType.COG,
                ),
            )

            collections_handles[idx].add_item(item)

            # break
            # print(json.dumps(item.to_dict(), indent=4))

        # break
        # print(json.dumps(collection1.to_dict(), indent=4))

    catalog.normalize_hrefs("https://storage.googleapis.com/geo-assets/est-topo-mtr")

    catalog.normalize_and_save(
        root_href="est-topo-mtr-stac",
        catalog_type=pystac.CatalogType.SELF_CONTAINED,
    )

    print("### ---- summary hrefs")
    print(catalog.describe())

    print("### ---- dump catalog")
    print(json.dumps(catalog.to_dict(), indent=4))
    print("### ---- dump collection")
    print(json.dumps(collections_handles[0].to_dict(), indent=4))
    print("### ---- dump item")
    print(json.dumps(item.to_dict(), indent=4))
