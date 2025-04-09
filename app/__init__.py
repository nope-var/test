from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'  # Папка для сохранения изображений
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-key')

    from .routes import main
    app.register_blueprint(main)

    return app
