FROM python:3.13-slim

WORKDIR /opt/app

# Установка uv (альтернатива pip)
RUN pip install uv

# Копируем зависимости
COPY pyproject.toml ./

# Установка зависимостей с помощью uv
RUN uv pip install -e .

# Копируем остальные файлы
COPY . .

# Команда для запуска
CMD ["python", "main.py"]