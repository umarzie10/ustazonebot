import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    bot_token: str
    admin_chat_id: int
    admin_id: int
    webapp_url: str
    
    # Socials
    social_telegram: str
    social_youtube: str
    social_tiktok: str
    
    # Database
    db_url: str
    
    # Redis
    redis_host: str
    redis_port: int

def load_config() -> Config:
    db_url_env = os.getenv("DATABASE_URL")
    if db_url_env and "${POSTGRES_PORT}" in db_url_env:
        db_url_env = None
    # Railway gives postgresql:// but we need postgresql+asyncpg://
    if db_url_env and db_url_env.startswith("postgresql://"):
        db_url_env = db_url_env.replace("postgresql://", "postgresql+asyncpg://", 1)
        
    return Config(
        bot_token=os.getenv("BOT_TOKEN", ""),
        admin_chat_id=int(os.getenv("ADMIN_CHAT_ID", "6265790648")),
        admin_id=int(os.getenv("ADMIN_ID", "6265790648")),
        webapp_url=os.getenv("WEBAPP_URL", "https://usta-zone-uz.vercel.app/"),
        
        social_telegram=os.getenv("SOCIAL_TELEGRAM", ""),
        social_youtube=os.getenv("SOCIAL_YOUTUBE", ""),
        social_tiktok=os.getenv("SOCIAL_TIKTOK", ""),
        
        db_url=db_url_env or "sqlite+aiosqlite:///database.db",
        
        redis_host=os.getenv("REDIS_HOST", "localhost"),
        redis_port=int(os.getenv("REDIS_PORT", "6379")),
    )

config = load_config()
