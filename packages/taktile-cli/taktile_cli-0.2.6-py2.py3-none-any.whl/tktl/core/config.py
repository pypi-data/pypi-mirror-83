import os
from typing import Dict

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    USERS_OPEN_REGISTRATION: bool = False
    IN_TESTING = False

    DEBUG: bool = False
    WEB_URL: str = "https://app.taktile.com"
    TAKTILE_API_URL: str = "http://taktile-api.local.taktile.com"
    DEPLOYMENT_API_URL: str = "http://deployment-api.local.taktile.com"
    LOG_HOST: str = "http://logs.local.taktile.com"

    TKTL_CONFIG_PATH: str = os.path.expanduser("~/.tktl")
    CONFIG_FILE_NAME: str = "config.json"
    TAKTILE_API_KEY: str = None
    HELP_HEADERS_COLOR: str = "yellow"
    HELP_OPTIONS_COLOR: str = "green"
    USE_CONSOLE_COLORS: str = True
    HELP_COLORS_DICT: Dict = {
        "help_headers_color": "yellow",
        "help_options_color": "green",
    }

    class Config:
        case_sensitive = True


settings = Settings()
