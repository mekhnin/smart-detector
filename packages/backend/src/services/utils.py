from datetime import datetime

from loguru import logger


async def print_logger_info(hash_sum: int, predicted):
    """
    Printing logger
    """
    logger.info({"hash": hash_sum, "detected": predicted})


def return_current_time():
    return datetime.utcnow().isoformat()
