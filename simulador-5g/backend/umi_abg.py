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


import numpy as np

def calcular_path_loss_abg(d3d, f_ghz, alpha, beta, gamma, sigma):
    """
    Calcula el pathloss usando modelo ABG
    
    Parámetros:
        d3d (float): distancia 3D en metros
        f_ghz (float): frecuencia en GHz
        alpha, beta, gamma (float): coeficientes ABG
        sigma (float): desviación estándar del shadow fading
    
    Retorna:
        tuple: (pathloss_total, shadowing)
    """

    # Shadow fading (componente aleatoria)
    shadowing = np.random.normal(0, sigma)

    # Fórmula ABG
    pl = (
        10 * alpha * math.log10(d3d)
        + beta
        + 10 * gamma * math.log10(f_ghz)
        + shadowing
    )

    return pl, shadowing

import random

def simular_enlace_5g(d2d, h_bs, h_ut, f_ghz):
    """
    Simula un enlace 5G usando modelo ABG
    
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
        alpha, beta, gamma, sigma = 2.1, 31.4, 2.1, 2.9
    else:
        estado = "NLOS"
        alpha, beta, gamma, sigma = 3.73, -12.5, 3.06, 7.6

    # =========================================
    # 3. Calcular pathloss
    # =========================================
    pl, shadowing = calcular_path_loss_abg(
        d3d, f_ghz, alpha, beta, gamma, sigma
    )

    return pl, estado, shadowing