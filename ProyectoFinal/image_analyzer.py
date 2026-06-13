import numpy as np
import cv2
from PIL import Image

class AnalizadorImagenes:
    def cargar_imagen(self, ruta_imagen):
        try:
            img = Image.open(ruta_imagen)
            img = img.resize((224, 224))
            return np.array(img)
        except Exception as e:
            print(f"Error al cargar imagen: {e}")
            return None
    
    def analizar_grietas(self, imagen):
        """RN26"""
        if imagen is None:
            return 0
        
        if len(imagen.shape) == 3:
            gris = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
        else:
            gris = imagen
        
        bordes = cv2.Canny(gris.astype(np.uint8), 50, 150)
        densidad_bordes = np.sum(bordes > 0) / bordes.size
        
        if densidad_bordes < 0.05:
            return 0
        elif densidad_bordes < 0.15:
            return 1
        elif densidad_bordes < 0.3:
            return 2
        return 3
    
    def analizar_humedad(self, imagen):
        """RN27"""
        if imagen is None:
            return 0
        
        if len(imagen.shape) == 3:
            gris = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
        else:
            gris = imagen
        
        zonas_oscuras = np.mean(gris < 100)
        
        if zonas_oscuras < 0.1:
            return 0
        elif zonas_oscuras < 0.2:
            return 1
        elif zonas_oscuras < 0.35:
            return 2
        return 3
    
    def analizar_deformacion(self, imagen):
        """RN28"""
        if imagen is None:
            return 0
        
        if len(imagen.shape) == 3:
            gris = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
        else:
            gris = imagen
        
        bordes = cv2.Canny(gris.astype(np.uint8), 50, 150)
        lines = cv2.HoughLinesP(bordes, 1, np.pi/180, 100, minLineLength=50, maxLineGap=10)
        
        if lines is None:
            return 0
        
        angulos = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if x2 - x1 != 0:
                angulo = np.arctan((y2 - y1) / (x2 - x1)) * 180 / np.pi
                angulos.append(abs(angulo))
        
        if len(angulos) == 0:
            return 0
        
        angulo_promedio = np.mean(angulos)
        
        if angulo_promedio < 5:
            return 0
        elif angulo_promedio < 15:
            return 1
        elif angulo_promedio < 30:
            return 2
        return 3
    
    def extraer_caracteristicas(self, ruta_imagen):
        imagen = self.cargar_imagen(ruta_imagen)
        
        return {
            'RN26_grietas_IA': self.analizar_grietas(imagen),
            'RN27_humedad_IA': self.analizar_humedad(imagen),
            'RN28_deformacion_IA': self.analizar_deformacion(imagen)
        }