import sys
from loguru import logger
from app.core.config import settings

# Remove default logger
logger.remove()

# Add console logger
logger.add(
    sys.stderr,
    format=settings.LOG_FORMAT,
    level=settings.LOG_LEVEL,
    colorize=True
)

# Add file logger
logger.add(
    "logs/app.log",
    rotation="500 MB",
    retention="10 days",
    format=settings.LOG_FORMAT,
    level=settings.LOG_LEVEL
) 