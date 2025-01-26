import httpx
from config import IMEI_API_SANDBOX_TOKEN, IMEI_API_BASE_URL


async def check_imei(imei: str) -> dict:
    """Проверяет IMEI через API imeicheck.net."""
    url = f"{IMEI_API_BASE_URL}/promo-api"
    headers = {
        "Authorization": f"Bearer {IMEI_API_SANDBOX_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"imei": imei}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Поднимает исключение при ошибке HTTP
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP ошибка: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"Произошла ошибка: {str(e)}"}
