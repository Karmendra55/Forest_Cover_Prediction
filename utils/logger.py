import logging
from pathlib import Path
from datetime import datetime

# --- Create logs directory ---
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / f"app_{datetime.now().strftime('%Y-%m-%d')}.log"

# --- Configure logger ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter("%(levelname)s | %(message)s"))
logging.getLogger("").addHandler(console)

def log_error(module: str, error: Exception) -> None:
    logging.error(f"[{module}] {error}", exc_info=True)

def log_info(module: str, message: str) -> None:
    logging.info(f"[{module}] {message}")
