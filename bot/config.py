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
    return Config(
        bot_token=os.getenv("BOT_TOKEN", ""),
        admin_chat_id=int(os.getenv("ADMIN_CHAT_ID", "0")),
        admin_id=int(os.getenv("ADMIN_ID", "0")),
        webapp_url=os.getenv("WEBAPP_URL", "https://barbertop.uz"),
        
        social_telegram=os.getenv("SOCIAL_TELEGRAM", ""),
        social_youtube=os.getenv("SOCIAL_YOUTUBE", ""),
        social_tiktok=os.getenv("SOCIAL_TIKTOK", ""),
        
        db_url=os.getenv(
            "DATABASE_URL", 
            "postgresql+asyncpg://postgres:postgres@localhost:5432/barbertop"
        ),
        
        redis_host=os.getenv("REDIS_HOST", "localhost"),
        redis_port=int(os.getenv("REDIS_PORT", "6379")),
    )

config = load_config()
