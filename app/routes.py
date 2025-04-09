from flask import render_template, request
from keras.models import load_model
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Загрузка модели
model = load_model('model.h5')

# Инициализация лейблов (нужно будет заменить DummyEncoders на настоящие)
class DummyEncoders:
    def transform(self, values):
        return [0]  # Заглушка для кодировки

# Создание заглушек для теста
le_animal, le_disease, le_symptom = DummyEncoders(), DummyEncoders(), DummyEncoders()

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

        # Преобразуем данные
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
