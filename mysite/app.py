import os
import uuid
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import io
import base64

# Ya no importamos cliente.py, implementaremos la función aquí
# from cliente import aplicar_otsu

app = Flask(__name__)

# Configuración de directorios para imágenes
UPLOAD_FOLDER = os.path.join('static', 'images', 'uploads')
PROCESSED_FOLDER = os.path.join('static', 'images', 'processed')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Asegurar que las carpetas existan
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB máximo

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Implementación directa de la función aplicar_otsu
def aplicar_otsu(input_path, output_path):
    """
    Aplica el algoritmo de umbralización de Otsu a una imagen
    """
    try:
        print(f"Leyendo imagen desde: {input_path}")
        img = cv2.imread(input_path)
        
        if img is None:
            print(f"ERROR: No se pudo cargar la imagen desde {input_path}")
            return False
        
        print(f"Imagen cargada correctamente, dimensiones: {img.shape}")
        
        # Convertir a escala de grises si no lo está
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            print("Imagen convertida a escala de grises")
        else:
            gray = img
            print("La imagen ya está en escala de grises")
        
        # Aplicar el algoritmo de Otsu
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        print(f"Algoritmo de Otsu aplicado")
        
        # Guardar la imagen procesada
        result = cv2.imwrite(output_path, binary)
        if result:
            print(f"Imagen procesada guardada exitosamente en: {output_path}")
        else:
            print(f"ERROR: No se pudo guardar la imagen en {output_path}")
        
        return result
    
    except Exception as e:
        print(f"ERROR en aplicar_otsu: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

@app.route('/')
def index():
    # Lista de imágenes disponibles en el servidor
    server_images = [f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)]
    print(f"Imágenes disponibles en el servidor: {server_images}")
    return render_template('index.html', server_images=server_images)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print("No se encontró el archivo en la solicitud")
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        print("Nombre de archivo vacío")
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Generar un nombre único para evitar colisiones
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        print(f"Guardando archivo en: {filepath}")
        file.save(filepath)
        
        # Decidir qué hacer según la opción seleccionada
        option = request.form.get('option', 'server_to_client')
        print(f"Opción seleccionada: {option}")
        
        return redirect(url_for('process_image', filename=unique_filename, option=option))
    
    print("Archivo no permitido o no válido")
    return redirect(url_for('index'))

@app.route('/select_server_image', methods=['POST'])
def select_server_image():
    selected_image = request.form.get('server_image')
    option = request.form.get('option', 'server_to_client')
    
    print(f"Imagen seleccionada del servidor: {selected_image}")
    print(f"Opción seleccionada: {option}")
    
    if selected_image:
        return redirect(url_for('process_image', filename=selected_image, option=option))
    
    print("No se seleccionó ninguna imagen")
    return redirect(url_for('index'))

@app.route('/process/<filename>/<option>')
def process_image(filename, option):
    # Ruta de la imagen original
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f"Ruta de imagen original: {image_path}")
    
    # Comprobar si el archivo existe
    if not os.path.exists(image_path):
        print(f"ERROR: El archivo {image_path} no existe")
        return redirect(url_for('index'))
    
    # Ruta donde se guardará la imagen procesada
    processed_filename = f"processed_{filename}"
    processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
    print(f"Ruta donde se guardará la imagen procesada: {processed_path}")
    
    # Aplicar el algoritmo de Otsu
    success = aplicar_otsu(image_path, processed_path)
    
    if not success:
        print("ERROR: No se pudo procesar la imagen")
        return redirect(url_for('index'))
    
    # Comprobar si la imagen procesada existe
    if not os.path.exists(processed_path):
        print(f"ERROR: La imagen procesada no se creó en {processed_path}")
        return redirect(url_for('index'))
    
    # Rutas relativas para mostrar en la plantilla
    original_image = f"images/uploads/{filename}"
    processed_image = f"images/processed/{processed_filename}"
    
    print(f"Ruta de imagen original para plantilla: {original_image}")
    print(f"Ruta de imagen procesada para plantilla: {processed_image}")
    
    return render_template('result.html', 
                          original_image=original_image, 
                          processed_image=processed_image,
                          filename=processed_filename,
                          option=option)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    print(f"Descargando archivo: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"ERROR: El archivo a descargar no existe: {file_path}")
        return redirect(url_for('index'))
    
    return send_file(file_path, as_attachment=True)

@app.route('/download_original/<filename>')
def download_original_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f"Descargando imagen original: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"ERROR: El archivo original a descargar no existe: {file_path}")
        return redirect(url_for('index'))
    
    # Extraer el nombre original si tiene un prefijo UUID
    if '_' in filename:
        original_name = filename.split('_', 1)[1]  # Tomar la parte después del primer '_'
    else:
        original_name = filename
    
    return send_file(file_path, as_attachment=True, download_name=f"original_{original_name}")

if __name__ == '__main__':
    print(f"Directorio actual: {os.getcwd()}")
    print(f"Carpeta de subidas: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"Carpeta de procesados: {os.path.abspath(PROCESSED_FOLDER)}")
    app.run(debug=True)