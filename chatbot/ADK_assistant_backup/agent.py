from __future__ import annotations

from dotenv import load_dotenv

from .config.settings import get_settings
from .agents.coordinator import build_root_agent
from .logging_setup import configure_logging

load_dotenv()

configure_logging()

settings = get_settings()

root_agent = build_root_agent(settings)
