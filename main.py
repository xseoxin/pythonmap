#!/usr/bin/env python3
"""
Google Maps Position Checker
Aplikacja do sprawdzania pozycji fraz w wynikach wyszukiwania Google Maps
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from ui import MainWindow
from config import Settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, Settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pythonmap.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main application entry point."""
    try:
        # Enable high DPI scaling
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("Google Maps Position Checker")
        app.setApplicationVersion("1.0.0")

        # Set application style
        app.setStyle('Fusion')

        # Create and show main window
        logger.info("Starting application")
        window = MainWindow()
        window.show()

        # Run application
        sys.exit(app.exec_())

    except Exception as e:
        logger.critical(f"Application failed to start: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
