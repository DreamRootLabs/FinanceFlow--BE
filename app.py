import os
import sys
import datetime
from dotenv import load_dotenv

from loguru import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.db_connector import get_firestore
from src.routers.api import api_router

# Load .env
load_dotenv()


# Logging Setup
logger.remove()
logger.add(
    sys.stderr,
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    colorize=True,
    level="INFO"
)

logger.add(
    f"logs/{datetime.datetime.now().date()}/app.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    level="DEBUG",
    rotation="10 MB",
    compression="zip",
)

logger.info("Loguru logger initialized.")


# FastAPI App

app = FastAPI(
    title="FinanceFlow API",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def init_db():
    get_firestore()
    logger.info(
        "Firestore initialized for project: {}",
        os.getenv("FIREBASE_PROJECT_ID")
    )

# Routers
app.include_router(api_router)


# Local dev run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=os.getenv("HOST_NAME"),
        port=int(os.getenv("PORT")),
        reload=True
    )
