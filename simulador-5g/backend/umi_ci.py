import math

def obtener_probabilidad_los(d2d):
    """
    Probabilidad LOS según 3GPP UMi
    
    Parámetro:
        d2d (float): distancia horizontal en metros
    
    Retorna:
        float: probabilidad entre 0 y 1
    """
    if d2d <= 18:
        return 1.0
    else:
        return (18 / d2d) + math.exp(-d2d / 36) * (1 - 18 / d2d)
def fspl_1m(f_ghz):
    """
    Calcula la pérdida de espacio libre a 1 metro
    
    Parámetro:
        f_ghz (float): frecuencia en GHz
    
    Retorna:
        float: FSPL en dB
    """
    c = 3e8  # velocidad de la luz (m/s)
    f_hz = f_ghz * 1e9

    return 20 * math.log10((4 * math.pi * f_hz) / c)

import numpy as np

def calcular_path_loss_ci(d3d, f_ghz, n, sigma):
    """
    Calcula el pathloss usando modelo CI
    
    Parámetros:
        d3d (float): distancia 3D en metros
        f_ghz (float): frecuencia en GHz
        n (float): exponente de pérdida
        sigma (float): desviación estándar del shadowing
    
    Retorna:
        tuple: (pathloss_total, shadowing)
    """

    # FSPL a 1 metro
    fspl = fspl_1m(f_ghz)

    # Shadow fading
    shadowing = np.random.normal(0, sigma)

    # Fórmula CI
    pl = fspl + 10 * n * math.log10(d3d) + shadowing

    return pl, shadowing

import random

def simular_enlace_ci(d2d, h_bs, h_ut, f_ghz):
    """
    Simula un enlace 5G usando modelo CI
    
    Parámetros:
        d2d (float): distancia horizontal (m)
        h_bs (float): altura estación base (m)
        h_ut (float): altura usuario (m)
        f_ghz (float): frecuencia (GHz)
    
    Retorna:
        tuple: (pathloss, estado, shadowing)
    """

    # =========================================
    # 1. Calcular distancia 3D
    # =========================================
    d3d = math.sqrt(d2d**2 + (h_bs - h_ut)**2)

    # =========================================
    # 2. Determinar LOS / NLOS
    # =========================================
    pr_los = obtener_probabilidad_los(d2d)

    if random.random() < pr_los:
        estado = "LOS"
        n, sigma = 2.1, 4.1
    else:
        estado = "NLOS"
        n, sigma = 3.17, 8.0

    # =========================================
    # 3. Calcular pathloss
    # =========================================
    pl, shadowing = calcular_path_loss_ci(d3d, f_ghz, n, sigma)

    return pl, estado, shadowing