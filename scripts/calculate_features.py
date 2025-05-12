import polars as pl
import turbofats
from tqdm import tqdm
import os
from utils import read_light_curves
import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

with open("dataset/4clasess.pkl","rb") as f:
    data = pkl.load(f)
feature_list = [
    "PeriodLS_v2",
    "Period_fit_v2",
    "Amplitude",
    "Rcs",
    "StetsonK",
    "Meanvariance",
    "Autocor_length",
    "SlottedA_length",
    "StetsonK_AC",
    #"StetsonL",
    "Con",
    #"Color",
    "Beyond1Std",
    "SmallKurtosis",
    "Std",
    "Skew",
    #"StetsonJ",
    "MaxSlope",
    "MedianAbsDev",
    "MedianBRP",
    "PairSlopeTrend",
    "FluxPercentileRatioMid20",
    "FluxPercentileRatioMid35",
    "FluxPercentileRatioMid50",
    "FluxPercentileRatioMid65",
    "FluxPercentileRatioMid80",
    "PercentDifferenceFluxPercentile",
    "PercentAmplitude",
    "LinearTrend",
    #"Eta_color",
    "Eta_e",
    "Mean",
    "Q31",
    #"Q31_color",
    "AndersonDarling",
    "Psi_CS_v2",
    "Psi_eta_v2",
    "Gskew",
    "StructureFunction_index_21",
    "StructureFunction_index_31",
    "StructureFunction_index_32",
    "Pvar",
    "ExcessVar",
    "PeriodPowerRate",
    "IAR_phi",
    "CIAR_phiR_beta",
    "SF_ML_amplitude",
    "SF_ML_gamma",
    "GP_DRW_sigma",
    "GP_DRW_tau",
    #"Harmonics"
]
feature_list = [
    "PeriodLS_v2",
    "Mean",
    "GP_DRW_sigma",
    "GP_DRW_tau",
    "IAR_phi",
    "Amplitude",
    "ExcessVar",
    "Meanvariance",
    "Std",
    "SF_ML_amplitude"
    ]

fs = turbofats.FeatureSpace(feature_list=feature_list)

all_features = []

for i, lc in tqdm(enumerate(data), total=len(data)):
    df = pd.DataFrame({
        "time": lc['mjd'],
        "magnitude": lc['flux'],
        "error": lc['err']
    })
    df['id'] = i
    df.set_index('id', inplace=True)

    try:
        features = fs.calculate_features(lightcurve=df)
        features['id'] = i
        all_features.append(features)
    except Exception as e:
        print(f"Error en curva {i}: {e}")


final_df = pd.concat(all_features, ignore_index=True)

final_df.to_csv("data.csv")