from flask import Flask
import tensorflow as tf
from keras.models import load_model
import pickle

def create_app():
    app = Flask(__name__)

    # Загрузка модели при старте приложения
    app.model = load_model('model.h5')

    # Загрузка энкодеров
    with open('le_animal.pkl', 'rb') as f:
        app.le_animal = pickle.load(f)
    with open('le_disease.pkl', 'rb') as f:
        app.le_disease = pickle.load(f)
    with open('le_symptom.pkl', 'rb') as f:
        app.le_symptom = pickle.load(f)

    # Импортируем маршруты
    from . import routes
    app.register_blueprint(routes.bp)

    return app
