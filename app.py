from flask import Flask, render_template, request, redirect, url_for, flash
import os
from shutil import copyfile

app = Flask(__name__)

# Configuración para manejar las subidas de archivos
UPLOAD_FOLDER = 'uploads'
STATIC_UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_UPLOAD_FOLDER'] = STATIC_UPLOAD_FOLDER
app.secret_key = 'your_secret_key'  # Cambia esto por una clave segura

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No se encontró el archivo"
    file = request.files['file']
    if file.filename == '':
        return "No seleccionaste ningún archivo"
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        # Copia el archivo a /static/uploads para que sea accesible
        static_path = os.path.join(app.config['STATIC_UPLOAD_FOLDER'], file.filename)
        copyfile(filepath, static_path)
        return redirect(url_for('show_uploads'))

@app.route('/uploads')
def show_uploads():
    files = os.listdir(app.config['STATIC_UPLOAD_FOLDER'])
    file_urls = [url_for('static', filename=f'uploads/{file}') for file in files]
    return render_template('uploads.html', files=file_urls)

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
