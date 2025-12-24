import io
import json
import uvicorn
import state
from ngrok import get_ngrok_base_url
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import Response, HTMLResponse
from PIL import Image
from pydantic import ValidationError
from schemas import QRRequest
from services import process_qr_overlay
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    state.BASE_URL = get_ngrok_base_url()
    print(f"{state.BASE_URL = }")
    yield


app = FastAPI(title="QR Code Overlay API", lifespan=lifespan)


@app.post("/overlay-qr")
async def overlay_qr(image: UploadFile = File(...), payload: str = Form(...)):
    try:
        # Парсим запрос
        request = QRRequest(**json.loads(payload))

        # Читаем изображение
        image_bytes = await image.read()
        base_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Обрабатываем через сервис
        result_bytes = process_qr_overlay(base_image, request)

        return Response(content=result_bytes, media_type="image/png")

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/invite", response_class=HTMLResponse)
def invite(chat_id: int, user_id: int):
    return f"""
    <html>
      <body style="font-family: sans-serif;">
        <h2>Invite accepted ✅</h2>
        <p>chat_id: {chat_id}</p>
        <p>user_id: {user_id}</p>
      </body>
    </html>
    """


@app.get("/")
async def root():
    return {"message": "QR Code Overlay API", "docs": "/docs"}


@app.get("/help")
async def get_help():
    return {"message": "command list..."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
