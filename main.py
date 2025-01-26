from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from config import API_AUTH_TOKEN
from scr.imei_checker import check_imei

app = FastAPI()


def authenticate(token: str):
    """Проверяет токен авторизации."""
    if token != API_AUTH_TOKEN:
        raise HTTPException(status_code=403, detail="Недействительный токен")
    return token


class IMEICheckRequest(BaseModel):
    imei: str
    token: str


@app.post("/api/check-imei")
async def api_check_imei(request: IMEICheckRequest):
    """Обрабатывает запрос на проверку IMEI через API."""
    authenticate(request.token)
    if not request.imei.isdigit() or len(request.imei) not in [15, 16]:
        raise HTTPException(status_code=400, detail="Неверный формат IMEI")

    result = await check_imei(request.imei)
    return result
