# evaluator.py
# Evaluación de modelos y métricas

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, mean_absolute_error, r2_score
from config import NIVELES_RIESGO

def evaluar_regresion(modelo, X_test, y_test):
    """Evalúa modelo de regresión"""
    y_pred = modelo.predict(X_test, verbose=0).flatten()
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n📈 Métricas de REGRESIÓN (RN29):")
    print(f"   Error Absoluto Medio (MAE): {mae:.2f} puntos")
    print(f"   Coeficiente R²: {r2:.4f}")
    
    return {'mae': mae, 'r2': r2, 'y_pred': y_pred}

def evaluar_clasificacion(modelo, X_test, y_test):
    """Evalúa modelo de clasificación"""
    y_pred_proba = modelo.predict(X_test, verbose=0)
    y_pred = np.argmax(y_pred_proba, axis=1)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n📈 Métricas de CLASIFICACIÓN:")
    print(f"   Precisión Global: {accuracy*100:.2f}%")
    
    # Obtener clases presentes
    unique_labels = np.unique(y_test)
    present_names = [NIVELES_RIESGO[i] for i in unique_labels]
    
    print("\n📊 Reporte de Clasificación:")
    print(classification_report(y_test, y_pred, target_names=present_names, labels=unique_labels))
    
    return {'accuracy': accuracy, 'y_pred': y_pred}

def plot_matriz_confusion(y_test, y_pred):
    """Genera y guarda matriz de confusión"""
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=NIVELES_RIESGO, 
                yticklabels=NIVELES_RIESGO)
    plt.title('Matriz de Confusión - Niveles de Riesgo')
    plt.xlabel('Predicción')
    plt.ylabel('Valor Real')
    plt.tight_layout()
    plt.savefig('matriz_confusion.png', dpi=100, bbox_inches='tight')
    plt.show()

def plot_curvas_entrenamiento(history_reg, history_clas):
    """Genera y guarda curvas de entrenamiento"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Curvas de regresión
    axes[0].plot(history_reg.history['loss'], label='Entrenamiento')
    axes[0].plot(history_reg.history['val_loss'], label='Validación')
    axes[0].set_title('Pérdida del Modelo de Regresión')
    axes[0].set_xlabel('Épocas')
    axes[0].set_ylabel('Pérdida (MSE)')
    axes[0].legend()
    axes[0].grid(True)
    
    # Curvas de clasificación
    axes[1].plot(history_clas.history['accuracy'], label='Entrenamiento')
    axes[1].plot(history_clas.history['val_accuracy'], label='Validación')
    axes[1].set_title('Precisión del Modelo de Clasificación')
    axes[1].set_xlabel('Épocas')
    axes[1].set_ylabel('Precisión')
    axes[1].legend()
    axes[1].grid(True)
    
    plt.tight_layout()
    plt.savefig('curvas_entrenamiento.png', dpi=100, bbox_inches='tight')
    plt.show()