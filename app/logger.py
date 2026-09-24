import logging

# Define ANSI color codes
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        # Format the log message with color applied to the levelname
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)


class Logger:
    def __init__(self):
        # Setup logging with the custom colored formatter
        handler = logging.StreamHandler()
        handler.setFormatter(ColoredFormatter("%(levelname)s:     [%(asctime)s] %(message)s"))
        logging.basicConfig(
            level=logging.INFO,
            handlers=[handler]
        )