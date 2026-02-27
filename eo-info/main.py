#!/usr/bin/env python3


from pathlib import Path
import geopandas as gpd
import pandas as pd


# variables
Path("eo-info/gpkg").mkdir(parents=False, exist_ok=True)
gpkg_path = Path('eo-info/gpkg')
Path("eo-info/parquet").mkdir(parents=False, exist_ok=True)
parquet_path = Path('eo-info/parquet')

# variables for the different files
eo = list(gpkg_path.glob('*ImageFrameEO.gpkg'))         # ImageFrameEO = eo
imf = list(gpkg_path.glob('*ImageFrames.gpkg'))          # ImageFrames = imf
imc = list(gpkg_path.glob('*ImageFrameCentroids.gpkg'))  # ImageFrameCentroids = imc


def merge_files(file_list: list, outfile: str):
   
    """
    This function reads a list of files and then
    merges them into one compressed parquet file
    """
    # red files into geopandas
    gdfs = [gpd.read_file(f) for f in file_list]

        # merge the files
    merged = gpd.GeoDataFrame(
        pd.concat(gdfs, ignore_index=True),
        crs=gdfs[0].crs
    )
    print(f'Merge {file_list} and writing to {outfile}.parquet')
    merged.to_parquet(f'{parquet_path}/{outfile}.parquet', 
                            compression='zstd',
                        write_covering_bbox=True)
    

def main():
    merge_files(eo, 'eo')
    merge_files(imf, 'imageframes')
    merge_files(imc, 'centroids')


if __name__ == "__main__":
    main()
    