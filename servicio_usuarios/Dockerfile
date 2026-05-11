FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/servicio_usuarios

EXPOSE 8002

CMD ["python", "-m", "uvicorn", "servicio_usuarios.main:app", "--host", "0.0.0.0", "--port", "8002"]
