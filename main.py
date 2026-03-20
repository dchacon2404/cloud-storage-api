from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os

# 🔐 Cargar variables de entorno
load_dotenv()

app = FastAPI()

# ✅ CORS (puedes restringir en producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 Variables de entorno
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "files"

# ❗ Validación de seguridad
if not CONNECTION_STRING:
    raise ValueError("❌ Falta la variable de entorno AZURE_STORAGE_CONNECTION_STRING")

# ✅ Inicializar cliente Azure
try:
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    if not container_client.exists():
        container_client.create_container()
        print("✅ Contenedor creado")

    print("✅ Conectado a Azure correctamente")

except Exception as e:
    print("❌ Error conectando a Azure:", e)
    raise e


@app.get("/")
def home():
    return {"message": "API funcionando 🚀"}


# ☁️ SUBIR ARCHIVO
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="Nombre de archivo inválido")

        blob_client = container_client.get_blob_client(file.filename)

        data = await file.read()

        if not data:
            raise HTTPException(status_code=400, detail="Archivo vacío")

        blob_client.upload_blob(data, overwrite=True)

        file_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{file.filename}"

        return {
            "message": "Archivo subido correctamente 🚀",
            "filename": file.filename,
            "url": file_url
        }

    except HTTPException:
        raise
    except Exception as e:
        print("❌ ERROR UPLOAD:", e)
        raise HTTPException(status_code=500, detail="Error subiendo archivo")


# 📂 LISTAR ARCHIVOS
@app.get("/files/")
def list_files():
    try:
        blobs = list(container_client.list_blobs())

        files = [
            {
                "name": blob.name,
                "url": f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{blob.name}"
            }
            for blob in blobs
        ]

        return {
            "count": len(files),
            "files": files
        }

    except Exception as e:
        print("❌ ERROR LIST:", e)
        raise HTTPException(status_code=500, detail="Error obteniendo archivos")


# 🧪 TEST
@app.get("/test/")
def test():
    try:
        blobs = list(container_client.list_blobs())
        return {
            "status": "ok",
            "total_files": len(blobs)
        }
    except Exception as e:
        return {
            "status": "error",
            "detail": str(e)
        }