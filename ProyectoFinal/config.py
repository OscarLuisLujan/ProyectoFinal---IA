import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Constantes del sistema
RANDOM_SEED = 42
N_MUESTRAS = 6000
TEST_SIZE = 0.2
VALIDATION_SPLIT = 0.2
EPOCHS = 100
BATCH_SIZE = 32

# Umbrales de clasificación
UMBRALES = {
    'BAJO': 30,
    'MEDIO': 55,
    'ALTO': 80,
    'CRITICO': 100
}

# Niveles de riesgo
NIVELES_RIESGO = ['BAJO', 'MEDIO', 'ALTO', 'CRITICO']
NIVEL_MAP = {'BAJO': 0, 'MEDIO': 1, 'ALTO': 2, 'CRITICO': 3}

# Variables de entrada (RN1 a RN28)
VARIABLES_ENTRADA = [
    'RN1_antiguedad', 'RN2_numero_pisos', 'RN3_tipo_construccion', 'RN4_estado_conservacion',
    'RN5_tamano_grietas', 'RN6_cantidad_grietas', 'RN7_evolucion_grietas', 'RN8_inclinacion_muros',
    'RN9_hundimientos', 'RN10_estado_columnas', 'RN11_filtraciones', 'RN12_humedad_visible',
    'RN13_acumulacion_agua', 'RN14_estado_drenaje', 'RN15_ubicacion_ladera', 'RN16_pendiente_terreno',
    'RN17_erosion_visible', 'RN18_historial_deslizamientos', 'RN19_excavaciones_cercanas',
    'RN20_movimiento_tierras', 'RN21_distancia_construcciones', 'RN22_densidad_edificaciones',
    'RN23_denuncias_previas', 'RN24_observaciones_municipales', 'RN25_reparaciones_realizadas',
    'RN26_grietas_IA', 'RN27_humedad_IA', 'RN28_deformacion_IA'
]

# Pesos para cálculo de riesgo (RN29) - ANTIGUO, SE DEPRECIA
PESOS_RIESGO = {
    'criticas': {
        'RN4_estado_conservacion': 6, 'RN5_tamano_grietas': 8, 'RN8_inclinacion_muros': 10,
        'RN9_hundimientos': 9, 'RN10_estado_columnas': 8
    },
    'importantes': {
        'RN6_cantidad_grietas': 5, 'RN7_evolucion_grietas': 6, 'RN11_filtraciones': 6,
        'RN15_ubicacion_ladera': 7, 'RN18_historial_deslizamientos': 6
    },
    'ia': {
        'RN26_grietas_IA': 5, 'RN27_humedad_IA': 4, 'RN28_deformacion_IA': 6
    }
}

# Pesos exactos del Cuestionario Técnico Estandarizado
MAPEO_PESOS = {
    'RN1_antiguedad': [0.0, 0.25, 0.50, 0.75, 1.00],
    'RN2_numero_pisos': [0.0, 0.25, 0.50, 0.75, 1.00],
    'RN3_tipo_construccion': [0.25, 0.75, 0.50, 1.00, 0.50],
    'RN4_estado_conservacion': [0.0, 0.25, 0.50, 0.75, 1.00],
    'RN5_tamano_grietas': [0.0, 0.05, 0.20, 0.50, 0.85, 1.00],
    'RN6_cantidad_grietas': [0.0, 0.15, 0.45, 0.80, 1.00],
    'RN7_evolucion_grietas': [0.0, 0.15, 0.35, 0.60, 0.85, 1.00],
    'RN8_inclinacion_muros': [0.0, 0.05, 0.20, 0.45, 0.70, 0.90, 1.00],
    'RN9_hundimientos': [0.0, 0.20, 0.60, 0.90, 1.00],
    'RN10_estado_columnas': [0.0, 0.10, 0.40, 0.80, 1.00],
    'RN11_filtraciones': [0.0, 0.10, 0.30, 0.55, 0.85, 1.00],
    'RN12_humedad_visible': [0.0, 0.15, 0.40, 0.75, 1.00],
    'RN13_acumulacion_agua': [0.0, 0.05, 0.20, 0.45, 0.75, 1.00],
    'RN14_estado_drenaje': [0.0, 0.15, 0.45, 0.80, 1.00],
    'RN15_ubicacion_ladera': [0.0, 0.15, 0.45, 0.75, 1.00],
    'RN16_pendiente_terreno': [0.0, 0.05, 0.20, 0.40, 0.65, 0.85, 1.00],
    'RN17_erosion_visible': [0.0, 0.20, 0.40, 0.60, 0.80, 1.00],
    'RN18_historial_deslizamientos': [0.0, 0.20, 0.40, 0.60, 0.80, 1.00],
    'RN19_excavaciones_cercanas': [0.0, 0.25, 0.50, 0.75, 1.00],
    'RN20_movimiento_tierras': [0.0, 0.25, 0.50, 0.75, 1.00],
    'RN21_distancia_construcciones': [0.0, 0.25, 0.50, 0.75, 1.00],
    'RN22_densidad_edificaciones': [0.0, 0.25, 0.50, 0.75, 1.00],
    'RN23_denuncias_previas': [0.0, 0.25, 0.50, 0.75, 1.00],
    'RN24_observaciones_municipales': [0.0, 0.25, 0.50, 0.75, 1.00],
    'RN25_reparaciones_realizadas': [0.0, 0.20, 0.40, 0.60, 0.80, 1.00],
    'RN26_grietas_IA': [0.0, 0.20, 0.40, 0.60, 0.80, 1.00],
    'RN27_humedad_IA': [0.0, 0.20, 0.40, 0.60, 0.80, 1.00],
    'RN28_deformacion_IA': [0.0, 0.20, 0.40, 0.60, 0.80, 1.00]
}


# Categorías del cuestionario
CATEGORIAS_CUESTIONARIO = {
    "Información General": ["RN1_antiguedad", "RN2_numero_pisos", "RN3_tipo_construccion", "RN4_estado_conservacion"],
    "Estado Estructural": ["RN5_tamano_grietas", "RN6_cantidad_grietas", "RN7_evolucion_grietas", 
                           "RN8_inclinacion_muros", "RN9_hundimientos", "RN10_estado_columnas"],
    "Humedad y Drenaje": ["RN11_filtraciones", "RN12_humedad_visible", "RN13_acumulacion_agua", "RN14_estado_drenaje"],
    "Terreno": ["RN15_ubicacion_ladera", "RN16_pendiente_terreno", "RN17_erosion_visible", "RN18_historial_deslizamientos"],
    "Entorno Constructivo": ["RN19_excavaciones_cercanas", "RN20_movimiento_tierras", 
                             "RN21_distancia_construcciones", "RN22_densidad_edificaciones"],
    "Historial Administrativo": ["RN23_denuncias_previas", "RN24_observaciones_municipales", "RN25_reparaciones_realizadas"],
    "Análisis IA": ["RN26_grietas_IA", "RN27_humedad_IA", "RN28_deformacion_IA"]
}