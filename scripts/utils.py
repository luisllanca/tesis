import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from astropy.io import fits
import gzip
import polars as pl
import os

def read_light_curves(star_type,id):
    path = os.path.join(star_type,id)
    with gzip.open(path,'rb') as f:
        with fits.open(f) as hdul:
            photometry_data = hdul[1].data
            header = hdul[1].header
            photometry_data_little_endian = np.array(photometry_data, dtype=photometry_data.dtype.newbyteorder('<'))
    df1 = pd.DataFrame(photometry_data_little_endian)
    df1['BAND'] = df1['BAND'].apply(lambda x: x.decode('utf-8').strip())
    df1 = pl.from_pandas(df1)
    df1 = df1.select(['MJD','BAND','FLUXCAL','FLUXCALERR'])
    df_polars = df1.with_columns(
        (pl.col('FLUXCAL') == -777).cast(pl.Int32).fill_null(0).cum_sum().alias('curve_id')
    )
    df_polars = df_polars.filter(pl.col('FLUXCAL') != -777)
    return df_polars