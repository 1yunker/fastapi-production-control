# import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import base
from core import logger
from core.config import app_settings

# from db.db import recreate_tables_in_db

app = FastAPI(
    title=app_settings.app_title,
    default_response_class=ORJSONResponse,
)
app.include_router(base.router)


if __name__ == '__main__':
    # asyncio.run(recreate_tables_in_db())
    uvicorn.run(
        'main:app',
        host=app_settings.project_host,
        port=app_settings.project_port,
        reload=True,
        log_config=logger.LOGGING
    )
