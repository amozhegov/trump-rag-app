import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging(level: int = logging.INFO) -> None:
    log_dir = Path(__file__).resolve().parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'app.log'

    root = logging.getLogger()
    if root.handlers:
        return

    root.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",        
    )

    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(formatter)

    file_handler = logging.FileHandler(
        log_file,
        mode = 'a',
        encoding = 'utf-8',
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    root.addHandler(console)
    root.addHandler(file_handler)

    logging.getLogger(__name__).info('Logging has been initiated %s', log_file)