# main.py
# Archivo principal - ejecuta todo el sistema

import numpy as np
import pandas as pd
from config import RANDOM_SEED, N_MUESTRAS, EPOCHS, BATCH_SIZE
from data_generator import generar_datos_completos
from preprocessing import preprocesar_datos, dividir_datos
from models import crear_modelo_regresion, crear_modelo_clasificacion
from evaluator import evaluar_regresion, evaluar_clasificacion, plot_matriz_confusion, plot_curvas_entrenamiento
from prediction_system import SistemaPriorizacion
from questionnaire import CuestionarioTecnico
from image_analyzer import AnalizadorImagenes

# Configurar semillas
np.random.seed(RANDOM_SEED)
import tensorflow as tf
from tensorflow.keras.callbacks import ReduceLROnPlateau
tf.random.set_seed(RANDOM_SEED)

print("="*80)
print("SISTEMA INTELIGENTE PARA PRIORIZACIÓN DE INSPECCIONES")
print("MATRIZ DE RIESGO URBANO - 28 VARIABLES DE ENTRADA")
print("MUNICIPIO DE LA PAZ")
print("="*80)

# 1. Generar datos
print(f"\n📊 Generando dataset con {N_MUESTRAS} muestras...")
df = generar_datos_completos(N_MUESTRAS)
print(f"✅ Dataset generado: {len(df)} registros")

print("\n📊 Distribución de niveles de riesgo:")
print(df['nivel_riesgo'].value_counts())

# 2. Preprocesar
print("\n🔄 Preprocesando datos...")
X_scaled, y_reg, y_clas, scaler = preprocesar_datos(df)
X_train, X_test, y_train_reg, y_test_reg, y_train_clas, y_test_clas = dividir_datos(X_scaled, y_reg, y_clas)

print(f"\n📊 División de datos:")
print(f"   Entrenamiento: {len(X_train)} muestras")
print(f"   Prueba: {len(X_test)} muestras")

# 3. Crear y entrenar modelos
print("\n🧠 Creando Red Neuronal de REGRESIÓN...")
# Configurar reductor de tasa de aprendizaje (Learning Rate Scheduler)
lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6, verbose=1)

modelo_reg = crear_modelo_regresion(X_train.shape[1])
print(modelo_reg.summary())

print("\n🏋️ Entrenando modelo de regresión...")
history_reg = modelo_reg.fit(X_train, y_train_reg, validation_split=0.2, epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=[lr_scheduler], verbose=1)

print("\n🧠 Creando Red Neuronal de CLASIFICACIÓN...")
modelo_clas = crear_modelo_clasificacion(X_train.shape[1])
print(modelo_clas.summary())

print("\n🏋️ Entrenando modelo de clasificación...")
history_clas = modelo_clas.fit(X_train, y_train_clas, validation_split=0.2, epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=[lr_scheduler], verbose=1)

# 4. Evaluar modelos
print("\n" + "="*60)
print("EVALUACIÓN DE MODELOS")
print("="*60)

evaluar_regresion(modelo_reg, X_test, y_test_reg)
eval_clas = evaluar_clasificacion(modelo_clas, X_test, y_test_clas)

# 5. Visualizaciones
plot_matriz_confusion(y_test_clas, eval_clas['y_pred'])
plot_curvas_entrenamiento(history_reg, history_clas)

# Guardar los modelos entrenados y el scaler para su uso en la web
print("\n💾 Guardando modelos y scaler en disco...")
modelo_reg.save('modelo_regresion.keras')
modelo_clas.save('modelo_clasificacion.keras')
import pickle
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print("✅ Modelos y scaler guardados correctamente.")

# 6. Inicializar sistema de priorización
print("\n🚀 Inicializando Sistema de Priorización...")
sistema = SistemaPriorizacion(modelo_reg, modelo_clas, scaler)
analizador_imagenes = AnalizadorImagenes()

# 7. Mostrar cuestionario
CuestionarioTecnico.mostrar()

# 8. Predicción en vivo
print("\n" + "="*80)
respuesta = input("¿Desea realizar una predicción para una obra? (s/n): ")

if respuesta.lower() == 's':
    datos_obra = CuestionarioTecnico.recoger_datos()
    
    # Preguntar si hay foto
    ruta_foto = None
    tiene_foto = input("¿Tiene evidencia fotográfica? (s/n): ")
    if tiene_foto.lower() == 's':
        ruta_foto = input("Ingrese la ruta de la imagen: ")
    
    # Evaluar
    resultado = sistema.evaluar_obra(datos_obra, analizador_imagenes, ruta_foto)
    
    print("\n" + "="*80)
    print("📋 RESULTADO DE LA EVALUACIÓN - MUNICIPIO DE LA PAZ")
    print("="*80)
    print(f"\n🏗️ ÍNDICE DE RIESGO (RN29): {resultado['indice_riesgo']} / 100")
    print(f"⚠️ NIVEL DE RIESGO: {resultado['nivel_riesgo']}")
    print(f"🎯 CONFIANZA DEL MODELO: {resultado['confianza']}%")
    print(f"⚡ PRIORIDAD DE INSPECCIÓN: {resultado['prioridad']}/10")
    print(f"\n🚨 {resultado['accion']}")
    print(f"📋 {resultado['detalle']}")
    print("="*80)
else:
    print("\n✅ Sistema listo para implementación en el Municipio de La Paz")

print("\n✨ Sistema completado exitosamente")