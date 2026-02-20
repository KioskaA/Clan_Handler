import os
from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).resolve().parent

    TEMP_DATABASE_DIR = BASE_DIR / "app" / "services" / "coc_api_service" / "tempdatabase"

    CLAN_BADGE_PATH = TEMP_DATABASE_DIR / "clanbadge.png"