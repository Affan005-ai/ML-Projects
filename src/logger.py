import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

# Create logs folder + subfolder
log_folder = "logs/app_logs"
os.makedirs(log_folder, exist_ok=True)

# Create a new log file for each run, timestamped
log_file = os.path.join(log_folder, f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Create handler (rotates daily if you want)
file_handler = TimedRotatingFileHandler(log_file, when="midnight", backupCount=7)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Get root logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.propagate = False  # Prevent double logging

# Optional: suppress Flask's default Werkzeug logs
werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.setLevel(logging.ERROR)

# Log startup message with local and network link
logger.info("------------------------------------------------------------")
logger.info("Web App is starting!")
logger.info("Open the web app using these links:")
logger.info("Local:   http://127.0.0.1:5000")
logger.info("Network: http://<YOUR_LOCAL_IP>:5000")
logger.info("------------------------------------------------------------")


