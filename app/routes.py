from flask import render_template, request
from app import app  # Импортируем объект Flask из __init__.py
from keras.src.models import load_model
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Загрузка модели
model = load_model('model.h5')

from sklearn.preprocessing import LabelEncoder

# Используем такие же энкодеры, как в десктопном приложении
le_animal = LabelEncoder()
le_disease = LabelEncoder()
le_symptom = LabelEncoder()

# Маршрут главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для предсказания
@app.route('/predict', methods=['POST'])
def predict():
    try:
        animal = request.form['animal']
        age = float(request.form['age'])
        temp = float(request.form['temp'])
        symptoms = [request.form[f'symptom{i}'] for i in range(1, 4)]

        # Преобразуем данные с использованием энкодеров
        input_data = {
            'Animal': le_animal.transform([animal])[0],
            'Age': age,
            'Temperature': temp,
            'Symptom 1': le_symptom.transform([symptoms[0]])[0] if symptoms[0] else 0,
            'Symptom 2': le_symptom.transform([symptoms[1]])[0] if symptoms[1] else 0,
            'Symptom 3': le_symptom.transform([symptoms[2]])[0] if symptoms[2] else 0
        }

        input_df = pd.DataFrame([input_data])

        # Получаем предсказание
        prediction = model.predict(input_df)
        disease_idx = prediction.argmax()
        disease = le_disease.inverse_transform([disease_idx])[0]

        return render_template('index.html', result=f"Predicted Disease: {disease}")
    except Exception as e:
        return render_template('index.html', result=f"Error: {str(e)}")

