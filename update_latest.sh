#!/bin/bash

# SOURCE_DIR=/media/rocket_gis/kmoch/nomograph/chm_zones
# TPS=chm_5m_pzone
# TP_DIR=chm_zones

SOURCE_DIR=/media/rocket_gis/kmoch/nomograph/soil_prep
TPS=slope_5m_pzone
TP_DIR=slope_5m_pzone

# for i in $(seq 1 22); do
#
#     FROM_TIF=${SOURCE_DIR}/${TPS}_${i}.tif
#     COGNAME=${TPS}_${i}_cog.tif
#     TMP_COG=/tmp/${COGNAME}
#
#     rio cogeo create -p LZW $FROM_TIF $TMP_COG
#
#     gsutil cp $TMP_COG gs://geo-assets/est-topo-mtr/${TP_DIR}/
#
#     rio cogeo validate gs://geo-assets/est-topo-mtr/${TP_DIR}/${COGNAME}
#
#     if [ $? -eq 0 ]; then
#         echo "ok"
#         rm $TMP_COG
#     else
#         echo "NOT UPLOADED CORRECTLY "
#     fi
# done

# for TP_DIR in buffer_size_default_pzone specific_slopenlength_default_pzone buffer_size_with_log_pzone specific_slopenlength_with_log_pzone buffer_size_with_log_interp250m_pzone; do
#     SOURCE_DIR=/media/rocket_gis/kmoch/nomograph/tests/v4
#     TPS=$TP_DIR
#     # TP_DIR=buffer_size_default_pzone
#
#     for i in $(seq 1 22); do
#
#         FROM_TIF=${SOURCE_DIR}/${TPS}_${i}.tif
#         COGNAME=${TPS}_${i}_cog.tif
#         TMP_COG=/tmp/${COGNAME}
#
#         rio cogeo create -p LZW $FROM_TIF $TMP_COG
#
#         gsutil cp $TMP_COG gs://geo-assets/est-topo-mtr/${TP_DIR}/
#
#         rio cogeo validate gs://geo-assets/est-topo-mtr/${TP_DIR}/${COGNAME}
#
#         if [ $? -eq 0 ]; then
#             echo "ok"
#             rm $TMP_COG
#         else
#             echo "NOT UPLOADED CORRECTLY "
#         fi
#     done
#
# done

SOURCE_DIR=/media/rocket_gis/HannaIngrid/saga_TWI_5m/TWI
TPS=twi_5m_pzone
TP_DIR=twi_5m_pzone

for i in $(seq 1 22); do

    FROM_TIF=${SOURCE_DIR}/${TPS}_${i}.tif
    COGNAME=${TPS}_${i}_cog.tif
    TMP_COG=/tmp/${COGNAME}

    rio cogeo create -p LZW $FROM_TIF $TMP_COG

    gsutil cp $TMP_COG gs://geo-assets/est-topo-mtr/${TP_DIR}/

    rio cogeo validate gs://geo-assets/est-topo-mtr/${TP_DIR}/${COGNAME}

    if [ $? -eq 0 ]; then
        echo "ok"
        rm $TMP_COG
    else
        echo "NOT UPLOADED CORRECTLY "
    fi
done

SOURCE_DIR=/media/rocket_gis/HannaIngrid/TRI_5m
TPS=tri_5m_pzone
TP_DIR=tri_5m_pzone

for i in $(seq 1 22); do

    FROM_TIF=${SOURCE_DIR}/${TPS}_${i}.tif
    COGNAME=${TPS}_${i}_cog.tif
    TMP_COG=/tmp/${COGNAME}

    rio cogeo create -p LZW $FROM_TIF $TMP_COG

    gsutil cp $TMP_COG gs://geo-assets/est-topo-mtr/${TP_DIR}/

    rio cogeo validate gs://geo-assets/est-topo-mtr/${TP_DIR}/${COGNAME}

    if [ $? -eq 0 ]; then
        echo "ok"
        rm $TMP_COG
    else
        echo "NOT UPLOADED CORRECTLY "
    fi
done
