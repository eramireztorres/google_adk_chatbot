import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler


def configure_logging() -> None:
    level = os.getenv("ADK_LOG_LEVEL", "INFO").upper()
    default_log_path = Path(__file__).resolve().parent / "logs" / "adk.log"
    log_path = Path(os.getenv("ADK_LOG_FILE", str(default_log_path)))
    if not log_path.is_absolute():
        log_path = (Path(__file__).resolve().parent / log_path).resolve()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    file_handler = RotatingFileHandler(
        log_path, maxBytes=5_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
