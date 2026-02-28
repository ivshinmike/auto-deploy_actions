# FastAPI test backend (server time)

## Запуск (локально)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Вариант 1: через uvicorn
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Вариант 2: запуск файла напрямую (читает HOST/PORT/DEBUG из окружения)
python .\main.py
```

## Переменные окружения

- `HOST` (по умолчанию `0.0.0.0`)
- `PORT` (по умолчанию `8000`)
- `DEBUG` (`true/false`, по умолчанию `false`; включает `reload` при запуске `python main.py`)

Можно положить их в `.env` рядом с `main.py`.

## Запуск (Docker)

```powershell
docker build -t time-server-api:latest .
docker run --rm -p 8000:8000 time-server-api:latest
```

## Эндпоинты

- `GET /` — приветствие
- `GET /time` — текущее время сервера (локальное) + UTC + timestamp + timezone
- `GET /datetime` — текущие дата и время сервера
- `GET /health` — healthcheck

Примеры:

```powershell
curl http://127.0.0.1:8000/time
curl http://127.0.0.1:8000/datetime
curl http://127.0.0.1:8000/health
```

