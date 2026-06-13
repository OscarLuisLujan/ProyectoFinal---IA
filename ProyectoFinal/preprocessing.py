import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from config import VARIABLES_ENTRADA, NIVEL_MAP, TEST_SIZE, RANDOM_SEED

def preprocesar_datos(df):    
    # Seleccionar características
    X = df[VARIABLES_ENTRADA].values
    # Variable objetivo regresión
    y_regresion = df['RN29_indice_riesgo'].values
    # Variable objetivo clasificación
    y_clasificacion = df['nivel_riesgo'].map(NIVEL_MAP).values
    # Normalizar
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y_regresion, y_clasificacion, scaler

def dividir_datos(X, y_reg, y_clas):
    return train_test_split(
        X, y_reg, y_clas, 
        test_size=TEST_SIZE, 
        random_state=RANDOM_SEED, 
        stratify=y_clas
    )