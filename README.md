# FastAPI test backend (server time)

## Запуск

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## Эндпоинты

- `GET /` — healthcheck
- `GET /time` — текущее время сервера (локальное) + UTC + unix timestamp

Пример:

```powershell
curl http://127.0.0.1:8000/time
```

