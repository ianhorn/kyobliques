#!/usr/bin/env python3

from pathlib import Path
import geopandas as gpd

eo_all_file = Path('eo-info/parquet/eo_all.parquet')

gdf = gpd.read_parquet(eo_all_file,  )