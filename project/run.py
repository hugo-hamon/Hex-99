from src.app import App
import logging
import sys

LOGGING_CONFIG = {
    'level': logging.INFO,
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'datefmt': '%d-%b-%y %H:%M:%S',
    'filename': 'log/log.log',
    'filemode': 'w'
}

DEFAULT_CONFIG_PATH = "config/default.toml"

if __name__ == "__main__":
    logging.basicConfig(**LOGGING_CONFIG)
    logging.info("Starting run.py")

    argv = len(sys.argv)
    path = DEFAULT_CONFIG_PATH
    if argv == 2:
        path = sys.argv[1]
        path = f"config/{path}.toml"
        logging.info(f"Using config path : {path}")
    else:
        logging.info(f"Using default config path : {path}")
    
    app = App(path)
    app.run()