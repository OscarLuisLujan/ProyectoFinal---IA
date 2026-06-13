import numpy as np
import pandas as pd
from config import RANDOM_SEED, N_MUESTRAS, EPOCHS, BATCH_SIZE
from data_generator import generar_datos_completos
from preprocessing import preprocesar_datos, dividir_datos
from models import crear_modelo_regresion, crear_modelo_clasificacion
import tensorflow as tf
from tensorflow.keras.callbacks import ReduceLROnPlateau
import pickle

np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)

print('Generando datos...')
df = generar_datos_completos(10000)

print('Preprocesando...')
X_scaled, y_reg, y_clas, scaler = preprocesar_datos(df)
X_train, X_test, y_train_reg, y_test_reg, y_train_clas, y_test_clas = dividir_datos(X_scaled, y_reg, y_clas)

lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6, verbose=1)

print('Entrenando Regresion...')
modelo_reg = crear_modelo_regresion(X_train.shape[1])
modelo_reg.fit(X_train, y_train_reg, validation_split=0.2, epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=[lr_scheduler], verbose=1)
modelo_reg.save('modelo_regresion.keras')

print('Entrenando Clasificacion...')
modelo_clas = crear_modelo_clasificacion(X_train.shape[1])
modelo_clas.fit(X_train, y_train_clas, validation_split=0.2, epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=[lr_scheduler], verbose=1)
modelo_clas.save('modelo_clasificacion.keras')

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print('Entrenamiento Finalizado Exitosamente.')
