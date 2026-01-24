import logging
import os


def configure_logging() -> None:
    level = os.getenv("ADK_LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
