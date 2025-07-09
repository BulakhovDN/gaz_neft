from src.core.logging_config import logger


def log_action(message: str, user_id: int, role: str):
    logger.info(message, extra={"user_id": user_id, "role": role})
