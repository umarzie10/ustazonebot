import asyncio
import logging
from bot.loader import bot, dp
from bot.handlers import setup_routers
from bot.middlewares.logging import LoggingMiddleware
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.middlewares.user import UserMiddleware

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting bot...")
    
    # Setup middlewares
    dp.update.outer_middleware(LoggingMiddleware())
    dp.message.middleware(ThrottlingMiddleware(limit=1))
    dp.update.middleware(UserMiddleware())
    
    # Setup routers
    router = setup_routers()
    dp.include_router(router)
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
