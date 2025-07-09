import logging
import os
from logging.handlers import RotatingFileHandler

from src.core.settings import settings


os.makedirs(settings.LOG_DIR, exist_ok=True)

logger = logging.getLogger("activity_logger")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    filename=os.path.join(settings.LOG_DIR, settings.LOG_FILE),
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=5,
    encoding="utf-8",
)

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [user_id=%(user_id)s] [role=%(role)s] %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
