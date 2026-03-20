## 🚀 Run with Docker

1. Create a `.env` file:

AZURE_STORAGE_CONNECTION_STRING=your_connection_string


2. Pull the image:

docker pull dchacon24/mi-app-fastapi


3. Run the container:

docker run -p 8000:8000 --env-file .env dchacon24/mi-app-fastapi


4. Open in browser:

http://localhost:8000/docs
