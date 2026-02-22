import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from sqlalchemy import text
import asyncio
from app.core.config import config
from app.api.v1.router import api_router
from app.db.session import engine
from sqlalchemy.exc import OperationalError
from app.core.constants import MAX_DB_RETRIES

# -------------------------
# Logging Configuration
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


# -------------------------
# Lifespan (Startup/Shutdown)
# -------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting application on {config.APP_HOST}:{config.APP_PORT}")
    retries = MAX_DB_RETRIES
    while retries > 0:
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                connection.commit()
                logger.info("PostgreSQL database connected successfully.")
                break
        except OperationalError:
            retries -= 1
            logger.critical(f"Database connection failed, retrying... {retries} left")
            if retries == 0:
                logger.critical("Could not connect to DB. Shutting down.")
                raise SystemExit(1)
            await asyncio.sleep(2)

    yield
    logger.info("Shutting down application...")
    engine.dispose()


# -------------------------
# App Factory
# -------------------------
def create_app() -> FastAPI:
    app = FastAPI(
        title=config.PROJECT_NAME,
        version=config.VERSION,
        lifespan=lifespan,
    )

    app.include_router(api_router, prefix="/api/v1")

    # Basic liveness check
    @app.get("/health", tags=["Health"], status_code=status.HTTP_200_OK)
    async def health():
        return {
            "status": "healthy",
            "version": config.VERSION,
        }

    # Readiness check (DB verification)
    @app.get("/ready", tags=["Health"])
    def readiness():
        try:
            with engine.connect() as connection:  # Blocking operation
                connection.execute(text("SELECT 1"))
            return {"status": "ready"}
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database not ready",
            )

    return app


app = create_app()
