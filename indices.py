import numpy as np
from climate_indices import compute

def calcular_spi(precipitacion_mensual):
    return compute.spi(precipitacion_mensual, scale=3, distribution="gamma")

def calcular_spei(precipitacion, evapotranspiracion):
    return compute.spei(precipitacion, evapotranspiracion, scale=3, fit_distribution="pearsoniii")
