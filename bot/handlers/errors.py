import logging
from aiogram import Router
from aiogram.types import ErrorEvent

router = Router()
logger = logging.getLogger(__name__)

@router.errors()
async def error_handler(event: ErrorEvent):
    logger.exception(f"Update: {event.update}\nException: {event.exception}")
