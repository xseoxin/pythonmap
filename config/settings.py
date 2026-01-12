import os
from typing import Dict, Any


class Settings:
    """Application settings."""

    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/pythonmap.db')

    # UI
    WINDOW_TITLE = "Google Maps - Sprawdzanie Pozycji Fraz"
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 900

    # Grid options
    GRID_SIZES = ['5x5', '7x7', '9x9', '12x12']
    DEFAULT_GRID_SIZE = '5x5'

    # Check settings
    DEFAULT_RADIUS_KM = 5
    MIN_RADIUS_KM = 1
    MAX_RADIUS_KM = 50
    DEFAULT_CHECK_FREQUENCY_HOURS = 24
    MIN_CHECK_FREQUENCY_HOURS = 1
    MAX_CHECK_FREQUENCY_HOURS = 168  # 1 week

    # Delays
    DELAY_BETWEEN_CHECKS_SECONDS = 2.0
    MIN_DELAY_SECONDS = 1.0
    MAX_DELAY_SECONDS = 10.0

    # Selenium
    HEADLESS_BROWSER = True
    PAGE_LOAD_TIMEOUT = 15

    # Reports
    REPORTS_DIR = 'reports'

    # Logging
    LOG_LEVEL = 'INFO'

    @classmethod
    def as_dict(cls) -> Dict[str, Any]:
        """Return settings as dictionary."""
        return {
            key: value
            for key, value in cls.__dict__.items()
            if not key.startswith('_') and not callable(value)
        }
