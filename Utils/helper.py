from config import DIR_LOGS_FILES
import logging
from datetime import datetime

def timestamp():
    """
    Get the current timestamp as a string.
    :return: Timestamp in 'YYYY-MM-DD HH:MM:SS' format.
    """
    return str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Configure logging
logging.basicConfig(
    filename= (DIR_LOGS_FILES+"/app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#manage log messages
#:param level: Logging level ('info', 'warning', 'error').  default = info
def log_message(message: str, level: str = "info") -> None:
    level = level.lower()
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)
    else:
        raise ValueError("Invalid log level. Use 'info', 'warning', or 'error'.")
    timest = timestamp()
    print(f"[{timest} - {level.upper()}] {message}")