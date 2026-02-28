import os
from datetime import datetime, timezone

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI(
    title="Time Server API",
    description="Простое API для получения текущего времени сервера",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "message": "Добро пожаловать в Time Server API! Используйте /time для получения текущего времени."
    }


@app.get("/time")
async def get_current_time():
    current_time = datetime.now().astimezone()
    utc_now = current_time.astimezone(timezone.utc)
    return {
        "current_time": current_time.isoformat(),
        "utc_time": utc_now.isoformat(),
        "timestamp": utc_now.timestamp(),
        "formatted_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": str(current_time.tzinfo),
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "false").lower() == "true"

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
    )

