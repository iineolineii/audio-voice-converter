import logging


# ANSI escape codes for color formatting
DIM    = "\033[2m"
BOLD   = "\033[1m"
GREY   = "\033[90m"
BLUE   = "\033[94m"
GREEN  = "\033[92m"
BLACK  = DIM + GREY # Combination of dim and grey
RESET  = "\033[0m"  # Reset code to clear coloring and styling
NORMAL = "\033[22m"# Reset code to clear styling

def setup_logging(name: str | None = None) -> logging.Logger:
    # Custom log message format
    log_format = (
        f"{BLACK+BOLD}[%(levelname)s] {RESET+BLACK}%(name)s"
        f"\n> {RESET+BLUE}%(asctime)s.%(msecs)06d{BLACK} · {RESET}%(message)s"
        + RESET
    )

    # Configure the basic logger
    formatter = logging.Formatter(log_format, datefmt=f"%Y-%m-%d {GREEN}%H:%M:%S")
    handler   = logging.StreamHandler()
    handler.setFormatter(formatter)

    # Setup logger
    logger = logging.getLogger(name)
    logger.parent = None
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    logging.basicConfig(level=logging.INFO, handlers=[handler])

    return logger

def log_command(msg, logger: logging.Logger | None = None, level: int = logging.INFO) -> None:
    logger = logger or logging.getLogger(__name__)

    command:   str = msg.command[0]
    user_id:   int = msg.from_user.id
    user_name: str = msg.from_user.full_name.strip()

    # Construct the log message with custom formatting
    logger.log(
        level,
        f"{RESET+BOLD}/{ command } {RESET+GREY}from"
        f"{RESET+BOLD} {user_name} {RESET+GREY}({user_id})"
        + RESET + "\n"
    )
