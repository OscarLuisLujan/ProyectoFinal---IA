# data_generator.py
# Generación de datos sintéticos balanceados con las 28 variables
import numpy as np
import pandas as pd
from config import RANDOM_SEED, UMBRALES, VARIABLES_ENTRADA, MAPEO_PESOS

np.random.seed(RANDOM_SEED)

def generar_datos_completos(n_muestras=10000):
    """Genera dataset sintético usando exactamente las categorías y pesos del cuestionario"""
    data_list = []
    muestras_por_grupo = n_muestras // 4
    
    for grupo in ['bajo', 'medio', 'alto', 'critico']:
        n = muestras_por_grupo
        group_data = {}
        
        for var in VARIABLES_ENTRADA:
            num_cats = len(MAPEO_PESOS[var])
            if grupo == 'bajo':
                max_cat = max(1, num_cats // 3)
                group_data[var] = np.random.randint(0, max_cat + 1, n)
            elif grupo == 'medio':
                min_cat = max(0, num_cats // 4)
                max_cat = max(min_cat + 1, int(num_cats * 0.6))
                group_data[var] = np.random.randint(min_cat, max_cat + 1, n)
            elif grupo == 'alto':
                min_cat = num_cats // 2
                max_cat = num_cats - 1
                group_data[var] = np.random.randint(min_cat, max_cat + 1, n)
            else: # critico
                min_cat = max(num_cats - 2, 0)
                max_cat = num_cats - 1
                group_data[var] = np.random.randint(min_cat, max_cat + 1, n)
                
        # Simular correlación de la IA con la realidad (con algo de ruido)
        group_data['RN26_grietas_IA'] = np.clip(group_data['RN5_tamano_grietas'] + np.random.choice([-1, 0, 1], n, p=[0.1, 0.8, 0.1]), 0, len(MAPEO_PESOS['RN26_grietas_IA'])-1)
        # Humedad IA map (RN11 is 6 levels, RN27 is 6 levels)
        group_data['RN27_humedad_IA'] = np.clip(group_data['RN11_filtraciones'] + np.random.choice([-1, 0, 1], n, p=[0.1, 0.8, 0.1]), 0, len(MAPEO_PESOS['RN27_humedad_IA'])-1)
        # Deformacion IA map (RN8 is 7 levels, RN28 is 6 levels -> might need mapping, but let's just use clip)
        group_data['RN28_deformacion_IA'] = np.clip(group_data['RN8_inclinacion_muros'] + np.random.choice([-1, 0, 1], n, p=[0.1, 0.8, 0.1]), 0, len(MAPEO_PESOS['RN28_deformacion_IA'])-1)
        
        df_group = pd.DataFrame(group_data)
        data_list.append(df_group)
        
    df = pd.concat(data_list, ignore_index=True)
    
    # Calcular RN29 como suma normalizada de pesos
    riesgo_score = np.zeros(n_muestras, dtype=float)
    
    for var in VARIABLES_ENTRADA:
        pesos_var = MAPEO_PESOS[var]
        pesos_array = np.array([pesos_var[i] for i in df[var].values])
        riesgo_score += pesos_array
        
    # El máximo puntaje posible si todas las variables tienen w=1.0 es 28
    riesgo_score = (riesgo_score / 28.0) * 100.0
    
    df['RN29_indice_riesgo'] = riesgo_score
    
    # Clasificación en niveles
    nivel_riesgo = []
    for score in riesgo_score:
        if score < UMBRALES['BAJO']:
            nivel_riesgo.append('BAJO')
        elif score < UMBRALES['MEDIO']:
            nivel_riesgo.append('MEDIO')
        elif score < UMBRALES['ALTO']:
            nivel_riesgo.append('ALTO')
        else:
            nivel_riesgo.append('CRITICO')
            
    df['nivel_riesgo'] = nivel_riesgo
    
    return df