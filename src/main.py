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
    <h2><a href="http://127.0.0.1:8001/docs">Documentation</a><br></h2>
    <h2><a href="http://127.0.0.1:8001/redoc">ReDoc</a></h2>
    """


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
