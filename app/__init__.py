# app/__init__.py
from flask import Flask
from keras.models import load_model

app = Flask(__name__)

# Загрузка модели и энкодеров
model = load_model('model.h5')
# Здесь можно добавить загрузку LabelEncoders из файлов, если они были сохранены
