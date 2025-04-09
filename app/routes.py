from flask import Blueprint, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

# Директория для хранения изображений
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Главная страница с формой
@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Загружаем изображение
        file = request.files.get('image')
        text = request.form.get('text')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
        
        # Сохраняем текст и путь к изображению
        return render_template('index.html', filename=filename, text=text)
    
    return render_template('index.html', filename=None, text=None)

