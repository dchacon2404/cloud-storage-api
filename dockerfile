# 1️⃣ Imagen base de Python
FROM python:3.11-slim

# 2️⃣ Carpeta de trabajo dentro del contenedor
WORKDIR /app

# 3️⃣ Copiar dependencias y instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ Copiar el resto de la app
COPY . .

# 5️⃣ Exponer el puerto de FastAPI
EXPOSE 8000

# 6️⃣ Comando para correr la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]