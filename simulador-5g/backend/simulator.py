
# import numpy as np
# import math
# from umi import pathloss_umi

# #Función PRx
# def calcular_prx(ptx_dbm, pathloss_db):
#     return ptx_dbm - pathloss_db

# # Grid
# def generar_grid(radio=1000, resolucion=10):
#     puntos = []

#     for x in range(-radio, radio + 1, resolucion):
#         for y in range(-radio, radio + 1, resolucion):
#             if x**2 + y**2 <= radio**2:
#                 puntos.append((x, y))

#     return puntos


# # Conversión coordenadas
# def latlon_to_xy(lat, lon, lat_ref, lon_ref):
#     R = 111000  # metros aprox

#     x = (lon - lon_ref) * R * math.cos(math.radians(lat_ref))
#     y = (lat - lat_ref) * R

#     return x, y


# def xy_to_latlon(x, y, lat_ref, lon_ref):
#     R = 111000

#     lat = lat_ref + (y / R)
#     lon = lon_ref + (x / (R * math.cos(math.radians(lat_ref))))

#     return lat, lon


# # Función principal

# def simular(antennas, fc):
#     resultados = []

#     # referencia (primera antena)
#     # lat_ref = antennas[0]["lat"]
#     # lon_ref = antennas[0]["lon"]
#     lat_ref = sum(a["lat"] for a in antennas) / len(antennas)
#     lon_ref = sum(a["lon"] for a in antennas) / len(antennas)

#     grid = generar_grid()

#     for (x, y) in grid:

#         # convertir punto a lat/lon
#         lat, lon = xy_to_latlon(x, y, lat_ref, lon_ref)

#         mejor_prx = -9999

#         for ant in antennas:
#             tx_pos = (0, 0, ant["h"])

#             rx_x, rx_y = latlon_to_xy(lat, lon, ant["lat"], ant["lon"])
#             rx_pos = (rx_x, rx_y, 1.5)

#             pl, _ = pathloss_umi(tx_pos, rx_pos, fc)

#             prx = calcular_prx(ant["ptx"], pl)

#             if prx > mejor_prx:
#                 mejor_prx = prx

#         resultados.append({
#             "lat": lat,
#             "lon": lon,
#             "value": mejor_prx
#         })
#     print("Ejemplo:", resultados[:5])
#     return resultados

import numpy as np
import math
from umi import pathloss_umi

# ==========================
# FUNCIÓN PRx
# ==========================
def calcular_prx(ptx_dbm, pathloss_db):
    return ptx_dbm - pathloss_db


# ==========================
# GRID
# ==========================
def generar_grid(radio=1000, resolucion=10):
    puntos = []

    for x in range(-radio, radio + 1, resolucion):
        for y in range(-radio, radio + 1, resolucion):
            if x**2 + y**2 <= radio**2:
                puntos.append((x, y))

    return puntos


def generar_grid_dinamico(antennas_xy, margen=600, resolucion=15):
    xs = [a["x"] for a in antennas_xy]
    ys = [a["y"] for a in antennas_xy]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # ampliar área alrededor de antenas
    min_x -= margen
    max_x += margen
    min_y -= margen
    max_y += margen

    puntos = []

    x = min_x
    while x <= max_x:
        y = min_y
        while y <= max_y:
            puntos.append((x, y))
            y += resolucion
        x += resolucion

    return puntos


# ==========================
# CONVERSIÓN COORDENADAS
# ==========================
def latlon_to_xy(lat, lon, lat_ref, lon_ref):
    R = 111000  # metros aprox

    x = (lon - lon_ref) * R * math.cos(math.radians(lat_ref))
    y = (lat - lat_ref) * R

    return x, y


def xy_to_latlon(x, y, lat_ref, lon_ref):
    R = 111000

    lat = lat_ref + (y / R)
    lon = lon_ref + (x / (R * math.cos(math.radians(lat_ref))))

    return lat, lon


# ==========================
# FUNCIÓN PRINCIPAL
# ==========================
def simular(antennas, fc):
    resultados = []

    # 🔥 Centro del sistema (promedio)
    lat_ref = sum(a["lat"] for a in antennas) / len(antennas)
    lon_ref = sum(a["lon"] for a in antennas) / len(antennas)

    # 🔥 Convertir TODAS las antenas a XY UNA VEZ
    antennas_xy = []
    for ant in antennas:
        x, y = latlon_to_xy(ant["lat"], ant["lon"], lat_ref, lon_ref)

        antennas_xy.append({
            "x": x,
            "y": y,
            "ptx": ant["ptx"],
            "h": ant["h"]
        })

    # Generar grid
    #grid = generar_grid()
    grid = generar_grid_dinamico(antennas_xy)
    for (x, y) in grid:

        # 🔥 Punto RX en el MISMO sistema
        rx_pos = (x, y, 1.5)

        mejor_prx = -9999

        for ant in antennas_xy:

            # 🔥 TX en su posición REAL en el mismo sistema
            tx_pos = (ant["x"], ant["y"], ant["h"])

            pl, _ = pathloss_umi(tx_pos, rx_pos, fc)

            prx = calcular_prx(ant["ptx"], pl)

            if prx > mejor_prx:
                mejor_prx = prx

        # Convertir a lat/lon para frontend
        lat, lon = xy_to_latlon(x, y, lat_ref, lon_ref)

        resultados.append({
            "lat": lat,
            "lon": lon,
            "value": mejor_prx
        })

    print("Ejemplo:", resultados[:5])
    return resultados


