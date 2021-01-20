#!/bin/bash

for tps in estsoil_labeled_pzone flowacc_5m_pzone flowlength_5m_pzone ls_faktor5m_pzone; do
        for i in $(seq 1 22); do
                    gsutil mv gs://geo-assets/est-topo-mtr/${tps}_${i}_cog.tif gs://geo-assets/est-topo-mtr/${tps}/
                        done
                    done

