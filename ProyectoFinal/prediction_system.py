import numpy as np
from config import NIVELES_RIESGO, VARIABLES_ENTRADA

class SistemaPriorizacion: 
    def __init__(self, modelo_regresion, modelo_clasificacion, scaler):
        self.modelo_regresion = modelo_regresion
        self.modelo_clasificacion = modelo_clasificacion
        self.scaler = scaler
        self.niveles = NIVELES_RIESGO
    
    def predecir(self, caracteristicas):
        caracteristicas_norm = self.scaler.transform([caracteristicas])
        
        # Regresión
        indice_riesgo = self.modelo_regresion.predict(caracteristicas_norm, verbose=0)[0][0]
        indice_riesgo = np.clip(indice_riesgo, 0, 100)
        
        # Clasificación
        prob_clases = self.modelo_clasificacion.predict(caracteristicas_norm, verbose=0)[0]
        clase = np.argmax(prob_clases)
        nivel = self.niveles[clase]
        confianza = np.max(prob_clases) * 100
        
        return indice_riesgo, nivel, confianza
    
    def calcular_prioridad(self, indice_riesgo, denuncias, observaciones):
        prioridad_base = (indice_riesgo / 100) * 8
        factor_denuncias = min(denuncias / 20, 1)
        factor_observaciones = min(observaciones / 10, 1)
        return min(10, prioridad_base + factor_denuncias + factor_observaciones)
    
    def obtener_accion(self, prioridad, nivel):
        if prioridad >= 8 or nivel == 'CRITICO':
            return {
                'accion': 'INSPECCIÓN INMEDIATA (24 horas)',
                'detalle': 'Activar protocolo de emergencia del GAMLP',
                'codigo': 4
            }
        elif prioridad >= 6 or nivel == 'ALTO':
            return {
                'accion': 'ALTA PRIORIDAD (2-3 días)',
                'detalle': 'Asignar inspector en las próximas 72 horas',
                'codigo': 3
            }
        elif prioridad >= 4 or nivel == 'MEDIO':
            return {
                'accion': 'PRIORIDAD MEDIA (1 semana)',
                'detalle': 'Programar inspección rutinaria',
                'codigo': 2
            }
        else:
            return {
                'accion': 'PRIORIDAD BAJA',
                'detalle': 'Archivar o programar inspección de bajo riesgo',
                'codigo': 1
            }
    
    def evaluar_obra(self, datos_obra, analizador_imagenes=None, ruta_foto=None):
        # Analizar imagen si existe
        if ruta_foto and analizador_imagenes:
            caracteristicas_img = analizador_imagenes.extraer_caracteristicas(ruta_foto)
            for key, value in caracteristicas_img.items():
                if key in datos_obra:
                    datos_obra[key] = value
        
        # Construir vector de características
        caracteristicas = [datos_obra[var] for var in VARIABLES_ENTRADA]
        
        # Predicciones
        indice_riesgo, nivel, confianza = self.predecir(caracteristicas)
        
        # Prioridad
        prioridad = self.calcular_prioridad(
            indice_riesgo,
            datos_obra.get('RN23_denuncias_previas', 0),
            datos_obra.get('RN24_observaciones_municipales', 0)
        )
        
        # Acción
        accion = self.obtener_accion(prioridad, nivel)
        
        return {
            'indice_riesgo': round(indice_riesgo, 2),
            'nivel_riesgo': nivel,
            'confianza': round(confianza, 2),
            'prioridad': round(prioridad, 2),
            'accion': accion['accion'],
            'detalle': accion['detalle']
        }