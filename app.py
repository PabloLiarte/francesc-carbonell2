from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuración para manejar las subidas de archivos
STATIC_UPLOAD_FOLDER = 'static/uploads'
os.makedirs(STATIC_UPLOAD_FOLDER, exist_ok=True)

app.config['STATIC_UPLOAD_FOLDER'] = STATIC_UPLOAD_FOLDER
app.secret_key = 'your_secret_key'  # Cambia esto por una clave segura

@app.route('/')
def index():
    image_files = os.listdir(os.path.join(app.static_folder, 'uploads'))
    image_files.sort()  # Opcional: ordenar los archivos
    image_urls = [
        url_for('static', filename=f'uploads/{filename}')
        for filename in image_files if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
    ]
    return render_template('index.html', images=image_urls)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash("No se encontró el archivo", "error")
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash("No seleccionaste ningún archivo", "error")
        return redirect(url_for('index'))
    if file:
        from werkzeug.utils import secure_filename
        static_path = os.path.join(app.config['STATIC_UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(static_path)
        flash("Archivo subido correctamente", "success")
        return redirect(url_for('show_uploads'))

@app.route('/uploads')
def show_uploads():
    # Listar las imágenes en el directorio static/uploads
    files = os.listdir(app.config['STATIC_UPLOAD_FOLDER'])
    
    # Filtrar solo los archivos de imagen
    image_urls = [
        url_for('static', filename=f'uploads/{file}')
        for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
    ]
    
    # Depurar: Imprime las URLs generadas para las imágenes
    print("Imágenes detectadas:", image_urls)
    
    # Renderizar la plantilla uploads.html
    return render_template('uploads.html', images=image_urls)


@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    message = request.form.get('message')

    # Validar los datos
    if not name or not phone or not email or not message:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('index'))

    # Procesar los datos (ejemplo: imprimir en la consola o guardar en una base de datos)
    print(f'Nombre: {name}')
    print(f'Teléfono: {phone}')
    print(f'Correo: {email}')
    print(f'Mensaje: {message}')

    # Confirmación de envío
    flash('Formulario enviado correctamente. ¡Gracias por contactarnos!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
