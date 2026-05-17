import logging
import uvicorn
import sys

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.api.auth import router as auth_router

logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.include_router(auth_router)


@app.get("/", response_class=HTMLResponse, tags=["Главная страница документации"])
def home():
    return """
    <h1>Выберите тип документации</h1>
    <h2><a href="https://booking-fastapi-project.ru/docs">Swagger UI</a><br></h2>
    <h2><a href="https://booking-fastapi-project.ru/redoc">ReDoc</a></h2>
    """


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)

