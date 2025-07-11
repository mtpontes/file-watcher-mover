import logging
import os
from datetime import datetime

# Creating logs directory
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# File name with timestamp (ex: app_2025-06-22_13-02-30.log)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"{LOG_DIR}/app_{timestamp}.log"

# Configure logger
file_handler = logging.FileHandler(log_filename, encoding="utf-8")
console_handler = logging.StreamHandler()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[file_handler, console_handler],
)

logger = logging.getLogger(__name__)

log = logger
