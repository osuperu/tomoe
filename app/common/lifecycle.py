from __future__ import annotations

import base64
import ssl

from adapters import database
from adapters import redis
from common import clients
from common import logger
from common import settings


async def _start_database() -> None:
    logger.info("Connecting to database...")
    clients.database = database.Database(
        read_dsn=database.dsn(
            scheme=settings.READ_DB_SCHEME,
            user=settings.READ_DB_USER,
            password=settings.READ_DB_PASS,
            host=settings.READ_DB_HOST,
            port=settings.READ_DB_PORT,
            database=settings.READ_DB_NAME,
        ),
        read_db_ssl=(
            ssl.create_default_context(
                purpose=ssl.Purpose.SERVER_AUTH,
                cadata=base64.b64decode(settings.READ_DB_CA_CERT_BASE64).decode(),
            )
            if settings.READ_DB_USE_SSL
            else False
        ),
        write_dsn=database.dsn(
            scheme=settings.WRITE_DB_SCHEME,
            user=settings.WRITE_DB_USER,
            password=settings.WRITE_DB_PASS,
            host=settings.WRITE_DB_HOST,
            port=settings.WRITE_DB_PORT,
            database=settings.WRITE_DB_NAME,
        ),
        write_db_ssl=(
            ssl.create_default_context(
                purpose=ssl.Purpose.SERVER_AUTH,
                cadata=base64.b64decode(settings.WRITE_DB_CA_CERT_BASE64).decode(),
            )
            if settings.WRITE_DB_USE_SSL
            else False
        ),
        min_pool_size=settings.READ_DB_MIN_POOL_SIZE,
        max_pool_size=settings.READ_DB_MAX_POOL_SIZE,
    )
    await clients.database.connect()
    logger.info("Connected to database(s)")


async def _shutdown_database() -> None:
    logger.info("Closing database connection...")
    await clients.database.disconnect()
    del clients.database
    logger.info("Closed database connection")


async def _start_redis() -> None:
    logger.info("Connecting to Redis...")
    clients.redis = await redis.from_url(
        url=redis.dsn(
            scheme=settings.REDIS_SCHEME,
            username=settings.REDIS_USER,
            password=settings.REDIS_PASS,
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            database=settings.REDIS_DB,
        ),
    )
    await clients.redis.ping()
    logger.info("Connected to Redis")


async def _shutdown_redis() -> None:
    logger.info("Closing Redis connection...")
    await clients.redis.close()
    del clients.redis
    logger.info("Closed Redis connection")


async def start() -> None:
    logger.info("Starting application...")
    await _start_database()
    await _start_redis()


async def shutdown() -> None:
    logger.info("Shutting down application...")
    await _shutdown_database()
    await _shutdown_redis()
