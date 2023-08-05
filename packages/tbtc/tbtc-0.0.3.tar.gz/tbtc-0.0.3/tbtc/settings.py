import os

HOME_DIR = os.path.expanduser("~")

# Logging settings
LOG_STDOUT = os.getenv("LOG_STDOUT", "TRUE")
LOG_FORMAT = os.getenv(
    "LOG_FORMAT", "[%(asctime)s][%(levelname)s][%(name)s] %(message)s")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
