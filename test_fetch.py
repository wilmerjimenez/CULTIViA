from data_fetch import fetch_open_meteo_data
from db import guardar_dato
from datetime import datetime
import random

# Quito: lat, lon
data = fetch_open_meteo_data(-0.1807, -78.4678, '2025-05-01', '2025-05-03')

# Simula SPI/SPEI con valores aleatorios para la prueba
for i in range(len(data['hourly']['time'])):
    fecha = data['hourly']['time'][i]
    temp = data['hourly']['temperature_2m'][i]
    precip = data['hourly']['precipitation'][i]
    humedad = data['hourly']['relative_humidity_2m'][i]
    spi = round(random.uniform(-2, 2), 2)
    spei = round(random.uniform(-2, 2), 2)
    alerta = "crítica" if spi < -1.5 else ""
    guardar_dato(fecha, temp, precip, humedad, spi, spei, alerta)
