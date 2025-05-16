# SD04-02
---

# Sistema Distribuido de Procesamiento de Imágenes con Algoritmo de Otsu

Este proyecto implementa una arquitectura **cliente-servidor** en la nube utilizando **Flask** y **PythonAnywhere** para realizar operaciones de procesamiento de imágenes, específicamente aplicando el **algoritmo de umbralización de Otsu**.

## 📌 Descripción

La aplicación permite:

* Seleccionar y leer imágenes del servidor mediante una interfaz HTML.
* Aplicar el algoritmo de Otsu a las imágenes (procesamiento en el servidor).
* Enviar imágenes modificadas al servidor.

Opciones adicionales:

* Leer imagen del cliente, modificarla y enviar al servidor.
* Leer imagen del servidor, modificarla y descargar en el cliente.

---

## ✅ Requisitos

* Python 3.8 o superior
* Flask
* OpenCV (`opencv-python` o `opencv-python-headless`)
* Numpy
* Pillow (PIL)
* Cuenta en [PythonAnywhere](https://www.pythonanywhere.com) (versión gratuita funciona)

---

## 📁 Estructura del Proyecto

```
mysite/
├── app.py                   # Aplicación principal Flask
├── cliente.py               # Procesamiento de imágenes (algoritmo Otsu)
├── wsgi.py                  # Configuración WSGI para PythonAnywhere
├── static/
│   ├── css/
│   ├── js/
│   │   └── script.js        # Interacciones del cliente
│   └── images/
│       ├── uploads/         # Imágenes originales
│       └── processed/       # Imágenes procesadas
└── templates/
    ├── index.html           # Página principal
    └── result.html          # Página de resultados
```

---

## ⚙️ Instalación Local

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/procesamiento-imagenes-distribuido.git
cd procesamiento-imagenes-distribuido

# 2. Crear entorno virtual (opcional)
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate

# 3. Instalar dependencias
pip install flask opencv-python numpy pillow werkzeug

# 4. Crear carpetas necesarias
mkdir -p static/images/uploads
mkdir -p static/images/processed

# 5. Ejecutar la aplicación local
python app.py
```

Abre tu navegador en: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## ☁️ Despliegue en PythonAnywhere

### 1. Crear cuenta en PythonAnywhere

Regístrate en: [https://www.pythonanywhere.com](https://www.pythonanywhere.com)

### 2. Crear una aplicación web

* Pestaña "Web" → "Add a new web app"
* Dominio: `tuusuario.pythonanywhere.com`
* Framework: Flask
* Python 3.8 o superior
* Ruta: `/home/tuusuario/mysite`

### 3. Subir archivos

**Opción 1:** Subir manualmente desde la pestaña "Files"
**Opción 2:** Clonar desde Git:

```bash
cd ~/mysite
git clone https://github.com/tu-usuario/procesamiento-imagenes-distribuido.git .
```

**Opción 3:** Subir archivo ZIP y descomprimir:

```bash
cd ~/mysite
unzip archivo.zip
```

### 4. Instalar dependencias

```bash
pip install --user flask opencv-python-headless numpy pillow werkzeug
```

> Nota: En PythonAnywhere se recomienda `opencv-python-headless`.

### 5. Configurar archivos estáticos

En la pestaña **Web → Static files**, añade:

* **URL:** `/static/`
* **Path:** `/home/tuusuario/mysite/static/`

### 6. Crear carpetas necesarias

```bash
mkdir -p ~/mysite/static/images/uploads
mkdir -p ~/mysite/static/images/processed
chmod -R 755 ~/mysite/static
```

### 7. Configurar archivo WSGI

Haz clic en "WSGI configuration file" y reemplaza el contenido con:

```python
import sys
import os

path = '/home/tuusuario/mysite'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

### 8. Recargar la aplicación

Desde la pestaña **Web**, haz clic en **"Reload"**.

Accede a: `https://tuusuario.pythonanywhere.com`

---

## 🧠 Funcionamiento

### 🧩 Arquitectura Cliente-Servidor

* **Servidor (PythonAnywhere)**:

  * Almacenamiento de imágenes
  * Procesamiento con algoritmo de Otsu
  * Envío de resultados

* **Cliente (Navegador Web)**:

  * Subida de imágenes
  * Selección de imágenes existentes
  * Visualización/descarga de resultados

### 🔁 Flujo de Operación

1. El usuario accede a la app web
2. Sube o selecciona una imagen
3. Elige una opción de procesamiento
4. La imagen se procesa con el algoritmo de Otsu
5. Se muestra el resultado

---

## 📷 Algoritmo de Otsu

* Método automático de **umbralización**.
* Calcula el **umbral óptimo** para binarizar una imagen.
* Convierte píxeles en **blanco o negro** según el umbral.
* Útil en segmentación, reconocimiento de texto, etc.

Procesamiento realizado en el servidor usando **OpenCV**.

---

## 🛠️ Resolución de Problemas

### ❌ Imágenes no se muestran

* Verifica permisos:

```bash
chmod -R 755 ~/mysite/static
```

* Revisa configuración de archivos estáticos:

```
URL: /static/
Path: /home/tuusuario/mysite/static/
```

* Revisa rutas en el código:

```python
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'images', 'uploads')
PROCESSED_FOLDER = os.path.join(BASE_DIR, 'static', 'images', 'processed')
```

### ❌ Error con OpenCV

* Instala versión headless:

```bash
pip install --user opencv-python-headless
```

* En `cliente.py`, usa:

```python
try:
    import cv2
except ImportError:
    print("Intentando importar la versión headless de OpenCV...")
    import cv2.cv2 as cv2
```

### ❌ Rutas incorrectas

* Evita rutas de Windows (`D:\...`)
* Usa rutas Linux: `/home/tuusuario/mysite`

---

## 📚 Recursos

* [Documentación Flask](https://flask.palletsprojects.com/)
* [Documentación OpenCV](https://docs.opencv.org/)
* [Guía PythonAnywhere](https://help.pythonanywhere.com/)
* [Algoritmo de Otsu en Wikipedia](https://es.wikipedia.org/wiki/Umbralizaci%C3%B3n_de_Otsu)

---

## 👨‍💻 Autores

Este proyecto fue desarrollado como parte de la asignatura **Sistemas Distribuidos**.

**Última actualización:** Mayo 2025

---

¿Quieres que te lo convierta también en PDF o lo prepare para GitHub con badges y licencia?
