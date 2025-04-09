from flask import Flask

app = Flask(__name__)  # Создаем объект Flask

# Импортируем маршруты после инициализации приложения
from app import routes
