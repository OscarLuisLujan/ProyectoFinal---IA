import os
import sys
import pickle
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prediction_system import SistemaPriorizacion
from image_analyzer import AnalizadorImagenes
from config import CATEGORIAS_CUESTIONARIO, VARIABLES_ENTRADA

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Máximo 16MB por imagen

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

modelo_reg = None
modelo_clas = None
scaler = None
sistema = None
analizador_imagenes = None

def cargar_modelos():
    global modelo_reg, modelo_clas, scaler, sistema, analizador_imagenes
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_reg = os.path.join(base_dir, 'modelo_regresion.keras')
    path_clas = os.path.join(base_dir, 'modelo_clasificacion.keras')
    path_scaler = os.path.join(base_dir, 'scaler.pkl')

    if not (os.path.exists(path_reg) and os.path.exists(path_clas) and os.path.exists(path_scaler)):
        print("❌ Error: Archivos de modelos o scaler no encontrados. Ejecute 'main.py' primero para entrenar la red.")
        return False
    
    try:
        modelo_reg = tf.keras.models.load_model(path_reg)
        modelo_clas = tf.keras.models.load_model(path_clas)
        with open(path_scaler, 'rb') as f:
            scaler = pickle.load(f)
        
        sistema = SistemaPriorizacion(modelo_reg, modelo_clas, scaler)
        analizador_imagenes = AnalizadorImagenes()
        print("✅ Modelos y scaler cargados correctamente en Flask.")
        return True
    except Exception as e:
        print(f"❌ Error al cargar los modelos: {e}")
        return False

cargar_modelos()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if sistema is None:
        return jsonify({'error': 'Los modelos de la red neuronal no están cargados.'}), 500
    
    try:
        datos_recibidos = request.get_json()
        if not datos_recibidos:
            return jsonify({'error': 'No se enviaron datos de entrada.'}), 400
        
        datos_obra = {}
        for var in VARIABLES_ENTRADA:
            if var not in datos_recibidos:
                return jsonify({'error': f'Falta la variable requerida: {var}'}), 400
            
            try:
                datos_obra[var] = float(datos_recibidos[var])
            except ValueError:
                return jsonify({'error': f'La variable {var} debe ser un valor numérico.'}), 400

        resultado = sistema.evaluar_obra(datos_obra)
        
        nivel = resultado['nivel_riesgo']
        color = '#10b981'  
        if nivel == 'MEDIO':
            color = '#f59e0b'   
        elif nivel == 'ALTO':
            color = '#f97316'  
        elif nivel == 'CRITICO':
            color = '#ef4444'  

        resultado['color'] = color
        for key, value in resultado.items():
            if isinstance(value, (np.generic, np.ndarray)):
                if isinstance(value, np.ndarray):
                    resultado[key] = value.tolist()
                else:
                    resultado[key] = value.item()
        return jsonify(resultado)

    except Exception as e:
        return jsonify({'error': f'Ocurrió un error al procesar la predicción: {str(e)}'}), 500

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if analizador_imagenes is None:
        return jsonify({'error': 'El analizador de imágenes no está inicializado.'}), 500
        
    if 'image' not in request.files:
        return jsonify({'error': 'No se envió ninguna imagen.'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'El archivo seleccionado está vacío.'}), 400
        
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            caracteristicas_ia = analizador_imagenes.extraer_caracteristicas(filepath)
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception:
                    pass
            return jsonify(caracteristicas_ia)
        except Exception as e:
            return jsonify({'error': f'Error al analizar la imagen: {str(e)}'}), 500

if __name__ == '__main__':
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    app.run(debug=True, port=5000)
