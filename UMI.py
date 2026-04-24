import math
import random

# =========================================
# FUNCION: Probabilidad de LOS
# =========================================
def probabilidad_los(d2D):
    """
    Calcula la probabilidad de línea de vista (LOS)
    
    Parámetro:
        d2D (float): distancia horizontal en metros
    
    Retorna:
        float: probabilidad entre 0 y 1
    """
    if d2D <= 18:
        return 1.0
    else:
        return (18 / d2D) + math.exp(-d2D / 36) * (1 - 18 / d2D)


# =========================================
# FUNCION PRINCIPAL: Pathloss UMi
# =========================================
def pathloss_umi(tx_pos, rx_pos, fc_GHz, h_BS=10, h_UT=1.5, modo="auto"):
    """
    Calcula el pathloss según el modelo UMi - Street Canyon (3GPP)

    Parámetros:
        tx_pos (tuple): (x, y, z) de la antena
        rx_pos (tuple): (x, y, z) del usuario
        fc_GHz (float): frecuencia en GHz
        h_BS (float): altura de estación base (default 10 m)
        h_UT (float): altura del usuario (default 1.5 m)
        modo (str): "auto", "LOS" o "NLOS"

    Retorna:
        tuple: (pathloss_dB, condicion)
    """

    # =========================================
    # 1. Calcular distancias
    # =========================================
    dx = tx_pos[0] - rx_pos[0]
    dy = tx_pos[1] - rx_pos[1]
    dz = tx_pos[2] - rx_pos[2]

    d2D = math.sqrt(dx**2 + dy**2)
    d3D = math.sqrt(dx**2 + dy**2 + dz**2)

    # =========================================
    # 2. Calcular distancia de ruptura (d_BP)
    # =========================================
    c = 3e8  # velocidad de la luz (m/s)
    fc_Hz = fc_GHz * 1e9

    h_E = 1.0
    h_BS_eff = h_BS - h_E
    h_UT_eff = h_UT - h_E

    d_BP = (4 * h_BS_eff * h_UT_eff * fc_Hz) / c

    # =========================================
    # 3. Determinar condición LOS / NLOS
    # =========================================
    if modo == "LOS":
        condicion = "LOS"
    elif modo == "NLOS":
        condicion = "NLOS"
    else:
        pr_los = probabilidad_los(d2D)
        if random.random() < pr_los:
            condicion = "LOS"
        else:
            condicion = "NLOS"

    # =========================================
    # 4. Calcular Pathloss LOS
    # =========================================
    if d2D < 10:
        d2D = 10  # límite mínimo del modelo

    if d2D <= d_BP:
        PL_LOS = 32.4 + 21 * math.log10(d3D) + 20 * math.log10(fc_GHz)
    else:
        PL_LOS = (
            32.4
            + 40 * math.log10(d3D)
            + 20 * math.log10(fc_GHz)
            - 9.5 * math.log10(d_BP**2 + (h_BS - h_UT)**2)
        )

    # =========================================
    # 5. Calcular Pathloss NLOS
    # =========================================
    PL_NLOS_prime = (
        35.3 * math.log10(d3D)
        + 22.4
        + 21.3 * math.log10(fc_GHz)
        - 0.3 * (h_UT - 1.5)
    )

    PL_NLOS = max(PL_LOS, PL_NLOS_prime)

    # =========================================
    # 6. Seleccionar resultado final
    # =========================================
    if condicion == "LOS":
        return PL_LOS, condicion
    else:
        return PL_NLOS, condicion



# Posición de la antena (TX)
tx = (0, 0, 10)

# Posición del usuario (RX)
rx = (100, 0, 1.5)

# Frecuencia en GHz (ej: 3.5 GHz para 5G)
fc = 3.5

# Calcular pathloss
pl, condicion = pathloss_umi(tx, rx, fc)

print(f"Pathloss: {pl:.2f} dB")
print(f"Condición: {condicion}")
