import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
import joblib
import os

# Загрузка данных
data = pd.read_csv("animal_disease_dataset.csv")

# Предобработка данных
def preprocess_data(data):
    df = data.copy()

    # Кодируем категориальные признаки
    le_animal = LabelEncoder()
    le_disease = LabelEncoder()
    df['Animal'] = le_animal.fit_transform(df['Animal'])
    df['Disease'] = le_disease.fit_transform(df['Disease'])

    # Кодируем симптомы
    all_symptoms = set()
    for col in ['Symptom 1', 'Symptom 2', 'Symptom 3']:
        all_symptoms.update(df[col].unique())

    le_symptom = LabelEncoder()
    le_symptom.fit(list(all_symptoms))

    return df, le_animal, le_disease, le_symptom

df, le_animal, le_disease, le_symptom = preprocess_data(data)

# Разделение данных
X = df.drop("Disease", axis=1)
y = to_categorical(df['Disease'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Построение нейронной сети
model_file = "model.h5"
if not os.path.exists(model_file):
    model = Sequential([
        Dense(64, activation='relu', input_shape=(X.shape[1],)),
        Dense(64, activation='relu'),
        Dense(y.shape[1], activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Обучение
    model.fit(X_train, y_train, epochs=50, batch_size=16, validation_split=0.1)

    # Сохранение
    model.save(model_file)
else:
    model = load_model(model_file)

# Сохраняем энкодеры
joblib.dump(le_animal, 'le_animal.pkl')
joblib.dump(le_disease, 'le_disease.pkl')
joblib.dump(le_symptom, 'le_symptom.pkl')

# Проверка точности
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Neural Network Accuracy: {accuracy * 100:.2f}%")
