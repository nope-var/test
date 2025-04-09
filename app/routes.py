import pickle
import pandas as pd
from flask import Blueprint, render_template, request, current_app
from keras.models import load_model
import numpy as np

bp = Blueprint('main', __name__)

# Загрузка модели и энкодеров при запуске приложения
@bp.before_app_request
def load_resources():
    current_app.model = load_model("model.h5")
    with open('le_animal.pkl', 'rb') as f:
        current_app.le_animal = pickle.load(f)
    with open('le_disease.pkl', 'rb') as f:
        current_app.le_disease = pickle.load(f)
    with open('le_symptom.pkl', 'rb') as f:
        current_app.le_symptom = pickle.load(f)

# Главная страница
@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получаем данные из формы
        animal = request.form['animal']
        age = float(request.form['age'])
        temp = float(request.form['temperature'])
        symptom1 = request.form['symptom1']
        symptom2 = request.form['symptom2']
        symptom3 = request.form['symptom3']

        try:
            # Преобразование введенных данных
            input_data = {
                'Animal': current_app.le_animal.transform([animal])[0],
                'Age': age,
                'Temperature': temp,
                'Symptom 1': safe_transform(current_app.le_symptom, symptom1),
                'Symptom 2': safe_transform(current_app.le_symptom, symptom2),
                'Symptom 3': safe_transform(current_app.le_symptom, symptom3)
            }

            input_df = pd.DataFrame([input_data])
            
            # Предсказание модели
            prediction = current_app.model.predict(input_df)
            disease_idx = np.argmax(prediction)
            disease = current_app.le_disease.inverse_transform([disease_idx])[0]
            
            return render_template('index.html', disease=disease)

        except ValueError as e:
            return render_template('index.html', disease="Error: " + str(e))
            
    return render_template('index.html', disease=None)

def safe_transform(encoder, value):
    """ Безопасно преобразует значение с помощью энкодера. Если значение не найдено,
        возвращает 0 (или другое значение по умолчанию).
    """
    try:
        return encoder.transform([value])[0]
    except ValueError:
        # Если значение не найдено, возвращаем 0 (или другое значение по умолчанию)
        return 0
