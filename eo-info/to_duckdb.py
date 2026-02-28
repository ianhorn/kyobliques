#!/usr/bin/env python3

import duckdb
from pathlib import Path

with duckdb.connect('obliques.ddb') as conn:
  
    conn.sql("""
    INSTALL spatial;
    LOAD spatial;
    
    CREATE OR REPLACE TABLE eo as 
    SELECT * 
    FROM read_parquet('eo-info/parquet/eo.parquet')
    ORDER BY ID;

    CREATE OR REPLACE TABLE frames as
    SELECT * 
    FROM read_parquet('eo-info/parquet/frames.parquet')
    ORDER BY Filename;
    
    CREATE OR REPLACE TABLE centroids as
    SELECT * 
    FROM read_parquet('eo-info/parquet/frames.parquet')
    ORDER BY Filename; 

    CREATE OR REPLACE TABLE bbox as
    SELECT Filename,  bbox
    from read_parquet('eo-info/parquet/bbox.parquet');
             
    CREATE OR REPLACE table eo_all as
    SELECT
        f.Filename,
        f.geometry, 
        f.bbox,
        f.FlightTime,
        f.ShotID,
        f.CameraID,
        f.year,
        f.Season,
        f.s3url as http_url,
        e.Omega,
        e.Phi,
        e.Kappa,
        e.CamName,
        e.CamWidthPx,
        e.CamHeighPx,
        e.CamFocalMm,
        e.CamCCDResU,
        e.CamOmegaDg,
        e.CamPhiDg,
        e.CamKappaDg,
        e.CamPpxMm,
        e.CamPpyMm,
        b.bbox.xmin,
        b.bbox.ymin,
        b.bbox.xmax,
        b.bbox.ymax
    FROM
        frames as f,
        eo as e,
        bbox as b
    WHERE
        f.Filename = e.ID || '.tif'
        AND f.Filename = b.Filename
    ORDER BY f.Filename;
             
    COPY (
        SELECT * 
        FROM eo_all
        ORDER BY Filename
        ) TO ('eo-info/parquet/eo_all.parquet')
        WITH (FORMAT 'parquet');
    """
    )

